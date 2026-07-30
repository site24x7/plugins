import argparse
import configparser
import json
import os
import re
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.request

# Global Constants & Defaults
PLUGIN_VERSION = 10  # Bumped version to force Site24x7 template refresh
HEARTBEAT = "true"
REQUEST_TIMEOUT = 5

LINE_RE = re.compile(
    r'^([a-zA-Z_:][a-zA-Z0-9_:]*)(\{[^}]*\})?\s+(-?[0-9.eE+\-]+|NaN|\+Inf|-Inf)\s*$'
)
LABEL_RE = re.compile(r'(\w+)="((?:[^"\\]|\\.)*)"')

UNITS = {
    "Response Time": "ms",
    "CPU Percent": "%",
    "Resident Memory": "MB",
    "Virtual Memory": "MB",
    "Heap Usage": "MB",
    "Heap Idle": "MB",
    "Heap System": "MB",
    "Memory Mapped Usage": "MB",
    "Next GC Threshold": "MB",
    "Entity Memory Usage": "MB",
    "System Threads": "count",
    "Active Goroutines": "count",
    "Total Metrics Count": "count",
    "Search Latency": "ms",
    "Query Latency": "ms",
    "Query Queue Latency": "ms",
    "Query Reduce Latency": "ms",
    "Core Search Latency": "ms",
    "Search Queue Latency": "ms",
    "Wait Result Latency": "ms",
    "Decode Result Latency": "ms",
    "Segment Load Latency": "ms",
    "Dispatcher Time Lag": "ms",
    "Index Build Latency": "ms",
    "Index Save Latency": "ms",
    "Index Queue Latency": "ms",
    "Index Load Latency": "ms",
    "Mutation Latency": "ms",
    "Encode Buffer Latency": "ms",
    "Data Save Latency": "ms",
    "Storage Request Latency": "ms",
    "GC Duration Average": "ms",
    "Message Stream Latency": "ms",
    "Proxy Time Lag": "ms",
    "Proxy Request Latency": "ms",
    "Primary Key Latency": "ms",
    "Timestamp Latency": "ms",
    "Cache Update Latency": "ms",
    "DDL Request Latency": "ms",
    "Sync Timetick Latency": "ms",
    "Consumer Time Lag": "ms",
    "Flushed Data Size": "MB",
    "Binlog Size": "MB",
    "Index Size": "MB",
    "Key Value Storage Size": "MB",
    "Proxy Sent Data": "MB",
    "Insert Data Size": "MB",
    "Query Nodes": "nodes",
    "Data Nodes": "nodes",
    "Index Nodes": "nodes",
    "Proxy Nodes": "nodes",
    "Collections Loaded": "count",
    "Total Collections": "count",
    "Total Partitions": "count",
    "Segments": "count",
    "Loaded Segments": "count",
    "Vectors": "count",
    "Search Vectors": "count",
    "Search Requests": "reqs",
    "Query Requests": "reqs",
    "Insert Requests": "reqs",
    "Search Top K Avg": "count",
    "Active Index Tasks": "tasks",
    "Deleted Vectors": "count",
    "Flush Requests": "reqs",
    "Flushed Rows": "rows",
    "Consumed Messages": "msgs",
    "Consumed Bytes": "bytes",
    "Storage Operations": "ops",
    "Write Denials": "count",
    "Open File Descriptors": "fds",
    "Max File Descriptors": "fds",
}

TABS = {
    "CPU & Memory": {
        "order": 1,
        "tablist": [
            "CPU Percent",
            "Heap Usage",
            "Heap Idle",
            "Heap System",
            "Resident Memory",
            "Virtual Memory",
            "System Threads",
            "Active Goroutines",
        ],
    },
    "Query Performance": {
        "order": 2,
        "tablist": [
            "Query Latency",
            "Query Requests",
            "Query Queue Latency",
            "Query Reduce Latency",
            "Search Latency",
            "Search Requests",
            "Search Vectors",
            "Search Top K Avg",
        ],
    },
    "Index Performance": {
        "order": 3,
        "tablist": [
            "Index Build Latency",
            "Index Load Latency",
            "Index Save Latency",
            "Index Size",
            "Active Index Tasks",
            "Index Queue Latency",
        ],
    },
    "Data Ingestion": {
        "order": 4,
        "tablist": [
            "Insert Requests",
            "Insert Data Size",
            "Deleted Vectors",
            "Flush Requests",
            "Flushed Rows",
            "Consumed Messages",
            "Consumed Bytes",
        ],
    },
    "Cluster Health": {
        "order": 5,
        "tablist": [
            "Query Nodes",
            "Data Nodes",
            "Index Nodes",
            "Proxy Nodes",
            "Collections Loaded",
            "Segments",
            "Vectors",
        ],
    },
    "Storage": {
        "order": 6,
        "tablist": [
            "Binlog Size",
            "Key Value Storage Size",
            "Storage Operations",
            "Storage Request Latency",
            "Memory Mapped Usage",
        ],
    },
}

