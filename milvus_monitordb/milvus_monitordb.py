#!/usr/bin/env python3
import json
import time
import sys
import socket
import urllib.request
import argparse

# Strict timeout (3s optimized for large Milvus payload parsing)
HTTP_TIMEOUT = 3.0
socket.setdefaulttimeout(HTTP_TIMEOUT)

# Version 41 - Fixed label parsing, optimized stream processing, and robust aggregation
PLUGIN_VERSION = 1
HEARTBEAT = "true"

# Define 5 Professional Dashboard Tabs with short and understandable names
TABS = {
    "System Health": {
        "order": 1,
        "tablist": [
            "Response Time",
            "Milvus Status",
            "Metrics Total",
            "CPU Percent",
            "Memory Usage",
            "Active Goroutines",
            "OS Threads",
            "Open File Descriptors",
            "Process Max FDs",
            "Resident Memory MB",
            "Virtual Memory MB",
            "Heap Usage MB",
            "Heap Idle MB",
            "Heap Sys MB",
            "MMap InUse MB",
            "Next GC Threshold MB",
            "GC Duration Avg ms",
            "GC Cycle Count",
            "Mallocs Count",
            "Write Blocks"
        ]
    },
    "Nodes": {
        "order": 2,
        "tablist": [
            "Total Nodes",
            "Proxy Nodes",
            "Query Nodes",
            "Data Nodes",
            "Index Nodes",
            "Streaming Nodes",
            "gRPC Active Conns",
            "Proxy Active Conns",
            "DML Channels Count",
            "Collections Loaded",
            "RootCoord Collections",
            "RootCoord Partitions",
            "QN Entity Count",
            "QN Entity Memory MB",
            "QN Flowgraph Count",
            "QN DML Channel Count",
            "DN Flowgraph Count",
            "DN Consume Bytes",
            "DN Consume Msg Count",
            "DN AutoFlush Op Count"
        ]
    },
    "Query & Search": {
        "order": 3,
        "tablist": [
            "Query Requests",
            "Query Latency ms",
            "Query Queue Latency ms",
            "Query Reduce Latency ms",
            "Query CoreSearch Latency ms",
            "Search Requests",
            "Search Latency ms",
            "Search Queue Latency ms",
            "Search TopK Avg",
            "Search WaitResult Latency ms",
            "Search DecodeResult Latency ms",
            "QN ReadTask Concurrency",
            "QN ReadTask Ready Queue",
            "QN ReadTask Unsolved Queue",
            "QN LoadSegment Concurrency",
            "QN LoadSegment Latency ms",
            "QN MsgDispatcher Lag ms",
            "Search QPS Rate",
            "Insert QPS Rate",
            "Searched Vector Count"
        ]
    },
    "Storage & Memory": {
        "order": 4,
        "tablist": [
            "Data Collections",
            "Query Collections",
            "Query Replicas",
            "Data Segments",
            "Loaded Segments",
            "Growing Segments",
            "Sealed Segments",
            "Flushed Segments",
            "Total Indexed Rows",
            "Loaded Entities QN",
            "Binlog Size MB",
            "Index Files Size MB",
            "Storage KV Size MB",
            "Meta KV Size MB",
            "Raw Data Size MB",
            "QN CGO Memory MB",
            "Insert Size MB",
            "Insert Request Count",
            "Delete Vectors Count",
            "Flushed Rows Count"
        ]
    },
    "Runtime & Queues": {
        "order": 5,
        "tablist": [
            "Proxy Request Count",
            "Ingestion Volume",
            "Flush Request Count",
            "Flushed Bytes MB",
            "Mutation Send Latency ms",
            "DN EncodeBuffer Latency ms",
            "DN Save Latency ms",
            "Storage Op Count",
            "Storage Request Latency ms",
            "MQ Consumer Count",
            "MsgStream Op Count",
            "MsgStream Request Latency ms",
            "Proxy TT Lag ms",
            "Consumer Lag ms",
            "Proxy Queue Length",
            "QN Queue Length",
            "Index Build Latency ms",
            "Index Save Latency ms",
            "Index Task Count",
            "Index TaskQueue Latency ms"
        ]
    }
}

