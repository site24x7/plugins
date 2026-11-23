# Site24x7 Linux Agent - NVIDIA NVML GPU Monitoring Plugin (`nvml`)

Production-ready Site24x7 Linux Monitoring Agent plugin collecting hardware, workload, health, and process telemetry from NVIDIA GPUs via **native NVML** (`nvidia-ml-py` / `pynvml`) with automatic fallback to **`nvidia-smi`**.

---

## 1. Performance Metrics

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | GPU_Utilization | % | Compute kernel load |
| 2 | Memory_Copy_Utilization | % | Memory bandwidth usage |
| 3 | SM_Clock | MHz | Streaming Multiprocessor clock |
| 4 | SM_Activity | % | SM active time |
| 5 | SM_Occupancy | % | Warp occupancy ratio |
| 6 | Core_Clock | MHz | Graphics core clock |
| 7 | Graphics_Engine_Activity | % | 3D pipeline load |
| 8 | Memory_Clock | MHz | Memory clock |
| 9 | Encoder_Utilization | % | NVENC video encode load |
| 10 | Decoder_Utilization | % | NVDEC video decode load |
| 11 | Tensor_Pipeline_Activity | % | Tensor Core AI pipeline |
| 12 | FP16_Activity | % | Half-precision compute |
| 13 | FP32_Activity | % | Single-precision compute |
| 14 | FP64_Activity | % | Double-precision compute |
| 15 | PCIe_TX_Throughput | KB/s | PCIe transmit throughput |
| 16 | PCIe_RX_Throughput | KB/s | PCIe receive throughput |
| 17 | NVLink_TX_Throughput | KB/s | NVLink fabric transmit |
| 18 | NVLink_RX_Throughput | KB/s | NVLink fabric receive |
| 19 | GPU_Saturation | % | Combined utilization index |

## 2. Resource Metrics

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | Memory_Total | MB | Total VRAM capacity |
| 2 | Memory_Used | MB | VRAM currently consumed |
| 3 | Memory_Free | MB | VRAM available |
| 4 | Memory_Reserved | MB | Driver/system reserved |
| 5 | Framebuffer_Utilization | % | VRAM usage ratio |
| 6 | BAR1_Memory_Total | MB | CPU-GPU address space total |
| 7 | BAR1_Memory_Used | MB | CPU-GPU address space used |
| 8 | BAR1_Memory_Free | MB | CPU-GPU address space free |
| 9 | PCIe_Link_Width | lanes | Current PCIe link width |
| 10 | NVLink_Active_Links | count | Active NVLink count |
| 11 | Allocatable_Capacity | MB | Usable VRAM for workloads |
| 12 | UUID | text | Hardware UUID |
| 13 | Serial_Number | text | Hardware serial number |
| 14 | VBIOS_Version | text | GPU firmware version |
| 15 | Compute_Capability | text | SM architecture version |
| 16 | Device_Capacity | text | Device capacity summary |

## 3. Health Metrics

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | GPU_Temperature | °C | Core silicon temperature |
| 2 | Memory_Temperature | °C | HBM/GDDR junction temperature |
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

## 4. Process Metrics

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | Active_Processes_Count | count | Number of running GPU processes |
| 2 | Process_ID | text | Top process PID |
| 3 | Process_Name | text | Top process binary name |
| 4 | Process_GPU_Memory | MB | Top process VRAM usage |
| 5 | Process_GPU_Utilization | % | Top process compute load |
| 6 | Pod_Level_GPU_Usage | text | Kubernetes Pod UID |
| 7 | Container_Level_GPU_Usage | text | Docker/Containerd ID |
| 8 | Slurm_Job_Attribution | text | Slurm Job ID |
| 9 | Training_Workload_Active | 0/1 | AI framework detected |
| 10 | GPU_Idle_Cost | $/hr | Financial waste per hour |

## 5. Fleet Summary Metrics

| # | Metric | Unit | Purpose |
|---|---|---|---|
| 1 | GPU_Device_Count | count | Total GPUs detected |
| 2 | GPU_Allocated_Devices | count | GPUs with active processes |
| 3 | GPU_Active_Devices | count | GPUs with utilization > 0 |
| 4 | GPU_Idle_Devices | count | GPUs with zero utilization |
| 5 | Total_Active_Processes | count | Total running GPU processes |
| 6 | GPU_Idle_Cost | $/hr | Total idle cost across fleet |
| 7 | Average_GPU_Utilization | % | Fleet-wide average utilization |
| 8 | GPU_Utilization_Highest | % | Highest utilization in fleet |
| 9 | GPU_Utilization_Lowest | % | Lowest utilization in fleet |
| 10 | Average_Memory_Utilization | % | Fleet-wide average memory usage |
| 11 | Average_Temperature | °C | Fleet-wide average temperature |
| 12 | Temperature_Highest | °C | Highest temperature in fleet |
| 13 | Temperature_Lowest | °C | Lowest temperature in fleet |
| 14 | Total_Power_Draw | W | Total power across all GPUs |
| 15 | Power_Highest | W | Highest power draw in fleet |
| 16 | Power_Lowest | W | Lowest power draw in fleet |
| 17 | Memory_Highest | MB | Highest memory usage in fleet |
| 18 | Memory_Lowest | MB | Lowest memory usage in fleet |
| 19 | XID_Errors_Count | count | Total XID critical errors |
| 20 | NVLink_Active_Links | count | Total active NVLink links |
| 21 | NVLink_TX_Throughput | KB/s | Total NVLink TX throughput |
| 22 | NVLink_RX_Throughput | KB/s | Total NVLink RX throughput |
| 23 | ECC_Errors | count | Total ECC errors |
| 24 | ECC_Errors_Single_Bit | count | Total single-bit ECC errors |
| 25 | ECC_Errors_Double_Bit | count | Total double-bit ECC errors |
| 26 | Driver_Version | text | NVIDIA driver version |
| 27 | CUDA_Version | text | CUDA toolkit version |

## 6. Summary

| Category | Count |
|---|---|
| Performance metrics | 19 |
| Resource metrics | 16 |
| Health metrics | 13 |
| Process metrics | 10 |
| Fleet summary metrics | 27 |
| **Total** | **85 metrics** |


---

## 2. Authentication & Collection Method

- **Authentication**: **None required**. NVML interfaces directly with the NVIDIA kernel driver (`/dev/nvidiactl`, `/dev/nvidia0..N`) at the system level without credential checks.
- **Library Collection**: Uses official NVIDIA Python bindings (`nvidia-ml-py` / `pynvml`).
- **CLI Fallback**: If Python NVML bindings are missing, automatically executes `nvidia-smi` queries.

---

## 3. Deployment on Linux Agent

The plugin **directory**, the **`.py` file**, and the **`.cfg` file** must all share the same
name. This plugin is named `nvml`, so the layout must be exactly:

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

> **Note:** if `nvidia-smi` itself is absent, the host has no NVIDIA driver installed and
> the plugin can only report `status: 0` with a diagnostic message — that is expected
> behaviour, not a plugin fault.

## 4. Optional `.cfg` parameters

```ini
[global_configurations]
use_agent_python=1

[instance_1]
nvidia_smi_path=nvidia-smi
hourly_cost=1.50
```

- `nvidia_smi_path` — path to the `nvidia-smi` binary. Defaults to `nvidia-smi` (resolved
  via `PATH` and the standard install locations). Do **not** wrap the value in quotes.
- `hourly_cost` — USD per GPU-hour used to compute the *GPU Idle Cost* metric.