METRIC_SPECS = [
    {"key": "Data Nodes", "source": "milvus_datacoord_datanode_num", "kind": "gauge"},
    {"key": "Index Nodes", "source": "milvus_datacoord_index_node_num", "kind": "gauge"},
    {"key": "Proxy Nodes", "source": "milvus_rootcoord_proxy_num", "kind": "gauge"},
    {"key": "Total Collections", "source": "milvus_rootcoord_collection_num", "kind": "gauge"},
    {"key": "Total Partitions", "source": "milvus_rootcoord_partition_num", "kind": "gauge"},
    {"key": "Open File Descriptors", "source": "process_open_fds", "kind": "gauge"},
    {"key": "Max File Descriptors", "source": "process_max_fds", "kind": "gauge"},
    {"key": "Query Queue Latency", "source": "milvus_proxy_req_in_queue_latency", "kind": "hist_ms"},
    {"key": "Query Reduce Latency", "source": "milvus_querynode_sq_reduce_latency", "kind": "hist_ms"},
    {"key": "Core Search Latency", "source": "milvus_internal_core_search_latency", "kind": "hist_us_ms"},
    {"key": "Search Queue Latency", "source": "milvus_querynode_sq_queue_latency", "kind": "hist_ms"},
    {"key": "Search Top K Avg", "source": "milvus_search_topk", "kind": "hist_raw"},
    {"key": "Wait Result Latency", "source": "milvus_proxy_sq_wait_result_latency", "kind": "hist_ms"},
    {"key": "Decode Result Latency", "source": "milvus_proxy_sq_decode_result_latency", "kind": "hist_ms"},
    {"key": "Entity Memory Usage", "source": "milvus_querynode_entity_size", "kind": "gauge_mb"},
    {"key": "Segment Load Latency", "source": "milvus_querynode_load_segment_latency", "kind": "hist_ms"},
    {"key": "Dispatcher Time Lag", "source": "milvus_querynode_msg_dispatcher_tt_lag_ms", "kind": "gauge"},
    {"key": "Index Build Latency", "source": "milvus_indexnode_build_index_latency", "kind": "hist_ms"},
    {"key": "Index Save Latency", "source": "milvus_indexnode_save_index_latency", "kind": "hist_ms"},
    {"key": "Active Index Tasks", "source": "milvus_indexnode_index_task_count", "kind": "gauge"},
    {"key": "Index Queue Latency", "source": "milvus_indexnode_index_task_latency_in_queue", "kind": "hist_ms"},
    {"key": "Index Load Latency", "source": "milvus_load_latency", "kind": "hist_ms"},
    {"key": "Insert Requests", "source": "milvus_proxy_req_count", "kind": "gauge", "labels": {"rpc_type": "Insert"}},
    {"key": "Deleted Vectors", "source": "milvus_proxy_delete_vectors_count", "kind": "gauge"},
    {"key": "Flush Requests", "source": "milvus_datanode_flush_req_count", "kind": "gauge"},
    {"key": "Flushed Rows", "source": "milvus_datanode_flushed_data_rows_count", "kind": "gauge"},
    {"key": "Flushed Data Size", "source": "milvus_datanode_flushed_data_size_count", "kind": "gauge_mb"},
    {"key": "Mutation Latency", "source": "milvus_proxy_mutation_send_latency", "kind": "hist_ms"},
    {"key": "Consumed Bytes", "source": "milvus_datanode_consume_bytes_count", "kind": "gauge"},
    {"key": "Consumed Messages", "source": "milvus_datanode_consume_msg_count", "kind": "gauge"},
    {"key": "Encode Buffer Latency", "source": "milvus_datanode_encode_buffer_latency", "kind": "hist_ms"},
    {"key": "Data Save Latency", "source": "milvus_datanode_save_latency", "kind": "hist_ms"},
    {"key": "Binlog Size", "source": "milvus_datacoord_stored_binlog_size", "kind": "gauge_mb"},
    {"key": "Index Size", "source": "milvus_datacoord_stored_index_files_size", "kind": "gauge_mb"},
    {"key": "Key Value Storage Size", "source": "milvus_storage_kv_size", "kind": "gauge_mb"},
    {"key": "Storage Operations", "source": "milvus_storage_op_count", "kind": "gauge"},
    {"key": "Storage Request Latency", "source": "milvus_storage_request_latency", "kind": "gauge"},
    {"key": "Heap Idle", "source": "go_memstats_heap_idle_bytes", "kind": "gauge_mb"},
    {"key": "Heap System", "source": "go_memstats_heap_sys_bytes", "kind": "gauge_mb"},
    {"key": "Resident Memory", "source": "process_resident_memory_bytes", "kind": "gauge_mb"},
    {"key": "Virtual Memory", "source": "process_virtual_memory_bytes", "kind": "gauge_mb"},
    {"key": "Memory Mapped Usage", "source": "milvus_internal_mmap_in_used_space_bytes", "kind": "gauge_mb"},
    {"key": "Next GC Threshold", "source": "go_memstats_next_gc_bytes", "kind": "gauge_mb"},
    {"key": "GC Duration Average", "source": "go_gc_duration_seconds", "kind": "hist_sec_ms"},
]

