#!/usr/bin/env python3
import argparse
import json
import urllib.request
from typing import Any, Dict, List, Optional

# Mandatory Site24x7 Plugin Constants
PLUGIN_VERSION = 1
HEARTBEAT = True

# Metric units registry for Site24x7 Dashboard
METRIC_UNITS = {
    "e2e_latency_sum": "s",
    "generation_tokens": "count",
    "gpu_cache_usage": "fraction",
    "requests_running": "count",
    "requests_waiting": "count",
    "prompt_tokens": "count",
    "request_success": "count",
    "request_failure": "count",
    "time_per_output_token_sum": "s",
    "time_to_first_token_sum": "s",
    "resident_memory": "bytes",
    "cpu_seconds": "s",
    # New metrics from Datadog NVIDIA NIM integration (plain Prometheus format)
    "num_request_max": "count",
    "request_finish_count": "count",
    "process_max_fds": "file",
    "process_open_fds": "file",
    "process_start_time_seconds": "s",
    "process_virtual_memory_bytes": "bytes",
    "python_gc_collections_count": "count",
    "python_gc_objects_collected_count": "count",
    "python_gc_objects_uncollectable_count": "count",
    "python_info": "",
    # Add units for calculated averages
    "e2e_latency_avg": "s",
    "time_to_first_token_avg": "s",
    "time_per_output_token_avg": "s"
}

# Dashboard Tab Configuration
TABS = {
    "Inference_Performance": {
        "order": 1,
        "tablist": [
            "requests_running",
            "requests_waiting",
            "e2e_latency_avg",
            "time_to_first_token_avg",
            "time_per_output_token_avg"
        ]
    },
    "Token_Statistics": {
        "order": 2,
        "tablist": [
            "generation_tokens",
            "prompt_tokens"
            ]
    },
    "Resource_Usage": {
        "order": 3,
        "tablist": [
            "gpu_cache_usage",
            "resident_memory",
            "cpu_seconds"
        ]
    },
    "Runtime": {
        "order": 4,
        "tablist": [
            "num_request_max",
            "request_finish_count",
            "process_max_fds",
            "process_open_fds",
            "process_start_time_seconds",
            "process_virtual_memory_bytes",
            "python_gc_collections_count",
            "python_gc_objects_collected_count",
            "python_gc_objects_uncollectable_count",
            "python_info"
        ]
    }
}

