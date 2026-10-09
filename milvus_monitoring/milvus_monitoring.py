import json
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PLUGIN_VERSION = 1
HEARTBEAT      = "true"

MILVUS_METRICS_URI = "/metrics"
MILVUS_HEALTH_URI  = "/healthz"

METRICS_UNITS = {
    "CPU Seconds"          : "s",
    "Memory Usage"         : "MB",
    "Virtual Memory"       : "MB",
    "Heap Usage"           : "MB",
    "Heap Idle"            : "MB",
    "Heap Sys"             : "MB",
    "Next GC Threshold"    : "MB",
    "GC Pause Duration"    : "ms",
    "GC Cycle Count"       : "cycles",
    "Goroutines"           : "goroutines",
    "OS Threads"           : "threads",
    "Open File Descriptors": "fds",
    "Max File Descriptors" : "fds",

    "Total Nodes"            : "nodes",
    "Thread Count"           : "threads",
    "Proxy Components"       : "components",
    "Query Components"       : "components",
    "Data Components"        : "components",
    "Coordinator Components" : "components",
    "Collection Count"       : "collections",
    "Partition Count"        : "partitions",
    "DML Channels"           : "channels",
    "Message Streams"        : "streams",

    "Data Segments"          : "segments",
    "Growing Segments"       : "segments",
    "Sealed Segments"        : "segments",
    "Flushed Segments"       : "segments",
    "Stored Rows"            : "entities",
    "Loaded Entities"        : "entities",
    "Storage KV Size"        : "MB",

    "Search Requests"        : "requests",
    "Search Latency"         : "ms",
    "Query Requests"         : "requests",
    "Query Latency"          : "ms",
    "Execution Latency"      : "ms",

    "Network Received"       : "MB",
    "Network Transmitted"    : "MB",
    "Storage Read Bytes"     : "MB",
    "Storage Write Bytes"    : "MB",
    "Storage Read Ops"       : "ops",
    "Storage Write Ops"      : "ops",
    "Storage Failed Ops"     : "ops",

    "Meta Store Operations"       : "ops",
    "Meta Store Latency"          : "ms",
    "Data Nodes (Managed)"        : "nodes",
    "Index Nodes (Managed)"       : "nodes",
    "Query Nodes (Managed)"       : "nodes",
    "Proxy Nodes (Managed)"       : "nodes",
    "QueryCoord Pending Tasks"    : "tasks",
    "Index/Stats Tasks In Progress": "tasks",
    "DDL Requests"                : "requests",
    "Segment GC Runs"             : "runs",
    "QueryNode Disk Used"         : "MB",
    "Process Uptime"              : "s",
}

TABS = {
    "Cluster Overview": {
        "order": 2,
        "tablist": [
            "Total Nodes",
            "Thread Count",
            "Proxy Components",
            "Query Components",
            "Data Components",
            "Coordinator Components",
            "Collection Count",
            "Partition Count",
            "DML Channels",
            "Message Streams",
        ]
    },
    "Storage": {
        "order": 3,
        "tablist": [
            "Data Segments",
            "Growing Segments",
            "Sealed Segments",
            "Flushed Segments",
            "Stored Rows",
            "Loaded Entities",
            "Storage KV Size",
            "QueryNode Disk Used",
        ]
    },
    "Query & Search": {
        "order": 4,
        "tablist": [
            "Search Requests",
            "Search Latency",
            "Query Requests",
            "Query Latency",
            "Execution Latency",
        ]
    },
    "Process & Memory": {
        "order": 5,
        "tablist": [
            "Memory Usage",
            "Virtual Memory",
            "Heap Usage",
            "Heap Idle",
            "Heap Sys",
            "Next GC Threshold",
            "CPU Seconds",
            "Open File Descriptors",
            "Max File Descriptors",
            "Process Uptime",
        ]
    },
    "Components": {
        "order": 1,
        "tablist": [
            "Component Details",
        ]
    }
}


def clean_quotes(value):
    if not value:
        return value
    value_str = str(value).strip()
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str


def bytes_to_mb(value):
    try:
        return round(float(value) / (1024 * 1024), 2)
    except Exception:
        return 0


def getHealth(data):
    """Confirm Milvus metrics endpoint is reachable."""
    try:
        url      = f"{MILVUS_SERVER}{MILVUS_METRICS_URI}"
        response = requests.get(url, verify=MILVUS_SSL_VERIFY, timeout=10)
        if response.status_code != 200:
            data["status"] = 0
            data["msg"]    = f"Milvus is not reachable (HTTP {response.status_code})"
            return None
        return response.text
    except Exception as e:
        data["status"] = 0
        data["msg"]    = f"Connection Error: {str(e)}"
        return None


