#!/usr/bin/python3

import json
import requests
import argparse

PLUGIN_VERSION = 1
HEARTBEAT = "true"

# -------------------------
# Metric Units
# -------------------------
UNITS = {
    "Total HDD": "MB",
    "Quota Total HDD": "MB",
    "Used HDD": "MB",
    "Used by Data HDD": "%",
    "Total Ram": "MB",
    "Used Ram": "MB",
    "Quota Used Ram": "MB",
    "Quota Used Ram Node": "MB",
    "Quota Total Ram Node": "MB",
    "Bucket Ops": "ops/sec",
    "Hit Ratio": "%",
    "Cache Miss Rate": "%",
    "Data Disk Size": "MB",
    "Actual Disk Size": "MB",
    "Doc Fragmentation": "%",
    "Bucket Mem Used": "MB",
    "Mem High Water": "%",
    "Mem Low Water": "%",
    "Mem Overhead": "MB",
    "Key Value Size": "MB",
    "Node Mem Used": "MB",
    "Mem Actual Used": "MB",
    "Mem Actual Free": "MB",
    "Index Disk Size": "MB",
    "Index Ram Used": "MB",
    "Index Fragmentation": "%",
    "Query Elapsed Time": "ms",
    "Query Execution Time": "ms",
    "Query Result Size": "bytes",
    "Xdcr Ops": "ops/sec",
    "Xdcr Meta Latency": "ms",
    "Virtual Bucket Active Resident Items Ratio": "%",
    "Ops Queued": "ops/sec",
    "Cmd Get": "ops/sec",
    "Get Hits": "ops/sec",
    "Ep Bg Fetched": "items/sec",
    "Mem Used": "MB",
    "Mem Actual Free": "MB",
    "Mem Actual Used": "MB",
    "Cache Hits": "ops/sec",
    "Cache Misses": "ops/sec",
    "Disk Write Queue": "ops/sec",
    "Disk Read Queue": "ops/sec"
}

# -------------------------
# Tabs
# -------------------------
TABS = {
    "Bucket": {
        "order": 0,
        "tablist": [
            "Bucket_Table","Bucket Ops","Get Hits","Get Misses","Hit Ratio","Evictions","Cache Miss Rate",
            "Create Ops","Update Ops","Bg Fetches","Data Disk Size","Actual Disk Size",
            "Doc Fragmentation","Write Queue","Bucket Mem Used"
        ]
    },
    "Memory": {
        "order": 1,
        "tablist": [
            "Mem High Water","Mem Low Water","Mem Overhead","Key Value Size","Node Cmd Get","Node Get Hits",
            "Node Items","Node Items Total","Node Bg Fetches","Node Mem Used",
            "Mem Actual Used","Mem Actual Free","Page Faults","Virtual Bucket Active Resident Items Ratio"
        ]
    },
    "Index": {
        "order": 2,
        "tablist": [
            "Index Docs Pending","Index Docs Queued","Index Docs Failed","Index Docs Indexed",
            "Index Disk Size","Index Ram Used","Index Fragmentation"
        ]
    },
    "Query": {
        "order": 3,
        "tablist": [
            "Query Elapsed Time","Query Execution Time","Query Result Count","Query Result Size","Query Service Load",
            "Xdcr Ops","Xdcr Docs Queue","Xdcr Meta Latency",
            "Dcp Replica Items","Dcp Xdcr Items","Dcp View Items"
        ]
    }
}

# -------------------------
# Helper Functions
# -------------------------
def bytes_to_mb(value):
    try:
        return round(float(value) / 1024 / 1024, 2)
    except:
        return 0

def safe_get(d, key):
    if d and key in d:
        return d[key]
    return None

def fetch_query_metrics(host, port, user, password, bucket):
    query_port=8093
    url = f"http://{host}:{query_port}/query/service"
    query = f'SELECT COUNT(*) FROM `{bucket}`;'
    payload = {"statement": query}
    metrics = {}
    try:
        r = requests.post(url, auth=(user, password), json=payload, timeout=10)
        r.raise_for_status()
        resp = r.json()
        m = resp.get("metrics", {})
        # Convert elapsedTime, executionTime strings (like '12.5ms') to float ms
        def to_ms(t):
            try:
                if isinstance(t, str) and t.endswith("ms"):
                    return float(t[:-2])
                return float(t)
            except:
                return 0
        metrics['Query Elapsed Time'] = to_ms(m.get("elapsedTime"))
        metrics['Query Execution Time'] = to_ms(m.get("executionTime"))
        metrics['Query Result Count'] = m.get("resultCount", 0)
        metrics['Query Result Size'] = m.get("resultSize", 0)
        metrics['Query Service Load'] = m.get("serviceLoad", 0)
    except Exception as e:
        metrics['msg'] = f"Query metrics error for bucket {bucket}: {str(e)}"
    return metrics

