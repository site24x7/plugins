#!/usr/bin/env python3
import json
import time
import sys
import socket
import urllib.request

# Strict timeout (2s) to prevent Site24x7 hard process termination
HTTP_TIMEOUT = 2.0
socket.setdefaulttimeout(HTTP_TIMEOUT)

# Version 37 forces Site24x7 to re-register metrics and tabs
PLUGIN_VERSION = 37
HEARTBEAT = "true"

# Define Dashboard Tabs Configuration (Exactly 49 total metrics including Response Time)
TABS = {
    "Overview": {
        "order": 1,
        "tablist": [
            "Response Time",
            "CPU Percent",
            "Memory Usage",
            "Active Goroutines",
            "OS Threads",
            "Open File Descriptors"
        ]
    },
    "Nodes and Topology": {
        "order": 2,
        "tablist": [
            "Total Nodes",
            "Proxy Nodes",
            "Query Nodes",
            "Data Nodes",
            "Index Nodes",
            "Streaming Nodes",
            "gRPC Active Conns",
            "Proxy Active Conns"
        ]
    },
    "Collections and Segments": {
        "order": 3,
        "tablist": [
            "Data Collections",
            "Query Collections",
            "Query Replicas",
            "Data Segments",
            "Loaded Segments",
            "Growing Segments",
            "Sealed Segments",
            "Flushed Segments"
        ]
    },
    "Storage and Memory": {
        "order": 4,
        "tablist": [
            "Total Indexed Rows",
            "Loaded Entities QN",
            "Binlog Size",
            "Index Files Size",
            "Storage KV Size",
            "Meta KV Size",
            "Raw Data Size",
            "QN CGO Memory"
        ]
    },
    "Latency": {
        "order": 5,
        "tablist": [
            "Search Query Latency",
            "Core Search Latency",
            "QN Search Latency",
            "Proxy Req Latency",
            "DataNode Flush Lat",
            "Index Build Latency",
            "gRPC Request Latency"
        ]
    },
    "Throughput and Queues": {
        "order": 6,
        "tablist": [
            "Proxy Request Count",
            "Ingestion Volume",
            "Delete Vectors Count",
            "Flush Request Count",
            "Flushed Rows Count",
            "Searched Vector Count",
            "Query Request Count",
            "Insert Request Count",
            "Search QPS Rate",
            "Insert QPS Rate",
            "Proxy Queue Length",
            "QN Queue Length"
        ]
    }
}

UNITS = {
    "Response Time": "ms",
    "CPU Percent": "%",
    "Memory Usage": "MB",
    "Active Goroutines": "goroutines",
    "OS Threads": "threads",
    "Open File Descriptors": "files",
    "Total Nodes": "nodes",
    "Proxy Nodes": "nodes",
    "Query Nodes": "nodes",
    "Data Nodes": "nodes",
    "Index Nodes": "nodes",
    "Streaming Nodes": "nodes",
    "gRPC Active Conns": "connections",
    "Proxy Active Conns": "connections",
    "Data Collections": "collections",
    "Query Collections": "collections",
    "Query Replicas": "replicas",
    "Data Segments": "segments",
    "Loaded Segments": "segments",
    "Growing Segments": "segments",
    "Sealed Segments": "segments",
    "Flushed Segments": "segments",
    "Total Indexed Rows": "entities",
    "Loaded Entities QN": "entities",
    "Binlog Size": "MB",
    "Index Files Size": "MB",
    "Storage KV Size": "MB",
    "Meta KV Size": "MB",
    "Raw Data Size": "MB",
    "QN CGO Memory": "MB",
    "Search Query Latency": "ms",
    "Core Search Latency": "ms",
    "QN Search Latency": "ms",
    "Proxy Req Latency": "ms",
    "DataNode Flush Lat": "ms",
    "Index Build Latency": "ms",
    "gRPC Request Latency": "ms",
    "Proxy Request Count": "requests",
    "Ingestion Volume": "MB",
    "Delete Vectors Count": "vectors",
    "Flush Request Count": "requests",
    "Flushed Rows Count": "rows",
    "Searched Vector Count": "vectors",
    "Query Request Count": "requests",
    "Insert Request Count": "requests",
    "Search QPS Rate": "qps",
    "Insert QPS Rate": "qps",
    "Proxy Queue Length": "items",
    "QN Queue Length": "items"
}

