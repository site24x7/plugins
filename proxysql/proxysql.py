#!/usr/bin/python

import json
import argparse

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the ProxySQL
HOST_NAME = ""

# Enter the port configured for the ProxySQL
PORT = ""

# Enter the User name of the ProxySQL
USER = ""

#Enter the password for the user in ProxySQL
PASSWORD = ""


QUERY = ""
result_json = {}


METRIC_UNITS = {
    "proxysql_uptime" : "seconds",
    "sqlite3_memory_bytes" : "bytes",
    "active_transactions" : "transactions",
    "client_connections_aborted" : "connections",
    "client_connections_connected" : "connections",
    "client_connections_created" : "connections",
    "server_connections_aborted" : "connections",
    "server_connections_connected" : "connections",
    "server_connections_created" : "connections",
    "client_connections_non_idle" : "connections",
    "backend_query_time_nsec" : "nanoseconds",
    "mysql_backend_buffers_bytes" : "bytes",
    "mysql_frontend_buffers_bytes" : "bytes",
    "mysql_session_internal_bytes" : "bytes",
    "mysql_thread_workers" : "workers",
    "mysql_monitor_workers" : "workers",
    "connpool_get_conn_success" : "connections",
    "connpool_get_conn_immediate" : "connections",
    "questions" : "questions",
    "slow_queries" : "queries",
    "connpool_memory_bytes" : "bytes",
    "stmt_client_active_total" : "units",
    "stmt_client_active_unique" : "units",
    "stmt_server_active_total" : "units",
    "stmt_server_active_unique" : "units",
    "stmt_cached" : "units",
    "query_cache_memory_bytes" : "bytes",
    "query_cache_entries" : "entries",
    "query_cache_purged" : "entries",
    "query_cache_bytes_in" : "bytes",
    "query_cache_bytes_out" : "bytes",
    "query_cache_count_get" : "queries",
    "query_cache_count_get_ok" : "queries",
    "query_cache_count_set" : "queries",
    "query_processor_time_nsec" : "nanoseconds",
    "jemalloc_resident" : "bytes",
    "jemalloc_active" : "bytes",
    "jemalloc_mapped" : "bytes",
    "jemalloc_allocated" : "bytes",
    "jemalloc_metadata" : "bytes",
    "jemalloc_retained" : "bytes",
    "Auth_memory" : "bytes",
    "query_digest_memory" : "bytes",
    "stack_memory_mysql_threads" : "bytes",
    "stack_memory_admin_threads" : "bytes",
    "stack_memory_cluster_threads" : "bytes",
}

proxysql_metrics = {
    "mysql_global_metrics" : {
        "ProxySQL_Uptime" : "proxysql_uptime",
        "SQLite3_memory_bytes" : "sqlite3_memory_bytes",
        "Active_Transactions" : "active_transactions",
        "Client_Connections_aborted" : "client_connections_aborted",
        "Client_Connections_connected" : "client_connections_connected",
        "Client_Connections_created" : "client_connections_created",
        "Server_Connections_aborted" : "server_connections_aborted",
        "Server_Connections_connected" : "server_connections_connected",
        "Server_Connections_created" : "server_connections_created",
        "Client_Connections_non_idle" : "client_connections_non_idle",
        "Backend_query_time_nsec" : "backend_query_time_nsec",
        "mysql_backend_buffers_bytes" : "mysql_backend_buffers_bytes",
        "mysql_frontend_buffers_bytes" : "mysql_frontend_buffers_bytes",
        "mysql_session_internal_bytes" : "mysql_session_internal_bytes",
        "MySQL_Thread_Workers" : "mysql_thread_workers",
        "MySQL_Monitor_Workers" : "mysql_monitor_workers",
        "ConnPool_get_conn_success" : "connpool_get_conn_success",
        "ConnPool_get_conn_immediate" : "connpool_get_conn_immediate",
        "Questions" : "questions",
        "Slow_queries" : "slow_queries",
        "ConnPool_memory_bytes" : "connpool_memory_bytes",
        "Stmt_Client_Active_Total" : "stmt_client_active_total",
        "Stmt_Client_Active_Unique" : "stmt_client_active_unique",
        "Stmt_Server_Active_Total" : "stmt_server_active_total",
        "Stmt_Server_Active_Unique" : "stmt_server_active_unique",
        "Stmt_Cached" : "stmt_cached",
        "Query_Cache_Memory_bytes" : "query_cache_memory_bytes",
        "Query_Cache_Entries" : "query_cache_entries",
        "Query_Cache_Purged" : "query_cache_purged",
        "Query_Cache_bytes_IN" : "query_cache_bytes_in",
        "Query_Cache_bytes_OUT" : "query_cache_bytes_out",
        "Query_Cache_count_GET" : "query_cache_count_get",
        "Query_Cache_count_GET_OK" : "query_cache_count_get_ok",
        "Query_Cache_count_SET" : "query_cache_count_set",
        "Query_Processor_time_nsec" : "query_processor_time_nsec",
    },
    "stats_memory_metrics" : {
        "jemalloc_resident" : "jemalloc_resident",
        "jemalloc_active" : "jemalloc_active",
        "jemalloc_mapped" : "jemalloc_mapped",
        "jemalloc_allocated" : "jemalloc_allocated",
        "jemalloc_metadata" : "jemalloc_metadata",
        "jemalloc_retained" : "jemalloc_retained",
        "Auth_memory" : "Auth_memory",
        "query_digest_memory" : "query_digest_memory",
        "stack_memory_mysql_threads" : "stack_memory_mysql_threads",
        "stack_memory_admin_threads" : "stack_memory_admin_threads",
        "stack_memory_cluster_threads" : "stack_memory_cluster_threads",
    }
}


def fetch_metrics_via_mysqlconnector(mycursor, QUERY, metric_map):
    
    result = {}
    try:
        mycursor.execute(QUERY)
        metrics = mycursor.fetchall()
        
        for metric in metrics:
            if metric[0] in metric_map:
                result[metric_map[metric[0]]] = metric[1]
                
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)
    
    return result


def get_output():
    
    result = {}
    try:
        import mysql.connector
        
        mydb = mysql.connector.connect(
          host=HOST_NAME,
          port=PORT,
          user=USER,
          password=PASSWORD,
        )
        mycursor = mydb.cursor()
        
        QUERY = "select * from stats_mysql_global"
        result = fetch_metrics_via_mysqlconnector(mycursor, QUERY, proxysql_metrics["mysql_global_metrics"])
        
        QUERY = "select * from stats_memory_metrics"
        result.update(fetch_metrics_via_mysqlconnector(mycursor, QUERY, proxysql_metrics["stats_memory_metrics"]))
        
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)

    return result     


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="proxysql host_name", type=str)
    parser.add_argument('--port', help="proxysql port", type=str)
    parser.add_argument('--user', help="proxysql user", type=str)
    parser.add_argument('--password', help="proxysql password", type=str)
    
    args = parser.parse_args()
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
    if args.user:
        USER = args.user
    if args.password:
        PASSWORD = args.password
        
    result_json = get_output()
    
    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS

    print(json.dumps(result_json, indent=4, sort_keys=True))
