#!/usr/bin/env python3
from __future__ import annotations

"""
Site24x7 Linux Agent Plugin - NVIDIA NVML GPU Monitoring (V1)
=============================================================================
Follows official Site24x7 Plugin Class template standard (`Plugin.getData()`).
Collects comprehensive GPU metrics across 4 Site24x7 Tabular Categories:
  1. GPU_Performance_Metrics   (GPU/memory utilization, clocks, encoder/decoder, throughput)
  2. GPU_Resource_Metrics      (Memory, Framebuffer, BAR1, PCIe, NVLink, Capacity)
  3. GPU_Health_Metrics        (Temperatures, Fan, Power, Throttling, ECC, XID)
  4. GPU_Process_Metrics       (Per-process GPU usage, Pods, Containers, Slurm, Workloads)

Uses native NVML (nvidia-ml-py / pynvml) with graceful fallback to nvidia-smi CLI.
"""


import os
import sys
import json
import argparse
import subprocess
from typing import Any, Dict, List, Optional, Tuple

# Mandatory Site24x7 Plugin Constants
PLUGIN_VERSION = 1
HEARTBEAT = True

# Default estimated hourly cost per GPU in USD (for idle cost calculation)
DEFAULT_HOURLY_GPU_COST = 1.50

# Well-known AI/ML Training Framework executable tokens
TRAINING_SIGNATURES = {
    "python", "torch", "deepspeed", "ray", "accelerate", "vllm", "triton",
    "jax", "train", "megatron", "tensorflow", "horovod"
}


# =============================================================================
# HELPER UTILITIES: LINUX KERNEL CGROUP & PROCESS ATTRIBUTION
# =============================================================================
def parse_smi_number(raw: str, cast: type = float) -> Any:
    """
    Parses a single nvidia-smi CSV cell. Handles '[N/A]' or 'N/A' markers.
    """
    if not raw:
        return cast(0)
    cleaned = raw.strip().strip("[]")
    if cleaned.upper() in ("N/A", "NA", "UNKNOWN", "-", ""):
        return cast(0)
    try:
        return cast(float(cleaned))
    except (ValueError, TypeError):
        return cast(0)


def get_process_container_context(pid: int) -> Tuple[str, str, str]:
    """
    Inspects Linux /proc/<pid>/ to extract Container ID, Pod UID, and Slurm Job ID.
    Returns: (container_id, pod_uid, slurm_job_id)
    """
    container_id = "N/A"
    pod_uid = "N/A"
    slurm_job_id = "N/A"

    if sys.platform != "linux":
        return container_id, pod_uid, slurm_job_id

    # 1. Parse cgroup for Docker/Containerd and Kubernetes Pod
    cgroup_path = f"/proc/{pid}/cgroup"
    if os.path.exists(cgroup_path):
        try:
            with open(cgroup_path, "r", errors="ignore") as f:
                for line in f:
                    if "pod" in line:
                        parts = line.strip().split("/")
                        for p in parts:
                            if p.startswith("pod"):
                                pod_uid = p.replace("pod", "").replace(".slice", "")
                            elif len(p) == 64:
                                container_id = p[:12]
                    elif "docker" in line or "containerd" in line:
                        parts = line.strip().split("/")
                        for p in parts:
                            if len(p) == 64:
                                container_id = p[:12]
        except Exception:
            pass

    # 2. Parse environ for Slurm Job Attribution
    environ_path = f"/proc/{pid}/environ"
    if os.path.exists(environ_path):
        try:
            with open(environ_path, "rb") as f:
                env_content = f.read().decode("utf-8", errors="ignore")
                for item in env_content.split("\x00"):
                    if item.startswith("SLURM_JOB_ID=") or item.startswith("SLURM_JOBID="):
                        slurm_job_id = item.split("=", 1)[1]
                        break
        except Exception:
            pass

    return container_id, pod_uid, slurm_job_id


def resolve_nvidia_smi(path_hint: str = "nvidia-smi") -> Optional[str]:
    """
    Locates the nvidia-smi binary. Site24x7 .cfg values may arrive wrapped in
    quotes, and nvidia-smi is frequently absent from the restricted PATH the
    agent service inherits, so we strip quotes and probe the usual install
    locations before giving up.
    """
    candidate = (path_hint or "nvidia-smi").strip().strip("\"'").strip()
    if not candidate:
        candidate = "nvidia-smi"

    # 1. Absolute or relative path the operator configured explicitly
    if os.path.dirname(candidate):
        return candidate if os.path.isfile(candidate) else None

    # 2. Resolve through PATH
    import shutil
    found = shutil.which(candidate)
    if found:
        return found

    # 3. Probe distro-specific install locations
    for probe in (
        "/usr/bin/nvidia-smi",
        "/usr/local/nvidia/bin/nvidia-smi",
        "/usr/local/bin/nvidia-smi",
        "/opt/nvidia/bin/nvidia-smi",
        "/usr/lib/wsl/lib/nvidia-smi",
    ):
        if os.path.isfile(probe):
            return probe

    return None