METRICS_MAP = {
    "process_cpu_seconds_total": ("CPU Percent", "DIRECT"),
    "process_resident_memory_bytes": ("Memory Usage", "MB"),
    "go_goroutines": ("Active Goroutines", "DIRECT"),
    "go_threads": ("OS Threads", "DIRECT"),
    "process_open_fds": ("Open File Descriptors", "DIRECT"),
    "milvus_num_node": ("Total Nodes", "DIRECT"),
    "milvus_rootcoord_proxy_num": ("Proxy Nodes", "DIRECT"),
    "milvus_querycoord_querynode_num": ("Query Nodes", "DIRECT"),
    "milvus_datacoord_datanode_num": ("Data Nodes", "DIRECT"),
    "milvus_datacoord_index_node_num": ("Index Nodes", "DIRECT"),
    "milvus_streamingnode_num": ("Streaming Nodes", "DIRECT"),
    "milvus_grpc_active_connections": ("gRPC Active Conns", "DIRECT"),
    "milvus_proxy_active_connections": ("Proxy Active Conns", "DIRECT"),
    "milvus_datacoord_collection_num": ("Data Collections", "DIRECT"),
    "milvus_querycoord_collection_num": ("Query Collections", "DIRECT"),
    "milvus_querycoord_replica_num": ("Query Replicas", "DIRECT"),
    "milvus_datacoord_segment_num": ("Data Segments", "DIRECT"),
    "milvus_querycoord_segment_num": ("Loaded Segments", "DIRECT"),
    "milvus_datacoord_growing_segment_num": ("Growing Segments", "DIRECT"),
    "milvus_datacoord_sealed_segment_num": ("Sealed Segments", "DIRECT"),
    "milvus_datacoord_flushed_segment_num": ("Flushed Segments", "DIRECT"),
    "milvus_datacoord_stored_rows_num": ("Total Indexed Rows", "DIRECT"),
    "milvus_querynode_entity_num": ("Loaded Entities QN", "DIRECT"),
    "milvus_datacoord_stored_binlog_size": ("Binlog Size", "MB"),
    "milvus_datacoord_stored_index_files_size": ("Index Files Size", "MB"),
    "milvus_storage_kv_size": ("Storage KV Size", "MB"),
    "milvus_meta_kv_size": ("Meta KV Size", "MB"),
    "milvus_datanode_raw_data_size": ("Raw Data Size", "MB"),
    "milvus_querynode_cgo_memory_bytes": ("QN CGO Memory", "MB"),
    "milvus_proxy_collection_sq_latency": ("Search Query Latency", "AVG"),
    "milvus_internal_core_search_latency": ("Core Search Latency", "AVG_US"),
    "milvus_querynode_search_latency": ("QN Search Latency", "AVG"),
    "milvus_proxy_req_latency": ("Proxy Req Latency", "AVG"),
    "milvus_datanode_flush_latency": ("DataNode Flush Lat", "AVG"),
    "milvus_indexnode_build_latency": ("Index Build Latency", "AVG"),
    "milvus_proxy_grpc_request_latency": ("gRPC Request Latency", "AVG"),
    "milvus_proxy_req_count": ("Proxy Request Count", "DIRECT"),
    "milvus_proxy_receive_bytes_count": ("Ingestion Volume", "MB"),
    "milvus_proxy_delete_vectors_count": ("Delete Vectors Count", "DIRECT"),
    "milvus_datanode_flush_req_count": ("Flush Request Count", "DIRECT"),
    "milvus_datanode_flushed_data_rows_count": ("Flushed Rows Count", "DIRECT"),
    "milvus_proxy_search_vectors_count": ("Searched Vector Count", "DIRECT"),
    "milvus_proxy_query_req_count": ("Query Request Count", "DIRECT"),
    "milvus_proxy_insert_req_count": ("Insert Request Count", "DIRECT"),
    "milvus_proxy_search_qps": ("Search QPS Rate", "DIRECT"),
    "milvus_proxy_insert_qps": ("Insert QPS Rate", "DIRECT"),
    "milvus_proxy_sq_queue_length": ("Proxy Queue Length", "DIRECT"),
    "milvus_querynode_sq_queue_length": ("QN Queue Length", "DIRECT")
}