def get_error_payload(error_message):
    return {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "status": 0,
        "msg": error_message,
        "units": UNITS,
        "tabs": TABS,
    }

def timed_get(url, ssl_verify=True):
    try:
        start = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Site24x7-Plugin'})
        ctx = ssl.create_default_context()
        if not ssl_verify:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ctx) as response:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            content = response.read().decode('utf-8', errors='replace')
            return response.status == 200, elapsed_ms, content
    except Exception:
        return False, 0, None

def parse_metrics(text):
    series = {}
    if not text:
        return series

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = LINE_RE.match(line)
        if not match:
            continue

        name, labels_text, value_text = match.groups()
        try:
            value = float(value_text)
            if value != value:  # Check for NaN
                continue
        except Exception:
            continue

        labels = {}
        if labels_text:
            for k, v in LABEL_RE.findall(labels_text):
                labels[k] = v

        series.setdefault(name, []).append({"labels": labels, "value": value})

    return series

def get_sum(series, metric, labels=None):
    total = 0.0
    for item in series.get(metric, []):
        if labels:
            if not all(item["labels"].get(k) == v for k, v in labels.items()):
                continue
        total += item["value"]
    return total

def histogram_average(series, metric):
    total = get_sum(series, metric + "_sum")
    count = get_sum(series, metric + "_count")
    if count > 0:
        return round((total / count) * 0.001, 2)
    return 0

def histogram_stat(series, metric_base, labels=None, scale=1.0, ndigits=2):
    total = get_sum(series, metric_base + "_sum", labels)
    count = get_sum(series, metric_base + "_count", labels)
    if count > 0:
        return round((total / count) * scale, ndigits)
    return 0

def bytes_to_mb(value):
    if not value:
        return 0
    return round(value / (1024 * 1024), 2)

def compute_new_metrics(series):
    new_values = {}
    for spec in METRIC_SPECS:
        key = spec["key"]
        source = spec["source"]
        kind = spec["kind"]
        labels = spec.get("labels")

        try:
            if kind == "gauge":
                value = round(get_sum(series, source, labels))
            elif kind == "gauge_mb":
                value = bytes_to_mb(get_sum(series, source, labels))
            elif kind == "hist_ms":
                value = histogram_stat(series, source, labels, scale=1.0)
            elif kind == "hist_us_ms":
                value = histogram_stat(series, source, labels, scale=0.001)
            elif kind == "hist_sec_ms":
                value = histogram_stat(series, source, labels, scale=1000.0)
            elif kind == "hist_raw":
                value = histogram_stat(series, source, labels, scale=1.0)
            else:
                value = 0
        except Exception:
            value = 0

        new_values[key] = value
    return new_values

CPU_STATE_FILE = os.path.join(tempfile.gettempdir(), "milvus_cpu_state.json")

def get_cpu_utilization_percent(current_cpu_seconds, cores=1):
    now = time.time()
    previous_time, previous_cpu = None, None

    try:
        with open(CPU_STATE_FILE, "r") as f:
            state = json.load(f)
            previous_time = state.get("timestamp")
            previous_cpu = state.get("cpu_seconds")
    except Exception:
        pass

    try:
        with open(CPU_STATE_FILE, "w") as f:
            json.dump({"timestamp": now, "cpu_seconds": current_cpu_seconds}, f)
    except Exception:
        pass

    if previous_time is None or previous_cpu is None:
        return 0

    delta_time = now - previous_time
    delta_cpu = current_cpu_seconds - previous_cpu

    if delta_cpu < 0 or delta_time <= 0:
        return 0

    cores = cores if cores and cores > 0 else 1
    return round(((delta_cpu / delta_time) * 100) / cores, 2)

