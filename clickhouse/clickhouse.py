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
            "MergesTimeMilliseconds": "milliseconds",
            "NetworkReceiveElapsedMicroseconds": "microseconds",
            "NetworkSendElapsedMicroseconds": "microseconds",
            "RWLockReadersWaitMilliseconds": "milliseconds",
            "ReadCompressedBytes": "bytes",
            "Selected bytes/second": "bytes",
            "Memory (tracked)": "bytes",
            "OS CPU Usage (userspace)": "seconds", "OS CPU Usage (kernel)": "seconds",
            "CPU usage (cores)": "%", "IO wait": "seconds", "CPU wait": "seconds",
            "Read from disk": "bytes",
            "clickhouse_rss_bytes": "bytes","DiskAvailable_default": "bytes","DiskUsed_default": "bytes",
            "TABLE_INFO": {"Table_Size_MB": "mb", "Used_Percent": "%"}
}

# ==== Metrics Tabs ====
METRICS_TABS = {
    "Database": {"order": 1, "tablist": [
        "NumberOfDatabases", "NumberOfTables", "ReplicasMaxQueueSize",
        "ReplicasSumInsertsInQueue", "ReplicasSumMergesInQueue",
        "ReplicasMaxRelativeDelay", "ReplicasMaxMergesInQueue",
        "ReplicasMaxInsertsInQueue", "ReplicasSumQueueSize",
        "ReplicasMaxAbsoluteDelay","TABLE_INFO","DATABASES_INFO"]},
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
        "OS CPU Usage (kernel)", "CPU usage (cores)", "IO wait",
        "CPU wait", "Read from disk", "Read from filesystem", "clickhouse_rss_bytes","DiskAvailable_default","DiskUsed_default"]}
}

# ==== Metrics to collect ====
ASYNC_METRICS = [
    "CompiledExpressionCacheCount", "MarkCacheBytes", "MarkCacheFiles",
    "MemoryResident", "MemoryShared", "MemoryVirtual",
    "ReplicasMaxAbsoluteDelay", "ReplicasMaxInsertsInQueue", "ReplicasMaxMergesInQueue",
    "ReplicasMaxQueueSize", "ReplicasMaxRelativeDelay", "ReplicasSumInsertsInQueue",
    "ReplicasSumMergesInQueue", "ReplicasSumQueueSize", "UncompressedCacheBytes",
    "Uptime", "jemalloc.allocated", "jemalloc.arenas.all.dirty_purged",
    "jemalloc.background_thread.num_threads", "jemalloc.resident", "jemalloc.retained"
]

EVENT_METRICS = [
    "CompressedReadBufferBlocks", "CompressedReadBufferBytes", "ContextLock",
    "DiskReadElapsedMicroseconds", "DiskWriteElapsedMicroseconds", "FailedQuery",
    "FailedSelectQuery", "FileOpen", "InsertedBytes", "Merge",
    "MergesTimeMilliseconds", "NetworkReceiveElapsedMicroseconds",
    "NetworkSendElapsedMicroseconds", "Query", "RWLockAcquiredReadLocks",
    "RWLockReadersWaitMilliseconds", "ReadCompressedBytes", "SelectQuery", "SoftPageFaults","BlockReadBytes","BlockWriteBytes"
]

SYSTEM_METRICS = [
    "ReplicatedFetch", "ReplicatedSend", "ReplicatedChecks",
    "MySQLConnection", "OpenFileForRead", "OpenFileForWrite", "PostgreSQLConnection",
    "Query", "RWLockWaitingReaders", "RWLockWaitingWriters", "Read",
    "ReadonlyReplica", "StorageBufferRows", "Write", "ZooKeeperRequest",
    "ZooKeeperSession", "ContextLockWait", "DelayedInserts",
    "OS CPU Usage (userspace)", "OS CPU Usage (kernel)", "CPU usage (cores)",
    "IO wait", "CPU wait", "Read from disk", "Read from filesystem", "clickhouse_rss_bytes","DiskAvailable_default","DiskUsed_default"
]