def parsePrometheus(raw_text):
    """Parse Prometheus text exposition format.

    Returns a dict:
        gauges[name]        -> summed value across all label sets
        sums[name_base]     -> summed _sum value for histograms/summaries
        counts[name_base]   -> summed _count value for histograms/summaries
    """
    gauges = {}
    sums   = {}
    counts = {}

    if not raw_text:
        return gauges, sums, counts

    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.rsplit(" ", 1)
        if len(parts) != 2:
            continue

        name_with_labels, value_str = parts
        name = name_with_labels.split("{")[0]

        if name.endswith("_bucket"):
            continue

        try:
            value = float(value_str)
        except ValueError:
            continue
        if value != value:  # NaN guard
            continue

        if name.endswith("_sum"):
            sums[name[:-4]] = sums.get(name[:-4], 0.0) + value
        elif name.endswith("_count"):
            counts[name[:-6]] = counts.get(name[:-6], 0.0) + value
        else:
            gauges[name] = gauges.get(name, 0.0) + value

    return gauges, sums, counts


def avg_latency(sums, counts, base):
    """Average latency (ms) from a Prometheus summary/histogram base name."""
    cnt = counts.get(base, 0.0)
    if cnt <= 0:
        return 0.0
    return round(sums.get(base, 0.0) / cnt, 2)


def getProcessMetrics(data, gauges, sums, counts):
    """Process, memory and Go runtime metrics."""
    data["CPU Seconds"]           = round(gauges.get("process_cpu_seconds_total", 0), 4)
    data["Memory Usage"]          = bytes_to_mb(gauges.get("process_resident_memory_bytes", 0))
    data["Virtual Memory"]        = bytes_to_mb(gauges.get("process_virtual_memory_bytes", 0))
    data["Heap Usage"]            = bytes_to_mb(gauges.get("go_memstats_heap_inuse_bytes", 0))
    data["Heap Idle"]             = bytes_to_mb(gauges.get("go_memstats_heap_idle_bytes", 0))
    data["Heap Sys"]              = bytes_to_mb(gauges.get("go_memstats_heap_sys_bytes", 0))
    data["Next GC Threshold"]     = bytes_to_mb(gauges.get("go_memstats_next_gc_bytes", 0))
    data["Open File Descriptors"] = int(gauges.get("process_open_fds", 0))
    data["Max File Descriptors"]  = int(gauges.get("process_max_fds", 0))
    data["Goroutines"]            = int(gauges.get("go_goroutines", 0))
    data["OS Threads"]            = int(gauges.get("go_threads", 0))
    data["GC Cycle Count"]        = int(counts.get("go_gc_duration_seconds", 0))
    data["GC Pause Duration"]     = round(sums.get("go_gc_duration_seconds", 0) * 1000, 4)

    start_time = gauges.get("process_start_time_seconds", 0)
    data["Process Uptime"] = int(time.time() - start_time) if start_time else 0


def parseBuildVersion(raw_text):
    """Extract Milvus version from the labeled milvus_build_info metric."""
    for line in raw_text.splitlines():
        line = line.strip()
        if line.startswith("milvus_build_info{"):
            start = line.find('version="')
            if start != -1:
                start += len('version="')
                end = line.find('"', start)
                if end != -1:
                    return line[start:end]
    return "-"


def parseComponentNodes(raw_text):
    """Parse milvus_num_node{node_id, role_name} into per-role and node-id sets.

    Returns:
        role_counts : {role_name: instance_count}
        node_ids    : set of distinct node_id values (true physical node count)
    """
    role_counts = {}
    node_ids    = set()

    for line in raw_text.splitlines():
        line = line.strip()
        if not line.startswith("milvus_num_node{"):
            continue

        parts = line.rsplit(" ", 1)
        if len(parts) != 2:
            continue
        try:
            value = float(parts[1])
        except ValueError:
            continue

        label_block = parts[0]
        role = _extract_label(label_block, "role_name")
        nid  = _extract_label(label_block, "node_id")

        if role:
            role_counts[role] = role_counts.get(role, 0) + int(value)
        if nid:
            node_ids.add(nid)

    return role_counts, node_ids


def _extract_label(label_block, key):
    marker = f'{key}="'
    start = label_block.find(marker)
    if start == -1:
        return None
    start += len(marker)
    end = label_block.find('"', start)
    if end == -1:
        return None
    return label_block[start:end]


def filtered_sum(raw_text, base_name, label_key, label_value):
    """Sum a plain counter/gauge, or a histogram's _sum/_count, keeping only samples
    where label_key==label_value (avoids double-counting sibling label breakdowns).

    Returns (value_total, sum_total, count_total).
    """
    value_total = 0.0
    sum_total   = 0.0
    count_total = 0.0

    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.rsplit(" ", 1)
        if len(parts) != 2:
            continue

        name_with_labels, value_str = parts
        name = name_with_labels.split("{")[0]

        if name == f"{base_name}_sum":
            kind = "sum"
        elif name == f"{base_name}_count":
            kind = "count"
        elif name == base_name:
            kind = "value"
        else:
            continue

        if _extract_label(name_with_labels, label_key) != label_value:
            continue

        try:
            value = float(value_str)
        except ValueError:
            continue

        if kind == "sum":
            sum_total += value
        elif kind == "count":
            count_total += value
        else:
            value_total += value

    return value_total, sum_total, count_total