def build_diagnostic(e_nvml: Exception) -> str:
    """
    Builds a self-diagnosing failure message.

    The most common deployment failure is that nvidia-ml-py was installed into a
    different interpreter (a virtualenv, or the system python) than the one the
    agent actually runs. Reporting sys.executable makes that immediately obvious.
    """
    exe = sys.executable or "unknown"
    ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return (
        f"NVML unavailable ({e_nvml}); nvidia-smi not found. "
        f"Runner interpreter: {exe} (Python {ver}). "
        f"Install the bindings into THAT interpreter: "
        f"'{exe} -m pip install nvidia-ml-py'. "
        f"If this host has no NVIDIA driver, no GPU metrics can be reported."
    )


def get_latest_xid_errors() -> int:
    """
    Checks dmesg or kernel logs for NVIDIA XID critical hardware/driver errors.
    Returns count of XID occurrences found in recent logs.
    """
    if sys.platform != "linux":
        return 0
    try:
        cmd = ["dmesg", "-T"]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=2).decode("utf-8", errors="ignore")
        return out.count("NVRM: Xid")
    except Exception:
        return 0


# =============================================================================
# 1. PERFORMANCE METRICS COLLECTOR (TAB 1)
# =============================================================================
class PerformanceCollector:
    """Extracts GPU utilization, clocks, encoder/decoder, and bus throughput metrics."""

    UNITS = {
        "GPU_Utilization": "%",
        "Memory_Copy_Utilization": "%",
        "SM_Clock": "MHz",
        "Core_Clock": "MHz",
        "Memory_Clock": "MHz",
        "Encoder_Utilization": "%",
        "Decoder_Utilization": "%",
        "PCIe_TX_Throughput": "KB/s",
        "PCIe_RX_Throughput": "KB/s",
        "NVLink_TX_Throughput": "KB/s",
        "NVLink_RX_Throughput": "KB/s"
    }

    @staticmethod
    def collect(pynvml: Any, handle: Any, gpu_name: str) -> Tuple[Dict[str, Any], Dict[str, float]]:
        gpu_util = 0.0
        mem_util = 0.0

        try:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_util = float(util.gpu)
            mem_util = float(util.memory)
        except Exception:
            pass

        sm_clock = 0
        try:
            sm_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM)
        except Exception:
            pass

        core_clock = 0
        try:
            core_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        except Exception:
            pass

        mem_clock = 0
        try:
            mem_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        except Exception:
            pass

        enc_util = 0.0
        try:
            enc = pynvml.nvmlDeviceGetEncoderUtilization(handle)
            enc_util = float(enc[0])
        except Exception:
            pass

        dec_util = 0.0
        try:
            dec = pynvml.nvmlDeviceGetDecoderUtilization(handle)
            dec_util = float(dec[0])
        except Exception:
            pass

        pcie_tx, pcie_rx = 0, 0
        try:
            pcie_tx = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
            pcie_rx = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
        except Exception:
            pass

        nvlink_tx, nvlink_rx = 0, 0
        try:
            for link in range(6):
                try:
                    if pynvml.nvmlDeviceGetNvLinkState(handle, link) == 1:
                        nvlink_tx += pynvml.nvmlDeviceGetNvLinkUtilizationCounter(handle, link, 0)["tx"]
                        nvlink_rx += pynvml.nvmlDeviceGetNvLinkUtilizationCounter(handle, link, 0)["rx"]
                except Exception:
                    break
        except Exception:
            pass

        metrics = {
            "name": gpu_name,
            "GPU_Utilization": gpu_util,
            "Memory_Copy_Utilization": mem_util,
            "SM_Clock": sm_clock,
            "Core_Clock": core_clock,
            "Memory_Clock": mem_clock,
            "Encoder_Utilization": enc_util,
            "Decoder_Utilization": dec_util,
            "PCIe_TX_Throughput": pcie_tx,
            "PCIe_RX_Throughput": pcie_rx,
            "NVLink_TX_Throughput": nvlink_tx,
            "NVLink_RX_Throughput": nvlink_rx
        }

        stats = {"gpu_util": gpu_util, "mem_util": mem_util}
        return metrics, stats


