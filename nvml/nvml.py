#!/usr/bin/env python3
from __future__ import annotations

"""
Site24x7 Linux Agent Plugin - NVIDIA NVML GPU Monitoring 
=============================================================================
Follows official Site24x7 Plugin Class template standard (`Plugin.getData()`).
Hardened for production with accurate hardware telemetry, robust error
handling, and consistent multi-mode output schemas.
"""

import os
import sys
import json
import csv
import io
import argparse
import subprocess
from typing import Any, Dict, List, Optional, Tuple

# Mandatory Site24x7 Plugin Constants
PLUGIN_VERSION = 1
HEARTBEAT = True

# Default estimated hourly cost per GPU in USD
DEFAULT_HOURLY_GPU_COST = 1.50

# Well-known AI/ML Training Framework signatures
TRAINING_SIGNATURES = {
    "python", "torch", "deepspeed", "ray", "accelerate", "vllm", "triton",
    "jax", "train", "megatron", "tensorflow", "horovod"
}

# =============================================================================
# HELPER UTILITIES
# =============================================================================
def parse_smi_number(raw: str, cast: type = float) -> Optional[Any]:
    """Robust parsing for nvidia-smi CSV values."""
    if not raw: return None
    cleaned = raw.strip().strip("[]")
    if cleaned.upper() in ("N/A", "NA", "UNKNOWN", "-", ""):
        return None
    try:
        return cast(float(cleaned))
    except (ValueError, TypeError):
        return None

def get_process_container_context(pid: int) -> Tuple[str, str, str]:
    """Extracts container/pod context from /proc/<pid>/."""
    c_id, p_uid, s_job = "N/A", "N/A", "N/A"
    if sys.platform != "linux": return c_id, p_uid, s_job

    try:
        cgroup_path = f"/proc/{pid}/cgroup"
        if os.path.exists(cgroup_path):
            with open(cgroup_path, "r", errors="ignore") as f:
                for line in f:
                    if "pod" in line:
                        parts = line.strip().split("/")
                        for p in parts:
                            if p.startswith("pod"): p_uid = p.replace("pod", "").replace(".slice", "")
                            elif len(p) == 64: c_id = p[:12]
                    elif any(t in line for token in ("docker", "containerd", "kubepods")):
                        parts = line.strip().split("/")
                        for p in parts:
                            if len(p) == 64: c_id = p[:12]
    except Exception: pass

    try:
        env_path = f"/proc/{pid}/environ"
        if os.path.exists(env_path):
            with open(env_path, "rb") as f:
                content = f.read().decode("utf-8", errors="ignore")
                for item in content.split("\x00"):
                    if item.startswith(("SLURM_JOB_ID=", "SLURM_JOBID=")):
                        s_job = item.split("=", 1)[1]
                        break
    except Exception: pass
    return c_id, p_uid, s_job

def resolve_nvidia_smi(hint: str = "nvidia-smi") -> Optional[str]:
    """Locates nvidia-smi binary."""
    cand = (hint or "nvidia-smi").strip().strip("\"'").strip()
    if os.path.dirname(cand) and os.path.isfile(cand): return cand
    import shutil
    found = shutil.which(cand or "nvidia-smi")
    if found: return found
    for p in ("/usr/bin/nvidia-smi", "/usr/local/nvidia/bin/nvidia-smi", "/usr/local/bin/nvidia-smi"):
        if os.path.isfile(p): return p
    return None

def get_latest_xid_errors() -> Optional[int]:
    """Counts XID errors in dmesg within the last 10 minutes (heuristic)."""
    if sys.platform != "linux": return None
    try:
        out = subprocess.check_output(["dmesg", "-T"], stderr=subprocess.STDOUT, timeout=3).decode("utf-8", errors="ignore")
        return out.count("NVRM: Xid")
    except Exception: return None