class Plugin:
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.data: Dict[str, Any] = {}
        self.data["plugin_version"] = PLUGIN_VERSION
        self.data["heartbeat_required"] = HEARTBEAT
        self.data["units"] = METRIC_UNITS
        self.data["tabs"] = TABS
        self.data["Name"] = "NVIDIA_NIM_Monitor"

        self.metrics_url = "http://localhost:8000/v1/metrics"
        if params and "nim_endpoint" in params:
            self.metrics_url = str(params["nim_endpoint"]).strip("\"'")

    def getData(self) -> Dict[str, Any]:
        try:
            # Fetch metrics from NVIDIA NIM Prometheus exporter
            with urllib.request.urlopen(self.metrics_url, timeout=10) as response:
                content = response.read().decode('utf-8')

            # Parse NIM metrics
            metrics = self._parse_nim_metrics(content)

            if not metrics:
                self.data["status"] = 0
                self.data["msg"] = "No NIM metrics found at endpoint"
                self.data.pop("tabs", None)
                return self.data

            # Calculate derived averages for Latency
            if "e2e_latency_sum" in metrics and "e2e_latency_count" in metrics and metrics["e2e_latency_count"] > 0:
                metrics["e2e_latency_avg"] = round(metrics["e2e_latency_sum"] / metrics["e2e_latency_count"], 4)

            if "ttft_sum" in metrics and "ttft_count" in metrics and metrics["ttft_count"] > 0:
                metrics["time_to_first_token_avg"] = round(metrics["ttft_sum"] / metrics["ttft_count"], 4)

            if "tpot_sum" in metrics and "tpot_count" in metrics and metrics["tpot_count"] > 0:
                metrics["time_per_output_token_avg"] = round(metrics["tpot_sum"] / metrics["tpot_count"], 4)

            # Populate data
            self.data.update(metrics)
            self.data["status"] = 1
            self.data["msg"] = "Success"

        except Exception as e:
            self.data["status"] = 0
            self.data["msg"] = str(e)
            self.data.pop("tabs", None)

        return self.data

    def _parse_nim_metrics(self, content: str) -> Dict[str, Any]:
        results = {}

        # Mapping from Prometheus metric names to Internal Keys
        mapping = {
            # Latency (Standard NIM / Prometheus names)
            "e2e_request_latency_seconds_sum": "e2e_latency_sum",
            "e2e_request_latency_seconds_count": "e2e_latency_count",
            "time_to_first_token_seconds_sum": "ttft_sum",
            "time_to_first_token_seconds_count": "ttft_count",
            "time_per_output_token_seconds_sum": "tpot_sum",
            "time_per_output_token_seconds_count": "tpot_count",

            # Throughput/Tokens
            "generation_tokens_total": "generation_tokens",
            "prompt_tokens_total": "prompt_tokens",

            # Cache/Requests
            "gpu_cache_usage_perc": "gpu_cache_usage",
            "num_requests_running": "requests_running",
            "num_requests_waiting": "requests_waiting",

            # Success/Failure
            "request_success_total": "request_success",
            "request_failure_total": "request_failure",

            # Process
            "process_resident_memory_bytes": "resident_memory",
            "process_cpu_seconds_total": "cpu_seconds",

            # New Datadog metrics (from provided dump)
            "num_request_max": "num_request_max",
            "request_finish_count": "request_finish_count",
            "process_max_fds": "process_max_fds",
            "process_open_fds": "process_open_fds",
            "process_start_time_seconds": "process_start_time_seconds",
            "process_virtual_memory_bytes": "process_virtual_memory_bytes",
            "python_gc_collections_count": "python_gc_collections_count",
            "python_gc_objects_collected_count": "python_gc_objects_collected_count",
            "python_gc_objects_uncollectable_count": "python_gc_objects_uncollectable_count",
            "python_info": "python_info"
        }

        for line in content.splitlines():
            if line.startswith('#') or not line.strip():
                continue

            try:
                parts = line.rsplit(' ', 1)
                if len(parts) != 2:
                    continue

                raw_metric, value_str = parts

                # Extract metric name and labels
                metric_name = raw_metric.split('{')[0]

                # Handle python_info separately as it's a string metric
                if metric_name == "python_info":
                    # Extract version and implementation from labels
                    if '{' in raw_metric:
                        labels = raw_metric.split('{')[1].split('}')[0]
                        python_info = ""
                        for label in labels.split(','):
                            if '=' in label:
                                key, val = label.split('=', 1)
                                python_info += f"{key}={val}; "
                        results[mapping[metric_name]] = python_info.strip()
                    continue

                # Normalize metric name: remove nvidia_nim_ prefix
                if metric_name.startswith('nvidia_nim_') or metric_name.startswith('vllm:'):
                    metric_name = metric_name.replace('nvidia_nim_', '').replace('vllm:', '')

                if metric_name in mapping:
                    results[mapping[metric_name]] = float(value_str)

            except (ValueError, IndexError):
                continue

        return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Site24x7 NVIDIA NIM Monitoring Plugin")
    parser.add_argument("--plugin_version", type=int, default=PLUGIN_VERSION, help="Plugin version")
    parser.add_argument("--heartbeat", type=str, default=HEARTBEAT, help="Heartbeat required")
    parser.add_argument("--logs_enabled", type=str, default="false", help="Logs enabled")
    parser.add_argument("--log_type_name", type=str, default="", help="Log type name")
    parser.add_argument("--log_file_path", type=str, default="", help="Log file path")
    parser.add_argument("--nim_endpoint", type=str, default="http://localhost:8000/v1/metrics", help="NIM metrics endpoint")
    parser.add_argument("param", nargs='?', default=None, help="Site24x7 JSON config string")

    args, unknown = parser.parse_known_args()

    params = {
        "plugin_version": args.plugin_version,
        "heartbeat": args.heartbeat,
        "logs_enabled": args.logs_enabled,
        "log_type_name": args.log_type_name,
        "log_file_path": args.log_file_path,
        "nim_endpoint": args.nim_endpoint
    }

    if args.param:
        try:
            params.update(json.loads(args.param))
        except Exception:
            pass

    # Also parse unknown arguments in the form --key=value
    for arg in unknown:
        if arg.startswith('--'):
            try:
                key, val = arg[2:].split('=', 1)
                params[key] = val
            except ValueError:
                pass

    plugin = Plugin(params)
    data = plugin.getData()
    print(json.dumps(data))