# =============================================================================
# 2. HARDWARE & RESOURCE METRICS COLLECTOR (TAB 2)
# =============================================================================
class ResourceCollector:
    """Extracts memory allocations, BAR1, interconnect link properties, and metadata."""

    UNITS = {
        "Memory_Total": "MB",
        "Memory_Used": "MB",
        "Memory_Free": "MB",
        "BAR1_Memory_Total": "MB",
        "BAR1_Memory_Used": "MB",
        "BAR1_Memory_Free": "MB",
        "PCIe_Link_Width": "lanes",
        "NVLink_Active_Links": "count",
        "UUID": "text",
        "Serial_Number": "text",
        "VBIOS_Version": "text",
        "PCIe_Link_Info": "text",
        "Compute_Capability": "text"
    }

    @staticmethod
    def collect(pynvml: Any, handle: Any, gpu_name: str) -> Tuple[Dict[str, Any], Dict[str, float]]:
        uuid_str = "N/A"
        try:
            raw_uuid = pynvml.nvmlDeviceGetUUID(handle)
            uuid_str = raw_uuid.decode("utf-8") if isinstance(raw_uuid, bytes) else str(raw_uuid)
        except Exception:
            pass

        serial_str = "N/A"
        try:
            raw_serial = pynvml.nvmlDeviceGetSerial(handle)
            serial_str = raw_serial.decode("utf-8") if isinstance(raw_serial, bytes) else str(raw_serial)
        except Exception:
            pass

        vbios_str = "N/A"
        try:
            vbios = pynvml.nvmlDeviceGetVbiosVersion(handle)
            vbios_str = vbios.decode("utf-8") if isinstance(vbios, bytes) else str(vbios)
        except Exception:
            pass

        total_mb, used_mb, free_mb = 0.0, 0.0, 0.0
        try:
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            total_mb = round(mem.total / (1024 * 1024), 2)
            used_mb = round(mem.used / (1024 * 1024), 2)
            free_mb = round(mem.free / (1024 * 1024), 2)
        except Exception:
            pass

        bar1_total, bar1_used, bar1_free = 0.0, 0.0, 0.0
        try:
            bar1 = pynvml.nvmlDeviceGetBAR1MemoryInfo(handle)
            bar1_total = round(bar1.bar1Total / (1024 * 1024), 2)
            bar1_used = round(bar1.bar1Used / (1024 * 1024), 2)
            bar1_free = round(bar1.bar1Free / (1024 * 1024), 2)
        except Exception:
            pass

        pcie_info = "N/A"
        curr_width = 0
        try:
            curr_gen = pynvml.nvmlDeviceGetCurrPcieLinkGeneration(handle)
            curr_width = pynvml.nvmlDeviceGetCurrPcieLinkWidth(handle)
            max_gen = pynvml.nvmlDeviceGetMaxPcieLinkGeneration(handle)
            max_width = pynvml.nvmlDeviceGetMaxPcieLinkWidth(handle)
            pcie_info = f"Gen{curr_gen} x{curr_width} (Max: Gen{max_gen} x{max_width})"
        except Exception:
            pass

        active_links = 0
        try:
            for link in range(12):
                if pynvml.nvmlDeviceGetNvLinkState(handle, link) == 1:
                    active_links += 1
        except Exception:
            pass

        comp_cap = "N/A"
        try:
            cap_major, cap_minor = pynvml.nvmlDeviceGetComputeCapability(handle)
            comp_cap = f"{cap_major}.{cap_minor}"
        except Exception:
            pass

        metrics = {
            "name": gpu_name,
            "UUID": uuid_str,
            "Serial_Number": serial_str,
            "VBIOS_Version": vbios_str,
            "Memory_Total": f"{int(total_mb)} MB",
            "Memory_Used": used_mb,
            "Memory_Free": free_mb,
            "BAR1_Memory_Total": f"{int(bar1_total)} MB",
            "BAR1_Memory_Used": bar1_used,
            "BAR1_Memory_Free": bar1_free,
            "PCIe_Link_Info": pcie_info,
            "PCIe_Link_Width": curr_width,
            "NVLink_Active_Links": active_links,
            "Compute_Capability": comp_cap
        }

        mem_stats = {"used_mb": used_mb, "total_mb": total_mb, "free_mb": free_mb}
        return metrics, mem_stats