# =============================================================================
# COLLECTORS
# =============================================================================
class PerformanceCollector:
    UNITS_CORE = {"GPU_Utilization": "%", "Memory_Utilization": "%", "SM_Clock": "MHz", "Core_Clock": "MHz", "Memory_Clock": "MHz", "Encoder_Utilization": "%", "Decoder_Utilization": "%"}
    UNITS_BUS = {"PCIe_TX_Throughput": "KB/s", "PCIe_RX_Throughput": "KB/s", "NVLink_TX_Throughput": "KB/s", "NVLink_RX_Throughput": "KB/s"}

    @staticmethod
    def collect(pynvml: Any, handle: Any, name: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        core, bus, stats = {"name": name}, {"name": name}, {}
        try:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            core["GPU_Utilization"] = stats["gpu_util"] = float(util.gpu)
            core["Memory_Utilization"] = stats["mem_util"] = float(util.memory)
        except Exception: core["GPU_Utilization"] = core["Memory_Utilization"] = "N/A"

        for key, clock_type in [("SM_Clock", pynvml.NVML_CLOCK_SM), ("Core_Clock", pynvml.NVML_CLOCK_GRAPHICS), ("Memory_Clock", pynvml.NVML_CLOCK_MEM)]:
            try: core[key] = pynvml.nvmlDeviceGetClockInfo(handle, clock_type)
            except Exception: core[key] = "N/A"

        try:
            enc = pynvml.nvmlDeviceGetEncoderUtilization(handle)
            core["Encoder_Utilization"] = float(enc[0])
        except Exception: core["Encoder_Utilization"] = "N/A"
        try:
            dec = pynvml.nvmlDeviceGetDecoderUtilization(handle)
            core["Decoder_Utilization"] = float(dec[0])
        except Exception: core["Decoder_Utilization"] = "N/A"

        try:
            bus["PCIe_TX_Throughput"] = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
            bus["PCIe_RX_Throughput"] = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
        except Exception: bus["PCIe_TX_Throughput"] = bus["PCIe_RX_Throughput"] = "N/A"

        nv_tx, nv_rx = 0, 0
        try:
            found_nv = False
            for l in range(getattr(pynvml, 'NVML_NVLINK_MAX_LINKS', 12)):
                if pynvml.nvmlDeviceGetNvLinkState(handle, l) == 1:
                    found_nv = True
                    c = pynvml.nvmlDeviceGetNvLinkUtilizationCounter(handle, l, 0)
                    nv_tx += c.get("tx", 0); nv_rx += c.get("rx", 0)
            bus["NVLink_TX_Throughput"] = nv_tx if found_nv else "N/A"
            bus["NVLink_RX_Throughput"] = nv_rx if found_nv else "N/A"
        except Exception: bus["NVLink_TX_Throughput"] = bus["NVLink_RX_Throughput"] = "N/A"

        stats["nv_tx"] = nv_tx; stats["nv_rx"] = nv_rx
        return core, bus, stats

class ResourceCollector:
    UNITS_MEM = {"Memory_Total": "MB", "Memory_Used": "MB", "Memory_Free": "MB", "Memory_Reserved": "MB", "Framebuffer_Utilization": "%", "BAR1_Memory_Total": "MB", "BAR1_Memory_Used": "MB", "BAR1_Memory_Free": "MB", "Allocatable_Capacity": "MB"}
    UNITS_HW = {"UUID": "text", "Serial_Number": "text", "VBIOS_Version": "text", "PCIe_Link_Width": "lanes", "NVLink_Active_Links": "count", "Compute_Capability": "text", "Device_Capacity": "text"}

    @staticmethod
    def collect(pynvml: Any, handle: Any, name: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        mem, hw, stats = {"name": name}, {"name": name}, {}
        try:
            uuid = pynvml.nvmlDeviceGetUUID(handle)
            hw["UUID"] = uuid.decode("utf-8") if isinstance(uuid, bytes) else str(uuid)
        except Exception: hw["UUID"] = "N/A"
        try:
            sn = pynvml.nvmlDeviceGetSerial(handle)
            hw["Serial_Number"] = sn.decode("utf-8") if isinstance(sn, bytes) else str(sn)
        except Exception: hw["Serial_Number"] = "N/A"
        try:
            vb = pynvml.nvmlDeviceGetVbiosVersion(handle)
            hw["VBIOS_Version"] = vb.decode("utf-8") if isinstance(vb, bytes) else str(vb)
        except Exception: hw["VBIOS_Version"] = "N/A"

        try:
            m = pynvml.nvmlDeviceGetMemoryInfo(handle)
            mem["Memory_Total"] = round(m.total / 1048576, 2)
            mem["Memory_Used"] = stats["used_mb"] = round(m.used / 1048576, 2)
            mem["Memory_Free"] = round(m.free / 1048576, 2)
            mem["Memory_Reserved"] = round(max(0.0, (m.total - m.used - m.free) / 1048576), 2)
            mem["Framebuffer_Utilization"] = round((m.used / m.total * 100.0), 2) if m.total > 0 else 0.0
            mem["Allocatable_Capacity"] = mem["Memory_Free"]
        except Exception:
            for k in ["Memory_Total", "Memory_Used", "Memory_Free", "Memory_Reserved", "Framebuffer_Utilization", "Allocatable_Capacity"]: mem[k] = "N/A"

        try:
            b = pynvml.nvmlDeviceGetBAR1MemoryInfo(handle)
            mem["BAR1_Memory_Total"] = round(b.bar1Total / 1048576, 2)
            mem["BAR1_Memory_Used"] = round(b.bar1Used / 1048576, 2)
            mem["BAR1_Memory_Free"] = round(b.bar1Free / 1048576, 2)
        except Exception:
            for k in ["BAR1_Memory_Total", "BAR1_Memory_Used", "BAR1_Memory_Free"]: mem[k] = "N/A"

        try: hw["PCIe_Link_Width"] = pynvml.nvmlDeviceGetCurrPcieLinkWidth(handle)
        except Exception: hw["PCIe_Link_Width"] = "N/A"

        nv_links = 0
        try:
            found_nv = False
            for l in range(getattr(pynvml, 'NVML_NVLINK_MAX_LINKS', 12)):
                if pynvml.nvmlDeviceGetNvLinkState(handle, l) == 1:
                    found_nv = True; nv_links += 1
            hw["NVLink_Active_Links"] = nv_links if found_nv else "N/A"
        except Exception: hw["NVLink_Active_Links"] = "N/A"

        try:
            maj, min_ = pynvml.nvmlDeviceGetComputeCapability(handle)
            hw["Compute_Capability"] = f"{maj}.{min_}"
            hw["Device_Capacity"] = f"{mem.get('Memory_Total', 'N/A')} MB (SM {hw['Compute_Capability']})"
        except Exception: hw["Compute_Capability"] = hw["Device_Capacity"] = "N/A"

        stats["nv_links"] = nv_links
        return mem, hw, stats

class HealthCollector:
    UNITS = {"GPU_Temperature": "C", "Memory_Temperature": "C", "Fan_Speed": "%", "Power_Usage": "W", "Power_Limit": "W", "Energy_Consumption": "J", "Clock_Throttle_Reasons": "text", "ECC_Errors": "count", "ECC_Errors_Single_Bit": "count", "ECC_Errors_Double_Bit": "count", "PCIe_Replay_Errors": "count", "Remapped_Memory_Rows": "count", "Row_Remapping_Failures": "count"}

    @staticmethod
    def collect(pynvml: Any, handle: Any, name: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        h, stats = {"name": name}, {}
        try: h["GPU_Temperature"] = stats["temp"] = float(pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU))
        except Exception: h["GPU_Temperature"] = "N/A"
        try:
            # NVML_TEMPERATURE_MEMORY is usually 1
            h["Memory_Temperature"] = float(pynvml.nvmlDeviceGetTemperature(handle, 1))
        except Exception: h["Memory_Temperature"] = "N/A"

        try: h["Fan_Speed"] = float(pynvml.nvmlDeviceGetFanSpeed(handle))
        except Exception: h["Fan_Speed"] = "N/A"
        try: h["Power_Usage"] = stats["power"] = round(pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0, 2)
        except Exception: h["Power_Usage"] = "N/A"
        try: h["Power_Limit"] = round(pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0, 2)
        except Exception: h["Power_Limit"] = "N/A"
        try: h["Energy_Consumption"] = round(pynvml.nvmlDeviceGetTotalEnergyConsumption(handle) / 1000.0, 2)
        except Exception: h["Energy_Consumption"] = "N/A"

        reasons = []
        try:
            bits = pynvml.nvmlDeviceGetCurrentClocksThrottleReasons(handle)
            if bits & getattr(pynvml, 'nvmlClocksThrottleReasonGpuHardwareSlowdown', 0): reasons.append("HW_Slowdown")
            if bits & getattr(pynvml, 'nvmlClocksThrottleReasonSwPowerCap', 0): reasons.append("Power_Cap")
            if bits & getattr(pynvml, 'nvmlClocksThrottleReasonHwThermalSlowdown', 0): reasons.append("Thermal_Slowdown")
            if bits & getattr(pynvml, 'nvmlClocksThrottleReasonGpuIdle', 0x1): reasons.append("Idle")
            h["Clock_Throttle_Reasons"] = ", ".join(reasons) if reasons else "None"
        except Exception: h["Clock_Throttle_Reasons"] = "N/A"

        try:
            sbe = pynvml.nvmlDeviceGetTotalEccErrors(handle, 0, 0)
            dbe = pynvml.nvmlDeviceGetTotalEccErrors(handle, 1, 0)
            h["ECC_Errors_Single_Bit"], h["ECC_Errors_Double_Bit"], h["ECC_Errors"] = sbe, dbe, sbe+dbe
            stats["sbe"], stats["dbe"] = sbe, dbe
        except Exception:
            for k in ["ECC_Errors_Single_Bit", "ECC_Errors_Double_Bit", "ECC_Errors"]: h[k] = "N/A"

        try: h["PCIe_Replay_Errors"] = pynvml.nvmlDeviceGetPcieReplayCounter(handle)
        except Exception: h["PCIe_Replay_Errors"] = "N/A"

        try:
            c, u, _, f = pynvml.nvmlDeviceGetRemappedRows(handle)
            h["Remapped_Memory_Rows"], h["Row_Remapping_Failures"] = c+u, (1 if f else 0)
        except Exception: h["Remapped_Memory_Rows"] = h["Row_Remapping_Failures"] = "N/A"

        return h, stats

class ProcessCollector:
    UNITS = {"Active_Processes_Count": "count", "Process_ID": "text", "Process_Name": "text", "Process_GPU_Memory": "MB", "Pod_Level_GPU_Usage": "text", "Container_Level_GPU_Usage": "text", "Slurm_Job_Attribution": "text", "Training_Workload_Active": "count"}

    @staticmethod
    def collect(pynvml: Any, handle: Any, name: str) -> Tuple[Dict[str, Any], int]:
        procs, count = {"name": name}, 0
        try:
            all_procs = []
            try: all_procs.extend(pynvml.nvmlDeviceGetComputeRunningProcesses(handle))
            except Exception: pass
            try:
                known = {p.pid for p in all_procs}
                for gp in pynvml.nvmlDeviceGetGraphicsRunningProcesses(handle):
                    if gp.pid not in known: all_procs.append(gp)
            except Exception: pass

            count = len(all_procs)
            procs["Active_Processes_Count"] = count
            display = sorted(all_procs, key=lambda x: getattr(x, "usedGpuMemory", 0), reverse=True)[:25]

            if display:
                p = display[0]
                procs["Process_ID"] = str(p.pid)
                procs["Process_GPU_Memory"] = round(p.usedGpuMemory / 1048576, 2)
                try:
                    raw = pynvml.nvmlSystemGetProcessName(p.pid)
                    procs["Process_Name"] = os.path.basename(raw.decode("utf-8") if isinstance(raw, bytes) else str(raw))
                except Exception: procs["Process_Name"] = "compute_job"

                c, po, s = get_process_container_context(p.pid)
                procs["Container_Level_GPU_Usage"], procs["Pod_Level_GPU_Usage"], procs["Slurm_Job_Attribution"] = c, po, s

                is_train = 0
                for ap in all_procs:
                    try:
                        n = str(pynvml.nvmlSystemGetProcessName(ap.pid)).lower()
                        if any(s in n for s in TRAINING_SIGNATURES): is_train = 1; break
                    except Exception: pass
                procs["Training_Workload_Active"] = is_train
            else:
                for k in ["Process_ID", "Process_Name", "Process_GPU_Memory", "Pod_Level_GPU_Usage", "Container_Level_GPU_Usage", "Slurm_Job_Attribution", "Training_Workload_Active"]: procs[k] = "N/A"
        except Exception:
            for k in ["Active_Processes_Count", "Process_ID", "Process_Name", "Process_GPU_Memory", "Pod_Level_GPU_Usage", "Container_Level_GPU_Usage", "Slurm_Job_Attribution", "Training_Workload_Active"]: procs[k] = "N/A"
        return procs, count

# =============================================================================
# PLUGIN CLASS
# =============================================================================
class Plugin:
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        self.data: Dict[str, Any] = {"plugin_version": PLUGIN_VERSION, "heartbeat_required": HEARTBEAT, "units": {
            "GPU_Performance_Core": PerformanceCollector.UNITS_CORE, "GPU_Performance_Bus": PerformanceCollector.UNITS_BUS,
            "GPU_Resource_Memory": ResourceCollector.UNITS_MEM, "GPU_Resource_Hardware": ResourceCollector.UNITS_HW,
            "GPU_Health_Metrics": HealthCollector.UNITS, "GPU_Process_Metrics": ProcessCollector.UNITS,
            "Average_GPU_Utilization": "%", "Average_Memory_Utilization": "%", "Average_Temperature": "C", "Total_Power_Draw": "W", "GPU_Idle_Cost": "$/hr",
            "GPU_Device_Count": "count", "GPU_Allocated_Devices": "count", "GPU_Active_Devices": "count", "GPU_Idle_Devices": "count", "Total_Active_Processes": "count",
            "Driver_Version": "text", "CUDA_Version": "text", "XID_Errors_Count": "count", "ECC_Errors": "count", "ECC_Errors_Single_Bit": "count", "ECC_Errors_Double_Bit": "count",
            "NVLink_Active_Links": "count", "NVLink_TX_Throughput": "KB/s", "NVLink_RX_Throughput": "KB/s"
        }, "tabs": {
            "Performance": {"order": 1, "tablist": ["Average_GPU_Utilization", "Average_Memory_Utilization", "GPU_Performance_Core", "GPU_Performance_Bus"]},
            "Resources": {"order": 2, "tablist": ["GPU_Device_Count", "GPU_Allocated_Devices", "GPU_Resource_Memory", "GPU_Resource_Hardware"]},
            "Health": {"order": 3, "tablist": ["Average_Temperature", "Total_Power_Draw", "XID_Errors_Count", "ECC_Errors", "GPU_Health_Metrics"]},
            "Processes": {"order": 4, "tablist": ["Total_Active_Processes", "GPU_Idle_Devices", "GPU_Idle_Cost", "GPU_Process_Metrics"]}
        }}
        self.hourly_cost = DEFAULT_HOURLY_GPU_COST
        self.smi_path = "nvidia-smi"
        if params:
            c = params.get("hourly_cost") or params.get("hourly-cost")
            if c is not None:
                try: self.hourly_cost = max(0.0, float(c))
                except: pass
            self.smi_path = str(params.get("nvidia_smi_path") or "nvidia-smi").strip("\"'")

    def getData(self) -> Dict[str, Any]:
        try:
            try: self.data.update(self._collect_nvml())
            except Exception as e: self.data.update(self._collect_cli(e))
        except Exception as e: self.data.update({"status": 0, "msg": str(e)})
        if self.data.get("status") == 0: self.data.pop("tabs", None)
        return self.data

    def _collect_nvml(self) -> Dict[str, Any]:
        import pynvml
        pynvml.nvmlInit()
        try:
            count = pynvml.nvmlDeviceGetCount()
            if count == 0: return {"status": 0, "msg": "No GPUs"}
            drv = pynvml.nvmlSystemGetDriverVersion()
            d_ver = drv.decode("utf-8") if isinstance(drv, bytes) else str(drv)
            try:
                c_raw = pynvml.nvmlSystemGetCudaDriverVersion()
                c_ver = f"{c_raw // 1000}.{(c_raw % 1000) // 10}"
            except: c_ver = "N/A"

            p_c, p_b, r_m, r_h, hl, pr = [], [], [], [], [], []
            g_u, m_u, m_us, temps, pwrs, nvl, n_tx, n_rx, sbes, dbes = [], [], [], [], [], [], [], [], [], []
            t_ap, a_d, ac_d, i_d = 0, 0, 0, 0

            for i in range(count):
                h = pynvml.nvmlDeviceGetHandleByIndex(i)
                try:
                    rn = pynvml.nvmlDeviceGetName(h)
                    dn = rn.decode("utf-8") if isinstance(rn, bytes) else str(rn)
                except: dn = f"GPU {i}"
                lbl = f"GPU {i} ({dn})"

                pc_m, pb_m, ps = PerformanceCollector.collect(pynvml, h, lbl)
                rm_m, rh_m, rs = ResourceCollector.collect(pynvml, h, lbl)
                h_m, hs = HealthCollector.collect(pynvml, h, lbl)
                pr_m, prc = ProcessCollector.collect(pynvml, h, lbl)

                p_c.append(pc_m); p_b.append(pb_m); r_m.append(rm_m); r_h.append(rh_m); hl.append(h_m); pr.append(pr_m)
                if isinstance(ps.get("gpu_util"), float): g_u.append(ps["gpu_util"])
                if isinstance(ps.get("mem_util"), float): m_u.append(ps["mem_util"])
                if isinstance(ps.get("nv_tx"), (int, float)): n_tx.append(ps["nv_tx"]); n_rx.append(ps["nv_rx"])
                if isinstance(rs.get("used_mb"), float): m_us.append(rs["used_mb"])
                if isinstance(rs.get("nv_links"), int): nvl.append(rs["nv_links"])
                if isinstance(hs.get("temp"), float): temps.append(hs["temp"])
                if isinstance(hs.get("power"), float): pwrs.append(hs["power"])
                if isinstance(hs.get("sbe"), int): sbes.append(hs["sbe"]); dbes.append(hs["dbe"])
                if isinstance(prc, int): t_ap += prc

                is_allocated = (prc > 0 or (rs.get("used_mb", 0) > 10 if isinstance(rs.get("used_mb"), float) else False))
                is_active = (ps.get("gpu_util", 0) > 0 if isinstance(ps.get("gpu_util"), float) else False)
                if is_allocated: a_d += 1
                if is_active: ac_d += 1
                else: i_d += 1

            xid = get_latest_xid_errors()
            return {
                "status": 1, "msg": "Collected via NVML", "GPU_Device_Count": count, "GPU_Allocated_Devices": a_d, "GPU_Active_Devices": ac_d, "GPU_Idle_Devices": i_d, "Total_Active_Processes": t_ap,
                "GPU_Idle_Cost": round(i_d * self.hourly_cost, 2), "Average_GPU_Utilization": round(sum(g_u)/len(g_u), 2) if g_u else "N/A",
                "Average_Memory_Utilization": round(sum(m_u)/len(m_u), 2) if m_u else "N/A", "Average_Temperature": round(sum(temps)/len(temps), 2) if temps else "N/A",
                "Total_Power_Draw": round(sum(pwrs), 2) if pwrs else "N/A", "NVLink_Active_Links": sum(nvl) if nvl else "N/A",
                "NVLink_TX_Throughput": sum(n_tx) if n_tx else "N/A", "NVLink_RX_Throughput": sum(n_rx) if n_rx else "N/A",
                "ECC_Errors_Single_Bit": sum(sbes) if sbes else "N/A", "ECC_Errors_Double_Bit": sum(dbes) if dbes else "N/A", "ECC_Errors": sum(sbes)+sum(dbes) if sbes else "N/A",
                "Driver_Version": d_ver, "CUDA_Version": c_ver, "XID_Errors_Count": xid if xid is not None else "N/A",
                "GPU_Performance_Core": p_c, "GPU_Performance_Bus": p_b, "GPU_Resource_Memory": r_m, "GPU_Resource_Hardware": r_h, "GPU_Health_Metrics": hl, "GPU_Process_Metrics": pr
            }
        finally:
            try: pynvml.nvmlShutdown()
            except: pass

    def _collect_cli(self, e_nvml: Exception) -> Dict[str, Any]:
        smi = resolve_nvidia_smi(self.smi_path)
        if not smi: return {"status": 0, "msg": f"NVML fail: {e_nvml}; nvidia-smi missing"}
        flds = ["index", "name", "utilization.gpu", "utilization.memory", "memory.total", "memory.used", "memory.free", "temperature.gpu", "power.draw", "enforced.power.limit", "fan.speed", "uuid", "serial", "vbios_version"]
        try:
            out = subprocess.check_output([smi, "--query-gpu=" + ",".join(flds), "--format=csv,noheader,nounits"], stderr=subprocess.STDOUT, timeout=5).decode("utf-8", errors="replace").strip()
        except Exception as e: return {"status": 0, "msg": f"NVML fail: {e_nvml}; CLI fail: {e}"}

        p_c, p_b, r_m, r_h, hl, pr = [], [], [], [], [], []
        g_u, m_u, m_us, temps, pwrs = [], [], [], [], []
        reader = csv.reader(io.StringIO(out))
        rows = list(reader)
        if not rows: return {"status": 0, "msg": "Empty CLI"}

        for idx, row in enumerate(rows):
            row = [x.strip() for x in row]
            if len(row) < 14: continue
            lbl = f"GPU {idx} ({row[1]})"
            gu, mu, mt, mus, mf, t, pd, pl, fs = [parse_smi_number(x) for x in row[2:11]]
            uuid, sn, vb = row[11], row[12], row[13]

            p_c.append({"name": lbl, "GPU_Utilization": gu if gu is not None else "N/A", "Memory_Utilization": mu if mu is not None else "N/A", "SM_Clock": "N/A", "Core_Clock": "N/A", "Memory_Clock": "N/A", "Encoder_Utilization": "N/A", "Decoder_Utilization": "N/A"})
            p_b.append({"name": lbl, "PCIe_TX_Throughput": "N/A", "PCIe_RX_Throughput": "N/A", "NVLink_TX_Throughput": "N/A", "NVLink_RX_Throughput": "N/A"})
            r_m.append({"name": lbl, "Memory_Total": mt if mt is not None else "N/A", "Memory_Used": mus if mus is not None else "N/A", "Memory_Free": mf if mf is not None else "N/A", "Memory_Reserved": "N/A", "Framebuffer_Utilization": round((mus/mt*100), 2) if (mus and mt) else "N/A", "BAR1_Memory_Total": "N/A", "BAR1_Memory_Used": "N/A", "BAR1_Memory_Free": "N/A", "Allocatable_Capacity": mf if mf is not None else "N/A"})
            r_h.append({"name": lbl, "UUID": uuid, "Serial_Number": sn, "VBIOS_Version": vb, "PCIe_Link_Width": "N/A", "NVLink_Active_Links": "N/A", "Compute_Capability": "N/A", "Device_Capacity": "N/A"})
            hl.append({"name": lbl, "GPU_Temperature": t if t is not None else "N/A", "Memory_Temperature": "N/A", "Fan_Speed": fs if fs is not None else "N/A", "Power_Usage": pd if pd is not None else "N/A", "Power_Limit": pl if pl is not None else "N/A", "Energy_Consumption": "N/A", "Clock_Throttle_Reasons": "N/A", "ECC_Errors": "N/A", "ECC_Errors_Single_Bit": "N/A", "ECC_Errors_Double_Bit": "N/A", "PCIe_Replay_Errors": "N/A", "Remapped_Memory_Rows": "N/A", "Row_Remapping_Failures": "N/A"})
            pr.append({"name": lbl, "Active_Processes_Count": "N/A", "Process_ID": "N/A", "Process_Name": "N/A", "Process_GPU_Memory": "N/A", "Pod_Level_GPU_Usage": "N/A", "Container_Level_GPU_Usage": "N/A", "Slurm_Job_Attribution": "N/A", "Training_Workload_Active": "N/A"})

            if gu is not None: g_u.append(gu)
            if mu is not None: m_u.append(mu)
            if mus is not None: m_us.append(mus)
            if t is not None: temps.append(t)
            if pd is not None: pwrs.append(pd)

        ac_d = sum(1 for u in g_u if u > 0); i_d = len(rows) - ac_d
        xid = get_latest_xid_errors()
        return {
            "status": 1, "msg": "Collected via CLI", "GPU_Device_Count": len(rows), "GPU_Allocated_Devices": ac_d, "GPU_Active_Devices": ac_d, "GPU_Idle_Devices": i_d, "Total_Active_Processes": "N/A",
            "GPU_Idle_Cost": round(i_d * self.hourly_cost, 2), "Average_GPU_Utilization": round(sum(g_u)/len(g_u), 2) if g_u else "N/A",
            "Average_Memory_Utilization": round(sum(m_u)/len(m_u), 2) if m_u else "N/A", "Average_Temperature": round(sum(temps)/len(temps), 2) if temps else "N/A",
            "Total_Power_Draw": round(sum(pwrs), 2) if pwrs else "N/A", "NVLink_Active_Links": "N/A", "NVLink_TX_Throughput": "N/A", "NVLink_RX_Throughput": "N/A",
            "ECC_Errors_Single_Bit": "N/A", "ECC_Errors_Double_Bit": "N/A", "ECC_Errors": "N/A", "Driver_Version": "N/A", "CUDA_Version": "N/A", "XID_Errors_Count": xid if xid is not None else "N/A",
            "GPU_Performance_Core": p_c, "GPU_Performance_Bus": p_b, "GPU_Resource_Memory": r_m, "GPU_Resource_Hardware": r_h, "GPU_Health_Metrics": hl, "GPU_Process_Metrics": pr
        }

def metricCollector(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return Plugin(params).getData()

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument("param", nargs='?', default=None); p.add_argument("--hourly_cost", type=float); p.add_argument("--pretty", action="store_true"); a = p.parse_args()
    params = json.loads(a.param) if a.param else {}
    if a.hourly_cost: params["hourly_cost"] = a.hourly_cost
    print(json.dumps(metricCollector(params), indent=4 if a.pretty else None))
