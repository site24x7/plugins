# NVIDIA DCGM Monitoring Plugin

This plugin monitors NVIDIA GPU hardware metrics by scraping the DCGM Prometheus exporter. It provides deep visibility into GPU utilization, memory states, thermal health, and performance states across multi-GPU systems.

## Prerequisites
- **Site24x7 Agent**: Download and install the latest [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor).
- **Python**: version 3.6 or higher.
- **NVIDIA DCGM Exporter**: Must be running and exposing metrics (default port 9400). Supports DCGM Exporter v3.x and above.
- **Network**: The agent must have HTTP/HTTPS access to the DCGM exporter endpoint.

## Quick Installation
1. Create a directory named `dcgm`:
   ```bash
   mkdir dcgm
   cd dcgm/
   ```
2. Download `dcgm.py` and `dcgm.cfg` into the directory.
3. Verify the plugin output manually:
   ```bash
   python3 dcgm.py --dcgm_endpoint "http://localhost:9400/metrics"
   ```
4. Move the folder to the Site24x7 agent plugin directory:
   ```bash
   mv dcgm /opt/site24x7/monagent/plugins/
   ```

## Configuration
Configure the following parameters in `dcgm.cfg`:

```ini
[instance_1]
dcgm_endpoint="http://localhost:9400/metrics"
plugin_version=1
heartbeat="true"
```

| Parameter | Description |
| :--- | :--- |
| `dcgm_endpoint` | The URL of the DCGM Prometheus exporter. |
| `plugin_version` | Plugin version (currently 3). |
| `heartbeat` | Set to "true" to receive alerts for data collection gaps. |

## Performance Metrics

| Tab | Metric Category | Individual Metrics | Unit |
| :--- | :--- | :--- | :--- |
| **Performance** | Utilization | `GPU_Utilization`, `Memory_Copy_Utilization` | % |
| | Clocks | `SM_Clock`, `Memory_Clock` | MHz |
| | Engines | `Encoder_Utilization`, `Decoder_Utilization` | % |
| | Throughput | `PCIe_TX_Throughput`, `PCIe_RX_Throughput` | KB/s |
| **Advanced** | GPU details | `SM_Active`, `SM_Occupancy`, `Tensor_Active`, `FP16/32/64_Active`, `Clock_Throttle_Reasons`, `XID_Errors` | fraction, bitmask, count |
| **Resources** | Memory | `Memory_Used`, `Memory_Free`, `Memory_Total`, `Memory_Reserved` | MB |
| | VRAM | `Framebuffer_Utilization` | % |
| **Health** | Thermal | `Temperature`, `Memory_Temperature`, `Slowdown_Temperature` | C |
| | Reliability | `Correctable_Remapped_Rows`, `Uncorrectable_Remapped_Rows` | count |
| | Hardware | `Power_Usage` (W), `Fan_Speed` (%), `Energy_Consumption` (mJ) | - |
| | State | `PState` | state |

*Note: The Advanced tab contains the `GPU_Advanced_Metrics` table. Each table has at most 10 columns, including the GPU name. Systems with more than 25 GPUs will have the tabular output truncated to the first 25 devices to comply with Site24x7 limits, flagged by `Truncated_Output: "true"`.*

## Sample JSON Output
```json
{
    "Average_GPU_Utilization": 45.5,
    "Memory_Copy_Utilization": 12.2,
    "Average_Temperature": 62.0,
    "GPU_Device_Count": 1,
    "GPU_Health_Metrics": [
        {
            "Energy_Consumption": 150230,
            "Fan_Speed": 35.0,
            "Power_Usage": 125.5,
            "Temperature": 62.0,
            "name": "GPU 0"
        }
    ],
    "GPU_Advanced_Metrics": [
        {
            "Clock_Throttle_Reasons": 0,
            "FP16_Active": 0.0,
            "FP32_Active": 0.0,
            "FP64_Active": 0.0,
            "SM_Active": 0.0,
            "SM_Occupancy": 0.0,
            "Tensor_Active": 0.0,
            "XID_Errors": 0,
            "name": "GPU 0"
        }
    ],
    "Name": "NVIDIA_DCGM_Monitor",
    "heartbeat_required": "true",
    "plugin_version": 3,
    "status": 1,
    "units": {
        "Average_GPU_Utilization": "%",
        "Memory_Copy_Utilization": "%",
        "GPU_Device_Count": "count",
        "GPU_Health_Metrics": {
            "Temperature": "C"
        }
    }
}
```

## Security & Permissions
- The plugin executes with the same privileges as the Site24x7 agent user.
- No root access is required for standard exporter scraping.
- Error messages are sanitized to prevent credential leakage.
- URL validation and response size limits are enforced.