CUSTOM_QUERIES = {
    "Queries/second": "SELECT value FROM system.metrics WHERE metric='Query'",
    "Queries running": "SELECT value FROM system.metrics WHERE metric='QueryActive'",
    "Inserted rows": "SELECT value FROM system.events WHERE event='InsertedRows'",
    "Merges running": "SELECT value FROM system.metrics WHERE metric='Merge'",
    "Selected bytes/second": "SELECT value FROM system.events WHERE event='SelectedBytes'",
    "Total MergeTree parts": "SELECT count() FROM system.parts",
    "Max parts for partition": "SELECT max(active) FROM system.parts",
    "Memory (tracked)": "SELECT value FROM system.metrics WHERE metric='MemoryTracking'",
    "OS CPU Usage (userspace)": "SELECT value FROM system.metrics WHERE metric='OSUserTime'",
    "OS CPU Usage (kernel)": "SELECT value FROM system.metrics WHERE metric='OSSystemTime'",
    "CPU usage (cores)": "SELECT value FROM system.metrics WHERE metric='CPUUsage'",
    "IO wait": "SELECT value FROM system.metrics WHERE metric='IOWaitTime'",
    "CPU wait": "SELECT value FROM system.metrics WHERE metric='WaitThreads'",
    "Read from disk": "SELECT value FROM system.events WHERE event='DiskReadBytes'",
    "Read from filesystem": "SELECT value FROM system.events WHERE event='FileOpen'",
    "clickhouse_rss_bytes": "SELECT value FROM system.metrics WHERE metric='RSS'",
    "DiskAvailable_default": "SELECT free_space FROM system.disks WHERE name='default'",
    "DiskUsed_default": "SELECT total_space - free_space FROM system.disks WHERE name='default'",
    "BlockReadBytes": "SELECT sum(value) FROM system.events WHERE event='ReadBytes'",
    "BlockWriteBytes": "SELECT sum(value) FROM system.events WHERE event='WrittenBytes'"
}

# ==== Functions ====
def fetch_metric(client, query):
    try:
        result = client.execute(query)
        return result[0][0] if result and len(result[0]) > 0 else 0
    except:
        return 0

# ==== Main ====
def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", default="localhost")
        parser.add_argument("--port", type=int, default=9000)
        parser.add_argument("--user", default="default")
        parser.add_argument("--password", default="default")
        parser.add_argument("--database", default="CUSTOM")
        args = parser.parse_args()

        data = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT_REQUIRED
        }

        client = Client(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            database=args.database,
            connect_timeout=10
        )
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
        data["NumberOfDatabases"] = fetch_metric(client, "SELECT count() FROM system.databases")
        data["NumberOfTables"] = fetch_metric(client, f"SELECT count() FROM system.tables WHERE database='{args.database}'")
        data["DiskAvailable_default"] = fetch_metric(client, "SELECT free_space FROM system.disks WHERE name='default'")
        data["DiskUsed_default"] = fetch_metric(client, "SELECT total_space - free_space FROM system.disks WHERE name='default'")
        data["BlockReadBytes"] = fetch_metric(client, "SELECT sum(read_bytes) FROM system.parts")
        data["BlockWriteBytes"] = fetch_metric(client, "SELECT sum(bytes_on_disk) FROM system.parts")
        # Fill SYSTEM_METRICS using cached dictionary
        for metric in SYSTEM_METRICS:
            data[metric] = system_metrics_data.get(metric, 0)


        for key, query in CUSTOM_QUERIES.items():
            data[key] = fetch_metric(client, query)

        # ==== DATABASES_INFO ====
        db_table_counts = client.execute("""
            SELECT d.name, count(t.name) AS table_count
            FROM system.databases d
            LEFT JOIN system.tables t ON d.name = t.database
            GROUP BY d.name
            ORDER BY d.name
        """)
        data["DATABASES_INFO"] = [{"name": db, "Table_Count": table_count} for db, table_count in db_table_counts]

        # ==== TABLE_INFO ====
        table_info = []
        tables = client.execute(f"SELECT name FROM system.tables WHERE database='{args.database}'")
        total_db_size = 0
        table_sizes = {}
        for table in tables:
            table_name = table[0]
            size_bytes = fetch_metric(client, f"SELECT sum(bytes_on_disk) FROM system.parts WHERE database='{args.database}' AND table='{table_name}' AND active=1")
            table_sizes[table_name] = size_bytes
            total_db_size += size_bytes

        for table in tables:
            table_name = table[0]
            row_count = fetch_metric(client, f"SELECT count() FROM {args.database}.{table_name}")
            column_count = fetch_metric(client, f"SELECT count() FROM system.columns WHERE database='{args.database}' AND table='{table_name}'")
            table_size_mb = round(table_sizes[table_name] / (1024*1024), 4) if table_sizes[table_name] else 0
            used_percent = round((table_sizes[table_name]/total_db_size)*100,2) if total_db_size>0 else 0

            table_info.append({
                "name": table_name,
                "Row_Count": row_count,
                "Column_Count": column_count,
                "Table_Size_MB": table_size_mb,
                "Used_Percent": used_percent
            })

        data["TABLE_INFO"] = table_info
        data["CUSTOM_Table_Count"] = len(table_info)
        data["tabs"] = METRICS_TABS

        print(json.dumps(data, indent=4))

    except Exception as e:
        # Only print the error message
        print(json.dumps({
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT_REQUIRED,
            "msg": f"Error: {str(e)}"
        }, indent=4))

if __name__ == "__main__":
    main()
