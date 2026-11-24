#!/usr/bin/env python3
import argparse
import json
import math
import re
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

# Mandatory Site24x7 Plugin Constants
PLUGIN_VERSION = 1
HEARTBEAT = True

# Metric units for individual categories (Tabular data)
PERF_UNITS = {
    "GPU_Utilization": "%",
    "Memory_Copy_Utilization": "%",
    "SM_Clock": "MHz",
    "Memory_Clock": "MHz",
    "Encoder_Utilization": "%",
    "Decoder_Utilization": "%",
    "SM_Active": "fraction",
    "SM_Occupancy": "fraction",
    "Tensor_Active": "fraction",
    "FP16_Active": "fraction",
    "FP32_Active": "fraction",
    "FP64_Active": "fraction",
    "PCIe_TX_Throughput": "KB/s",
    "PCIe_RX_Throughput": "KB/s"
}

RESOURCE_UNITS = {
    "Memory_Used": "MB",
    "Memory_Free": "MB",
    "Memory_Total": "MB",
    "Framebuffer_Utilization": "%",
    "Memory_Reserved": "MB"
}

HEALTH_UNITS = {
    "Temperature": "C",
    "Memory_Temperature": "C",
    "Power_Usage": "W",
    "Fan_Speed": "%",
    "Energy_Consumption": "mJ",
    "Clock_Throttle_Reasons": "bitmask",
    "Correctable_Remapped_Rows": "count",
    "Uncorrectable_Remapped_Rows": "count",
    "XID_Errors": "count",
    "PState": "state",
    "Slowdown_Temperature": "C"
}

TOP_LEVEL_UNITS = {
    "Average_GPU_Utilization": "%",
    "Average_Memory_Utilization": "%",
    "Average_Temperature": "C",
    "Total_Power_Draw": "W",
    "GPU_Device_Count": "count"
}

# Global units registry reference
METRIC_UNITS = {
    "GPU_Performance_Metrics": PERF_UNITS,
    "GPU_Resource_Metrics": RESOURCE_UNITS,
    "GPU_Health_Metrics": HEALTH_UNITS,
    **TOP_LEVEL_UNITS
}

# Dashboard Tab Configuration
TABS = {
    "Performance": {
        "order": 1,
        "tablist": [
            "Average_GPU_Utilization",
            "Average_Memory_Utilization",
            "GPU_Performance_Metrics"
        ]
    },
    "Resources": {
        "order": 2,
        "tablist": [
            "GPU_Device_Count",
            "GPU_Resource_Metrics"
        ]
    },
    "Health": {
        "order": 3,
        "tablist": [
            "Average_Temperature",
            "Total_Power_Draw",
            "GPU_Health_Metrics"
        ]
    }
}