def getClusterMetrics(data, gauges, role_counts, node_ids):
    """True node count, per-component counts and cluster-level metrics."""
    # True physical node count = distinct node_id (standalone shares node_id=1)
    data["Total Nodes"]            = len(node_ids) if node_ids else 0
    data["Thread Count"]           = int(gauges.get("milvus_thread_num", 0))

    data["Proxy Components"]       = int(role_counts.get("proxy", 0))
    data["Query Components"]       = int(role_counts.get("querynode", 0))
    data["Data Components"]        = int(role_counts.get("datanode", 0))
    # v3.x merges rootcoord/datacoord/querycoord/indexcoord into "mixcoord"
    data["Coordinator Components"] = int(
        role_counts.get("mixcoord", 0)
        + role_counts.get("rootcoord", 0)
        + role_counts.get("datacoord", 0)
        + role_counts.get("querycoord", 0)
        + role_counts.get("indexcoord", 0)
    )

    data["Collection Count"]       = int(gauges.get("milvus_datacoord_collection_num", 0))
    data["Partition Count"]        = int(gauges.get("milvus_rootcoord_partition_num", 0))
    data["DML Channels"]           = int(gauges.get("milvus_rootcoord_dml_channel_num", 0))
    data["Message Streams"]        = int(gauges.get("milvus_rootcoord_msgstream_obj_num", 0))


def getStorageMetrics(data, gauges):
    """Segment, entity and storage size metrics."""
    data["Data Segments"]    = int(gauges.get("milvus_datacoord_segment_num", 0))
    data["Growing Segments"] = int(gauges.get("milvus_datacoord_growing_segment_num", 0))
    data["Sealed Segments"]  = int(gauges.get("milvus_datacoord_sealed_segment_num", 0))
    data["Flushed Segments"] = int(gauges.get("milvus_datacoord_flushed_segment_num", 0))
    data["Stored Rows"]      = int(gauges.get("milvus_datacoord_stored_rows_num", 0))
    data["Loaded Entities"]  = int(gauges.get("milvus_querynode_entity_num", 0))
    data["Storage KV Size"]  = bytes_to_mb(gauges.get("milvus_meta_kv_size", 0))
    data["QueryNode Disk Used"] = round(gauges.get("milvus_querynode_disk_used_size", 0), 2)


def getQuerySearchMetrics(data, raw_text):
    """Search/queue/execute latency (populated after real traffic).

    Filtered to module="cardinal" (the top-level segment-core entry point) so the
    per-index-type "knowhere" breakdown of the same requests isn't double-counted.
    """
    _, search_sum, search_count = filtered_sum(raw_text, "search_latency", "module", "cardinal")
    data["Search Requests"] = int(search_count)
    data["Search Latency"]  = round(search_sum / search_count, 2) if search_count > 0 else 0.0

    _, queue_sum, queue_count = filtered_sum(raw_text, "queue_latency", "module", "cardinal")
    data["Query Requests"] = int(queue_count)
    data["Query Latency"]  = round(queue_sum / queue_count, 2) if queue_count > 0 else 0.0

    _, exec_sum, exec_count = filtered_sum(raw_text, "exec_latency", "module", "cardinal")
    data["Execution Latency"] = round(exec_sum / exec_count, 2) if exec_count > 0 else 0.0


def getNetworkStorageMetrics(data, gauges):
    """Process network throughput and underlying object-storage I/O counters."""
    data["Network Received"]    = bytes_to_mb(gauges.get("process_network_receive_bytes_total", 0))
    data["Network Transmitted"] = bytes_to_mb(gauges.get("process_network_transmit_bytes_total", 0))
    data["Storage Read Bytes"]  = bytes_to_mb(gauges.get("milvus_storage_filesystem_read_bytes", 0))
    data["Storage Write Bytes"] = bytes_to_mb(gauges.get("milvus_storage_filesystem_write_bytes", 0))
    data["Storage Read Ops"]    = int(gauges.get("milvus_storage_filesystem_read_count", 0))
    data["Storage Write Ops"]   = int(gauges.get("milvus_storage_filesystem_write_count", 0))
    data["Storage Failed Ops"]  = int(gauges.get("milvus_storage_filesystem_failed_count", 0))


