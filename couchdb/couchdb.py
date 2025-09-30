#!/usr/bin/python3

import json
import requests
import argparse

PLUGIN_VERSION = 2
HEARTBEAT = "true"

# -------------------------
# Metric Units
# -------------------------
UNITS = {
    'request_time': 'ms',
    'couchdb.couchdb.request_time.arithmetic_mean': 'ms',
    'couchdb.couchdb.request_time.geometric_mean': 'ms',
    'couchdb.couchdb.request_time.harmonic_mean': 'ms',
    'couchdb.couchdb.request_time.max': 'ms',
    'couchdb.couchdb.request_time.median': 'ms',
    'couchdb.couchdb.request_time.min': 'ms',
    'couchdb.couchdb.request_time.percentile.50': 'ms',
    'couchdb.couchdb.request_time.percentile.75': 'ms',
    'couchdb.couchdb.request_time.percentile.90': 'ms',
    'couchdb.couchdb.request_time.percentile.95': 'ms',
    'couchdb.couchdb.request_time.percentile.99': 'ms',
    'couchdb.couchdb.request_time.percentile.999': 'ms'
}

# -------------------------
# Tabs
# -------------------------
TABS = {
    "Database": {
        "order": 1,
        "tablist": [
            'auth_cache_hits',
            'auth_cache_misses',
            'couchdb.couchdb.local_document_writes',
            'couchdb.couchdb.document_purges.total',
            'couchdb.couchdb.document_purges.success',
            'couchdb.couchdb.document_purges.failure',
            'couchdb.couchdb.dbinfo.n',
            'couchdb.couchdb.dbinfo.max',
            'couchdb.couchdb.dbinfo.min',
            'couchdb.couchdb.dbinfo.median',
            'couchdb.active_tasks.db_compaction.count',
            'couchdb.active_tasks.indexer.count',
            'couchdb.active_tasks.view_compaction.count',
            'Databases_Details'
        ]
    },
    "HTTP": {
        "order": 2,
        "tablist": [
            'no_of_http_post_requests',
            'no_of_http_copy_requests',
            'no_of_http_get_requests',
            'no_of_http_head_requests',
            'no_of_http_move_requests',
            'no_of_http_put_requests',
            'no_of_http_200_responses',
            'no_of_http_201_responses',
            'no_of_http_202_responses',
            'no_of_http_301_responses',
            'no_of_http_304_responses',
            'no_of_http_400_responses',
            'no_of_http_401_responses',
            'no_of_http_403_responses',
            'no_of_http_404_responses',
            'no_of_http_405_responses',
            'no_of_http_409_responses',
            'no_of_http_412_responses',
            'no_of_http_500_responses',
            'view_reads',
            'bulk_requests',
            'temporary_view_reads',
            'clients_requesting_changes'
        ]
    },
    "Performance": {
        "order": 3,
        "tablist": [
            'couchdb.couchdb.request_time.min',
            'couchdb.couchdb.request_time.max',
            'couchdb.couchdb.request_time.arithmetic_mean',
            'couchdb.couchdb.request_time.geometric_mean',
            'couchdb.couchdb.request_time.harmonic_mean',
            'couchdb.couchdb.request_time.median',
            'couchdb.couchdb.request_time.variance',
            'couchdb.couchdb.request_time.standard_deviation',
            'couchdb.couchdb.request_time.skewness',
            'couchdb.couchdb.request_time.kurtosis',
            'couchdb.couchdb.request_time.percentile.50',
            'couchdb.couchdb.request_time.percentile.75',
            'couchdb.couchdb.request_time.percentile.90',
            'couchdb.couchdb.request_time.percentile.95',
            'couchdb.couchdb.request_time.percentile.99',
            'couchdb.couchdb.request_time.percentile.999'
        ]
    }
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
# CouchDB Database Details (dynamic)
# -------------------------
def get_databases_details(host, port, user, password, data):
    databases_details = []
    try:
        r = requests.get(f"http://{host}:{port}/_all_dbs", auth=(user,password), timeout=10)
        db_list = r.json()  # List of database names
        for db_name in db_list:
            r_db = requests.get(f"http://{host}:{port}/{db_name}", auth=(user,password), timeout=10)
            db_info = r_db.json()
            databases_details.append({
                "name": db_name,
                "doc_count": db_info.get("doc_count", 0),
                "disk_size": round(db_info.get("disk_size", 0)/1024/1024,2),
                "doc_del_count": db_info.get("doc_del_count", 0)
            })
    except Exception as e:
        data['msg'] = f"CouchDB Error fetching DB info: {str(e)}"
    return databases_details

# -------------------------
# CouchDB Metrics
# -------------------------
def collect_couchdb(host, port, user, password):
    data = {}
    url = f"http://{host}:{port}/_node/_local/_stats"
    try:
        r = requests.get(url, auth=(user,password), timeout=10)
        stats = r.json().get('couchdb', {})

        # Basic metrics
        for key in ['request_time','auth_cache_hits','auth_cache_misses','database_reads','database_writes',
                    'open_databases','open_os_files']:
            val = stats.get(key,{}).get('value',0)
            if key == 'request_time' and isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    if sub_key == "percentile" and isinstance(sub_val, list):
                        for item in sub_val:
                            pct, pct_val = item
                            data[f"couchdb.couchdb.request_time.percentile.{pct}"] = pct_val
                    elif sub_key == "histogram" and isinstance(sub_val, list):
                        for idx, item in enumerate(sub_val):
                            if isinstance(item, list) and len(item) == 2:
                                data[f"couchdb.couchdb.request_time.histogram.{idx}_bucket"] = item[0]
                                data[f"couchdb.couchdb.request_time.histogram.{idx}_count"] = item[1]
                    else:
                        data[f"couchdb.couchdb.request_time.{sub_key}"] = sub_val
            data[key] = val if key != 'request_time' else data.get(f"couchdb.couchdb.request_time.arithmetic_mean", val)

        # HTTP methods
        methods = stats.get('httpd_request_methods',{})
        for m in ['POST','COPY','GET','HEAD','MOVE','PUT']:
            data[f'no_of_http_{m.lower()}_requests'] = methods.get(m,{}).get('value',0)

        # HTTP status codes
        status = stats.get('httpd_status_codes',{})
        for s in ['200','201','202','301','304','400','401','403','404','405','409','412','500']:
            data[f'no_of_http_{s}_responses'] = status.get(s,{}).get('value',0)

        # HTTP other metrics
        httpd = stats.get('httpd',{})
        for key in ['view_reads','bulk_requests','temporary_view_reads','clients_requesting_changes']:
            data[key] = httpd.get(key,{}).get('value',0)

        # Active tasks & logs
        tasks = stats.get('active_tasks',{})
        data['couchdb.active_tasks.db_compaction.count'] = tasks.get('db_compaction',{}).get('count',0)
        data['couchdb.active_tasks.indexer.count'] = tasks.get('indexer',{}).get('count',0)
        data['couchdb.active_tasks.view_compaction.count'] = tasks.get('view_compaction',{}).get('count',0)

        couch_log = stats.get('couch_log',{})
        for level in ['alert','critical','error','warning','info']:
            data[f'couchdb.couch_log.level.{level}'] = couch_log.get('level',{}).get(level,0)

        data['couchdb.couchdb.open_databases'] = stats.get('couchdb',{}).get('open_databases',{}).get('value',0)
        data['couchdb.couchdb.open_os_files'] = stats.get('couchdb',{}).get('open_os_files',{}).get('value',0)

        # Document & DB info
        couchdb_main = stats.get('couchdb', {})
        for key in ['document_inserts','document_writes','local_document_writes']:
            data[f'couchdb.couchdb.{key}'] = couchdb_main.get(key,{}).get('value',0)

        for key in ['document_purges']:
            for sub_key in ['total','success','failure']:
                data[f'couchdb.couchdb.{key}.{sub_key}'] = couchdb_main.get(key,{}).get(sub_key,0)

        dbinfo = couchdb_main.get('dbinfo', {})
        for sub_key in ['n','max','min','median']:
            data[f'couchdb.couchdb.dbinfo.{sub_key}'] = dbinfo.get(sub_key,0)

        # Add dynamic database info
        data['Databases_Details'] = get_databases_details(host, port, user, password, data)

    except Exception as e:
        data['msg'] = f"CouchDB Error: {str(e)}"
    return data

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--couchdb_host", default="127.0.0.1")
    parser.add_argument("--couchdb_port", default="5984")
    parser.add_argument("--couchdb_user", default="admin")
    parser.add_argument("--couchdb_pass", default="admin")
    args = parser.parse_args()

    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "units": UNITS
    }

    # CouchDB metrics
    output.update(collect_couchdb(args.couchdb_host, args.couchdb_port, args.couchdb_user, args.couchdb_pass))

    # Tabs at the end
    output["tabs"] = TABS

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()