class Plugin:
    def __init__(self, args):
        self.args = args
        self.data = {
            "plugin_version": args.plugin_version,
            "heartbeat_required": args.heartbeat,
            "Name": "NVIDIA_DCGM_Monitor",
            "units": METRIC_UNITS,
            "tabs": TABS
        }

    def getData(self) -> Dict[str, Any]:
        try:
            # Fetch metrics from DCGM Prometheus exporter with timeout and response size limit
            req = urllib.request.Request(self.args.dcgm_endpoint)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read(1024 * 512).decode('utf-8', errors='replace')

            # Parse metrics per GPU
            gpu_data = self._parse_multi_gpu_metrics(content)

            # Remove tabs and return early if no GPU metrics found
            if not gpu_data:
                self.data["status"] = 0
                self.data["msg"] = "No GPU metrics found in exporter output"
                self.data.pop("tabs", None)
                return self.data

            # Build Site24x7 Tabular lists
            perf_list = []
            resource_list = []
            health_list = []

            gpu_utils = []
            mem_utils = []
            temps = []
            powers = []

            for gpu_id, m in sorted(gpu_data.items(), key=lambda x: int(x[0]) if x[0].isdigit() else x[0]):
                gpu_name = f"GPU {gpu_id}"

                # Performance Tab
                perf_row = {"name": gpu_name}
                perf_row["GPU_Utilization"] = m.get("gpu_util", 0)
                perf_row["Memory_Copy_Utilization"] = m.get("mem_util", 0)
                perf_row["SM_Clock"] = m.get("sm_clock", 0)
                perf_row["Memory_Clock"] = m.get("mem_clock", 0)
                perf_row["Encoder_Utilization"] = m.get("enc_util", 0)
                perf_row["Decoder_Utilization"] = m.get("dec_util", 0)
                perf_row["SM_Active"] = m.get("sm_active", 0)
                perf_row["SM_Occupancy"] = m.get("sm_occupancy", 0)
                perf_row["Tensor_Active"] = m.get("tensor_active", 0)
                perf_row["FP16_Active"] = m.get("fp16_active", 0)
                perf_row["FP32_Active"] = m.get("fp32_active", 0)
                perf_row["FP64_Active"] = m.get("fp64_active", 0)
                perf_row["PCIe_TX_Throughput"] = m.get("pcie_tx", 0)
                perf_row["PCIe_RX_Throughput"] = m.get("pcie_rx", 0)
                perf_list.append(perf_row)

                # Resource Tab
                resource_row = {"name": gpu_name}
                resource_row["Memory_Used"] = m.get("fb_used", 0)
                resource_row["Memory_Free"] = m.get("fb_free", 0)
                resource_row["Memory_Total"] = m.get("fb_total", 0)
                fb_util = 0
                if "fb_used" in m and "fb_total" in m and m["fb_total"] > 0:
                    fb_util = round((m["fb_used"] / m["fb_total"] * 100), 2)
                resource_row["Framebuffer_Utilization"] = fb_util
                resource_row["Memory_Reserved"] = m.get("fb_reserved", 0)
                resource_list.append(resource_row)

                # Health Tab
                health_row = {"name": gpu_name}
                health_row["Temperature"] = m.get("temp", 0)
                health_row["Memory_Temperature"] = m.get("mem_temp", 0)
                health_row["Power_Usage"] = m.get("power", 0)
                health_row["Fan_Speed"] = m.get("fan", 0)
                health_row["Energy_Consumption"] = m.get("energy", 0)
                health_row["Clock_Throttle_Reasons"] = m.get("clock_throttle", 0)
                health_row["Correctable_Remapped_Rows"] = m.get("corr_remap", 0)
                health_row["Uncorrectable_Remapped_Rows"] = m.get("uncorr_remap", 0)
                health_row["XID_Errors"] = m.get("xid_errors", 0)
                health_row["PState"] = m.get("pstate", 0)
                health_row["Slowdown_Temperature"] = m.get("slowdown_temp", 0)
                health_list.append(health_row)

                # Collect values for aggregates
                gpu_utils.append(m.get("gpu_util", 0))
                mem_utils.append(m.get("mem_util", 0))
                temps.append(m.get("temp", 0))
                powers.append(m.get("power", 0))

            # Populate top-level aggregate metrics
            self.data["GPU_Device_Count"] = len(gpu_data)
            self.data["Average_GPU_Utilization"] = round(sum(gpu_utils) / len(gpu_utils), 2) if gpu_utils else 0
            self.data["Average_Memory_Utilization"] = round(sum(mem_utils) / len(mem_utils), 2) if mem_utils else 0
            self.data["Average_Temperature"] = round(sum(temps) / len(temps), 2) if temps else 0
            self.data["Total_Power_Draw"] = round(sum(powers), 2) if powers else 0

            # Assign tabular data (Limit to 25 rows)
            self.data["GPU_Performance_Metrics"] = perf_list[:25]
            self.data["GPU_Resource_Metrics"] = resource_list[:25]
            self.data["GPU_Health_Metrics"] = health_list[:25]

            if len(gpu_data) > 25:
                self.data["Truncated_Output"] = "true"

            self.data["status"] = 1
            self.data["msg"] = "Success"

        except Exception:
            # Generic error message to prevent URL/credential leaks into Site24x7 UI
            self.data["status"] = 0
            self.data["msg"] = "Failed to collect metrics. Check exporter connectivity."
            self.data.pop("tabs", None)

        return self.data

    def _parse_multi_gpu_metrics(self, content: str) -> Dict[str, Dict[str, float]]:
        """
        Parses Prometheus output and groups metrics by GPU ID.
        Returns: { "0": { "gpu_util": 45.0, ... }, "1": { ... } }
        """
        gpu_map = {}
        mapping = {
            "DCGM_FI_DEV_GPU_UTIL": "gpu_util",
            "DCGM_FI_DEV_MEM_COPY_UTIL": "mem_util",
            "DCGM_FI_DEV_ENC_UTIL": "enc_util",
            "DCGM_FI_DEV_DEC_UTIL": "dec_util",
            "DCGM_FI_DEV_POWER_USAGE": "power",
            "DCGM_FI_DEV_GPU_TEMP": "temp",
            "DCGM_FI_DEV_MEMORY_TEMP": "mem_temp",
            "DCGM_FI_DEV_SM_CLOCK": "sm_clock",
            "DCGM_FI_DEV_MEM_CLOCK": "mem_clock",
            "DCGM_FI_DEV_FB_USED": "fb_used",
            "DCGM_FI_DEV_FB_FREE": "fb_free",
            "DCGM_FI_DEV_FB_TOTAL": "fb_total",
            "DCGM_FI_DEV_FAN_SPEED": "fan",
            "DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION": "energy",
            "DCGM_FI_DEV_SM_ACTIVE": "sm_active",
            "DCGM_FI_DEV_SM_OCCUPANCY": "sm_occupancy",
            "DCGM_FI_DEV_TENSOR_ACTIVE": "tensor_active",
            "DCGM_FI_DEV_PIPE_FP64_ACTIVE": "fp64_active",
            "DCGM_FI_DEV_PIPE_FP32_ACTIVE": "fp32_active",
            "DCGM_FI_DEV_PIPE_FP16_ACTIVE": "fp16_active",
            "DCGM_FI_PROF_PCIE_TX_BYTES": "pcie_tx",
            "DCGM_FI_DEV_PCIE_TX_THROUGHPUT": "pcie_tx",
            "DCGM_FI_PROF_PCIE_RX_BYTES": "pcie_rx",
            "DCGM_FI_DEV_PCIE_RX_THROUGHPUT": "pcie_rx",
            "DCGM_FI_DEV_CLOCK_THROTTLE_REASONS": "clock_throttle",
            "DCGM_FI_DEV_CORRECTABLE_REMAP_ROWS": "corr_remap",
            "DCGM_FI_DEV_UNCORRECTABLE_REMAP_ROWS": "uncorr_remap",
            "DCGM_FI_DEV_XID_ERRORS": "xid_errors",
            "DCGM_FI_DEV_PSTATE": "pstate",
            "DCGM_FI_DEV_SLOWDOWN_TEMP": "slowdown_temp",
            "DCGM_FI_DEV_FB_RESERVED": "fb_reserved"
        }

        # Regex to parse Prometheus metric lines: metric_name{labels} value [timestamp]
        metric_line_pattern = re.compile(r'^[ \t]*([a-zA-Z_:][a-zA-Z0-9_:]*)(?:\{(.*)\})?[ \t]+(\S+)')
        gpu_label_pattern = re.compile(r'(?:^|,)\s*gpu\s*=\s*"([^"]+)"')

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = metric_line_pattern.match(line)
            if not match:
                continue

            metric_name, labels_part, value_str = match.groups()

            if metric_name not in mapping or not labels_part:
                continue

            try:
                value = float(value_str)
                # Reject NaN and Infinity to maintain JSON compliance
                if not math.isfinite(value):
                    continue
            except (ValueError, TypeError):
                continue

            # Extract GPU ID from labels
            gpu_match = gpu_label_pattern.search(labels_part)
            if not gpu_match:
                continue

            gpu_id = gpu_match.group(1).strip()
            if not gpu_id.isdigit():
                continue

            # Convert bytes to KB/s for PCIe throughput if reported in bytes
            if metric_name in ("DCGM_FI_PROF_PCIE_TX_BYTES", "DCGM_FI_PROF_PCIE_RX_BYTES"):
                value = round(value / 1024.0, 2)

            if gpu_id not in gpu_map:
                gpu_map[gpu_id] = {}

            gpu_map[gpu_id][mapping[metric_name]] = value

        return gpu_map


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin_version', type=int, default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', type=lambda x: (str(x).lower() == 'true'), default=HEARTBEAT)
    parser.add_argument('--dcgm_endpoint', type=str, default='http://localhost:9400/metrics')
    parser.add_argument('--logs_enabled', type=lambda x: (str(x).lower() == 'true'), default=False)
    parser.add_argument('--log_type_name', type=str, default='')
    parser.add_argument('--log_file_path', type=str, default='')
    args, unknown = parser.parse_known_args()

    plugin = Plugin(args)
    data = plugin.getData()
    print(json.dumps(data, indent=4, sort_keys=True, allow_nan=False))
