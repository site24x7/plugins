# NVIDIA NIM Monitoring Plugin for Site24x7

**Custom Plugin** — Monitors NVIDIA NIM inference endpoints via Prometheus metrics.

---

## Overview
This plugin scrapes metrics from the NVIDIA NIM Prometheus exporter (`http://localhost:8000/v1/metrics`) and exposes them through the Site24x7 Custom Plugin interface. It provides four dashboard tabs: **Inference Performance**, **Token Statistics**, **Resource Usage**, and **Runtime**, covering latency, throughput, GPU cache usage, process health, and Python garbage collection stats.

---

## Overview of Calculated Metrics
The plugin calculates average latency metrics by dividing the Prometheus `_sum` by `_count`.

*   **`e2e_latency_avg`**: Average End-to-End latency (seconds).
*   **`time_to_first_token_avg`**: Average Time-To-First-Token (TTFT) (seconds).
*   **`time_per_output_token_avg`**: Average Time-Per-Output-Token (TPOT) (seconds).

---

## Installation

### Prerequisites
*   Site24x7 Linux Agent installed on the target server.
*   Python 3.x available to the Site24x7 agent process.
*   NVIDIA NIM instance running with the Prometheus metrics endpoint enabled on port **8000**.

### Quick Setup
1.  Ensure the NIM Prometheus exporter is accessible: `curl http://localhost:8000/v1/metrics`
2.  Copy the plugin files to the Site24x7 Agent plugin directory:
    ```bash
    mkdir -p /opt/site24x7/monagent/plugins/nvidia-nim
    cp nvidia-nim.py nvidia-nim.cfg README.md /opt/site24x7/monagent/plugins/nvidia-nim/
    ```
3.  Verify the plugin runs correctly:
    ```bash
    python3 /opt/site24x7/monagent/plugins/nvidia-nim/nvidia-nim.py
    ```
    Expected: Valid JSON output with `status: 1` and metric values.
4.  Restart or wait for the Site24x7 agent to auto-detect and execute the plugin (interval: ~5 min).

### Configuration
Edit `nvidia-nim.cfg` if your NIM endpoint differs from the default:
```ini
[global_configurations]
use_agent_python=1

[instance_1]
nim_endpoint=http://localhost:8000/v1/metrics
```
*   `nim_endpoint`: Full URL to the NIM Prometheus metrics endpoint.

---

## Metrics Summary
The plugin maps the following Prometheus metric families to Site24x7 dashboard categories:

| **Category** | **Metric** | **Description** |
|---|---|---|
| **Inference Performance** | `requests_running` | Requests currently running on GPU |
| | `requests_waiting` | Requests waiting in queue |
| | `e2e_latency_avg` | **Calculated** average end-to-end latency (s) |
| | `time_to_first_token_avg` | **Calculated** average TTFT (s) |
| | `time_per_output_token_avg` | **Calculated** average TPOT (s) |
| **Token Statistics** | `generation_tokens` | Total output tokens processed |
| | `prompt_tokens` | Total input/prompt tokens processed |
| **Resource Usage** | `gpu_cache_usage` | GPU KV-cache usage (fraction, 1.0 = 100%) |
| | `resident_memory` | Process resident memory (bytes) |
| | `cpu_seconds` | Total CPU time consumed (s) |
| **Runtime** | `num_request_max` | Maximum concurrent requests observed |
| | `request_finish_count` | Total finished requests |
| | `process_max_fds` | Max open file descriptors |
| | `process_open_fds` | Current open file descriptors |
| | `process_start_time_seconds` | Process start epoch time |
| | `process_virtual_memory_bytes` | Process virtual memory size (bytes) |
| | `python_gc_collections_count` | Number of GC events |
| | `python_gc_objects_collected_count` | Objects collected by GC |
| | `python_gc_objects_uncollectable_count` | Uncollectable objects found |
| | `python_info` | Python platform information (from Prometheus labels) |

*The plugin calculates derived averages (latency/TPOT) internally by dividing the `_sum` by `_count` from the Prometheus output.*

---

## Sample Output (JSON)
Running the plugin manually typically produces output similar to this:

```json
{
  "plugin_version": 1,
  "heartbeat_required": true,
  "name": "NVIDIA_NIM_Monitor",
  "status": 1,
  "msg": "Success",
  "units": {
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
    "e2e_latency_avg": "s",
    "time_to_first_token_avg": "s",
    "time_per_output_token_avg": "s"
  },
  "tabs": {
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
    ...
  }
}
```

---

## How to configure a non-default endpoint
If your NIM instance is not on the default port 8000, update the `nvidia-nim.cfg` file:

```ini
[global_configurations]
use_agent_python=1

[instance_1]
nim_endpoint=http://YOUR_NIM_HOST:YOUR_PORT/v1/metrics
```
*   Change the `nim_endpoint` value to point to your specific NIM deployment.

---

## python_info clarification
The `python_info` metric is a standard Prometheus metadata metric. The numeric sample value is typically `1`, but the useful information (Python version, implementation) resides in the **labels** (e.g., `python_info{implementation="CPython", version="3.10.0"}`). This plugin attempts to extract and display that label information in the `python_info` field.

---

## Verification
After the agent picks up the plugin, navigate in Site24x7 to:
**Server tab → Plugin Integration → List of plugin monitors → NVIDIA NIM Monitor**

You should see four tabs populated with live metric values. If the plugin reports `status: 0`, ensure:
*   The NIM endpoint is reachable from the agent server.
*   The `nvidia-nim.cfg` `nim_endpoint` is correct.
*   Python 3 is the interpreter used by the Site24x7 agent.

---

## References
*   NVIDIA NIM Documentation: [docs.nvidia.com/nim](https://docs.nvidia.com/nim)
*   Prometheus NIM Exporter: Standard `/metrics` endpoint on NIM container/pod.
*   Site24x7 Custom Plugin Docs: [site24x7.com](https://www.site24x7.com)