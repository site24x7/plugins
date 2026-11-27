# Site24x7 Linux Agent - NVIDIA NVML GPU Monitoring Plugin (`nvml`)

Production-ready Site24x7 Linux Monitoring Agent plugin collecting hardware, workload, health, and process telemetry from NVIDIA GPUs via **native NVML** (`nvidia-ml-py` / `pynvml`) with automatic fallback to **`nvidia-smi`**.

---

## 1. Performance Core Metrics (`GPU_Performance_Core`)

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | GPU_Utilization | % | Compute kernel load |
| 2 | Memory_Copy_Utilization | % | Memory bandwidth usage |
| 3 | SM_Clock | MHz | Streaming Multiprocessor clock |
| 4 | Core_Clock | MHz | Graphics core clock |
| 5 | Memory_Clock | MHz | VRAM memory clock |
| 6 | Encoder_Utilization | % | NVENC video encode load |
| 7 | Decoder_Utilization | % | NVDEC video decode load |
| 8 | GPU_Saturation | % | Combined compute/memory utilization index |

## 2. Performance Bus Metrics (`GPU_Performance_Bus`)

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | PCIe_TX_Throughput | KB/s | PCIe transmit throughput |
| 2 | PCIe_RX_Throughput | KB/s | PCIe receive throughput |
| 3 | NVLink_TX_Throughput | KB/s | NVLink fabric transmit (all links) |
| 4 | NVLink_RX_Throughput | KB/s | NVLink fabric receive (all links) |

## 3. Resource Memory Metrics (`GPU_Resource_Memory`)

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | Memory_Total | MB | Total VRAM capacity |
| 2 | Memory_Used | MB | VRAM currently consumed |
| 3 | Memory_Free | MB | VRAM available |
| 4 | Memory_Reserved | MB | Driver/system reserved VRAM |
| 5 | Framebuffer_Utilization | % | VRAM usage ratio |
| 6 | BAR1_Memory_Total | MB | CPU-GPU address space total |
| 7 | BAR1_Memory_Used | MB | CPU-GPU address space used |
| 8 | BAR1_Memory_Free | MB | CPU-GPU address space free |
| 9 | Allocatable_Capacity | MB | Usable VRAM for workloads |

## 4. Resource Hardware Metrics (`GPU_Resource_Hardware`)

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | UUID | text | Hardware UUID |
| 2 | Serial_Number | text | Hardware serial number |
| 3 | VBIOS_Version | text | GPU firmware version |
| 4 | PCIe_Link_Width | lanes | Current PCIe link width |
| 5 | NVLink_Active_Links | count | Active NVLink count |
| 6 | Compute_Capability | text | SM architecture version |
| 7 | Device_Capacity | text | Device capacity summary |

## 5. Health Metrics (`GPU_Health_Metrics`)

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | GPU_Temperature | °C | Core silicon temperature |
| 2 | Memory_Temperature | °C | HBM/GDDR junction temperature (if supported) |
| 3 | Fan_Speed | % | Cooling fan speed |
| 4 | Power_Usage | W | Instantaneous power draw |
| 5 | Power_Limit | W | Configured power ceiling |
| 6 | Energy_Consumption | J | Cumulative energy consumed |
| 7 | Clock_Throttle_Reasons | text | Why GPU is throttling |
| 8 | ECC_Errors | count | Total ECC errors |
| 9 | ECC_Errors_Single_Bit | count | Correctable memory errors |
| 10 | ECC_Errors_Double_Bit | count | Uncorrectable memory errors |
| 11 | PCIe_Replay_Errors | count | PCIe link retries |
| 12 | Remapped_Memory_Rows | count | Hardware row remapping count |
| 13 | Row_Remapping_Failures | count | Remapping failure flag |

## 6. Process Metrics (`GPU_Process_Metrics`)

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | Active_Processes_Count | count | Number of running GPU processes |
| 2 | Process_ID | text | Top process PID (by VRAM usage) |
| 3 | Process_Name | text | Top process binary name |
| 4 | Process_GPU_Memory | MB | Top process VRAM usage |
| 5 | Pod_Level_GPU_Usage | text | Kubernetes Pod UID |
| 6 | Container_Level_GPU_Usage | text | Docker/Containerd ID |
| 7 | Slurm_Job_Attribution | text | Slurm Job ID |
| 8 | Training_Workload_Active | 0/1 | AI framework detected (PyTorch, Ray, etc) |