# =============================================================================
# 3. HEALTH & ENVIRONMENTAL METRICS COLLECTOR (TAB 3)
# =============================================================================
class HealthCollector:
    """Extracts thermal, power, clock throttling, and hardware reliability metrics."""

    UNITS = {
        "GPU_Temperature": "C",
        "Memory_Temperature": "C",
        "Fan_Speed": "%",
        "Power_Usage": "W",
        "Power_Limit": "W",
        "Energy_Consumption": "J",
        "Clock_Throttle_Reasons": "text",
        "ECC_Errors_Single_Bit": "count",
        "ECC_Errors_Double_Bit": "count",
        "PCIe_Replay_Errors": "count",
        "Remapped_Memory_Rows": "count",
        "Row_Remapping_Failures": "count"
    }

    @staticmethod
    def collect(pynvml: Any, handle: Any, gpu_name: str) -> Tuple[Dict[str, Any], Dict[str, float]]:
        temp_core = 0.0
        try:
            temp_core = float(pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU))
        except Exception:
            pass

        temp_mem = 0.0
        try:
            temp_mem = float(pynvml.nvmlDeviceGetTemperature(handle, 1))
        except Exception:
            pass

        fan = 0.0
        try:
            fan = float(pynvml.nvmlDeviceGetFanSpeed(handle))
        except Exception:
            pass

        pwr_w = 0.0
        try:
            pwr_w = round(pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0, 2)
        except Exception:
            pass

        pwr_limit_w = 0.0
        try:
            pwr_limit_w = round(pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0, 2)
        except Exception:
            pass

        energy_j = 0.0
        try:
            energy_mj = pynvml.nvmlDeviceGetTotalEnergyConsumption(handle)
            energy_j = round(energy_mj / 1000.0, 2)
        except Exception:
            pass

        throttle_str = "None"
        try:
            throttle_bits = pynvml.nvmlDeviceGetCurrentClocksThrottleReasons(handle)
            reasons = []
            if throttle_bits & pynvml.nvmlClocksThrottleReasonGpuHardwareSlowdown:
                reasons.append("HW_Slowdown")
            if throttle_bits & pynvml.nvmlClocksThrottleReasonSwPowerCap:
                reasons.append("Power_Cap")
            if throttle_bits & pynvml.nvmlClocksThrottleReasonHwThermalSlowdown:
                reasons.append("Thermal_Slowdown")
            if throttle_bits & getattr(pynvml, "nvmlClocksThrottleReasonGpuIdle", 0x0000000000000001):
                reasons.append("Idle")
            if reasons:
                throttle_str = ", ".join(reasons)
        except Exception:
            pass

        sbe, dbe = 0, 0
        try:
            sbe = pynvml.nvmlDeviceGetTotalEccErrors(handle, 0, 0)
            dbe = pynvml.nvmlDeviceGetTotalEccErrors(handle, 1, 0)
        except Exception:
            pass

        replays = 0
        try:
            replays = pynvml.nvmlDeviceGetPcieReplayCounter(handle)
        except Exception:
            pass

        remapped_rows, remapping_failures = 0, 0
        try:
            corr_rows, uncorr_rows, is_pending, failure_occurred = pynvml.nvmlDeviceGetRemappedRows(handle)
            remapped_rows = corr_rows + uncorr_rows
            remapping_failures = 1 if failure_occurred else 0
        except Exception:
            pass

        metrics = {
            "name": gpu_name,
            "GPU_Temperature": temp_core,
            "Memory_Temperature": temp_mem,
            "Fan_Speed": fan,
            "Power_Usage": pwr_w,
            "Power_Limit": pwr_limit_w,
            "Energy_Consumption": energy_j,
            "Clock_Throttle_Reasons": throttle_str,
            "ECC_Errors_Single_Bit": sbe,
            "ECC_Errors_Double_Bit": dbe,
            "PCIe_Replay_Errors": replays,
            "Remapped_Memory_Rows": remapped_rows,
            "Row_Remapping_Failures": remapping_failures
        }

        health_stats = {"temp": temp_core, "power": pwr_w}
        return metrics, health_stats