UNITS = {
    "Response Time": "ms",
    "Milvus Status": "status",
    "Metrics Total": "metrics",
    "CPU Percent": "%",
    "Memory Usage": "MB",
    "Active Goroutines": "goroutines",
    "OS Threads": "threads",
    "Open File Descriptors": "files",
    "Process Max FDs": "files",
    "Resident Memory MB": "MB",
    "Virtual Memory MB": "MB",
    "Heap Usage MB": "MB",
    "Heap Idle MB": "MB",
    "Heap Sys MB": "MB",
    "MMap InUse MB": "MB",
    "Next GC Threshold MB": "MB",
    "GC Duration Avg ms": "ms",
    "GC Cycle Count": "cycles",
    "Mallocs Count": "allocs",
    "Write Blocks": "blocks",
    "Total Nodes": "nodes",
    "Proxy Nodes": "nodes",
    "Query Nodes": "nodes",
    "Data Nodes": "nodes",
    "Index Nodes": "nodes",
    "Streaming Nodes": "nodes",
    "gRPC Active Conns": "connections",
    "Proxy Active Conns": "connections",
    "DML Channels Count": "channels",
    "Collections Loaded": "collections",
    "RootCoord Collections": "collections",
    "RootCoord Partitions": "partitions",
    "QN Entity Count": "entities",
    "QN Entity Memory MB": "MB",
    "QN Flowgraph Count": "pipelines",
    "QN DML Channel Count": "channels",
    "DN Flowgraph Count": "pipelines",
    "DN Consume Bytes": "bytes",
    "DN Consume Msg Count": "messages",
    "DN AutoFlush Op Count": "operations",
    "Query Requests": "requests",
    "Query Latency ms": "ms",
    "Query Queue Latency ms": "ms",
    "Query Reduce Latency ms": "ms",
    "Query CoreSearch Latency ms": "ms",
    "Search Requests": "requests",
    "Search Latency ms": "ms",
    "Search Queue Latency ms": "ms",
    "Search TopK Avg": "items",
    "Search WaitResult Latency ms": "ms",
    "Search DecodeResult Latency ms": "ms",
    "QN ReadTask Concurrency": "tasks",
    "QN ReadTask Ready Queue": "items",
    "QN ReadTask Unsolved Queue": "items",
    "QN LoadSegment Concurrency": "segments",
    "QN LoadSegment Latency ms": "ms",
    "QN MsgDispatcher Lag ms": "ms",
    "Search QPS Rate": "qps",
    "Insert QPS Rate": "qps",
    "Searched Vector Count": "vectors",
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
    "Binlog Size MB": "MB",
    "Index Files Size MB": "MB",
    "Storage KV Size MB": "MB",
    "Meta KV Size MB": "MB",
    "Raw Data Size MB": "MB",
    "QN CGO Memory MB": "MB",
    "Insert Size MB": "MB",
    "Insert Request Count": "requests",
    "Delete Vectors Count": "vectors",
    "Flushed Rows Count": "rows",
    "Proxy Request Count": "requests",
    "Ingestion Volume": "MB",
    "Flush Request Count": "requests",
    "Flushed Bytes MB": "MB",
    "Mutation Send Latency ms": "ms",
    "DN EncodeBuffer Latency ms": "ms",
    "DN Save Latency ms": "ms",
    "Storage Op Count": "operations",
    "Storage Request Latency ms": "ms",
    "MQ Consumer Count": "consumers",
    "MsgStream Op Count": "operations",
    "MsgStream Request Latency ms": "ms",
    "Proxy TT Lag ms": "ms",
    "Consumer Lag ms": "ms",
    "Proxy Queue Length": "items",
    "QN Queue Length": "items",
    "Index Build Latency ms": "ms",
    "Index Save Latency ms": "ms",
    "Index Task Count": "tasks",
    "Index TaskQueue Latency ms": "ms"
}

