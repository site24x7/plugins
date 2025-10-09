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
            'Databases_Details','database_writes','open_databases'
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
            'clients_requesting_changes'
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
        r = requests.get(url, auth=(user, password), timeout=10)
        stats = r.json().get('couchdb', {})

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
                    if sub_key not in ['percentile', 'histogram','n']:
                        data[f"couchdb_request_time.{sub_key}"] = sub_val

                # Top-level request_time using arithmetic_mean if available
                data['request_time'] = data.get('couchdb_request_time.arithmetic_mean', 0)
            else:
                data['request_time'] = request_time_val

        # -------- Simple Metrics --------
        for key in ['auth_cache_hits','auth_cache_misses','database_reads','database_writes',
                    'open_databases','open_os_files']:
            if key in stats:
                data[key] = stats[key].get('value', 0)
            else:
                data[key] = 0

        # -------- HTTP Methods --------
        methods = stats.get('httpd_request_methods')
        if methods:
            if 'POST' in methods:
                data['No_of_http_Post_Requests'] = methods['POST'].get('value', 0)
            else:
                data['No_of_http_Post_Requests'] = 0

            if 'COPY' in methods:
                data['No_of_http_Copy_Requests'] = methods['COPY'].get('value', 0)
            else:
                data['No_of_http_Copy_Requests'] = 0

            if 'GET' in methods:
                data['No_of_http_Get_Requests'] = methods['GET'].get('value', 0)
            else:
                data['No_of_http_Get_Requests'] = 0

            if 'HEAD' in methods:
                data['No_of_http_Head_Requests'] = methods['HEAD'].get('value', 0)
            else:
                data['No_of_http_Head_Requests'] = 0

            if 'MOVE' in methods:
                data['No_of_http_Move_Requests'] = methods['MOVE'].get('value', 0)
            else:
                data['No_of_http_Move_Requests'] = 0

            if 'PUT' in methods:
                data['No_of_http_Put_Requests'] = methods['PUT'].get('value', 0)
            else:
                data['No_of_http_Put_Requests'] = 0
        # else: do nothing (no keys created if parent missing)

        # -------- HTTP Status Codes --------
        status = stats.get('httpd_status_codes')
        status_codes = ['200','201','202','301','304','400','401','403','404','405','409','412','500']
        if status:
            for s in status_codes:
                if s in status:
                    data[f'No_of_http_{s}_Responses'] = status[s].get('value', 0)
                else:
                    data[f'No_of_http_{s}_Responses'] = 0
        # else: do nothing

        # -------- HTTP Other Metrics --------
        httpd = stats.get('httpd')
        if httpd:
            for key in ['view_reads','bulk_requests','temporary_view_reads','clients_requesting_changes']:
                if key in httpd:
                    data[key] = httpd[key].get('value', 0)
                else:
                    data[key] = 0
        # else: do nothing

        # -------- Active Tasks --------
        tasks = stats.get('active_tasks')
        if tasks:
            if 'db_compaction' in tasks:
                data['couchdb_active_tasks_db_compaction_count'] = tasks['db_compaction'].get('count', 0)
            else:
                data['couchdb_active_tasks_db_compaction_count'] = 0

            if 'indexer' in tasks:
                data['couchdb_active_tasks_indexer_count'] = tasks['indexer'].get('count', 0)
            else:
                data['couchdb_active_tasks_indexer_count'] = 0

            if 'view_compaction' in tasks:
                data['couchdb_active_tasks_view_compaction_count'] = tasks['view_compaction'].get('count', 0)
            else:
                data['couchdb_active_tasks_view_compaction_count'] = 0
        # else: do nothing

        # -------- Couch Log Levels --------
        couch_log = stats.get('couch_log')
        levels = ['alert','critical','error','warning','info']
        if couch_log and 'level' in couch_log:
            for level in levels:
                if level in couch_log['level']:
                    data[f'couchdb_couch_log.level.{level}'] = couch_log['level'][level]
                else:
                    data[f'couchdb_couch_log.level.{level}'] = 0
        # else: do nothing

        # -------- Document & DB Info --------
        couchdb_main = stats.get('couchdb', {})
        for key in ['document_inserts','document_writes','local_document_writes']:
            if key in couchdb_main:
                data[f'couchdb_{key}'] = couchdb_main[key].get('value', 0)
            else:
                data[f'couchdb_{key}'] = 0

        if 'document_purges' in couchdb_main:
            for sub_key in ['total','success','failure']:
                if sub_key in couchdb_main['document_purges']:
                    data[f'couchdb_document_purges.{sub_key}'] = couchdb_main['document_purges'][sub_key]
                else:
                    data[f'couchdb_document_purges.{sub_key}'] = 0

        if 'dbinfo' in couchdb_main:
            for sub_key in ['n','max','min','median']:
                if sub_key in couchdb_main['dbinfo']:
                    data[f'couchdb_dbinfo.{sub_key}'] = couchdb_main['dbinfo'][sub_key]
                else:
                    data[f'couchdb_dbinfo.{sub_key}'] = 0

        # -------- Dynamic Database Details --------
        data['Databases_Details'] = get_databases_details(host, port, user, password, data)

    except Exception as e:
        data['msg'] = f"CouchDB Error: {str(e)}"
    return data
# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default="5984")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="admin")
    args = parser.parse_args()

    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "units": UNITS
    }

    # CouchDB metrics
    output.update(collect_couchdb(args.host, args.port, args.user, args.password))

    # Tabs at the end
    output["tabs"] = TABS

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()