# =============================================================================
# 4. PROCESS & ADVANCED MONITORING COLLECTOR (TAB 4)
# =============================================================================
class ProcessCollector:
    """Extracts process GPU usage, pod/container mappings, Slurm attribution, and workload classification."""

    UNITS = {
        "Active_Processes_Count": "count",
        "Process_GPU_Memory": "MB",
        "Training_Workload_Active": "count",
        "Process_ID": "text",
        "Process_Name": "text",
        "Pod_Level_GPU_Usage": "text",
        "Container_Level_GPU_Usage": "text",
        "Slurm_Job_Attribution": "text"
    }

    @staticmethod
    def collect(pynvml: Any, handle: Any, gpu_name: str) -> Tuple[Dict[str, Any], int]:
        running_procs: List[Any] = []
        try:
            try:
                compute_procs = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
                running_procs.extend(compute_procs)
            except Exception:
                pass

            try:
                graphics_procs = pynvml.nvmlDeviceGetGraphicsRunningProcesses(handle)
                known_pids = {p.pid for p in running_procs}
                for gp in graphics_procs:
                    if gp.pid not in known_pids:
                        running_procs.append(gp)
            except Exception:
                pass
        except Exception:
            pass

        is_training_active = 0
        top_proc_pid = "N/A"
        top_proc_name = "N/A"
        top_proc_mem = 0.0
        top_pod_uid = "N/A"
        top_container_id = "N/A"
        top_slurm_job = "N/A"

        if running_procs:
            sorted_procs = sorted(running_procs, key=lambda x: getattr(x, "usedGpuMemory", 0), reverse=True)
            primary_proc = sorted_procs[0]
            top_proc_pid = str(primary_proc.pid)
            top_proc_mem = round(primary_proc.usedGpuMemory / (1024 * 1024), 2)

            try:
                raw_name = pynvml.nvmlSystemGetProcessName(primary_proc.pid)
                top_proc_name = raw_name.decode("utf-8") if isinstance(raw_name, bytes) else str(raw_name)
                top_proc_name = os.path.basename(top_proc_name)
            except Exception:
                top_proc_name = "compute_job"

            c_id, p_uid, s_job = get_process_container_context(primary_proc.pid)
            if c_id != "N/A":
                top_container_id = c_id
            if p_uid != "N/A":
                top_pod_uid = p_uid
            if s_job != "N/A":
                top_slurm_job = s_job

            for p in running_procs:
                try:
                    pname = pynvml.nvmlSystemGetProcessName(p.pid)
                    pname_str = (pname.decode("utf-8") if isinstance(pname, bytes) else str(pname)).lower()
                    if any(sig in pname_str for sig in TRAINING_SIGNATURES):
                        is_training_active = 1
                        break
                except Exception:
                    pass

        metrics = {
            "name": gpu_name,
            "Active_Processes_Count": len(running_procs),
            "Process_ID": top_proc_pid,
            "Process_Name": top_proc_name,
            "Process_GPU_Memory": top_proc_mem,
            "Pod_Level_GPU_Usage": top_pod_uid,
            "Container_Level_GPU_Usage": top_container_id,
            "Slurm_Job_Attribution": top_slurm_job,
            "Training_Workload_Active": is_training_active
        }

        return metrics, len(running_procs)


# =============================================================================
# METRIC UNITS REGISTRY (SITE24x7 TABULAR SCHEMA)
# =============================================================================
METRIC_UNITS = {
    "GPU_Performance_Metrics": PerformanceCollector.UNITS,
    "GPU_Resource_Metrics": ResourceCollector.UNITS,
    "GPU_Health_Metrics": HealthCollector.UNITS,
    "GPU_Process_Metrics": ProcessCollector.UNITS,
    "Average_GPU_Utilization": "%",
    "Average_Memory_Utilization": "%",
    "Average_Memory_Used": "MB",
    "Average_Temperature": "C",
    "Total_Power_Draw": "W",
    "GPU_Idle_Cost": "$/hr",
    "GPU_Device_Count": "count",
    "GPU_Allocated_Devices": "count",
    "GPU_Active_Devices": "count",
    "GPU_Idle_Devices": "count",
    "Total_Active_Processes": "count",
    "XID_Errors_Count": "count",
    "GPU_Utilization_Highest": "%",
    "GPU_Utilization_Lowest": "%",
    "Highest_Memory_Utilization": "%",
    "Lowest_Memory_Utilization": "%",
    "Temperature_Lowest": "C",
    "Power_Highest": "W",
    "Power_Lowest": "W",
    "NVLink_Active_Links": "count",
    "NVLink_TX_Throughput": "KB/s",
    "NVLink_RX_Throughput": "KB/s",
    "ECC_Errors_Single_Bit": "count",
    "ECC_Errors_Double_Bit": "count",
    "Driver_Version": "text",
    "CUDA_Version": "text"
}


# =============================================================================
# TABULAR CATEGORY CONFIGURATION (SITE24x7 DASHBOARD TABS)
# =============================================================================
TABS = {
    "Performance": {
        "order": 1,
        "tablist": [
            "Average_GPU_Utilization",            
            "Average_Memory_Utilization",
            "GPU_Utilization_Highest",            
            "GPU_Utilization_Lowest",
            "Highest_Memory_Utilization",
            "Lowest_Memory_Utilization",
            "GPU_Performance_Metrics"
        ]
    },
    "Resources": {
        "order": 2,
        "tablist": [
            "Average_Memory_Used",
            "GPU_Device_Count",
            "GPU_Allocated_Devices",
            "NVLink_Active_Links",
            "NVLink_TX_Throughput",
            "NVLink_RX_Throughput",
            "GPU_Resource_Metrics"
        ]
    },
    "Health": {
        "order": 3,
        "tablist": [
            "Average_Temperature",
            "Total_Power_Draw",
            "Temperature_Highest",
            "Temperature_Lowest",
            "Power_Highest",
            "Power_Lowest",
            "XID_Errors_Count",
            "ECC_Errors_Single_Bit",
            "ECC_Errors_Double_Bit",
            "GPU_Health_Metrics"
        ]
    },
    "Processes": {
        "order": 4,
        "tablist": [
            "Total_Active_Processes",
            "GPU_Idle_Devices",
            "GPU_Idle_Cost",
            "GPU_Process_Metrics"
        ]
    }
}


