#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import re
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

# Mandatory Site24x7 Plugin Constants
PLUGIN_VERSION = 1
HEARTBEAT = True

# Metric units registry for Site24x7 Dashboard
METRIC_UNITS = {
    "e2e_latency_sum": "s",
    "e2e_latency_count": "count",
    "generation_tokens": "count",
    "requests_running": "count",
    "requests_waiting": "count",
    "prompt_tokens": "count",
    "request_success": "count",
    "request_failure": "count",
    "ttft_sum": "s",
    "ttft_count": "count",
    "tpot_sum": "s",
    "tpot_count": "count",
    "resident_memory": "bytes",
    "cpu_seconds": "s",
    "num_request_max": "count",
    "request_finish_count": "count",
    "process_max_fds": "file",
    "process_open_fds": "file",
    "process_start_time_seconds": "s",
    "process_virtual_memory_bytes": "bytes",
    "python_gc_collections_count": "count",
    "python_gc_objects_collected_count": "count",
    "python_gc_objects_uncollectable_count": "count",
    "python_info": ""
}

# Dashboard Tab Configuration
TABS = {
    "Inference_Performance": {
        "order": 1,
        "tablist": [
            "e2e_latency_sum",
            "e2e_latency_count"
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


def _latency_bucket_metric_name(upper_bound: str) -> str:
    try:
        numeric_bound = float(upper_bound)
    except ValueError as exc:
        raise ValueError("Invalid e2e latency bucket boundary: " + upper_bound) from exc
    if math.isnan(numeric_bound):
        raise ValueError("Invalid e2e latency bucket boundary: " + upper_bound)
    if math.isinf(numeric_bound):
        suffix = "inf" if numeric_bound > 0 else "negative_inf"
    else:
        normalized_bound = repr(numeric_bound).lower()
        if normalized_bound.startswith("-"):
            normalized_bound = "negative_" + normalized_bound[1:]
        normalized_bound = re.sub(
            r"e([+-])(\d+)",
            lambda match: "e_" + ("m" if match.group(1) == "-" else "p") + match.group(2),
            normalized_bound,
        )
        suffix = re.sub(r"[^a-zA-Z0-9_]", "_", normalized_bound)
    return "e2e_latency_bucket_le_" + suffix


def _gpu_cache_metric_name(labels: Dict[str, str]) -> str:
    if not labels:
        return "gpu_cache_usage_unlabeled"

    identity = json.dumps(labels, sort_keys=True, separators=(",", ":"))
    label_text = "_".join(
        f"{name}_{value}" for name, value in sorted(labels.items())
    )
    readable_suffix = re.sub(r"[^a-zA-Z0-9_]", "_", label_text).strip("_").lower()
    readable_suffix = readable_suffix[:48] or "labeled"
    identity_hash = hashlib.sha1(identity.encode("utf-8")).hexdigest()[:8]
    return f"gpu_cache_usage_{readable_suffix}_{identity_hash}"


def _parse_prometheus_sample(
    line: str,
) -> Tuple[str, Dict[str, str], float, Optional[float]]:
    text = line.strip()
    metric_match = re.match(r"[a-zA-Z_:][a-zA-Z0-9_:]*", text)
    if not metric_match:
        raise ValueError("Invalid Prometheus metric name")

    metric_name = metric_match.group(0)
    position = metric_match.end()
    labels: Dict[str, str] = {}

    if position < len(text) and text[position] == "{":
        position += 1
        while True:
            while position < len(text) and text[position].isspace():
                position += 1
            if position < len(text) and text[position] == "}":
                position += 1
                break

            label_match = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", text[position:])
            if not label_match:
                raise ValueError("Invalid Prometheus label name")
            label_name = label_match.group(0)
            if label_name in labels:
                raise ValueError("Duplicate Prometheus label: " + label_name)
            position += label_match.end()

            while position < len(text) and text[position].isspace():
                position += 1
            if position >= len(text) or text[position] != "=":
                raise ValueError("Expected '=' after Prometheus label name")
            position += 1
            while position < len(text) and text[position].isspace():
                position += 1
            if position >= len(text) or text[position] != '"':
                raise ValueError("Expected quoted Prometheus label value")

            value_start = position
            position += 1
            escaped = False
            while position < len(text):
                char = text[position]
                if char == '"' and not escaped:
                    break
                if char == "\\" and not escaped:
                    escaped = True
                else:
                    escaped = False
                position += 1
            if position >= len(text):
                raise ValueError("Unterminated Prometheus label value")

            labels[label_name] = json.loads(text[value_start:position + 1])
            position += 1
            while position < len(text) and text[position].isspace():
                position += 1
            if position < len(text) and text[position] == ",":
                position += 1
                continue
            if position < len(text) and text[position] == "}":
                position += 1
                break
            raise ValueError("Expected ',' or '}' after Prometheus label")

    fields = text[position:].split()
    if len(fields) not in (1, 2):
        raise ValueError("Expected a sample value and optional timestamp")

    value = float(fields[0])
    timestamp = float(fields[1]) if len(fields) == 2 else None
    if timestamp is not None and not math.isfinite(timestamp):
        raise ValueError("Invalid Prometheus sample timestamp")
    return metric_name, labels, value, timestamp


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

            bucket_metrics = sorted(
                name for name in metrics if name.startswith("e2e_latency_bucket_le_")
            )
            cache_metrics = sorted(
                name for name in metrics if name.startswith("gpu_cache_usage_")
            )
            units = dict(METRIC_UNITS)
            units.update({name: "count" for name in bucket_metrics})
            units.update({name: "fraction" for name in cache_metrics})
            self.data["units"] = units
            tabs = {
                name: {"order": tab["order"], "tablist": list(tab["tablist"])}
                for name, tab in TABS.items()
            }
            tabs["Inference_Performance"]["tablist"].extend(bucket_metrics)
            tabs["Resource_Usage"]["tablist"].extend(cache_metrics)
            self.data["tabs"] = tabs

            if not metrics:
                self.data["status"] = 0
                self.data["msg"] = "No NIM metrics found at endpoint"
                self.data.pop("tabs", None)
                return self.data

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
        results: Dict[str, Any] = {}
        additive_metrics = {
            "e2e_latency_sum",
            "e2e_latency_count",
            "ttft_sum",
            "ttft_count",
            "tpot_sum",
            "tpot_count",
            "generation_tokens",
            "prompt_tokens",
            "requests_running",
            "requests_waiting",
            "request_success",
            "request_failure",
            "cpu_seconds",
            "request_finish_count",
            "python_gc_collections_count",
            "python_gc_objects_collected_count",
            "python_gc_objects_uncollectable_count",
        }

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
            "request_generation_tokens_sum": "generation_tokens",
            "request_prompt_tokens_sum": "prompt_tokens",

            # Cache/Requests
            "num_requests_running": "requests_running",
            "num_requests_waiting": "requests_waiting",

            # vLLM latency histogram names
            "inter_token_latency_seconds_sum": "tpot_sum",
            "inter_token_latency_seconds_count": "tpot_count",

            # Success/Failure
            "request_success_total": "request_success",
            "request_failure_total": "request_failure",
            "num_requests_success": "request_success",
            "num_requests_failure": "request_failure",

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

            metric_name, labels, value, _timestamp = _parse_prometheus_sample(line)

            # Normalize metric name: remove nvidia_nim_ prefix
            if metric_name.startswith('nvidia_nim_') or metric_name.startswith('vllm:'):
                metric_name = metric_name.replace('nvidia_nim_', '').replace('vllm:', '')

            if metric_name == "e2e_request_latency_seconds_bucket":
                if "le" not in labels:
                    raise ValueError("e2e latency bucket sample is missing the 'le' label")
                if not math.isfinite(value):
                    raise ValueError("Non-finite sample value for metric " + metric_name)
                bucket_name = _latency_bucket_metric_name(labels["le"])
                results[bucket_name] = results.get(bucket_name, 0.0) + value
                continue

            if metric_name in ("gpu_cache_usage_perc", "kv_cache_usage_perc"):
                if not math.isfinite(value):
                    raise ValueError("Non-finite sample value for metric " + metric_name)
                cache_metric = _gpu_cache_metric_name(labels)
                results[cache_metric] = value
                continue

            if metric_name not in mapping:
                continue

            result_name = mapping[metric_name]
            if result_name == "python_info":
                results[result_name] = "; ".join(
                    f'{key}="{label_value}"' for key, label_value in labels.items()
                )
                continue

            if not math.isfinite(value):
                raise ValueError("Non-finite sample value for metric " + metric_name)
            if result_name in additive_metrics:
                results[result_name] = results.get(result_name, 0.0) + value
            else:
                results[result_name] = value

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
