#!/usr/bin/python3
import json
import pymysql
import traceback
from decimal import Decimal
HAS_PSUTIL = False
PLUGIN_VERSION = "1"
HEARTBEAT = True
MYSQL_DEFAULTS = {
    "host": "localhost",
    "port": 3306,
    "username": "user",
    "password": ""
}
METRICS_UNITS = {
    "Uptime": "seconds",
    "Connection_usage": "%",
    "Open_files_usage": "%",
    "Fetch_Latency_ms": "ms",
    "Insert_Latency_ms": "ms",
    "Throughput_qps": "queries/s",
    "Version": "text",
    "Type_Instance": "text",
    "Table_open_cache_hit_ratio": "%",
    "Buffer_pool_utilization": "%",
    
    "Slave_running": "boolean",
    "Slave_sql_running": "boolean",
    "Slave_io_running": "boolean",
    "Seconds_behind_master": "seconds",
    "Relay_log_space": "bytes",
    "Master_host": "text",
    "Master_user": "text",
    "Database": {
        "Db_size_MB": "MB",
        "Index_MB": "MB",
        "Fetch_Latency_ms": "ms",
        "Insert_Latency_ms": "ms",
        "Throughput_qps": "queries/s"
    }
}
METRICS_MAPPING = {
    "Database": [
        "name", "Db_size_MB", "Index_MB", "Number_of_Tables", "status", "Open_tables",
        "Fetch_Latency_ms", "Insert_Latency_ms", "Throughput_qps", "Queries_executed", "Errors"
    ],
    "Threads": [
        "Threads_running",
        "Threads_connected",
        "Threads_cached",
        "Threads_created",
        "Aborted_clients",
        "Aborted_connects",
        "Max_used_connections",
        "Connections"
    ],
    "Handler": [
        "Com_select",
        "Com_insert",
        "Com_update",
        "Com_delete",
        "Com_replace",
        "Com_load",
        "Handler_read_first",
        "Handler_read_key",
        "Handler_read_rnd",
        "Handler_read_rnd_next",
        "Handler_write",
        "Handler_update",
        "Handler_delete",
        "Handler_commit",
        "Handler_rollback",
        "Com_delete_multi",
        "Com_insert_select",
        "Com_replace_select",
        "Com_update_multi"
    ],
    "Query and Storage": [
        "Queries",
        "Questions",
        "Slow_queries",
        "Opened_tables",
        "Opened_files",
        "Binlog_cache_use",
        "Binlog_cache_disk_use",
        "Bytes_received",
        "Bytes_sent",
        "Com_commit",
        "Com_rollback",
        "Table_locks_waited",
        "Table_locks_immediate",
        "Created_tmp_files",
        "Created_tmp_tables",
        "Created_tmp_disk_tables",
        "Commands_per_second",
        "Avg_query_time",
        "Max_used_connections",
        "Connection_usage",
        "Open_files_usage",
        "Innodb_buffer_pool_pages_data",
        "Innodb_buffer_pool_pages_dirty",
        "Innodb_buffer_pool_pages_free",
        "Innodb_rows_deleted",
        "Innodb_rows_inserted",
        "Innodb_rows_updated",
        "Slave_running",
        "Slave_sql_running",
        "Slave_io_running",
        "Seconds_behind_master",
        "Relay_log_space",
        "Master_host",
        "Master_user",
        "Master_retry_count",
        "Skip_counter",
        "Open_files_limit",
        "Open_files_used",
        "Key_reads",
        "Key_writes",
        "Key_blocks_used",
        "Key_blocks_unused",
        "Key_blocks_not_flushed",
        "Innodb_buffer_pool_pages_total",
        "Innodb_pages_read",
        "Innodb_pages_written",
        "Innodb_log_writes",
        "Innodb_log_waits",
        "Innodb_buffer_pool_reads",
        "Innodb_buffer_pool_write_requests",
        "Innodb_data_reads",
        "Innodb_data_writes",
        "Innodb_pages_created",
        "Innodb_row_lock_time_avg",
        "Innodb_row_lock_time_max",
        "Innodb_row_lock_waits",
        "Innodb_buffer_pool_wait_free",
        "Innodb_buffer_pool_pages_flushed",
        "Innodb_buffer_pool_read_ahead_evicted",
        "Innodb_buffer_pool_read_ahead",
        "Innodb_buffer_pool_read_ahead_rnd",
        "Innodb_buffer_pool_read_requests",
        "Innodb_data_fsyncs",
        "Innodb_data_pending_fsyncs",
        "Innodb_data_pending_reads",
        "Innodb_data_pending_writes",
        "Innodb_log_write_requests",
        "Innodb_os_log_fsyncs",
        "Innodb_os_log_pending_fsyncs",
        "Innodb_os_log_pending_writes",
        "Innodb_os_log_written",
        "Innodb_rows_read",
        "Qcache_hits",
        "Qcache_free_memory",
        "Qcache_not_cached",
        "Qcache_queries_in_cache",
        "Qcache_free_blocks",
        "Qcache_inserts",
        "Qcache_lowmem_prunes",
        "Qcache_total_blocks",
        "Connection_errors_max_connections",
        "max_connections",
        "Select_full_join",
        "Select_full_range_join",
        "Select_range",
        "Select_range_check",
        "Select_scan",
        "Max_execution_time_exceeded",
        "Open_files",
        "Table_open_cache_hits",
        "Table_open_cache_misses",
        "Table_open_cache_overflows",
        "Prepared_stmt_count",
        "Sort_merge_passes",
        "Sort_range",
        "Sort_rows",
        "Sort_scan",
        "Key_read_requests",
        "Key_write_requests"
    ]
}
class MySQLMonitor:
    def __init__(self, args):
        self.args = args
        self.host = getattr(args, "host", MYSQL_DEFAULTS["host"])
        self.port = int(getattr(args, "port", MYSQL_DEFAULTS["port"]))
        self.username = getattr(args, "username", MYSQL_DEFAULTS["username"])
        self.password = getattr(args, "password", MYSQL_DEFAULTS["password"])
        self.maindata = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            
        }
        self.connection = None
        self.cursor = None
        
    def to_str(self, val):
        try:
            f = float(val)
            return f"{f:.2f}"
        except Exception:
            return str(val)
        
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                cursorclass=pymysql.cursors.DictCursor,
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = f"Connection error: {repr(e)}"
            return False
        
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = f"Error closing the connection: {repr(e)}"

    def collect_database(self):
        dbs = []
        try:
            self.cursor.execute("""
                SELECT table_schema AS name,
                       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS Db_size_MB,
                       ROUND(SUM(index_length) / 1024 / 1024, 2) AS Index_MB,
                       COUNT(table_name) AS Number_of_Tables,
                       1 AS status
                FROM information_schema.tables
                WHERE table_schema NOT IN ('mysql', 'performance_schema', 'sys', 'information_schema')
                GROUP BY table_schema
            """)
            db_size_info = {row["name"]: row for row in self.cursor.fetchall()}
            self.cursor.execute("""
                SELECT ROUND(IFNULL(AVG_TIMER_WAIT/1000000000, 0)*1000, 2) AS avg_fetch_latency_ms
                FROM performance_schema.events_statements_summary_by_digest
                WHERE digest_text LIKE 'select%%' AND SCHEMA_NAME IS NOT NULL
                LIMIT 1
            """)
            fetch_latency = 0.0
            r = self.cursor.fetchone()
            if r and "avg_fetch_latency_ms" in r:
                fetch_latency = float(r["avg_fetch_latency_ms"])
            self.cursor.execute("""
                SELECT ROUND(IFNULL(AVG_TIMER_WAIT/1000000000, 0)*1000, 2) AS avg_insert_latency_ms
                FROM performance_schema.events_statements_summary_by_digest
                WHERE digest_text LIKE 'insert%%' AND SCHEMA_NAME IS NOT NULL
                LIMIT 1
            """)
            insert_latency = 0.0
            r = self.cursor.fetchone()
            if r and "avg_insert_latency_ms" in r:
                insert_latency = float(r["avg_insert_latency_ms"])
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions'")
            questions_row = self.cursor.fetchone()
            questions = int(questions_row['Value']) if questions_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Uptime'")
            uptime_row = self.cursor.fetchone()
            uptime = int(uptime_row['Value']) if uptime_row else 1 
            throughput_qps = round(questions / uptime, 2) if uptime > 0 else 0.0
            queries_executed = questions
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Errors'")
            errors_row = self.cursor.fetchone()
            errors = int(errors_row['Value']) if errors_row else 0
            self.cursor.execute("SELECT VERSION() AS version")
            version_row = self.cursor.fetchone()
            version = version_row.get("version", "") if version_row else ""
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Connections'")
            connections_attempted_row = self.cursor.fetchone()
            connections_attempted = int(connections_attempted_row['Value']) if connections_attempted_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Threads_connected'")
            threads_connected_row = self.cursor.fetchone()
            threads_connected = int(threads_connected_row['Value']) if threads_connected_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Table_open_cache_hits'")
            table_open_cache_hits_row = self.cursor.fetchone()
            table_open_cache_hits = int(table_open_cache_hits_row['Value']) if table_open_cache_hits_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Table_open_cache_misses'")
            table_open_cache_misses_row = self.cursor.fetchone()
            table_open_cache_misses = int(table_open_cache_misses_row['Value']) if table_open_cache_misses_row else 0
            table_open_cache_hit_ratio = 0.0
            total = table_open_cache_hits + table_open_cache_misses
            if total > 0:
                table_open_cache_hit_ratio = round((table_open_cache_hits / total) * 100, 2)
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_data'")
            pages_data_row = self.cursor.fetchone()
            pages_data = int(pages_data_row['Value']) if pages_data_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_total'")
            pages_total_row = self.cursor.fetchone()
            pages_total = int(pages_total_row['Value']) if pages_total_row else 0
            buffer_pool_utilization = 0.0
            if pages_total > 0:
                buffer_pool_utilization = round((pages_data / pages_total) * 100, 2)
            for dbname, dbdata in db_size_info.items():
                rec = {
                    "name": dbname,
                    "Db_size_MB": self.to_str(dbdata.get("Db_size_MB", 0)),
                    "Index_MB": self.to_str(dbdata.get("Index_MB", 0)),
                    "Number_of_Tables": self.to_str(dbdata.get("Number_of_Tables", 0)),
                    "Fetch_Latency_ms": self.to_str(fetch_latency),
                    "Insert_Latency_ms": self.to_str(insert_latency),
                    "Throughput_qps": self.to_str(throughput_qps),
                    "Queries_executed": str(queries_executed),
                    "Errors": str(errors),
                    
                    # "Version": version,
                    # "Connections_attempted": str(connections_attempted),
                    # "Threads_connected": str(threads_connected),
                    # "Table_open_cache_hit_ratio": str(table_open_cache_hit_ratio),
                    # "Buffer_pool_utilization": str(buffer_pool_utilization)
                }
                dbs.append(rec)
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = f"Database collection error: {e}"
        return dbs
    
    def collect_sessions(self):
        try:
            self.cursor.execute("""
                SELECT
                    COUNT(*) AS total_sessions,
                    SUM(CASE WHEN COMMAND != 'Sleep' THEN 1 ELSE 0 END) AS active_sessions,
                    SUM(CASE WHEN COMMAND = 'Sleep' THEN 1 ELSE 0 END) AS idle_sessions,
                    (
                        SELECT VARIABLE_VALUE 
                        FROM performance_schema.global_status 
                        WHERE VARIABLE_NAME = 'Aborted_clients'
                    ) AS killed_sessions
                FROM information_schema.PROCESSLIST
            """)
            row = self.cursor.fetchone()
            # Safely cast and supply session stats; handle None gracefully
            sessions = {
                "total_sessions": int(row.get('total_sessions', 0)),
                "active_sessions": int(row.get('active_sessions', 0)),
                "idle_sessions": int(row.get('idle_sessions', 0)),
                "killed_sessions": int(row.get('killed_sessions', 0)) if row.get('killed_sessions') is not None else 0
            }
            return sessions
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = f"Session collection error: {e}"


    def collect_metrics(self):
        if not self.connect():
            return self.maindata
        try:
            self.cursor.execute("SHOW GLOBAL STATUS")
            status = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
            self.cursor.execute("SHOW GLOBAL VARIABLES")
            variables = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
            self.maindata["Uptime"] = self.to_str(status.get("Uptime", 0))
            for tab_name in ["Threads", "Handler", "Query and Storage"]:
                for metric in METRICS_MAPPING[tab_name]:
                    val = status.get(metric) or variables.get(metric)
                    if val is not None:
                        display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                        self.maindata[display_name] = self.to_str(val)
                        # self.maindata[metric] = self.to_str(val)
            max_used = status.get("Max_used_connections")
            self.maindata["Max_used_connections"] = self.to_str(int(max_used)) if max_used else "0.00"
            max_conn = int(variables.get("max_connections", "0"))
            threads = int(status.get("Threads_running", "0"))
            open_files = int(status.get("Open_files", "0"))
            open_files_limit = int(variables.get("open_files_limit", "0"))
            self.maindata["Connection_usage"] = self.to_str(round(threads / max_conn * 100, 2)) if max_conn else "0.00"
            self.maindata["Open_files_usage"] = self.to_str(round(open_files / open_files_limit * 100, 2)) if open_files_limit else "0.00"
            self.maindata["Database"] = self.collect_database()
            session_stats = self.collect_sessions()
            self.maindata["total_sessions"] = session_stats["total_sessions"]
            self.maindata["active_sessions"] = session_stats["active_sessions"]
            self.maindata["idle_sessions"] = session_stats["idle_sessions"]
            self.maindata["killed_sessions"] = session_stats["killed_sessions"]
            self.maindata["s247config"] = {
                "childdiscovery": ["Database"]
            }
            self.maindata["units"] = METRICS_UNITS
            self.maindata["tabs"] = {
                "Database": {
                    "order": 1,
                    "tablist": ["Database"]
                },
                "Threads": {
                    "order": 2,
                    "tablist": [
                        "Threads_running",
                        "Threads_connected",
                        "Threads_cached",
                        "Threads_created"
                    ],
                },
                "Handler": {
                    "order": 3,
                    "tablist":  [
                        "Handler_read_first",
                        "Handler_read_key",
                        "Handler_read_rnd",
                        "Handler_read_rnd_next",
                        "Handler_write",
                        "Handler_update",
                        "Handler_delete",
                        "Handler_commit",
                        "Handler_rollback"
                    ],
                },
                "Query and Storage": {
                    "order": 4,
                    "tablist": [
                        "Queries",
                        "Questions",
                        "Slow_queries",
                        "Opened_tables",
                        "Opened_files",
                        "Binlog_cache_use",
                        "Binlog_cache_disk_use",
                        "Bytes_received",
                        "Bytes_sent",
                        "Table_locks_waited",
                        "Table_locks_immediate",
                        "Created_tmp_files",
                        "Created_tmp_tables",
                        "Created_tmp_disk_tables",
                        "Commands_per_second",
                        "Avg_query_time",
                        "Connection_usage",
                        "Open_files_usage",
                        "Innodb_buffer_pool_pages_data",
                        "Innodb_buffer_pool_pages_dirty",
                        "Innodb_buffer_pool_pages_free",
                        "Innodb_rows_deleted",
                        "Innodb_rows_inserted",
                        "Innodb_rows_updated",
                        "Slave_running",
                        "Slave_sql_running",
                        "Slave_io_running",
                        "Seconds_behind_master",
                        "Relay_log_space",
                        "Master_host",
                        "Master_user",
                        "Master_retry_count",
                        "Skip_counter",
                        "Open_files_limit",
                        "Open_files_used",
                        "Key_reads",
                        "Key_writes",
                        "Key_blocks_used",
                        "Key_blocks_unused",
                        "Key_blocks_not_flushed",
                        "Innodb_buffer_pool_pages_total",
                        "Innodb_pages_read",
                        "Innodb_pages_written",
                        "Innodb_log_writes",
                        "Innodb_log_waits",
                        "Innodb_buffer_pool_reads",
                        "Innodb_buffer_pool_write_requests",
                        "Innodb_data_reads",
                        "Innodb_data_writes",
                        "Innodb_pages_created",
                        "Innodb_row_lock_time_avg",
                        "Innodb_row_lock_time_max",
                        "Innodb_row_lock_waits",
                        "Innodb_buffer_pool_wait_free",
                        "Innodb_buffer_pool_pages_flushed",
                        "Innodb_buffer_pool_read_ahead_evicted",
                        "Innodb_buffer_pool_read_ahead",
                        "Innodb_buffer_pool_read_ahead_rnd",
                        "Innodb_buffer_pool_read_requests",
                        "Innodb_data_fsyncs",
                        "Innodb_data_pending_fsyncs",
                        "Innodb_data_pending_reads",
                        "Innodb_data_pending_writes",
                        "Innodb_log_write_requests",
                        "Innodb_os_log_fsyncs",
                        "Innodb_os_log_pending_fsyncs",
                        "Innodb_os_log_pending_writes",
                        "Innodb_os_log_written",
                        "Innodb_rows_read",
                        "Qcache_hits",
                        "Qcache_free_memory",
                        "Qcache_not_cached",
                        "Qcache_queries_in_cache",
                        "Qcache_free_blocks",
                        "Qcache_inserts",
                        "Qcache_lowmem_prunes",
                        "Qcache_total_blocks",
                        "Connection_errors_max_connections",
                        "max_connections",
                        "Select_full_join",
                        "Select_full_range_join",
                        "Select_range",
                        "Select_range_check",
                        "Select_scan",
                        "Max_execution_time_exceeded",
                        "Open_files",
                        "Table_open_cache_hits",
                        "Table_open_cache_misses",
                        "Table_open_cache_overflows",
                        "Prepared_stmt_count",
                        "Sort_merge_passes",
                        "Sort_range",
                        "Sort_rows",
                        "Sort_scan",
                        "Key_read_requests",
                        "Key_write_requests"
                    ]
                }
            }
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = f"Metric collection error: {e}\n{traceback.format_exc()}"
        finally:
            self.close()
        return self.maindata
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=MYSQL_DEFAULTS["host"])
    parser.add_argument("--port", default=MYSQL_DEFAULTS["port"])
    parser.add_argument("--username", default=MYSQL_DEFAULTS["username"])
    parser.add_argument("--password", default=MYSQL_DEFAULTS["password"])

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    
    args = parser.parse_args()
    monitor = MySQLMonitor(args)
    result = monitor.collect_metrics()
    print(json.dumps(result, indent=2))
