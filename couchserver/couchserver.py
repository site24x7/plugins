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
    'hdd.total': 'MB',
    'hdd.quotaTotal': 'MB',
    'hdd.used': 'MB',
    'hdd.usedByData': 'MB',
    'ram.total': 'MB',
    'ram.used': 'MB',
    'ram.quotaUsed': 'MB',
    'ram.quotaUsedPerNode': 'MB',
    'ram.quotaTotalPerNode': 'MB'
}

# -------------------------
# Helper to convert Bytes to MB
# -------------------------
def bytes_to_mb(value):
    try:
        return round(float(value)/1024/1024,2)
    except:
        return 0

# -------------------------
# Couchbase Metrics
# -------------------------
def collect_couchbase(host, port, user, password):
    data = {}
    url = f"http://{host}:{port}/pools/default"
    try:
        r = requests.get(url, auth=(user,password), timeout=10)
        pool = r.json()
        storage = pool.get('storageTotals',{})
        hdd = storage.get('hdd',{})
        ram = storage.get('ram',{})
        data['hdd.total'] = bytes_to_mb(hdd.get('total',0))
        data['hdd.quotaTotal'] = bytes_to_mb(hdd.get('quotaTotal',0))
        data['hdd.used'] = bytes_to_mb(hdd.get('used',0))
        data['hdd.usedByData'] = bytes_to_mb(hdd.get('usedByData',0))
        data['ram.total'] = bytes_to_mb(ram.get('total',0))
        data['ram.used'] = bytes_to_mb(ram.get('used',0))
        data['ram.quotaUsed'] = bytes_to_mb(ram.get('quotaUsed',0))
        data['ram.quotaUsedPerNode'] = bytes_to_mb(ram.get('quotaUsedPerNode',0))
        data['ram.quotaTotalPerNode'] = bytes_to_mb(ram.get('quotaTotalPerNode',0))
    except Exception as e:
        data['msg'] = f"Couchbase Error: {str(e)}"
    return data

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--couchbase_host", default="127.0.0.1")
    parser.add_argument("--couchbase_port", default="8091")
    parser.add_argument("--couchbase_user", default="admin")
    parser.add_argument("--couchbase_pass", default="password")
    args = parser.parse_args()

    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "units": UNITS
    }

    # Couchbase metrics
    output.update(collect_couchbase(args.couchbase_host, args.couchbase_port, args.couchbase_user, args.couchbase_pass))

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
