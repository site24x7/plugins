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

# -------------------------
# Tabs
# -------------------------
TABS = {
    "Database": {
        "order": 1,
        "tablist": [
            'auth_cache_hits',
            'auth_cache_misses',
            'couchdb_local_document_writes',
            'couchdb_document_inserts',
            'couchdb_document_writes',
            'couchdb_document_purges.total',
            'couchdb_document_purges.success',
            'couchdb_document_purges.failure',
            'couchdb_dbinfo.n',
            'couchdb_dbinfo.max',
            'couchdb_dbinfo.min',
            'couchdb_dbinfo.median',
            'couchdb_active_tasks_db_compaction_count',
            'couchdb_active_tasks_indexer_count',
            'couchdb_active_tasks_view_compaction_count',
            'Databases_Details',
            'database_writes',
            'open_databases',
            'open_os_files'
        ]
    },
    "HTTP": {
        "order": 2,
        "tablist": [
            'No_of_http_Post_Requests',
            'No_of_http_Copy_Requests',
            'No_of_http_Get_Requests',
            'No_of_http_Head_Requests',
            'No_of_http_Move_Requests',
            'No_of_http_Put_Requests',
            'No_of_http_200_Responses',
            'No_of_http_201_Responses',
            'No_of_http_202_Responses',
            'No_of_http_301_Responses',
            'No_of_http_304_Responses',
            'No_of_http_400_Responses',
            'No_of_http_401_Responses',
            'No_of_http_403_Responses',
            'No_of_http_404_Responses',
            'No_of_http_405_Responses',
            'No_of_http_409_Responses',
            'No_of_http_412_Responses',
            'No_of_http_500_Responses',
            'view_reads',
            'bulk_requests',
            'temporary_view_reads',
            'clients_requesting_changes',
            'lru_skips',
            'vdu_rejects',
            'map_doc',
            'emits',
            'view_timeouts'
        ]
    },
    "Performance": {
        "order": 3,
        "tablist": [
            'couchdb_request_time.min',
            'couchdb_request_time.max',
            'couchdb_request_time.arithmetic_mean',
            'couchdb_request_time.geometric_mean',
            'couchdb_request_time.harmonic_mean',
            'couchdb_request_time.median',
            'couchdb_request_time.variance',
            'couchdb_request_time.standard_deviation',
            'couchdb_request_time.skewness',
            'couchdb_request_time.kurtosis',
            'couchdb_request_time_percentile.50',
            'couchdb_request_time_percentile.75',
            'couchdb_request_time_percentile.90',
            'couchdb_request_time_percentile.95',
            'couchdb_request_time_percentile.99',
            'couchdb_request_time_percentile.999'
        ]
    }
}

# -------------------------
# Helper to convert Bytes to MB
# -------------------------
def bytes_to_mb(value):
    try:
        return round(float(value) / 1024 / 1024, 2)
    except Exception:
        return 0