def metricCollector(param):
    host = param.get("host", "localhost")
    port = param.get("port", "9091")
    ssl_enabled = str(param.get("ssl", "false")).lower() == "true"
    ssl_verify_val = str(param.get("ssl_verify", "true")).lower() == "true"

    protocol = "https" if ssl_enabled else "http"
    metrics_url = f"{protocol}://{host}:{port}/metrics"

    status_ok, response_time_ms, raw_text = timed_get(metrics_url, ssl_verify=ssl_verify_val)

    if not status_ok or not raw_text:
        return get_error_payload(f"Failed to reach Milvus Prometheus Endpoint at {metrics_url}")

    series = parse_metrics(raw_text)

    cpu_seconds = get_sum(series, "process_cpu_seconds_total")
    cpu_percent = get_cpu_utilization_percent(cpu_seconds, cores=os.cpu_count() or 1)
    threads = get_sum(series, "go_threads") or get_sum(series, "milvus_thread_num")

    payload = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "status": 1,
        "Response Time": response_time_ms,
        "Total Metrics Count": sum(len(v) for v in series.values()),
        "Query Nodes": round(get_sum(series, "milvus_querycoord_querynode_num")),
        "Collections Loaded": round(get_sum(series, "milvus_querynode_collection_num")),
        "Search Vectors": round(get_sum(series, "milvus_proxy_search_vectors_count")),
        "Search Requests": round(
            get_sum(series, "milvus_proxy_collection_sq_latency_count", {"query_type": "search"})
        ),
        "Search Latency": histogram_average(series, "milvus_proxy_collection_sq_latency"),
        "Vectors": round(get_sum(series, "milvus_datacoord_stored_rows_num")),
        "Segments": round(get_sum(series, "milvus_querynode_segment_num")),
        "Insert Data Size": round(get_sum(series, "milvus_proxy_receive_bytes_count") / (1024 * 1024), 2),
        "Query Latency": histogram_average(series, "milvus_proxy_collection_sq_latency"),
        "Query Requests": round(
            get_sum(series, "milvus_proxy_collection_sq_latency_count", {"query_type": "query"})
        ),
        "Loaded Segments": round(
            get_sum(series, "milvus_querynode_segment_num", {"segment_state": "Sealed"})
        ),
        "CPU Percent": cpu_percent,
        "System Threads": round(threads),
        "Active Goroutines": round(get_sum(series, "go_goroutines")),
        "Heap Usage": round(get_sum(series, "go_memstats_heap_inuse_bytes") / (1024 * 1024), 2),
        "Write Denials": round(get_sum(series, "milvus_rootcoord_force_deny_writing_counter")),
        "Consumer Time Lag": round(get_sum(series, "milvus_datanode_consume_tt_lag_ms")),
        "units": UNITS,
        "tabs": TABS,
    }

    payload.update(compute_new_metrics(series))
    return payload

def load_cfg_parameters(cfg_path=None):
    """
    Reads parameters from a .cfg file if found.
    Checks the explicitly passed file path, or falls back to looking for a file
    with the same base name as this script in the same directory.
    """
    config_params = {}
    
    if not cfg_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        cfg_path = os.path.join(script_dir, f"{script_name}.cfg")

    if os.path.exists(cfg_path):
        config = configparser.ConfigParser()
        try:
            config.read(cfg_path)
            # Scan all common Site24x7 sections for configurations
            for section in ["global_configurations", "display", "plugin"]:
                if config.has_section(section):
                    for key, value in config.items(section):
                        # Clean key names to avoid encrypted prefixes or unwanted spaces
                        clean_key = key.split(".")[-1]
                        config_params[clean_key] = value
        except Exception:
            pass  # Fallback gracefully to default parameters if read fails

    return config_params

def run(param):
    try:
        return metricCollector(param)
    except Exception as e:
        return get_error_payload(f"Plugin Execution Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Host Name", nargs="?", default=None)
    parser.add_argument("--port", help="Metrics Port", nargs="?", default=None)
    parser.add_argument("--ssl", help="Use SSL/HTTPS", default=None)
    parser.add_argument("--ssl_verify", help="SSL Verification", default=None)
    parser.add_argument("--name", help="Plugin Name", nargs="?", default=None)
    parser.add_argument("--cfg_file", help="Custom path to .cfg file", default=None)

    args, _ = parser.parse_known_args()
    
    # 1. Read configurations from the .cfg file first
    final_params = load_cfg_parameters(args.cfg_file)
    
    # 2. Merge values explicitly passed as CLI arguments (CLI takes priority)
    cli_args = {k: v for k, v in vars(args).items() if v is not None and k != "cfg_file"}
    final_params.update(cli_args)
    
    # 3. Apply absolute defaults for any remaining missing key parameters
    final_params.setdefault("host", "localhost")
    final_params.setdefault("port", "9091")
    final_params.setdefault("ssl", "false")
    final_params.setdefault("ssl_verify", "true")
    final_params.setdefault("name", "milvus_monitor_v2")

    result = run(final_params)
    print(json.dumps(result))