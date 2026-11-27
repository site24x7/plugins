# NVIDIA NIM Monitoring Plugin for Site24x7

**Custom Plugin** — Monitors NVIDIA NIM inference endpoints via Prometheus metrics.

---

## Overview
This plugin scrapes metrics from the NVIDIA NIM Prometheus exporter (`http://localhost:8000/v1/metrics`) and exposes them through the Site24x7 Custom Plugin interface. It provides four dashboard tabs: **Inference Performance**, **Token Statistics**, **Resource Usage**, and **Runtime**, covering latency, throughput, GPU cache usage, process health, and Python garbage collection stats. End-to-end latency sum, count, and bucket metrics are included in **Inference Performance**.

---

## Latency Metrics
The plugin exposes Prometheus latency `_sum` and `_count` values directly; it
does not calculate lifetime averages.

The End-to-End latency histogram is exposed as `e2e_latency_sum` and
`e2e_latency_count`. Each `_bucket{le="..."}` sample becomes a count metric
named `e2e_latency_bucket_le_<boundary>`; for example, `le="0.5"` becomes
`e2e_latency_bucket_le_0_5` and `le="+Inf"` becomes
`e2e_latency_bucket_le_inf`. Bucket values are cumulative observation counts.
TTFT and TPOT histogram inputs are exposed as `ttft_sum`/`ttft_count` and
`tpot_sum`/`tpot_count`.

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
| **Summary only** | `requests_running` | Requests currently running on GPU |
| | `requests_waiting` | Requests waiting in queue |
| **Inference Performance** | `e2e_latency_sum` | Total end-to-end latency (s) |
| | `e2e_latency_count` | Number of observed end-to-end requests |
| | `e2e_latency_bucket_le_<boundary>` | Cumulative request count up to the bucket boundary |
| **Summary only** | `request_success` | Total successful requests |
| | `request_failure` | Total failed requests |
| | `ttft_sum` / `ttft_count` | Total time to first token / observed requests |
| | `tpot_sum` / `tpot_count` | Total inter-token latency / observed tokens |
| **Token Statistics** | `generation_tokens` | Total output tokens processed |
| | `prompt_tokens` | Total input/prompt tokens processed |
| **Resource Usage** | `gpu_cache_usage_<labels>_<hash>` | Per-label GPU KV-cache usage (fraction, 1.0 = 100%) |
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

For vLLM endpoints, the plugin also maps `kv_cache_usage_perc`, `inter_token_latency_seconds_sum/count`, `request_generation_tokens_sum`, `request_prompt_tokens_sum`, and `num_requests_success/failure` to the corresponding dashboard metrics.

GPU cache samples are kept separate by their Prometheus labels rather than collapsed into one value. Each label set produces a scalar metric named `gpu_cache_usage_<labels>_<hash>` (or `gpu_cache_usage_unlabeled` when no labels are present), which is added to the Resource Usage tab. Select those per-label metrics in a Site24x7 table visualization to compare models. The plugin emits scalar metrics, not a separate row-based table payload.

---

## Sample Output (JSON)
The following abbreviated example illustrates the output shape. Summary metrics
such as `requests_running` are included at the top level, but are not listed in
a dashboard tab unless explicitly configured there. Bucket and per-label cache
metrics, their units, and their tab entries are added dynamically when present
in the scrape.

```json
{
  "plugin_version": 1,
  "heartbeat_required": true,
  "Name": "NVIDIA_NIM_Monitor",
  "status": 1,
  "msg": "Success",
  "units": {
    "e2e_latency_sum": "s",
    "e2e_latency_count": "count",
    "generation_tokens": "count",
    "gpu_cache_usage_model_a_6f77be4c": "fraction",
    "gpu_cache_usage_model_b_8c15c3b2": "fraction",
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
    "python_info": "",
    "e2e_latency_bucket_le_0_5": "count"
  },
  "tabs": {
    "Inference_Performance": {
      "order": 1,
      "tablist": [
        "e2e_latency_sum",
        "e2e_latency_count",
        "e2e_latency_bucket_le_0_5"
      ]
    },
    "Token_Statistics": {
      "order": 2,
      "tablist": ["generation_tokens", "prompt_tokens"]
    },
    "Resource_Usage": {
      "order": 3,
      "tablist": [
        "resident_memory",
        "cpu_seconds",
        "gpu_cache_usage_model_a_6f77be4c",
        "gpu_cache_usage_model_b_8c15c3b2"
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
  },
  "requests_running": 3.0,
  "requests_waiting": 0.0,
  "gpu_cache_usage_model_a_6f77be4c": 0.4,
  "gpu_cache_usage_model_b_8c15c3b2": 0.8,
  "e2e_latency_sum": 187.432,
  "e2e_latency_count": 150.0,
  "e2e_latency_bucket_le_0_5": 12.0
}
```

Exponent signs are encoded using letters to keep metric names symbol-free and
distinct: `1e-20` becomes `e2e_latency_bucket_le_1e_m20`, while `1e+20` becomes
`e2e_latency_bucket_le_1e_p20`. Decimal boundaries such as `0.5` continue to
become `e2e_latency_bucket_le_0_5`.

### Parser failure test cases
Run the focused tests with:

```bash
python3 -m unittest discover -s . -p "test_*.py" -v
```

The suite includes expected-failure cases: a bucket without its required `le`
label, a bucket with a non-finite value, a NaN boundary, and a malformed scrape
that should make the plugin return `status: 0`. It also checks that exponent
signs produce distinct names and that normal decimal and `+Inf` boundaries
remain supported.

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