def getClusterHealthMetrics(data, gauges, sums, counts, raw_text):
    """Managed-node counts from coordinators, metastore throughput/latency and task queues."""
    data["Data Nodes (Managed)"]     = int(gauges.get("milvus_datacoord_datanode_num", 0))
    data["Index Nodes (Managed)"]    = int(gauges.get("milvus_datacoord_index_node_num", 0))
    data["Query Nodes (Managed)"]    = int(gauges.get("milvus_querycoord_querynode_num", 0))
    data["Proxy Nodes (Managed)"]    = int(gauges.get("milvus_rootcoord_proxy_num", 0))
    data["QueryCoord Pending Tasks"] = int(gauges.get("milvus_querycoord_task_num", 0))
    data["Segment GC Runs"]          = int(gauges.get("milvus_datacoord_gc_run_count", 0))
    data["Meta Store Latency"]       = avg_latency(sums, counts, "milvus_meta_request_latency")

    meta_ops, _, _ = filtered_sum(raw_text, "milvus_meta_op_count", "status", "total")
    data["Meta Store Operations"] = int(meta_ops)

    ddl_requests, _, _ = filtered_sum(raw_text, "milvus_rootcoord_ddl_req_count", "status", "total")
    data["DDL Requests"] = int(ddl_requests)

    tasks_in_progress, _, _ = filtered_sum(raw_text, "milvus_datacoord_task_count", "task_state", "JobStateInProgress")
    data["Index/Stats Tasks In Progress"] = int(tasks_in_progress)


def getComponentDetails(data, role_counts):
    """Build per-component (role) summary table for the single Milvus node."""
    roles = [
        "proxy",
        "querynode",
        "datanode",
        "mixcoord",
        "rootcoord",
        "datacoord",
        "querycoord",
        "indexcoord",
    ]

    component_details = []
    for role in roles:
        count = int(role_counts.get(role, 0))
        if count > 0:
            component_details.append({
                "name"          : role,
                "Instance Count": count,
                "State"         : "HEALTHY",
            })

    data["Component Details"] = component_details if component_details else \
        [{"name": "-", "Instance Count": 0, "State": "-"}]


def metricCollector():
    data = {}
    data["plugin_version"]     = PLUGIN_VERSION
    data["heartbeat_required"] = HEARTBEAT
    data["units"]              = METRICS_UNITS
    data["tabs"]               = TABS

    raw_text = getHealth(data)
    if raw_text is None:
        return data

    gauges, sums, counts   = parsePrometheus(raw_text)
    role_counts, node_ids  = parseComponentNodes(raw_text)

    data["Milvus Version"] = parseBuildVersion(raw_text)

    getProcessMetrics(data, gauges, sums, counts)
    getClusterMetrics(data, gauges, role_counts, node_ids)
    getStorageMetrics(data, gauges)
    getQuerySearchMetrics(data, raw_text)
    getNetworkStorageMetrics(data, gauges)
    getClusterHealthMetrics(data, gauges, sums, counts, raw_text)
    getComponentDetails(data, role_counts)

    return data


def run(param):
    global MILVUS_HOST, MILVUS_PORT, MILVUS_SERVER, MILVUS_SSL_VERIFY

    MILVUS_HOST = clean_quotes(param.get("host", "localhost"))
    MILVUS_PORT = clean_quotes(param.get("metrics_port", param.get("port", "9091")))

    ssl_enabled       = clean_quotes(param.get("ssl", "false")).lower() == "true"
    insecure          = clean_quotes(param.get("insecure", "false")).lower() == "true"
    protocol          = "https" if ssl_enabled else "http"
    MILVUS_SERVER     = f"{protocol}://{MILVUS_HOST}:{MILVUS_PORT}"
    MILVUS_SSL_VERIFY = not insecure

    try:
        return metricCollector()
    except Exception as e:
        return {
            "status"            : 0,
            "msg"               : f"Plugin Error: {str(e)}",
            "plugin_version"    : PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host",         help="Milvus Host",                        nargs="?", default="localhost")
    parser.add_argument("--port",         help="Milvus Metrics Port",                nargs="?", default="9091")
    parser.add_argument("--metrics_port", help="Milvus Prometheus Metrics Port",     nargs="?", default="9091")
    parser.add_argument("--ssl",          help="Use SSL/HTTPS (true/false)",                    default="false")
    parser.add_argument("--insecure",     help="Skip SSL certificate verification",             default="false")
    args = parser.parse_args()

    MILVUS_HOST = args.host
    MILVUS_PORT = args.metrics_port if args.metrics_port else args.port

    ssl_enabled       = args.ssl.lower() == "true"
    insecure          = args.insecure.lower() == "true"
    protocol          = "https" if ssl_enabled else "http"
    MILVUS_SERVER     = f"{protocol}://{MILVUS_HOST}:{MILVUS_PORT}"
    MILVUS_SSL_VERIFY = not insecure

    print(json.dumps(metricCollector(), indent=2))
