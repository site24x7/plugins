# NVIDIA DCGM Monitoring
**Note:**

This plugin monitors NVIDIA GPU hardware metrics by scraping the DCGM Prometheus exporter.

## Quick installation

Ensure the `nvidia-dcgm-exporter` is running and reachable at `http://localhost:9400/metrics` on the target server.

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.
- NVIDIA DCGM exporter must be running and exposing metrics on port 9400.

### Plugin Installation
- Create a directory named `dcgm` in your server.

```bash
mkdir dcgm
cd dcgm/
```

- Place the following files under the `dcgm` directory:
  - `dcgm.py`
  - `dcgm.cfg`

- Execute the below command with appropriate arguments to check for the valid JSON output:

```bash
python3 dcgm.py
```

- After running the command, configure the relevant parameters in the `dcgm.cfg` file.

```ini
[global_configurations]
use_agent_python=1

[instance_1]
dcgm_endpoint=http://localhost:9400/metrics
plugin_version=1
heartbeat=true
logs_enabled=false
log_type_name=
log_file_path=
```

#### Linux

- Place the `dcgm` folder under the Site24x7 Linux Agent plugin directory:

```bash
mv dcgm /opt/site24x7/monagent/plugins
```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

- Further, move the folder `dcgm` into the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Performance Metrics

| Tab | Metric Category | Individual Metrics Provided |
| :--- | :--- | :--- |
| **Performance** | GPU Utilization | `GPU_Utilization` (%) |
| | Memory Copy Utilization | `Memory_Copy_Utilization` (%) |
| | SM Clock | `SM_Clock` (MHz) |
| | Memory Clock | `Memory_Clock` (MHz) |
| | Encoder/Decoder Utilization | `Encoder_Utilization`, `Decoder_Utilization` (%) |
| | SM Activity | `SM_Active` (fraction) |
| | SM Occupancy | `SM_Occupancy` (fraction) |
| | Tensor Core Activity | `Tensor_Active` (fraction) |
| | FP Precision Pipes | `FP16_Active`, `FP32_Active`, `FP64_Active` (fraction) |
| | PCIe Throughput | `PCIe_TX_Throughput`, `PCIe_RX_Throughput` (KB/s) |
| **Resources** | Memory Usage | `Memory_Used`, `Memory_Free`, `Memory_Total` (MB) |
| | Framebuffer Utilization | `Framebuffer_Utilization` (%) |
| | Memory Reserved | `Memory_Reserved` (MB) |
| **Health** | Temperature | `Temperature`, `Memory_Temperature` (C) |
| | Power & Fan | `Power_Usage` (W), `Fan_Speed` (%) |
| | Energy Consumption | `Energy_Consumption` (mJ) |
| | Clock Throttle Reasons | `Clock_Throttle_Reasons` (bitmask) |
| | Remapped Rows | `Correctable_Remapped_Rows`, `Uncorrectable_Remapped_Rows` (count) |
| | XID Errors | `XID_Errors` (count) |
| | Performance State | `PState` (state) |
| | Slowdown Temperature | `Slowdown_Temperature` (C) |

### Sample JSON Output

```json
{
    "plugin_version": 1,
    "heartbeat_required": true,
    "units": {
        "Average_GPU_Utilization": "%",
        "Average_Memory_Utilization": "%",
        "Average_Temperature": "C",
        "Total_Power_Draw": "W",
        "GPU_Device_Count": "count",
        "GPU_Performance_Metrics": {
            "GPU_Utilization": "%",
            ...
        },
        ...
    },
    "tabs": {
        "Performance": {
            "order": 1,
            "tablist": [
                "Average_GPU_Utilization",
                "Average_Memory_Utilization",
                "GPU_Performance_Metrics"
            ]
        },
        ...
    },
    "Name": "NVIDIA_DCGM_Monitor",
    "GPU_Device_Count": 1,
    "Average_GPU_Utilization": 10.5,
    "Average_Memory_Utilization": 5.2,
    "Average_Temperature": 45.0,
    "Total_Power_Draw": 120.5,
    "GPU_Performance_Metrics": [
        {
            "name": "GPU 0",
            "GPU_Utilization": 10.5,
            ...
        }
    ],
    ...
    "status": 1,
    "msg": "Success"
}
```

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7.

To see the dcgm monitor in the Site24x7's web client, login Site24x7 with your account, navigate to Server tab -> Plugin Integration -> list of plugin monitors -> user can check the dcgm monitor.