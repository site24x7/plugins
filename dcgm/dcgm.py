#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import argparse
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

# Global units registry
METRIC_UNITS = {
    "GPU_Performance_Metrics": PERF_UNITS,
    "GPU_Resource_Metrics": RESOURCE_UNITS,
    "GPU_Health_Metrics": HEALTH_UNITS,
    "Average_GPU_Utilization": "%",
    "Average_Memory_Utilization": "%",
    "Average_Temperature": "C",
    "Total_Power_Draw": "W",
    "GPU_Device_Count": "count"
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
        self.data = {}
        self.data["plugin_version"] = args.plugin_version
        self.data["heartbeat_required"] = args.heartbeat
        self.data["units"] = METRIC_UNITS
        self.data["tabs"] = TABS
        self.data["Name"] = "NVIDIA_DCGM_Monitor"

    def getData(self) -> Dict[str, Any]:
        try:
            # Fetch metrics from DCGM Prometheus exporter
            req = urllib.request.Request(self.args.dcgm_endpoint)
            response = urllib.request.urlopen(req, timeout=10)
            content = response.read().decode('utf-8')

            # Parse metrics per GPU
            gpu_data = self._parse_multi_gpu_metrics(content)

            # Remove tabs if no GPU metrics found - early return path
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

            for gpu_id, m in gpu_data.items():
                gpu_name = f"GPU {gpu_id}"

                # Performance Tab
                perf_list.append({
                    "name": gpu_name,
                    "GPU_Utilization": m.get("gpu_util", 0),
                    "Memory_Copy_Utilization": m.get("mem_util", 0),
                    "SM_Clock": m.get("sm_clock", 0),
                    "Memory_Clock": m.get("mem_clock", 0),
                    "Encoder_Utilization": m.get("enc_util", 0),
                    "Decoder_Utilization": m.get("dec_util", 0),
                    "SM_Active": m.get("sm_active", 0),
                    "SM_Occupancy": m.get("sm_occupancy", 0),
                    "Tensor_Active": m.get("tensor_active", 0),
                    "FP16_Active": m.get("fp16_active", 0),
                    "FP32_Active": m.get("fp32_active", 0),
                    "FP64_Active": m.get("fp64_active", 0),
                    "PCIe_TX_Throughput": m.get("pcie_tx", 0),
                    "PCIe_RX_Throughput": m.get("pcie_rx", 0)
                })

                # Resource Tab
                fb_used = m.get("fb_used", 0)
                fb_total = m.get("fb_total", 0)
                resource_list.append({
                    "name": gpu_name,
                    "Memory_Used": fb_used,
                    "Memory_Free": m.get("fb_free", 0),
                    "Memory_Total": fb_total,
                    "Framebuffer_Utilization": round((fb_used / fb_total * 100), 2) if fb_total > 0 else 0,
                    "Memory_Reserved": m.get("fb_reserved", 0)
                })

                # Health Tab
                health_list.append({
                    "name": gpu_name,
                    "Temperature": m.get("temp", 0),
                    "Memory_Temperature": m.get("mem_temp", 0),
                    "Power_Usage": m.get("power", 0),
                    "Fan_Speed": m.get("fan", 0),
                    "Energy_Consumption": m.get("energy", 0),
                    "Clock_Throttle_Reasons": m.get("clock_throttle", 0),
                    "Correctable_Remapped_Rows": m.get("corr_remap", 0),
                    "Uncorrectable_Remapped_Rows": m.get("uncorr_remap", 0),
                    "XID_Errors": m.get("xid_errors", 0),
                    "PState": m.get("pstate", 0),
                    "Slowdown_Temperature": m.get("slowdown_temp", 0)
                })

                # Collect values for aggregates
                if "gpu_util" in m: gpu_utils.append(m["gpu_util"])
                if "mem_util" in m: mem_utils.append(m["mem_util"])
                if "temp" in m: temps.append(m["temp"])
                if "power" in m: powers.append(m["power"])

            # Populate top-level aggregate metrics
            self.data["GPU_Device_Count"] = len(gpu_data)
            if gpu_utils: self.data["Average_GPU_Utilization"] = round(sum(gpu_utils) / len(gpu_utils), 2)
            if mem_utils: self.data["Average_Memory_Utilization"] = round(sum(mem_utils) / len(mem_utils), 2)
            if temps: self.data["Average_Temperature"] = round(sum(temps) / len(temps), 2)
            if powers: self.data["Total_Power_Draw"] = round(sum(powers), 2)

            # Assign tabular data
            self.data["GPU_Performance_Metrics"] = perf_list[:25] # Limit to 25 rows
            self.data["GPU_Resource_Metrics"] = resource_list[:25]
            self.data["GPU_Health_Metrics"] = health_list[:25]

            self.data["status"] = 1
            self.data["msg"] = "Success"

        except Exception as e:
            self.data["status"] = 0
            self.data["msg"] = str(e)
            # Remove tabs on error so Site24x7 shows the error message prominently
            self.data.pop("tabs", None)

        return self.data

    def _parse_multi_gpu_metrics(self, content: str) -> Dict[str, Dict[str, float]]:
        """
        Parses Prometheus output and groups metrics by GPU ID.
        Returns: { "0": { "gpu_util": 45, ... }, "1": { ... } }
        """
        gpu_map = {}
        mapping = {
            "DCGM_FI_DEV_GPU_UTIL": "gpu_util",
            "DCGM_FI_DEV_MEM_COPY_UTIL": "mem_util",
            "DCGM_FI_DEV_ENC_UTIL": "enc_util",
            "DCGM_FI_DEV_DEC_UTIL": "dec_util",
            "DCGM_FI_DEV_POWER_USAGE": "power",
            "DCGM_FI_DEV_GPU_TEMP": "temp",
            "DCGM_FI_DEV_MEM_TEMP": "mem_temp",
            "DCGM_FI_DEV_SM_CLOCK": "sm_clock",
            "DCGM_FI_DEV_MEM_CLOCK": "mem_clock",
            "DCGM_FI_DEV_FB_USED": "fb_used",
            "DCGM_FI_DEV_FB_FREE": "fb_free",
            "DCGM_FI_DEV_FB_TOTAL": "fb_total",
            "DCGM_FI_DEV_FAN_SPEED": "fan",
            "DCGM_FI_DEV_ENERGY_CONSUMPTION": "energy",
            "DCGM_FI_DEV_SM_ACTIVE": "sm_active",
            "DCGM_FI_DEV_SM_OCCUPANCY": "sm_occupancy",
            "DCGM_FI_DEV_TENSOR_ACTIVE": "tensor_active",
            "DCGM_FI_DEV_PIPE_FP64_ACTIVE": "fp64_active",
            "DCGM_FI_DEV_PIPE_FP32_ACTIVE": "fp32_active",
            "DCGM_FI_DEV_PIPE_FP16_ACTIVE": "fp16_active",
            "DCGM_FI_DEV_PCIE_TX_THROUGHPUT": "pcie_tx",
            "DCGM_FI_DEV_PCIE_RX_THROUGHPUT": "pcie_rx",
            "DCGM_FI_DEV_CLOCK_THROTTLE_REASONS": "clock_throttle",
            "DCGM_FI_DEV_CORRECTABLE_REMAP_ROWS": "corr_remap",
            "DCGM_FI_DEV_UNCORRECTABLE_REMAP_ROWS": "uncorr_remap",
            "DCGM_FI_DEV_XID_ERRORS": "xid_errors",
            "DCGM_FI_DEV_PSTATE": "pstate",
            "DCGM_FI_DEV_SLOWDOWN_TEMP": "slowdown_temp",
            "DCGM_FI_DEV_FB_RESERVED": "fb_reserved"
        }

        for line in content.splitlines():
            if line.startswith('#') or not line.strip():
                continue
            try:
                parts = line.rsplit(' ', 1)
                if len(parts) != 2:
                    continue
                raw_metric, value_str = parts
                value = float(value_str)
                metric_name = raw_metric.split('{')[0]

                if metric_name not in mapping:
                    continue

                # Extract GPU ID from labels: {gpu="0",...}
                gpu_id = None
                if '{' in raw_metric:
                    labels_part = raw_metric.split('{')[1].split('}')[0]
                    for label in labels_part.split(','):
                        label = label.strip()
                        if label.startswith('gpu="'):
                            try:
                                gpu_id = label.split('"')[1]
                                if not gpu_id.isdigit():
                                    gpu_id = None
                            except IndexError:
                                gpu_id = None
                            break

                if gpu_id is None:
                    # Skip metrics without valid GPU label
                    continue

                if gpu_id not in gpu_map:
                    gpu_map[gpu_id] = {}

                # Only add metric if it's not None
                if value is not None:
                    gpu_map[gpu_id][mapping[metric_name]] = value
            except (ValueError, IndexError):
                continue

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
    print(json.dumps(data, indent=4, sort_keys=True))