# =============================================================================
# MAIN SITE24x7 PLUGIN CLASS (MATCHES OFFICIAL TEMPLATE)
# =============================================================================
class Plugin:
    """Official Site24x7 Custom Plugin Class implementation."""

    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.data: Dict[str, Any] = {}
        self.data["plugin_version"] = PLUGIN_VERSION
        self.data["heartbeat_required"] = HEARTBEAT
        self.data["units"] = METRIC_UNITS
        self.data["tabs"] = TABS

        self.hourly_cost = DEFAULT_HOURLY_GPU_COST
        self.nvidia_smi_path = "nvidia-smi"

        # Parse config params passed by Site24x7 Agent
        if params:
            if "hourly_cost" in params:
                try:
                    self.hourly_cost = float(params["hourly_cost"])
                except Exception:
                    pass
            if "nvidia_smi_path" in params:
                self.nvidia_smi_path = str(params["nvidia_smi_path"]).strip("\"'")

    def getData(self) -> Dict[str, Any]:
        """Site24x7 standard data collection entry point."""
        try:
            # 1. Attempt Native NVML API
            try:
                nvml_data = self._collect_nvml()
                self.data.update(nvml_data)
            except Exception as e_nvml:
                # 2. Fallback to CLI
                cli_data = self._collect_cli(e_nvml)
                self.data.update(cli_data)
        except Exception as e:
            self.data["status"] = 0
            self.data["msg"] = str(e)

        # Only return tabs if the plugin is healthy (status=1)
        # This forces Site24x7 to use the Summary tab for error messages
        if self.data.get("status") == 0:
            self.data.pop("tabs", None)

        return self.data

    def _collect_nvml(self) -> Dict[str, Any]:
        """Primary NVML metric collector."""
        import pynvml  # type: ignore

        pynvml.nvmlInit()
        try:
            device_count = pynvml.nvmlDeviceGetCount()
            if device_count == 0:
                return {
                    "status": 0,
                    "msg": "No NVIDIA GPU devices found on host"
                }

            try:
                drv = pynvml.nvmlSystemGetDriverVersion()
                driver_version = drv.decode("utf-8") if isinstance(drv, bytes) else str(drv)
            except Exception:
                driver_version = "N/A"

            try:
                cuda_raw = pynvml.nvmlSystemGetCudaDriverVersion()
                cuda_version = f"{cuda_raw // 1000}.{(cuda_raw % 1000) // 10}"
            except Exception:
                cuda_version = "N/A"

            perf_list: List[Dict[str, Any]] = []
            resource_list: List[Dict[str, Any]] = []
            health_list: List[Dict[str, Any]] = []
            process_list: List[Dict[str, Any]] = []

            gpu_utils: List[float] = []
            mem_utils: List[float] = []
            mems_used: List[float] = []
            temps: List[float] = []
            power_draws: List[float] = []

            total_active_procs = 0
            allocated_devices = 0
            active_devices = 0
            idle_devices = 0

            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)

                try:
                    raw_name = pynvml.nvmlDeviceGetName(handle)
                    dev_name = raw_name.decode("utf-8") if isinstance(raw_name, bytes) else str(raw_name)
                except Exception:
                    dev_name = f"NVIDIA GPU {i}"

                gpu_label = f"GPU {i} ({dev_name})"

                # 1. Performance
                perf_metrics, perf_stats = PerformanceCollector.collect(pynvml, handle, gpu_label)
                perf_list.append(perf_metrics)
                gpu_utils.append(perf_stats["gpu_util"])
                mem_utils.append(perf_stats["mem_util"])

                # Add flat metrics for graphing (first 2 GPUs)
                # (removed GPU0/GPU1Utilization; averages computed across all GPUs)

                # 2. Resource
                resource_metrics, mem_stats = ResourceCollector.collect(pynvml, handle, gpu_label)
                resource_list.append(resource_metrics)
                mems_used.append(mem_stats["used_mb"])

                # 3. Health
                health_metrics, health_stats = HealthCollector.collect(pynvml, handle, gpu_label)
                health_list.append(health_metrics)

                # Temperatures and power are aggregated across all GPUs (not per-GPU flat fields)

                if health_stats["temp"] > 0:
                    temps.append(health_stats["temp"])
                if health_stats["power"] > 0:
                    power_draws.append(health_stats["power"])

                # 4. Process
                proc_metrics, proc_count = ProcessCollector.collect(pynvml, handle, gpu_label)
                process_list.append(proc_metrics)
                total_active_procs += proc_count

                # Allocation tracking
                is_allocated = 1 if proc_count > 0 else 0
                is_active = 1 if perf_stats["gpu_util"] > 0 else 0
                is_idle = 1 if (not is_active and proc_count == 0) else 0

                if is_allocated: allocated_devices += 1
                if is_active: active_devices += 1
                if is_idle: idle_devices += 1

            return {
                "GPU_Device_Count": device_count,
                "GPU_Allocated_Devices": allocated_devices,
                "GPU_Active_Devices": active_devices,
                "GPU_Idle_Devices": idle_devices,
                "Total_Active_Processes": total_active_procs,
                "GPU_Idle_Cost": round(idle_devices * self.hourly_cost, 2),
                "Average_GPU_Utilization": round(sum(gpu_utils) / len(gpu_utils), 2) if gpu_utils else 0.0,
                "GPU_Utilization_Highest": round(max(gpu_utils), 2) if gpu_utils else 0.0,
                "GPU_Utilization_Lowest": round(min(gpu_utils), 2) if gpu_utils else 0.0,
                "Average_Memory_Utilization": round(sum(mem_utils) / len(mem_utils), 2) if mem_utils else 0.0,
                "Highest_Memory_Utilization": round(max(mem_utils), 2) if mem_utils else 0.0,
                "Lowest_Memory_Utilization": round(min(mem_utils), 2) if mem_utils else 0.0,
                "Average_Memory_Used": round(sum(mems_used) / len(mems_used), 2) if mems_used else 0.0,
                "Average_Temperature": round(sum(temps) / len(temps), 2) if temps else 0.0,
                "Temperature_Highest": round(max(temps), 2) if temps else 0.0,
                "Temperature_Lowest": round(min(temps), 2) if temps else 0.0,
                "Total_Power_Draw": round(sum(power_draws), 2) if power_draws else 0.0,
                "Power_Highest": round(max(power_draws), 2) if power_draws else 0.0,
                "Power_Lowest": round(min(power_draws), 2) if power_draws else 0.0,
                "XID_Errors_Count": get_latest_xid_errors(),
                "NVLink_Active_Links": sum(r.get("NVLink_Active_Links", 0) for r in resource_list),
                "NVLink_TX_Throughput": sum(p.get("NVLink_TX_Throughput", 0) for p in perf_list),
                "NVLink_RX_Throughput": sum(p.get("NVLink_RX_Throughput", 0) for p in perf_list),
                "ECC_Errors_Single_Bit": sum(h.get("ECC_Errors_Single_Bit", 0) for h in health_list),
                "ECC_Errors_Double_Bit": sum(h.get("ECC_Errors_Double_Bit", 0) for h in health_list),
                "Driver_Version": driver_version,
                "CUDA_Version": f"v {cuda_version}" if cuda_version != "N/A" else cuda_version,

                # 4 Tabular Metric Category Arrays (Rendered as individual Tabs in Site24x7)
                "GPU_Performance_Metrics": perf_list,
                "GPU_Resource_Metrics": resource_list,
                "GPU_Health_Metrics": health_list,
                "GPU_Process_Metrics": process_list,

                "status": 1,
                "msg": "GPU telemetry collected successfully via native NVML"
            }

        finally:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass

    def _collect_cli(self, e_nvml: Exception) -> Dict[str, Any]:
        """CLI fallback metric collector."""
        smi_bin = resolve_nvidia_smi(self.nvidia_smi_path)
        if not smi_bin:
            return {
                "status": 0,
                "msg": build_diagnostic(e_nvml)
            }

        fields = [
            "index", "name", "uuid", "driver_version", "utilization.gpu", "utilization.memory",
            "memory.total", "memory.used", "memory.free", "temperature.gpu", "power.draw",
            "enforced.power.limit", "fan.speed", "clocks.current.graphics", "clocks.current.memory"
        ]

        cmd = [smi_bin, "--query-gpu=" + ",".join(fields), "--format=csv,noheader,nounits"]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8", errors="replace").strip()
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]

        if not lines:
            return {
                "status": 0,
                "msg": f"NVML error: {e_nvml}; No GPU output returned from nvidia-smi"
            }

        perf_list, resource_list, health_list, process_list = [], [], [], []
        gpu_utils, mem_utils, mems_used, temps, powers = [], [], [], [], []
        driver_version = "N/A"

        for idx, ln in enumerate(lines):
            parts = [p.strip() for p in ln.split(",")]
            name = parts[1] if len(parts) > 1 else f"GPU {idx}"
            driver_version = parts[3] if len(parts) > 3 else "N/A"
            gpu_label = f"GPU {idx} ({name})"

            gpu_u = parse_smi_number(parts[4])
            mem_u = parse_smi_number(parts[5])
            mem_tot = parse_smi_number(parts[6])
            mem_usd = parse_smi_number(parts[7])
            mem_fre = parse_smi_number(parts[8])
            temp_v = parse_smi_number(parts[9])
            pwr_v = parse_smi_number(parts[10])
            pwr_lim = parse_smi_number(parts[11])
            fan_v = parse_smi_number(parts[12])
            clk_gfx = parse_smi_number(parts[13], cast=int)
            clk_mem = parse_smi_number(parts[14], cast=int)

            gpu_utils.append(gpu_u)
            mem_utils.append(mem_u)
            mems_used.append(mem_usd)
            temps.append(temp_v)
            powers.append(pwr_v)



            perf_list.append({
                "name": gpu_label,
                "GPU_Utilization": gpu_u,
                "Memory_Copy_Utilization": mem_u,
                "Core_Clock": clk_gfx,
                "Memory_Clock": clk_mem
            })

            resource_list.append({
                "name": gpu_label,
                "Memory_Total": f"{int(mem_tot)} MB",
                "Memory_Used": mem_usd,
                "Memory_Free": mem_fre
            })

            health_list.append({
                "name": gpu_label,
                "GPU_Temperature": temp_v,
                "Power_Usage": pwr_v,
                "Power_Limit": pwr_lim,
                "Fan_Speed": fan_v
            })

            process_list.append({
                "name": gpu_label,
                "Active_Processes_Count": 0,
                "Training_Workload_Active": 0
            })

        active_devs = sum(1 for u in gpu_utils if u > 0)
        idle_devs = len(lines) - active_devs

        return {
            "GPU_Device_Count": len(lines),
            "GPU_Allocated_Devices": active_devs,
            "GPU_Active_Devices": active_devs,
            "GPU_Idle_Devices": idle_devs,
            "Total_Active_Processes": 0,
            "GPU_Idle_Cost": round(idle_devs * self.hourly_cost, 2),
            "Average_GPU_Utilization": round(sum(gpu_utils) / len(gpu_utils), 2) if gpu_utils else 0.0,
            "GPU_Utilization_Highest": round(max(gpu_utils), 2) if gpu_utils else 0.0,
            "GPU_Utilization_Lowest": round(min(gpu_utils), 2) if gpu_utils else 0.0,
            "Average_Memory_Utilization": round(sum(mem_utils) / len(mem_utils), 2) if mem_utils else 0.0,
            "Highest_Memory_Utilization": round(max(mem_utils), 2) if mem_utils else 0.0,
            "Lowest_Memory_Utilization": round(min(mem_utils), 2) if mem_utils else 0.0,
            "Average_Memory_Used": round(sum(mems_used) / len(mems_used), 2) if mems_used else 0.0,
            "Average_Temperature": round(sum(temps) / len(temps), 2) if temps else 0.0,
            "Temperature_Highest": round(max(temps), 2) if temps else 0.0,
            "Temperature_Lowest": round(min(temps), 2) if temps else 0.0,
            "Total_Power_Draw": round(sum(powers), 2) if powers else 0.0,
            "Power_Highest": round(max(powers), 2) if powers else 0.0,
            "Power_Lowest": round(min(powers), 2) if powers else 0.0,
            "XID_Errors_Count": get_latest_xid_errors(),
            "Driver_Version": driver_version,
            
            "GPU_Performance_Metrics": perf_list,
            "GPU_Resource_Metrics": resource_list,
            "GPU_Health_Metrics": health_list,
            "GPU_Process_Metrics": process_list,

            "status": 1,
            "msg": "GPU telemetry collected via nvidia-smi CLI"
        }