# -------------------------
# Main collection function
# -------------------------
def collect_couchbase(host, port, user, password):
    data = {}
    try:
        base_url = f"http://{host}:{port}/pools/default"
        r = requests.get(base_url, auth=(user, password), timeout=10)
        stats = r.json()

        # -------- Bucket Metrics --------
        bucket_names = stats.get('bucketNames', [])
        bucket_table = []

        for bucket_info in bucket_names:
            bucket_name = bucket_info.get('bucketName')
            if bucket_name:
                bucket_url = f"{base_url}/buckets/{bucket_name}"
                r_bucket = requests.get(bucket_url, auth=(user,password), timeout=10)
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

                    # -------- Added for Bucket Table --------
                    bucket_table.append({
                        "name": bucket_name,
                        "Item_Count": basic.get('itemCount', 0),
                        "Ops_Per_Sec": basic.get('opsPerSec', 0)
                    })

                # -------- Query Metrics (bucket specific) --------
                query_metrics = fetch_query_metrics(host, port, user, password, bucket_name)
                data.update(query_metrics)

        # Attach the table to data
        data["Bucket_Table"] = bucket_table  # <--- added table output

        # -------- Memory / Storage Totals --------
        storage_totals = stats.get('storageTotals', {})
        ram = storage_totals.get('ram', {})
        hdd = storage_totals.get('hdd', {})

        if ram:
            data['Total Ram'] = bytes_to_mb(ram.get('total', 0))
            data['Used Ram'] = bytes_to_mb(ram.get('used', 0))
            data['Quota Used Ram'] = bytes_to_mb(ram.get('quotaUsed', 0))
            data['Quota Used Ram Node'] = bytes_to_mb(ram.get('quotaUsedPerNode', 0))
            data['Quota Total Ram Node'] = bytes_to_mb(ram.get('quotaTotalPerNode', 0))

        if hdd:
            data['Total HDD'] = bytes_to_mb(hdd.get('total', 0))
            data['Quota Total HDD'] = bytes_to_mb(hdd.get('quotaTotal', 0))
            data['Used HDD'] = bytes_to_mb(hdd.get('used', 0))
            data['Used by Data HDD'] = bytes_to_mb(hdd.get('usedByData', 0))

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
            if index:
                data['Index Docs Pending'] = index.get('docsPending', 0)
                data['Index Docs Queued'] = index.get('docsQueued', 0)
                data['Index Docs Failed'] = index.get('docsFailed', 0)
                data['Index Docs Indexed'] = index.get('docsIndexed', 0)
                data['Index Disk Size'] = bytes_to_mb(index.get('diskSize', 0))
                data['Index Ram Used'] = bytes_to_mb(index.get('ramUsed', 0))
                data['Index Fragmentation'] = index.get('fragmentation', 0)

        # -------- XDCR / DCP Metrics --------
        xdcr = stats.get('xdcr', {})
        if xdcr:
            if 'ops' in xdcr:
                data['Xdcr Ops'] = xdcr['ops']
            if 'docsQueued' in xdcr:
                data['Xdcr Docs Queue'] = xdcr['docsQueued']
            if 'metaLatency' in xdcr:
                data['Xdcr Meta Latency'] = xdcr['metaLatency']

        dcp = stats.get('dcp', {})
        if dcp:
            if 'replicaItems' in dcp:
                data['Dcp Replica Items'] = dcp['replicaItems']
            if 'xdcrItems' in dcp:
                data['Dcp Xdcr Items'] = dcp['xdcrItems']
            if 'viewItems' in dcp:
                data['Dcp View Items'] = dcp['viewItems']

    except Exception as e:
        data['msg'] = f"Couchbase Error: {str(e)}"
    return data

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="8091")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="password")
    args = parser.parse_args()

    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "units": UNITS
    }

    # Couchbase metrics
    output.update(collect_couchbase(args.host, args.port, args.user, args.password))

    # Tabs at the end
    output["tabs"] = TABS

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
