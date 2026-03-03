#!/usr/bin/python3
"""
Site24x7 Plugin to monitor ClickHouse metrics with categorized tabs.
"""

import json
import argparse
from clickhouse_driver import Client

# ==== Plugin Info ====
PLUGIN_VERSION = 1
HEARTBEAT_REQUIRED = "true"
# ==== Units ====
units = {
            "MarkCacheBytes": "bytes","MemoryResident": "bytes", "MemoryShared": "bytes", "MemoryVirtual": "bytes",
            "ReplicasMaxAbsoluteDelay": "seconds","ReplicasMaxRelativeDelay": "seconds",
            "UncompressedCacheBytes": "bytes", "Uptime": "seconds",
            "jemalloc.allocated": "bytes", "jemalloc.arenas.all.dirty_purged": "bytes","jemalloc.resident": "bytes",
            "jemalloc.retained": "bytes","CompressedReadBufferBytes": "bytes",
            "DiskReadElapsedMicroseconds": "microseconds","DiskWriteElapsedMicroseconds": "microseconds","InsertedBytes": "bytes",
            "MergeTotalMilliseconds": "milliseconds",
            "NetworkReceiveElapsedMicroseconds": "microseconds",
            "NetworkSendElapsedMicroseconds": "microseconds",
            "RWLockReadersWaitMilliseconds": "milliseconds",
            "ReadCompressedBytes": "bytes",
            "Selected bytes/second": "bytes",
            "Memory (tracked)": "bytes",
            "OS CPU Usage (userspace)": "seconds", "OS CPU Usage (kernel)": "seconds",
            "IO wait": "seconds",
            "BlockReadBytes": "bytes", "BlockWriteBytes": "bytes",
            "clickhouse_rss_bytes": "bytes","DiskAvailable_default": "bytes","DiskUsed_default": "bytes",
            "DATABASES_INFO":{
                "Size":"MB"
            }
}

# ==== Metrics Tabs ====
METRICS_TABS = {
    "Database": {"order": 1, "tablist": [
        "NumberOfDatabases", "NumberOfTables", "ReplicasMaxQueueSize",
        "ReplicasSumInsertsInQueue", "ReplicasSumMergesInQueue",
        "ReplicasMaxRelativeDelay", "ReplicasMaxMergesInQueue",
        "ReplicasMaxInsertsInQueue", "ReplicasSumQueueSize",
        "ReplicasMaxAbsoluteDelay","DATABASES_INFO"]},
    "Memory": {"order": 2, "tablist": [
        "MemoryResident", "MemoryVirtual", "MemoryShared",
        "Memory (tracked)", "jemalloc.allocated", "jemalloc.retained",
        "jemalloc.resident", "jemalloc.background_thread.num_threads",
        "jemalloc.arenas.all.dirty_purged", "Uptime"]},
    "Events": {"order": 3, "tablist": [
        "CompressedReadBufferBlocks", "CompressedReadBufferBytes",
        "ContextLock", "DiskReadElapsedMicroseconds", "DiskWriteElapsedMicroseconds",
        "FileOpen", "ReadCompressedBytes", "Merge", "RWLockAcquiredReadLocks",
        "RWLockReadersWaitMilliseconds", "SoftPageFaults","BlockReadBytes","BlockWriteBytes"]},
    "System": {"order": 4, "tablist": [
        "ReplicatedFetch", "ReplicatedSend", "ReplicatedChecks",
        "MySQLConnection", "PostgreSQLConnection", "OpenFileForRead",
        "OpenFileForWrite", "Read", "Write", "ReadonlyReplica",
        "ZooKeeperSession", "ZooKeeperRequest", "DelayedInserts",
        "ContextLockWait", "StorageBufferRows", "RWLockWaitingReaders",
        "RWLockWaitingWriters", "OS CPU Usage (userspace)",
        "OS CPU Usage (kernel)", "IO wait",
        "clickhouse_rss_bytes","DiskAvailable_default","DiskUsed_default"]}
}

# ==== Metrics to collect ====
ASYNC_METRICS = [
    "MemoryResident", "MemoryShared", "MemoryVirtual",
    "ReplicasMaxAbsoluteDelay", "ReplicasMaxInsertsInQueue", "ReplicasMaxMergesInQueue",
    "ReplicasMaxQueueSize", "ReplicasMaxRelativeDelay", "ReplicasSumInsertsInQueue",
    "ReplicasSumMergesInQueue", "ReplicasSumQueueSize",
    "Uptime", "jemalloc.allocated", "jemalloc.arenas.all.dirty_purged",
    "jemalloc.background_thread.num_threads", "jemalloc.resident", "jemalloc.retained"
]

EVENT_METRICS = [
    "CompressedReadBufferBlocks", "CompressedReadBufferBytes", "ContextLock",
    "DiskReadElapsedMicroseconds", "DiskWriteElapsedMicroseconds", "FailedQuery",
    "FailedSelectQuery", "FileOpen", "InsertedBytes", "Merge",
    "MergeTotalMilliseconds", "NetworkReceiveElapsedMicroseconds",
    "NetworkSendElapsedMicroseconds", "Query", "RWLockAcquiredReadLocks",
    "RWLockReadersWaitMilliseconds", "ReadCompressedBytes", "SelectQuery", "SoftPageFaults"
]

