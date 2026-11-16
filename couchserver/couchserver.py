#!/usr/bin/python3
# ==============================================================================
# Couchbase Server Monitoring Plugin - Optimized for High-Scale Deployments
# ==============================================================================

import json
import requests
import argparse
import sys

PLUGIN_VERSION = 2
HEARTBEAT = "true"

# ----------------------------------------------------------------------
# Config Section
# ----------------------------------------------------------------------
COUCHBASE_SERVER_HOST = '127.0.0.1'
COUCHBASE_SERVER_PORT = "8091"
COUCHBASE_SERVER_QUERY_PORT = "8093"
COUCHBASE_SERVER_STATS_URI = "pools/default"
COUCHBASE_SERVER_USERNAME = None
COUCHBASE_SERVER_PASSWORD = None
DEFAULT_TIMEOUT = 10

# High-Load Safeguards:
ENABLE_QUERY_METRICS = False    # Set to True to collect query engine metrics
MAX_BUCKETS_TO_POLL = 20        # Cap HTTP requests on large multi-bucket clusters

# ----------------------------------------------------------------------
# Metric Units
# ----------------------------------------------------------------------
UNITS = {
    # Storage Totals
    "hdd.total": "MB",
    "hdd.quotaTotal": "MB",
    "hdd.used": "MB",
    "hdd.usedByData": "MB",      # Corrected from % to MB
    "ram.total": "MB",
    "ram.used": "MB",
    "ram.quotaUsed": "MB",
    "ram.quotaUsedPerNode": "MB",
    "ram.quotaTotalPerNode": "MB",

    # Bucket Metrics
    "Bucket Ops": "ops/sec",
    "Hit Ratio": "%",
    "Cache Miss Rate": "%",
    "Data Disk Size": "MB",
    "Actual Disk Size": "MB",
    "Doc Fragmentation": "%",
    "Bucket Mem Used": "MB",
    "Write Queue": "ops/sec",
    "Get Hits": "ops/sec",
    "Get Misses": "ops/sec",
    "Evictions": "ops/sec",
    "Create Ops": "ops/sec",
    "Update Ops": "ops/sec",
    "Bg Fetches": "items/sec",

    # Memory & Node Metrics
    "Mem High Water": "%",
    "Mem Low Water": "%",
    "Mem Overhead": "MB",
    "Key Value Size": "MB",
    "Node Mem Used": "MB",
    "Mem Actual Used": "MB",
    "Mem Actual Free": "MB",
    "Virtual Bucket Active Resident Items Ratio": "%",
    "Ops Queued": "ops/sec",
    "Cmd Get": "ops/sec",
    "Node Cmd Get": "ops/sec",
    "Node Get Hits": "ops/sec",
    "Node Bg Fetches": "items/sec",
    "Page Faults": "count",

    # Index Metrics
    "Index Disk Size": "MB",
    "Index Ram Used": "MB",
    "Index Fragmentation": "%",
    "Index Docs Pending": "count",
    "Index Docs Queued": "count",
    "Index Docs Failed": "count",
    "Index Docs Indexed": "count",

    # Query Engine Vitals (Zero-load metrics)
    "Query Elapsed Time": "ms",
    "Query Active Requests": "count",
    "Query Completed Requests": "count",
    "Query Request Rate 1m": "req/sec",
    "Query Service CPU Sys": "%",
    "Query Service CPU User": "%",

    # Replication (XDCR / DCP)
    "Xdcr Ops": "ops/sec",
    "Xdcr Meta Latency": "ms",
    "Xdcr Docs Queue": "count",
    "Dcp Replica Items": "count",
    "Dcp Xdcr Items": "count",
    "Dcp View Items": "count",

    # Tabular Metadata
    "Bucket_Table": {
        "Item_Count": "count",
        "Ops_Per_Sec": "ops/sec"
    }
}