# =============================================================================
# BACKWARD COMPATIBILITY ENTRY POINTS FOR SITE24x7 AGENT
# =============================================================================
def metricCollector(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Standard entry point for Site24x7 Agent."""
    plugin = Plugin(params)
    return plugin.getData()


def run(param: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Runner alias."""
    return metricCollector(param)


# =============================================================================
# STANDALONE EXECUTION / TEST RUNNER
# =============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Site24x7 NVIDIA NVML GPU Monitoring Plugin")
    parser.add_argument("param", nargs='?', default=None, help="Site24x7 JSON config string passed as positional arg")
    parser.add_argument("--hourly-cost", type=float, default=None, help="Hourly GPU idle cost rate in USD")
    parser.add_argument("--nvidia-smi-path", default=None, help="Path to nvidia-smi binary")
    parser.add_argument("--pretty", action="store_true", help="Print formatted indented JSON output")
    args = parser.parse_args()

    params: Dict[str, Any] = {}
    if args.param:
        try:
            params = json.loads(args.param)
        except Exception:
            pass

    if args.hourly_cost is not None:
        params["hourly_cost"] = args.hourly_cost
    if args.nvidia_smi_path is not None:
        params["nvidia_smi_path"] = args.nvidia_smi_path

    plugin = Plugin(params)
    data = plugin.getData()

    if args.pretty:
        print(json.dumps(data, indent=4, sort_keys=False))
    else:
        print(json.dumps(data, sort_keys=False))