def clean_quotes(value):
    if not value:
        return value
    value_str = str(value).strip()
    if (value_str.startswith('"') and value_str.endswith('"')) or (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str

# -------------------------
# CouchDB Database Details (dynamic)
# -------------------------
def get_databases_details(host, port, user, password, data):
    databases_details = []
    try:
        r = requests.get(f"http://{host}:{port}/_all_dbs", auth=(user, password), timeout=10)
        
        if r.status_code == 401:
            data['status'] = 0
            data['msg'] = "Authentication failed while fetching databases"
            return databases_details
        elif r.status_code != 200:
            data['status'] = 0
            data['msg'] = f"HTTP Error fetching databases: {r.status_code}"
            return databases_details

        response_json = r.json()
        if isinstance(response_json, dict) and 'error' in response_json:
            data['status'] = 0
            data['msg'] = f"CouchDB Error: {response_json.get('reason', 'Unknown error')}"
            return databases_details
        
        db_list = response_json if isinstance(response_json, list) else []
        for db_name in db_list:
            r_db = requests.get(f"http://{host}:{port}/{db_name}", auth=(user, password), timeout=10)
            if r_db.status_code == 200:
                db_info = r_db.json()
                databases_details.append({
                    "name": db_name,
                    "doc_count": db_info.get("doc_count", 0),
                    "disk_size": bytes_to_mb(db_info.get("disk_size", 0)),
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
        r = requests.get(url, auth=(user, password), timeout=10)
        
        # Check for HTTP errors
        if r.status_code == 401:
            data['status'] = 0
            data['msg'] = "Authentication failed: Invalid username or password"
            return data
        elif r.status_code != 200:
            data['status'] = 0
            data['msg'] = f"HTTP Error: {r.status_code} - {r.text}"
            return data
        
        # Parse JSON and ensure stats_root is defined
        stats_root = r.json()
        if isinstance(stats_root, dict) and 'error' in stats_root:
            data['status'] = 0
            data['msg'] = f"CouchDB Error: {stats_root.get('error', 'Unknown')} - {stats_root.get('reason', 'No reason provided')}"
            return data
        
        stats = stats_root.get('couchdb', {})

        # -------- Request Time --------
        if 'request_time' in stats:
            request_time_val = stats['request_time'].get('value', 0)
            if isinstance(request_time_val, dict):
                # Percentile
                if 'percentile' in request_time_val:
                    for item in request_time_val['percentile']:
                        pct, pct_val = item
                        data[f"couchdb_request_time_percentile.{pct}"] = pct_val

                # Histogram
                if 'histogram' in request_time_val:
                    for idx, item in enumerate(request_time_val['histogram']):
                        data[f"couchdb_request_time_histogram.{idx}_bucket"] = item[0]
                        data[f"couchdb_request_time_histogram.{idx}_count"] = item[1]

                # Other keys
                for sub_key, sub_val in request_time_val.items():
                    if sub_key not in ['percentile', 'histogram', 'n']:
                        data[f"couchdb_request_time.{sub_key}"] = sub_val

                # Top-level request_time using arithmetic_mean if available
                data['request_time'] = data.get('couchdb_request_time.arithmetic_mean', 0)
            else:
                data['request_time'] = request_time_val

        # -------- Simple Metrics --------
        core_keys = [
            'database_reads', 'database_writes', 'open_databases', 'open_os_files',
            'document_inserts', 'document_writes', 'local_document_writes'
        ]
        for key in core_keys:
            val = stats.get(key, {}).get('value', 0) if isinstance(stats.get(key), dict) else 0
            data[key] = val
            data[f'couchdb_{key}'] = val

        # Handle local_document_writes fix
        data['couchdb_local_document_writes'] = (
            stats.get('local_document_writes', {}).get('value', 0)
            if isinstance(stats.get('local_document_writes'), dict) else 0
        )

        # -------- Auth Cache Counters --------
        auth_hits_metric = stats.get('auth_cache_hits', stats_root.get('auth_cache_hits', {}))
        auth_misses_metric = stats.get('auth_cache_misses', stats_root.get('auth_cache_misses', {}))

        auth_hits = (
            auth_hits_metric.get('value', 0)
            if isinstance(auth_hits_metric, dict)
            else (auth_hits_metric if isinstance(auth_hits_metric, (int, float)) else 0)
        )
        auth_misses = (
            auth_misses_metric.get('value', 0)
            if isinstance(auth_misses_metric, dict)
            else (auth_misses_metric if isinstance(auth_misses_metric, (int, float)) else 0)
        )

        data['auth_cache_hits'] = auth_hits
        data['couchdb_auth_cache_hits'] = auth_hits
        data['auth_cache_misses'] = auth_misses
        data['couchdb_auth_cache_misses'] = auth_misses

        # -------- HTTP Methods --------
        methods = stats.get('httpd_request_methods', {})
        for m in ['POST', 'COPY', 'GET', 'HEAD', 'MOVE', 'PUT']:
            val = methods.get(m, {}).get('value', 0) if isinstance(methods.get(m), dict) else 0
            data[f'No_of_http_{m.capitalize()}_Requests'] = val

        # -------- HTTP Status Codes --------
        status_data = stats.get('httpd_status_codes', {})
        status_codes = ['200', '201', '202', '301', '304', '400', '401', '403', '404', '405', '409', '412', '500']
        for s in status_codes:
            val = status_data.get(s, {}).get('value', 0) if isinstance(status_data.get(s), dict) else 0
            data[f'No_of_http_{s}_Responses'] = val

        # -------- HTTP Other Metrics --------
        httpd = stats_root.get('httpd', stats.get('httpd', {}))
        for key in ['view_reads', 'bulk_requests', 'temporary_view_reads', 'clients_requesting_changes', 'view_timeouts']:
            val = httpd.get(key, {}) if isinstance(httpd, dict) else {}
            data[key] = (
                val.get('value', 0)
                if isinstance(val, dict)
                else (val if isinstance(val, (int, float)) else 0)
            )

        # -------- CouchDB Statistics in Other Groups --------
        mrview = stats_root.get('mrview', stats_root.get('couchdb.mrview', stats.get('mrview', {})))
        query_server = stats_root.get('query_server', stats_root.get('couchdb.query_server', stats.get('query_server', {})))
        couch_server = stats.get('couch_server', stats_root.get('couch_server', stats_root.get('couchdb.couch_server', {})))

        data['map_doc'] = mrview.get('map_doc', {}).get('value', 0) if isinstance(mrview.get('map_doc'), dict) else 0
        data['emits'] = mrview.get('emits', {}).get('value', 0) if isinstance(mrview.get('emits'), dict) else 0
        data['vdu_rejects'] = query_server.get('vdu_rejects', {}).get('value', 0) if isinstance(query_server.get('vdu_rejects'), dict) else 0
        data['lru_skips'] = couch_server.get('lru_skip', {}).get('value', 0) if isinstance(couch_server.get('lru_skip'), dict) else 0

        # -------- Document & DB Info --------
        if 'document_purges' in stats and isinstance(stats['document_purges'], dict):
            dp = stats['document_purges']
            for sub_key in ['total', 'success', 'failure']:
                val = dp.get(sub_key, 0)
                data[f'couchdb_document_purges.{sub_key}'] = val.get('value', val) if isinstance(val, dict) else val
        else:
            for sub_key in ['total', 'success', 'failure']:
                data[f'couchdb_document_purges.{sub_key}'] = 0

        if 'dbinfo' in stats and isinstance(stats['dbinfo'], dict):
            dbi = stats['dbinfo']
            for sub_key in ['n', 'max', 'min', 'median']:
                val = dbi.get(sub_key, 0)
                data[f'couchdb_dbinfo.{sub_key}'] = val.get('value', val) if isinstance(val, dict) else val
        else:
            for sub_key in ['n', 'max', 'min', 'median']:
                data[f'couchdb_dbinfo.{sub_key}'] = 0

        # -------- Active Tasks --------
        for t in ['db_compaction', 'indexer', 'view_compaction']:
            data[f'couchdb_active_tasks_{t}_count'] = 0
        try:
            r_tasks = requests.get(f"http://{host}:{port}/_active_tasks", auth=(user, password), timeout=10)
            if r_tasks.status_code == 200:
                active_tasks_list = r_tasks.json()
                if isinstance(active_tasks_list, list):
                    for task in active_tasks_list:
                        ttype = task.get('type', '')
                        if ttype in ['db_compaction', 'database_compaction']:
                            data['couchdb_active_tasks_db_compaction_count'] += 1
                        elif ttype == 'indexer':
                            data['couchdb_active_tasks_indexer_count'] += 1
                        elif ttype == 'view_compaction':
                            data['couchdb_active_tasks_view_compaction_count'] += 1
        except Exception:
            tasks = stats.get('active_tasks', {})
            if isinstance(tasks, dict):
                for t in ['db_compaction', 'indexer', 'view_compaction']:
                    data[f'couchdb_active_tasks_{t}_count'] = (
                        tasks.get(t, {}).get('count', 0) if isinstance(tasks.get(t), dict) else 0
                    )

        # -------- Couch Log Levels --------
        couch_log = stats_root.get('couch_log', stats_root.get('couchdb.couch_log', stats.get('couch_log', {})))
        if isinstance(couch_log, dict):
            log_levels = couch_log.get('level', {})
            if isinstance(log_levels, dict):
                for l in ['alert', 'critical', 'error', 'warning', 'info']:
                    val = log_levels.get(l, 0)
                    if isinstance(val, dict):
                        val = val.get('value', 0)
                    data[f'couchdb_couch_log.level.{l}'] = val if isinstance(val, (int, float)) else 0
            else:
                for l in ['alert', 'critical', 'error', 'warning', 'info']:
                    data[f'couchdb_couch_log.level.{l}'] = 0
        else:
            for l in ['alert', 'critical', 'error', 'warning', 'info']:
                data[f'couchdb_couch_log.level.{l}'] = 0

        # -------- Dynamic Database Details --------
        data['Databases_Details'] = get_databases_details(host, port, user, password, data)

    except Exception as e:
        data['status'] = 0
        data['msg'] = f"CouchDB Error: {str(e)}"
    return data

# -------------------------
# Agent Runner Integration
# -------------------------
def run(param):
    host = clean_quotes(param.get("host")) if param and param.get("host") else "127.0.0.1"
    port = clean_quotes(param.get("port")) if param and param.get("port") else "5984"
    user = clean_quotes(param.get("user")) if param and param.get("user") else "admin"
    password = clean_quotes(param.get("password")) if param and param.get("password") else "admin"
    
    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT
    }
    
    metrics = collect_couchdb(host, port, user, password)
    
    # Check for errors
    if 'status' in metrics and metrics['status'] == 0:
        output['status'] = 0
        output['msg'] = metrics['msg']
        return output
    
    output["units"] = UNITS
    output.update(metrics)
    output["tabs"] = TABS
    output["s247config"] = {
        "childdiscovery": [
            "Databases_Details"
        ]
    }
    
    return output

# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="5984")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="admin")
    args, unknown = parser.parse_known_args()

    param = {
        "host": args.host,
        "port": args.port,
        "user": args.user,
        "password": args.password
    }

    output = run(param)
    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()