# -------------------------
# Tabs
# -------------------------
TABS = {
    "Bucket": {
        "order": 1,
        "tablist": [
            "Bucket_Table", "Bucket Ops", "Get Hits", "Get Misses", "Hit Ratio", "Evictions",
            "Cache Miss Rate", "Create Ops", "Update Ops", "Bg Fetches", "Data Disk Size",
            "Actual Disk Size", "Doc Fragmentation", "Write Queue", "Bucket Mem Used"
        ]
    },
    "Memory": {
        "order": 2,
        "tablist": [
            "Mem High Water", "Mem Low Water", "Mem Overhead", "Key Value Size", "Node Cmd Get",
            "Node Get Hits", "Node Items", "Node Items Total", "Node Bg Fetches", "Node Mem Used",
            "Mem Actual Used", "Mem Actual Free", "Page Faults",
            "Virtual Bucket Active Resident Items Ratio"
        ]
    },
    "Index": {
        "order": 3,
        "tablist": [
            "Index Docs Pending", "Index Docs Queued", "Index Docs Failed", "Index Docs Indexed",
            "Index Disk Size", "Index Ram Used", "Index Fragmentation"
        ]
    },
    "Query": {
        "order": 4,
        "tablist": [
            "Query Elapsed Time", "Query Active Requests", "Query Completed Requests",
            "Query Request Rate 1m", "Query Service CPU Sys", "Query Service CPU User",
            "Xdcr Ops", "Xdcr Docs Queue", "Xdcr Meta Latency",
            "Dcp Replica Items", "Dcp Xdcr Items", "Dcp View Items"
        ]
    }
}

# -------------------------
# Helper Functions
# -------------------------
def bytes_to_mb(value):
    try:
        return round(float(value) / 1024 / 1024, 2)
    except Exception:
        return 0

def fetch_query_vitals(host, query_port, user, password):
    """
    Zero-load query metrics collector using Couchbase's native /admin/vitals endpoint.
    Avoids running synthetic SQL/N1QL statements across buckets.
    """
    metrics = {}
    url = f"http://{host}:{query_port}/admin/vitals"
    auth = (user, password) if user and password else None

    def to_ms(t):
        try:
            if isinstance(t, str):
                t = t.strip()
                factors = [("ms", 1), ("µs", 0.001), ("μs", 0.001), ("us", 0.001),
                           ("ns", 0.000001), ("s", 1000), ("m", 60000), ("h", 3600000)]
                for suffix, factor in factors:
                    if t.endswith(suffix):
                        return round(float(t[:-len(suffix)]) * factor, 2)
            return round(float(t), 2)
        except Exception:
            return 0

    try:
        r = requests.get(url, auth=auth, timeout=DEFAULT_TIMEOUT)
        if r.status_code == 200:
            vitals = r.json()
            metrics['Query Elapsed Time'] = to_ms(vitals.get("request.time.mean", 0))
            metrics['Query Active Requests'] = vitals.get("request.active.count", 0)
            metrics['Query Completed Requests'] = vitals.get("request.completed.count", 0)
            metrics['Query Request Rate 1m'] = round(float(vitals.get("request.per.sec.1m", 0)), 2)
            metrics['Query Service CPU Sys'] = round(float(vitals.get("cpu.sys.percent", 0)), 2)
            metrics['Query Service CPU User'] = round(float(vitals.get("cpu.user.percent", 0)), 2)
    except Exception:
        # Silently pass if query service is not co-located on this node
        pass

    return metrics