def get_error_payload(msg):
    payload = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "status": 0,
        "msg": str(msg)[:100],
        "units": UNITS,
        "tabs": TABS
    }
    for k in UNITS.keys():
        payload[k] = 0
    return payload

def metricCollector(host, port):
    start = time.time()
    res = {display_name: 0.0 for display_name in UNITS.keys()}
    url = f"http://{host}:{port}/metrics"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Site24x7-Plugin"})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            raw_text = resp.read().decode("utf-8")
    except Exception as e:
        err = get_error_payload(f"Connect failed: {str(e)}")
        err["Response Time"] = round((time.time() - start) * 1000, 2)
        return err

    gauges, sums, counts = {}, {}, {}
    for line in raw_text.split("\n"):
        if not line or line.startswith("#"):
            continue

        parts = line.rsplit(" ", 1)
        if len(parts) != 2:
            continue

        k = parts[0].split("{")[0]
        if not (k in METRICS_MAP or k.endswith("_sum") or k.endswith("_count")):
            continue

        try:
            val = float(parts[1])
            if val != val or val in (float('inf'), float('-inf')):
                val = 0.0
        except ValueError:
            continue

        if k in METRICS_MAP:
            gauges[k] = gauges.get(k, 0.0) + val
        elif k.endswith("_sum"):
            base = k[:-4]
            if base in METRICS_MAP:
                sums[base] = sums.get(base, 0.0) + val
        elif k.endswith("_count"):
            base = k[:-6]
            if base in METRICS_MAP:
                counts[base] = counts.get(base, 0.0) + val

    for prom_key, val in gauges.items():
        if prom_key in METRICS_MAP:
            display_name, calc_type = METRICS_MAP[prom_key]
            if calc_type == "MB":
                res[display_name] = round(val / (1024 * 1024), 2)
            elif calc_type == "DIRECT":
                res[display_name] = round(val, 2)

    for prom_key, (display_name, calc_type) in METRICS_MAP.items():
        if calc_type in ("AVG", "AVG_US"):
            cnt = counts.get(prom_key, 0.0)
            avg = (sums.get(prom_key, 0.0) / cnt) if cnt > 0 else 0.0
            res[display_name] = round(avg / 1000.0 if calc_type == "AVG_US" else avg, 2)

    res["Response Time"] = round((time.time() - start) * 1000, 2)

    out = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "status": 1,
        "msg": "OK",
        "units": UNITS,
        "tabs": TABS
    }
    out.update(res)
    return out

def clean_param(val, default):
    if not val or not isinstance(val, str):
        return default
    val = val.strip("\"'")
    if len(val) > 20 and ("==" in val or "+" in val or "/" in val):
        return default
    return val

def parse_cli_args():
    raw_args = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            k = k.lstrip("-").replace("encrypted.", "")
            raw_args[k] = v

    host = clean_param(raw_args.get("host"), "127.0.0.1")
    port = clean_param(raw_args.get("metrics_port"), "9091")

    try:
        int(port)
    except ValueError:
        port = "9091"

    return host, port

if __name__ == "__main__":
    try:
        host, port = parse_cli_args()
        print(json.dumps(metricCollector(host, port)))
        sys.stdout.flush()
    except Exception as fatal_e:
        print(json.dumps(get_error_payload(f"Fatal Exec Error: {str(fatal_e)}")))
        sys.stdout.flush()