METRICS_MAP = {
    "milvus_status": ("Milvus Status", "DIRECT"),
    "process_cpu_seconds_total": ("CPU Percent", "DIRECT"),
    "process_resident_memory_bytes": ("Memory Usage", "MB"),
    "go_goroutines": ("Active Goroutines", "DIRECT"),
    "go_threads": ("OS Threads", "DIRECT"),
    "process_open_fds": ("Open File Descriptors", "DIRECT"),
    "process_max_fds": ("Process Max FDs", "DIRECT"),
    "process_virtual_memory_bytes": ("Virtual Memory MB", "MB"),
    "go_memstats_heap_inuse_bytes": ("Heap Usage MB", "MB"),
    "go_memstats_heap_idle_bytes": ("Heap Idle MB", "MB"),
    "go_memstats_heap_sys_bytes": ("Heap Sys MB", "MB"),
    "milvus_internal_mmap_in_used_space_bytes": ("MMap InUse MB", "MB"),
    "go_memstats_next_gc_bytes": ("Next GC Threshold MB", "MB"),
    "go_gc_duration_seconds": ("GC Duration Avg ms", "AVG_SEC_TO_MS"),
    "go_gc_duration_seconds_count": ("GC Cycle Count", "DIRECT"),
    "go_memstats_mallocs_total": ("Mallocs Count", "DIRECT"),
    "milvus_rootcoord_force_deny_writing_counter": ("Write Blocks", "DIRECT"),

    "milvus_num_node": ("Total Nodes", "DIRECT"),
    "milvus_rootcoord_proxy_num": ("Proxy Nodes", "DIRECT"),
    "milvus_querycoord_querynode_num": ("Query Nodes", "DIRECT"),
    "milvus_datacoord_datanode_num": ("Data Nodes", "DIRECT"),
    "milvus_datacoord_index_node_num": ("Index Nodes", "DIRECT"),
    "milvus_streamingnode_num": ("Streaming Nodes", "DIRECT"),
    "milvus_grpc_active_connections": ("gRPC Active Conns", "DIRECT"),
    "milvus_proxy_active_connections": ("Proxy Active Conns", "DIRECT"),
    "milvus_rootcoord_dml_channel_num": ("DML Channels Count", "DIRECT"),
    "milvus_querynode_collection_num": ("Collections Loaded", "DIRECT"),
    "milvus_rootcoord_collection_num": ("RootCoord Collections", "DIRECT"),
    "milvus_rootcoord_partition_num": ("RootCoord Partitions", "DIRECT"),
    "milvus_querynode_entity_num": ("QN Entity Count", "DIRECT"),
    "milvus_querynode_entity_size": ("QN Entity Memory MB", "MB"),
    "milvus_querynode_flowgraph_num": ("QN Flowgraph Count", "DIRECT"),
    "milvus_querynode_dml_vchannel_num": ("QN DML Channel Count", "DIRECT"),
    "milvus_datanode_flowgraph_num": ("DN Flowgraph Count", "DIRECT"),
    "milvus_datanode_consume_bytes_count": ("DN Consume Bytes", "DIRECT"),
    "milvus_datanode_consume_msg_count": ("DN Consume Msg Count", "DIRECT"),
    "milvus_datanode_autoflush_buffer_op_count": ("DN AutoFlush Op Count", "DIRECT"),

    "milvus_proxy_collection_sq_latency_count_query": ("Query Requests", "DIRECT"),
    "milvus_proxy_collection_sq_latency_query": ("Query Latency ms", "AVG"),
    "milvus_proxy_req_in_queue_latency": ("Query Queue Latency ms", "AVG"),
    "milvus_querynode_sq_reduce_latency": ("Query Reduce Latency ms", "AVG"),
    "milvus_internal_core_search_latency": ("Query CoreSearch Latency ms", "AVG_US"),
    "milvus_proxy_collection_sq_latency_count_search": ("Search Requests", "DIRECT"),
    "milvus_proxy_collection_sq_latency_search": ("Search Latency ms", "AVG"),
    "milvus_querynode_sq_queue_latency": ("Search Queue Latency ms", "AVG"),
    "milvus_search_topk": ("Search TopK Avg", "AVG"),
    "milvus_proxy_sq_wait_result_latency": ("Search WaitResult Latency ms", "AVG"),
    "milvus_proxy_sq_decode_result_latency": ("Search DecodeResult Latency ms", "AVG"),
    "milvus_querynode_read_task_concurrency": ("QN ReadTask Concurrency", "DIRECT"),
    "milvus_querynode_read_task_ready_len": ("QN ReadTask Ready Queue", "DIRECT"),
    "milvus_querynode_read_task_unsolved_len": ("QN ReadTask Unsolved Queue", "DIRECT"),
    "milvus_querynode_load_segment_concurrency": ("QN LoadSegment Concurrency", "DIRECT"),
    "milvus_querynode_load_segment_latency": ("QN LoadSegment Latency ms", "AVG"),
    "milvus_querynode_msg_dispatcher_tt_lag_ms": ("QN MsgDispatcher Lag ms", "DIRECT"),
    "milvus_proxy_search_qps": ("Search QPS Rate", "DIRECT"),
    "milvus_proxy_insert_qps": ("Insert QPS Rate", "DIRECT"),
    "milvus_proxy_search_vectors_count": ("Searched Vector Count", "DIRECT"),

    "milvus_datacoord_collection_num": ("Data Collections", "DIRECT"),
    "milvus_querycoord_collection_num": ("Query Collections", "DIRECT"),
    "milvus_querycoord_replica_num": ("Query Replicas", "DIRECT"),
    "milvus_datacoord_segment_num": ("Data Segments", "DIRECT"),
    "milvus_querycoord_segment_num": ("Loaded Segments", "DIRECT"),
    "milvus_datacoord_growing_segment_num": ("Growing Segments", "DIRECT"),
    "milvus_datacoord_sealed_segment_num": ("Sealed Segments", "DIRECT"),
    "milvus_datacoord_flushed_segment_num": ("Flushed Segments", "DIRECT"),
    "milvus_datacoord_stored_rows_num": ("Total Indexed Rows", "DIRECT"),
    "milvus_datacoord_stored_binlog_size": ("Binlog Size MB", "MB"),
    "milvus_datacoord_stored_index_files_size": ("Index Files Size MB", "MB"),
    "milvus_storage_kv_size": ("Storage KV Size MB", "MB"),
    "milvus_meta_kv_size": ("Meta KV Size MB", "MB"),
    "milvus_datanode_raw_data_size": ("Raw Data Size MB", "MB"),
    "milvus_querynode_cgo_memory_bytes": ("QN CGO Memory MB", "MB"),
    "milvus_proxy_receive_bytes_count": ("Insert Size MB", "MB"),
    "milvus_proxy_insert_req_count": ("Insert Request Count", "DIRECT"),
    "milvus_proxy_delete_vectors_count": ("Delete Vectors Count", "DIRECT"),
    "milvus_datanode_flushed_data_rows_count": ("Flushed Rows Count", "DIRECT"),
    "milvus_querynode_entity_num": ("Loaded Entities QN", "DIRECT"),

    "milvus_proxy_req_count": ("Proxy Request Count", "DIRECT"),
    "milvus_proxy_receive_bytes_count": ("Ingestion Volume", "MB"),
    "milvus_datanode_flush_req_count": ("Flush Request Count", "DIRECT"),
    "milvus_datanode_flushed_data_size_count": ("Flushed Bytes MB", "MB"),
    "milvus_proxy_mutation_send_latency": ("Mutation Send Latency ms", "AVG"),
    "milvus_datanode_encode_buffer_latency": ("DN EncodeBuffer Latency ms", "AVG"),
    "milvus_datanode_save_latency": ("DN Save Latency ms", "AVG"),
    "milvus_storage_op_count": ("Storage Op Count", "DIRECT"),
    "milvus_storage_request_latency": ("Storage Request Latency ms", "DIRECT"),
    "milvus_msg_queue_consumer_num": ("MQ Consumer Count", "DIRECT"),
    "milvus_msgstream_op_count": ("MsgStream Op Count", "DIRECT"),
    "milvus_msgstream_request_latency": ("MsgStream Request Latency ms", "AVG"),
    "milvus_proxy_tt_lag_ms": ("Proxy TT Lag ms", "DIRECT"),
    "milvus_datanode_consume_tt_lag_ms": ("Consumer Lag ms", "DIRECT"),
    "milvus_proxy_sq_queue_length": ("Proxy Queue Length", "DIRECT"),
    "milvus_querynode_sq_queue_length": ("QN Queue Length", "DIRECT"),
    "milvus_indexnode_build_index_latency": ("Index Build Latency ms", "AVG"),
    "milvus_indexnode_save_index_latency": ("Index Save Latency ms", "AVG"),
    "milvus_indexnode_index_task_count": ("Index Task Count", "DIRECT"),
    "milvus_indexnode_index_task_latency_in_queue": ("Index TaskQueue Latency ms", "AVG")
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
        res["Milvus Status"] = 1.0
    except Exception as e:
        err = get_error_payload(f"Connect failed: {str(e)}")
        err["Response Time"] = round((time.time() - start) * 1000, 2)
        err["Milvus Status"] = 0.0
        return err

    gauges, sums, counts = {}, {}, {}
    total_series_count = 0

    for line in raw_text.split("\n"):
        if not line or line.startswith("#"):
            continue

        parts = line.rsplit(" ", 1)
        if len(parts) != 2:
            continue

        total_series_count += 1
        raw_key_part = parts[0]
        
        effective_key = raw_key_press = raw_key_part.split("{")[0]
        if "query_type=\"query\"" in raw_key_part:
            effective_key = f"{raw_key_press}_query"
        elif "query_type=\"search\"" in raw_key_part:
            effective_key = f"{raw_key_press}_search"

        try:
            val = float(parts[1])
            if val != val or val in (float('inf'), float('-inf')):
                val = 0.0
        except ValueError:
            continue

        if effective_key in METRICS_MAP:
            gauges[effective_key] = gauges.get(effective_key, 0.0) + val
        elif raw_key_press in METRICS_MAP:
            gauges[raw_key_press] = gauges.get(raw_key_press, 0.0) + val
        elif effective_key.endswith("_sum"):
            base = effective_key[:-4]
            if base in METRICS_MAP:
                sums[base] = sums.get(base, 0.0) + val
        elif effective_key.endswith("_count"):
            base = effective_key[:-6]
            if base in METRICS_MAP:
                counts[base] = counts.get(base, 0.0) + val

    res["Metrics Total"] = float(total_series_count)

    for prom_key, val in gauges.items():
        if prom_key in METRICS_MAP:
            display_name, calc_type = METRICS_MAP[prom_key]
            if calc_type == "MB":
                res[display_name] = round(val / (1024 * 1024), 2)
            elif calc_type == "DIRECT":
                res[display_name] = round(val, 2)

    for prom_key, (display_name, calc_type) in METRICS_MAP.items():
        if calc_type in ("AVG", "AVG_US", "AVG_SEC_TO_MS"):
            cnt = counts.get(prom_key, 0.0)
            avg = (sums.get(prom_key, 0.0) / cnt) if cnt > 0 else 0.0
            if calc_type == "AVG_US":
                res[display_name] = round(avg / 1000.0, 2)
            elif calc_type == "AVG_SEC_TO_MS":
                res[display_name] = round(avg * 1000.0, 2)
            else:
                res[display_name] = round(avg, 2)

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



if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Milvus Monitoring Plugin")
        parser.add_argument('--host', help='Host to be monitored', nargs='?', default="127.0.0.1")
        parser.add_argument('--port', help='Port number', type=int, nargs='?', default=9091)
        parser.add_argument('--metrics_port', help='Metrics port number', type=int, nargs='?', default=9091)
        parser.add_argument('--username', help='Username', nargs='?', default="")
        parser.add_argument('--password', help='Password', nargs='?', default="")
        parser.add_argument('--ssl_option', help='SSL option', nargs='?', default="")
        parser.add_argument('--cafile', help='CA file', nargs='?', default="")
        parser.add_argument('--logs_enabled', help='Enable logs', default="false")
        parser.add_argument('--log_type_name', help='Log type name', nargs='?', default="")
        parser.add_argument('--log_file_path', help='Log file path', nargs='?', default="")
        
        args, _ = parser.parse_known_args()

        host = clean_param(str(args.host), "127.0.0.1")
        port = args.metrics_port if args.metrics_port != 9091 else args.port

        try:
            port = str(int(port))
        except ValueError:
            port = "9091"

        print(json.dumps(metricCollector(host, port)))
        sys.stdout.flush()
    except Exception as fatal_e:
        print(json.dumps(get_error_payload(f"Fatal Exec Error: {str(fatal_e)}")))
        sys.stdout.flush()