# -------------------------
# Main Collection Function
# -------------------------
def collect_couchbase(host, port, user, password, query_port=COUCHBASE_SERVER_QUERY_PORT,
                      enable_query=ENABLE_QUERY_METRICS, max_buckets=MAX_BUCKETS_TO_POLL):
    data = {'status': 1}
    auth = (user, password) if user and password else None
    base_url = f"http://{host}:{port}/{COUCHBASE_SERVER_STATS_URI}"

    try:
        r = requests.get(base_url, auth=auth, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        stats = r.json()

        # -------- Memory / Storage Totals --------
        storage_totals = stats.get('storageTotals', {})
        ram = storage_totals.get('ram', {})
        hdd = storage_totals.get('hdd', {})

        if ram:
            data['ram.total'] = bytes_to_mb(ram.get('total', 0))
            data['ram.used'] = bytes_to_mb(ram.get('used', 0))
            data['ram.quotaUsed'] = bytes_to_mb(ram.get('quotaUsed', 0))
            data['ram.quotaUsedPerNode'] = bytes_to_mb(ram.get('quotaUsedPerNode', 0))
            data['ram.quotaTotalPerNode'] = bytes_to_mb(ram.get('quotaTotalPerNode', 0))

        if hdd:
            data['hdd.total'] = bytes_to_mb(hdd.get('total', 0))
            data['hdd.quotaTotal'] = bytes_to_mb(hdd.get('quotaTotal', 0))
            data['hdd.used'] = bytes_to_mb(hdd.get('used', 0))
            data['hdd.usedByData'] = bytes_to_mb(hdd.get('usedByData', 0))

        # -------- Bucket Metrics (Capped to prevent timeout) --------
        bucket_names = stats.get('bucketNames', [])
        bucket_table = []

        for idx, bucket_info in enumerate(bucket_names):
            if idx >= max_buckets:
                break

            bucket_name = bucket_info.get('bucketName') if isinstance(bucket_info, dict) else str(bucket_info)
            if not bucket_name:
                continue

            bucket_url = f"http://{host}:{port}/pools/default/buckets/{bucket_name}"
            try:
                r_bucket = requests.get(bucket_url, auth=auth, timeout=DEFAULT_TIMEOUT)
                if r_bucket.status_code == 200:
                    bucket = r_bucket.json()
                    basic = bucket.get('basicStats', {})
                    if basic:
                        data['Bucket Items'] = basic.get('itemCount', 0)
                        data['Total Bucket Items'] = basic.get('itemCount', 0)
                        data['Bucket Ops'] = basic.get('opsPerSec', 0)
                        data['Get Hits'] = basic.get('get_hits', 0)
                        data['Get Misses'] = basic.get('get_misses', 0)
                        data['Hit Ratio'] = basic.get('hitRatio', 0)
                        data['Evictions'] = basic.get('evictions', 0)
                        data['Cache Miss Rate'] = basic.get('cacheMissRate', 0)
                        data['Create Ops'] = basic.get('opsCreate', 0)
                        data['Update Ops'] = basic.get('opsUpdate', 0)
                        data['Bg Fetches'] = basic.get('bgFetched', 0)
                        data['Data Disk Size'] = bytes_to_mb(basic.get('diskUsed', 0))
                        data['Actual Disk Size'] = bytes_to_mb(basic.get('diskUsed', 0))
                        data['Doc Fragmentation'] = basic.get('docFragmentation', 0)
                        data['Write Queue'] = basic.get('opsQueued', 0)
                        data['Bucket Mem Used'] = bytes_to_mb(basic.get('memUsed', 0))

                        bucket_table.append({
                            "name": bucket_name,
                            "Item_Count": basic.get('itemCount', 0),
                            "Ops_Per_Sec": basic.get('opsPerSec', 0)
                        })
            except Exception:
                continue

        data["Bucket_Table"] = bucket_table

        # -------- Query Engine Metrics (Called ONCE, Outside Loop) --------
        if enable_query:
            query_metrics = fetch_query_vitals(host, query_port, user, password)
            data.update(query_metrics)

        # -------- Node Interesting Stats --------
        nodes = stats.get('nodes', [])
        for node in nodes:
            interesting = node.get('interestingStats', {})
            if interesting:
                data['Mem High Water'] = interesting.get('mem_high_watermark', 0)
                data['Mem Low Water'] = interesting.get('mem_low_watermark', 0)
                data['Mem Overhead'] = bytes_to_mb(interesting.get('mem_overhead', 0))
                data['Key Value Size'] = bytes_to_mb(interesting.get('mem_used', 0))
                data['Node Cmd Get'] = interesting.get('cmd_get', 0)
                data['Node Get Hits'] = interesting.get('get_hits', 0)
                data['Node Items'] = interesting.get('curr_items', 0)
                data['Node Items Total'] = interesting.get('curr_items_tot', 0)
                data['Node Bg Fetches'] = interesting.get('ep_bg_fetched', 0)
                data['Node Mem Used'] = bytes_to_mb(interesting.get('mem_used', 0))
                data['Page Faults'] = interesting.get('page_faults', 0)
                data['Virtual Bucket Active Resident Items Ratio'] = interesting.get('vb_active_resident_items_ratio', 0)
                data['Cmd Get'] = interesting.get('cmd_get', 0)
                data['Curr Items'] = interesting.get('curr_items', 0)
                data['Ops Queued'] = interesting.get('ops_queued', 0)

        data['Mem Actual Used'] = bytes_to_mb(stats.get('memActualUsed', 0))
        data['Mem Actual Free'] = bytes_to_mb(stats.get('memActualFree', 0))

        # -------- Index Metrics --------
        indexes = stats.get('indexes', [])
        for index in indexes:
            if index and isinstance(index, dict):
                data['Index Docs Pending'] = index.get('docsPending', 0)
                data['Index Docs Queued'] = index.get('docsQueued', 0)
                data['Index Docs Failed'] = index.get('docsFailed', 0)
                data['Index Docs Indexed'] = index.get('docsIndexed', 0)
                data['Index Disk Size'] = bytes_to_mb(index.get('diskSize', 0))
                data['Index Ram Used'] = bytes_to_mb(index.get('ramUsed', 0))
                data['Index Fragmentation'] = index.get('fragmentation', 0)

        # -------- XDCR / DCP Replication Metrics --------
        xdcr = stats.get('xdcr', {})
        if isinstance(xdcr, dict):
            if 'ops' in xdcr:
                data['Xdcr Ops'] = xdcr['ops']
            if 'docsQueued' in xdcr:
                data['Xdcr Docs Queue'] = xdcr['docsQueued']
            if 'metaLatency' in xdcr:
                data['Xdcr Meta Latency'] = xdcr['metaLatency']

        dcp = stats.get('dcp', {})
        if isinstance(dcp, dict):
            if 'replicaItems' in dcp:
                data['Dcp Replica Items'] = dcp['replicaItems']
            if 'xdcrItems' in dcp:
                data['Dcp Xdcr Items'] = dcp['xdcrItems']
            if 'viewItems' in dcp:
                data['Dcp View Items'] = dcp['viewItems']

    except Exception as e:
        data['status'] = 0
        data['msg'] = f"Couchbase Error: {str(e)}"

    return data

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Site24x7 Couchbase Monitoring Plugin")
    parser.add_argument("--host", default=COUCHBASE_SERVER_HOST, help="Couchbase host")
    parser.add_argument("--port", default=COUCHBASE_SERVER_PORT, help="Couchbase management port")
    parser.add_argument("--query-port", default=COUCHBASE_SERVER_QUERY_PORT, help="Couchbase N1QL query port")
    parser.add_argument("--user", "--username", dest="user", default=COUCHBASE_SERVER_USERNAME, help="Admin username")
    parser.add_argument("--password", "--pass", dest="password", default=COUCHBASE_SERVER_PASSWORD, help="Admin password")
    parser.add_argument("--enable-query-metrics", action="store_true", default=ENABLE_QUERY_METRICS,
                        help="Collect lightweight query engine vitals (default: False)")
    parser.add_argument("--max-buckets", type=int, default=MAX_BUCKETS_TO_POLL,
                        help="Maximum number of buckets to poll (default: 20)")
    args, unknown = parser.parse_known_args()

    # Clean quotes if passed via CLI or configuration wrapper
    host = args.host.strip('"\'') if args.host else COUCHBASE_SERVER_HOST
    port = args.port.strip('"\'') if args.port else COUCHBASE_SERVER_PORT
    query_port = args.query_port.strip('"\'') if args.query_port else COUCHBASE_SERVER_QUERY_PORT
    user = args.user.strip('"\'') if args.user else COUCHBASE_SERVER_USERNAME
    password = args.password.strip('"\'') if args.password else COUCHBASE_SERVER_PASSWORD

    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "units": UNITS
    }

    # Collect Couchbase metrics
    output.update(collect_couchbase(
        host=host,
        port=port,
        user=user,
        password=password,
        query_port=query_port,
        enable_query=args.enable_query_metrics,
        max_buckets=args.max_buckets
    ))

    # Tabs at the end
    output["tabs"] = TABS

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