SYSTEM_METRICS = [
    "ReplicatedFetch", "ReplicatedSend", "ReplicatedChecks",
    "MySQLConnection", "OpenFileForRead", "OpenFileForWrite", "PostgreSQLConnection",
    "RWLockWaitingReaders", "RWLockWaitingWriters", "Read",
    "ReadonlyReplica", "StorageBufferRows", "Write", "ZooKeeperRequest",
    "ZooKeeperSession", "ContextLockWait", "DelayedInserts",
    "CompiledExpressionCacheCount", "MarkCacheBytes", "MarkCacheFiles", "UncompressedCacheBytes"
]

# Metrics resolved from already-fetched cached dictionaries (no extra queries)
# Format: output_key -> (source: "async"|"event"|"system", metric_name)
CACHED_METRICS = {
    "Queries/second": ("system", "Query"),
    "Inserted rows": ("event", "InsertedRows"),
    "Merges running": ("system", "Merge"),
    "Selected bytes/second": ("event", "SelectedBytes"),
    "Memory (tracked)": ("system", "MemoryTracking"),
    "OS CPU Usage (userspace)": ("async", "OSUserTime"),
    "OS CPU Usage (kernel)": ("async", "OSSystemTime"),
    "IO wait": ("async", "OSIOWaitTime"),
    "clickhouse_rss_bytes": ("async", "MemoryResident"),
    "BlockReadBytes": ("event", "OSReadBytes"),
    "BlockWriteBytes": ("event", "OSWriteBytes")
}

# Queries that need actual DB calls (system.parts, system.disks)
CUSTOM_QUERIES = {
    "Total MergeTree parts": "SELECT count() FROM system.parts",
    "Max parts for partition": "SELECT max(active) FROM system.parts",
    "DiskAvailable_default": "SELECT free_space FROM system.disks WHERE name='default'",
    "DiskUsed_default": "SELECT total_space - free_space FROM system.disks WHERE name='default'"
}

# ==== Functions ====
def fetch_metric(client, query, data):
    try:
        result = client.execute(query)
        return result[0][0] if result and len(result[0]) > 0 else 0
    except Exception as e:
        if "msg" in data:
            data["msg"] += "; " + str(e)
        else:
            data["msg"] = str(e)
        return 0

# ==== Main ====
def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", default="localhost")
        parser.add_argument("--port", type=int, default=9000)
        parser.add_argument("--user", default="default")
        parser.add_argument("--password", default="default")
        args = parser.parse_args()

        data = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT_REQUIRED
        }

        client = Client(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password
        )
        try:
            data["units"]=units
            # ==== Fetch Metrics ===
            # Fetch all metric data at once
            async_metrics_data = dict(client.execute("SELECT metric, value FROM system.asynchronous_metrics"))
            event_metrics_data = dict(client.execute("SELECT event, value FROM system.events"))
            system_metrics_data = dict(client.execute("SELECT metric, value FROM system.metrics"))

            # Fill ASYNC_METRICS using cached dictionary
            for metric in ASYNC_METRICS:
                data[metric] = async_metrics_data.get(metric, 0)

            # Fill EVENT_METRICS using cached dictionary
            for metric in EVENT_METRICS:
                data[metric] = event_metrics_data.get(metric, 0)

            # Number of databases and tables
            data["NumberOfDatabases"] = fetch_metric(client, "SELECT count() FROM system.databases", data)
            data["NumberOfTables"] = fetch_metric(client, "SELECT count() FROM system.tables", data)
            # Fill SYSTEM_METRICS using cached dictionary
            for metric in SYSTEM_METRICS:
                data[metric] = system_metrics_data.get(metric, 0)


            # Fill CACHED_METRICS from already-fetched dictionaries (no extra queries)
            source_map = {"async": async_metrics_data, "event": event_metrics_data, "system": system_metrics_data}
            for key, (source, metric_name) in CACHED_METRICS.items():
                data[key] = source_map[source].get(metric_name, 0)

            # Run only queries that need actual DB calls
            for key, query in CUSTOM_QUERIES.items():
                data[key] = fetch_metric(client, query, data)

            # ==== DATABASES_INFO ====
            try:
                db_table_counts = client.execute("""
                    SELECT 
                        d.name,
                        d.engine,
                        count(DISTINCT nullIf(t.name, '')) AS table_count,
                        coalesce(ps.total_size_bytes, 0) AS total_size_bytes,
                        coalesce(ps.total_rows, 0) AS total_rows
                    FROM system.databases d
                    LEFT JOIN system.tables t ON d.name = t.database
                    LEFT JOIN (
                        SELECT database, sum(bytes_on_disk) AS total_size_bytes, sum(rows) AS total_rows
                        FROM system.parts
                        WHERE active = 1
                        GROUP BY database
                    ) ps ON d.name = ps.database
                    GROUP BY d.name, d.engine, ps.total_size_bytes, ps.total_rows
                    ORDER BY d.name
                """)
                data["DATABASES_INFO"] = [
                    {
                        "name": db,
                        "Engine": engine,
                        "Table_Count": table_count,
                        "Size": round(size_bytes / (1024 * 1024), 4) if size_bytes else 0,
                        "Total_Rows": total_rows
                    }
                    for db, engine, table_count, size_bytes, total_rows in db_table_counts
                ]
            except Exception as e:
                if "msg" in data:
                    data["msg"] += "; " + str(e)
                else:
                    data["msg"] = str(e)
                data["DATABASES_INFO"] = [{"name": "-", "Engine": "-", "Table_Count": -1, "Size": -1, "Total_Rows": -1}]

            
            data["tabs"] = METRICS_TABS

            print(json.dumps(data, indent=4))
        finally:
            client.disconnect()

    except Exception as e:
        print(json.dumps({
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT_REQUIRED,
            "status": 0,
            "msg": f"Error: {str(e)}"
        }, indent=4))

if __name__ == "__main__":
    main()
