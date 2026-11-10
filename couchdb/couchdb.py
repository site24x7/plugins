#!/usr/bin/python3
# CouchDB Monitoring Plugin - Optimized for 3.3.3+
import json
import requests
import argparse

PLUGIN_VERSION = 4  # Marking this as the Final Audit version
HEARTBEAT = "true"

UNITS = {
    'request_time': 'ms',
    'couchdb_request_time.arithmetic_mean': 'ms',
    'couchdb_request_time.geometric_mean': 'ms',
    'couchdb_request_time.harmonic_mean': 'ms',
    'couchdb_request_time.max': 'ms',
    'couchdb_request_time.median': 'ms',
    'couchdb_request_time.min': 'ms',
    'couchdb_request_time_percentile.50': 'ms',
    'couchdb_request_time_percentile.75': 'ms',
    'couchdb_request_time_percentile.90': 'ms',
    'couchdb_request_time_percentile.95': 'ms',
    'couchdb_request_time_percentile.99': 'ms',
    'couchdb_request_time_percentile.999': 'ms'
}

TABS = {
    "Database": {
        "order": 1,
        "tablist": [
            'auth_cache_hits', 'auth_cache_misses', 'couchdb_local_document_writes',
            'couchdb_document_inserts', 'couchdb_document_writes',
            'couchdb_document_purges.total', 'couchdb_document_purges.success', 'couchdb_document_purges.failure',
            'couchdb_dbinfo.n', 'couchdb_dbinfo.max', 'couchdb_dbinfo.min', 'couchdb_dbinfo.median',
            'couchdb_active_tasks_db_compaction_count', 'couchdb_active_tasks_indexer_count',
            'couchdb_active_tasks_view_compaction_count', 'Databases_Details', 'database_writes', 
            'open_databases', 'open_os_files'
        ]
    },
    "HTTP": {
        "order": 2,
        "tablist": [
            'No_of_http_Post_Requests', 'No_of_http_Copy_Requests', 'No_of_http_Get_Requests',
            'No_of_http_Head_Requests', 'No_of_http_Move_Requests', 'No_of_http_Put_Requests',
            'No_of_http_200_Responses', 'No_of_http_201_Responses', 'No_of_http_202_Responses',
            'No_of_http_301_Responses', 'No_of_http_304_Responses', 'No_of_http_400_Responses',
            'No_of_http_401_Responses', 'No_of_http_403_Responses', 'No_of_http_404_Responses',
            'No_of_http_405_Responses', 'No_of_http_409_Responses', 'No_of_http_412_Responses',
            'No_of_http_500_Responses', 'view_reads', 'bulk_requests', 'temporary_view_reads',
            'clients_requesting_changes', 'lru_skips', 'vdu_rejects', 'map_doc', 'emits', 'view_timeouts'
        ]
    },
    "Performance": {
        "order": 3,
        "tablist": [
            'couchdb_request_time.min', 'couchdb_request_time.max', 'couchdb_request_time.arithmetic_mean',
            'couchdb_request_time.geometric_mean', 'couchdb_request_time.harmonic_mean',
            'couchdb_request_time.median', 'couchdb_request_time.variance', 'couchdb_request_time.standard_deviation',
            'couchdb_request_time.skewness', 'couchdb_request_time.kurtosis',
            'couchdb_request_time_percentile.50', 'couchdb_request_time_percentile.75',
            'couchdb_request_time_percentile.90', 'couchdb_request_time_percentile.95',
            'couchdb_request_time_percentile.99', 'couchdb_request_time_percentile.999'
        ]
    }
}

def get_databases_details(host, port, user, password, data):
    databases_details = []
    try:
        r = requests.get(f"http://{host}:{port}/_all_dbs", auth=(user,password), timeout=10)
        db_list = r.json()
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

def collect_couchdb(host, port, user, password):
    data = {}
    url = f"http://{host}:{port}/_node/_local/_stats"
    try:
        r = requests.get(url, auth=(user, password), timeout=10)
        stats_root = r.json()
        stats = stats_root.get('couchdb', {})

        # -------- Request Time --------
        if 'request_time' in stats:
            rt_val = stats['request_time'].get('value', 0)
            if isinstance(rt_val, dict):
                if 'percentile' in rt_val:
                    for pct, pct_val in rt_val['percentile']:
                        data[f"couchdb_request_time_percentile.{pct}"] = pct_val
                for sub_key, sub_val in rt_val.items():
                    if sub_key not in ['percentile', 'histogram','n']:
                        data[f"couchdb_request_time.{sub_key}"] = sub_val
                data['request_time'] = data.get('couchdb_request_time.arithmetic_mean', 0)
            else:
                data['request_time'] = rt_val

        # -------- Core Metrics (Fixed Mapping) --------
        core_keys = ['database_reads','database_writes','open_databases','open_os_files', 
                     'document_inserts', 'document_writes', 'local_document_writes']
        for key in core_keys:
            val = stats.get(key, {}).get('value', 0)
            data[key] = val
            data[f'couchdb_{key}'] = val

        # -------- Modern Auth Mapping --------
        data['auth_cache_hits'] = stats.get('password_hashing_fast', {}).get('value', 0)
        data['couchdb_auth_cache_hits'] = data['auth_cache_hits']
        data['auth_cache_misses'] = stats.get('password_hashing_slow', {}).get('value', 0)
        data['couchdb_auth_cache_misses'] = data['auth_cache_misses']

        # -------- HTTP Methods & Status Codes --------
        methods = stats.get('httpd_request_methods', {})
        for m in ['POST', 'COPY', 'GET', 'HEAD', 'MOVE', 'PUT']:
            data[f'No_of_http_{m}_Requests'] = methods.get(m, {}).get('value', 0)

        status_data = stats.get('httpd_status_codes', {})
        for s in ['200','201','202','301','304','400','401','403','404','405','409','412','500']:
            data[f'No_of_http_{s}_Responses'] = status_data.get(s, {}).get('value', 0)

        # -------- Active Tasks & Logs --------
        tasks = stats.get('active_tasks', {})
        for t in ['db_compaction', 'indexer', 'view_compaction']:
            data[f'couchdb_active_tasks_{t}_count'] = tasks.get(t, {}).get('count', 0)

        log_levels = stats.get('couch_log', {}).get('level', {})
        for l in ['alert','critical','error','warning','info']:
            data[f'couchdb_couch_log.level.{l}'] = log_levels.get(l, 0)

        data['Databases_Details'] = get_databases_details(host, port, user, password, data)

    except Exception as e:
        data['msg'] = f"CouchDB Error: {str(e)}"
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="5984")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="admin")
    args = parser.parse_args()
    output = {"plugin_version": PLUGIN_VERSION, "heartbeat_required": HEARTBEAT, "units": UNITS}
    output.update(collect_couchdb(args.host, args.port, args.user, args.password))
    output["tabs"] = TABS
    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()