## 7. Fleet Summary Metrics

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | GPU_Device_Count | count | Total GPUs detected |
| 2 | GPU_Allocated_Devices | count | GPUs with active processes or memory used |
| 3 | GPU_Active_Devices | count | GPUs with utilization > 0 |
| 4 | GPU_Idle_Devices | count | GPUs with zero utilization |
| 5 | Total_Active_Processes | count | Total running GPU processes |
| 6 | GPU_Idle_Cost | $/hr | Total idle cost across fleet |
| 7 | Average_GPU_Utilization | % | Fleet-wide average utilization |
| 8 | Average_Memory_Utilization | % | Fleet-wide average memory activity |
| 9 | Highest_Memory_Utilization | % | Highest memory activity across GPUs |
| 10 | Lowest_Memory_Utilization | % | Lowest memory activity across GPUs |
| 11 | Average_Memory_Used | MB | Average VRAM used across GPUs |
| 12 | Average_Temperature | °C | Fleet-wide average temperature |
| 13 | Total_Power_Draw | W | Total power across all GPUs |
| 14 | XID_Errors_Count | count | Total XID critical errors |
| 15 | NVLink_Active_Links | count | Total active NVLink links |
| 16 | NVLink_TX_Throughput | KB/s | Total NVLink TX throughput |
| 17 | NVLink_RX_Throughput | KB/s | Total NVLink RX throughput |
| 18 | ECC_Errors | count | Total ECC errors |
| 19 | ECC_Errors_Single_Bit | count | Total single-bit ECC errors |
| 20 | ECC_Errors_Double_Bit | count | Total double-bit ECC errors |
| 21 | Driver_Version | text | NVIDIA driver version |
| 22 | CUDA_Version | text attribute | CUDA driver-supported version, prefixed with `v` to keep it textual |

## 8. Summary

| Category | Count |
|---|---|
| Performance metrics | 12 |
| Resource metrics | 16 |
| Health metrics | 13 |
| Process metrics | 8 |
| Fleet summary metrics | 22 |
| **Total** | **71 metrics** |

---

## 2. Authentication & Collection Method

- **Authentication**: **None required**. NVML interfaces directly with the NVIDIA kernel driver (`/dev/nvidiactl`, `/dev/nvidia0..N`) at the system level without credential checks.
- **Library Collection**: Uses official NVIDIA Python bindings (`nvidia-ml-py` / `pynvml`).
- **CLI Fallback**: If Python NVML bindings are missing, automatically executes `nvidia-smi` queries with standardized output schemas.

---

## 3. Deployment on Linux Agent

The plugin **directory**, the **`.py` file**, and the **`.cfg` file** must all share the same name. This plugin is named `nvml`, so the layout must be exactly:

```
/opt/site24x7/monagent/plugins/nvml/nvml.py
/opt/site24x7/monagent/plugins/nvml/nvml.cfg
```

```bash
# 1. Create plugin directory
sudo mkdir -p /opt/site24x7/monagent/plugins/nvml

# 2. Copy files (both must be named nvml)
sudo cp nvml.py  /opt/site24x7/monagent/plugins/nvml/nvml.py
sudo cp nvml.cfg /opt/site24x7/monagent/plugins/nvml/nvml.cfg

# 3. Permissions and ownership (match the agent's service user)
sudo chmod +x /opt/site24x7/monagent/plugins/nvml/nvml.py
sudo chown site24x7:site24x7 /opt/site24x7/monagent/plugins/nvml/nvml.py \
                             /opt/site24x7/monagent/plugins/nvml/nvml.cfg

# 4. Install the NVML Python bindings into the AGENT's Python
#    (the agent's bundled interpreter does NOT ship with pynvml)
sudo /opt/site24x7/monagent/python/bin/pip install nvidia-ml-py

# 5. Test as the agent's own user — not as root
sudo -u site24x7 /opt/site24x7/monagent/python/bin/python \
     /opt/site24x7/monagent/plugins/nvml/nvml.py --pretty
```

### Verifying it is running

```bash
# Is the agent even attempting to run the plugin?
grep -i nvml /opt/site24x7/monagent/logs/*.txt

# Confirm the driver is reachable at all
nvidia-smi
```

> **Note:** if `nvidia-smi` itself is absent, the host has no NVIDIA driver installed and the plugin can only report `status: 0` with a diagnostic message — that is expected behaviour, not a plugin fault.

## 4. Optional `.cfg` parameters

```ini
[global_configurations]
use_agent_python=1

[instance_1]
nvidia_smi_path=nvidia-smi
hourly_cost=1.50
```

- `nvidia_smi_path` — path to the `nvidia-smi` binary. Defaults to `nvidia-smi` (resolved via `PATH` and the standard install locations). Do **not** wrap the value in quotes.
- `hourly_cost` — USD per GPU-hour used to compute the *GPU Idle Cost* metric.
