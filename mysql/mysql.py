#!/usr/bin/python3
import json
import pymysql
import traceback
from decimal import Decimal
# import psutil
# HAS_PSUTIL = True
HAS_PSUTIL = False
PLUGIN_VERSION = "1"
HEARTBEAT = True
MYSQL_DEFAULTS = {
    "host": "localhost",
    "port": 3306,
    "username": "site24x7",
    "password": "StrongPassword123!"
}
METRICS_UNITS = {
    "Uptime": "seconds",
    "Connection_usage": "%",
    "Open_files_usage": "%",
    "Open_tables": "units",
    "threads_running": "units",
    "Innodb_buffer_pool_wait_free": "units",
    "Innodb_buffer_pool_pages_flushed": "units",
    "Innodb_buffer_pool_read_ahead_evicted": "units",
    "Innodb_buffer_pool_read_ahead": "units",
    "Innodb_buffer_pool_read_ahead_rnd": "units",
    "Innodb_buffer_pool_read_requests": "units",
    "Innodb_data_fsyncs": "units",
    "Innodb_data_pending_fsyncs": "units",
    "Innodb_data_pending_reads": "units",
    "Innodb_data_pending_writes": "units",
    "Innodb_log_write_requests": "units",
    "Innodb_os_log_fsyncs": "units",
    "Innodb_os_log_pending_fsyncs": "units",
    "Innodb_os_log_pending_writes": "units",
    "Innodb_os_log_written": "units",
    "Innodb_rows_read": "units",
    "Qcache_hits": "units",
    "Qcache_free_memory": "bytes",
    "Qcache_not_cached": "units",
    "Qcache_queries_in_cache": "units",
    "Qcache_free_blocks": "units",
    "Qcache_inserts": "units",
    "Qcache_lowmem_prunes": "units",
    "Qcache_total_blocks": "units",
    "Connection_errors_max_connections": "units",
    # Added metrics for displayed database table
    "Fetch_Latency_ms": "ms",
    "Insert_Latency_ms": "ms",
    "Throughput_qps": "queries/s",
    "Queries_executed": "units",
    "Errors": "units",
    # Added ManageEngine metrics with direct SQL access (examples)
    "Version": "text",
    "Type_Instance": "text",
    "Connections_attempted": "count",
    "Table_open_cache_hit_ratio": "%",
    "Buffer_pool_utilization": "%",
    "Threads_connected": "count",
    "Threads_running": "count",
    "Threads_cached": "count",
    "Threads_created": "count",
    "Update_command": "count",
    "Insert_command": "count",
    "Insert_select_command": "count",
    "Delete_command": "count",
    "Create_db_command": "count",
    "Drop_db_command": "count",
    "Drop_table_command": "count",
    "Alter_table_command": "count",
    "Binlog_command": "count",
    "Load_command": "count",
    "Replace_command": "count",
    "Replace_select_command": "count",
    "Select_command": "count",
    "Shutdown_command": "count",
    "Group_replication_start_command": "count",
    "Group_replication_stop_command": "count",
    "Slave_start_command": "count",
    "Slave_stop_command": "count",
    "Change_master_command": "count",
    "Revoke_command": "count",
    "Revoke_all_command": "count",
    "Rollback_command": "count",
    "Rollback_to_savepoint_command": "count",
    "Savepoint_command": "count",
    "Handler_external_lock": "count",
    "Handler_savepoint": "count",
    "Handler_savepoint_rollback": "count",
    "Binlog_stmt_cache_use": "count",
    "Binlog_stmt_cache_disk_use": "count",
    "Binlog_size": "bytes",
    "Binlog_file_count": "count",
    "Relay_log_size": "bytes",
    "Relay_log_file_count": "count",
    "InnoDB_active_transactions": "count",
    "InnoDB_locked_transactions": "count",
    "InnoDB_current_transactions": "count",
    "InnoDB_history_list_length": "count",
    "InnoDB_lock_structs": "count",
    "InnoDB_tables_in_use": "count",
    "InnoDB_locked_tables": "count",
    # Existing nested units
    "Database": {
        "Db_size_MB": "MB",
        "Index_MB": "MB",
        "Fetch_Latency_ms": "ms",
        "Insert_Latency_ms": "ms",
        "Throughput_qps": "queries/s",
        "Queries_executed": "units",
        "Errors": "units"
    },
    "Session": {
        "Lock_Latency": "ms",
        # "CPU": "s",  # Commented out as requested
        # "Memory": "KB"  # Commented out as requested
    }
}
METRICS_MAPPING = {
    "Database": [
        "name", "Db_size_MB", "Index_MB", "Number_of_Tables", "status", "Open_tables",
        "Fetch_Latency_ms", "Insert_Latency_ms", "Throughput_qps", "Queries_executed", "Errors"
    ],
    "Session": [
        "name", "User", "db",
        # "Memory",  # Commented out as requested
        # "CPU",     # Commented out as requested
        "Lock_Latency"
    ],
    "Threads": [
        "Threads_running",
        "Threads_connected",
        "Threads_cached",
        "Threads_created",
        "Aborted_clients",
        "Aborted_connects",
        "Max_used_connections",
        "Connections",
        "threads_running"  # from old name compatibility
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
        # Added missing old metrics
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
            "units": METRICS_UNITS,
            "tabs": {
                "Database and Session": {
                    "order": 1,
                    "tablist": ["Database", "Session"]
                },
                "Threads": {
                    "order": 2,
                    "tablist": METRICS_MAPPING["Threads"]
                },
                "Handler": {
                    "order": 3,
                    "tablist": METRICS_MAPPING["Handler"]
                },
                "Query and Storage": {
                    "order": 4,
                    "tablist": METRICS_MAPPING["Query and Storage"]
                }
            }
        }
        self.connection = None
        self.cursor = None
    def safe_int(self, val):
        try:
            return int(val)
        except Exception:
            return 0
    def safe_float(self, val):
        try:
            return float(val)
        except Exception:
            return 0.0
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
                autocommit=True,
                connect_timeout=10
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            self.maindata["availability"] = 0
            self.maindata["msg"] = f"Connection error: {repr(e)}"
            return False
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception:
            pass
    def collect_database(self):
        dbs = []
        try:
            # Collect base db info
            self.cursor.execute("""
                SELECT table_schema AS name,
                       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS Db_size_MB,
                       ROUND(SUM(index_length) / 1024 / 1024, 2) AS Index_MB,
                       COUNT(table_name) AS Number_of_Tables,
                       1 AS status
                FROM information_schema.tables
                WHERE table_schema NOT IN ('mysql', 'performance_schema', 'sys', 'information_schema')
                GROUP BY table_schema
                LIMIT 25
            """)
            db_size_info = {row["name"]: row for row in self.cursor.fetchall()}
            # Fetch Latency (average SELECT latency in ms)
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
            # Insert Latency (average INSERT latency in ms)
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
            # Throughput (queries per second) calculated over uptime
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions'")
            questions_row = self.cursor.fetchone()
            questions = int(questions_row['Value']) if questions_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Uptime'")
            uptime_row = self.cursor.fetchone()
            uptime = int(uptime_row['Value']) if uptime_row else 1  # avoid zero division
            throughput_qps = round(questions / uptime, 2) if uptime > 0 else 0.0
            # Queries executed - total queries count
            queries_executed = questions
            # Errors - sum of errors from SHOW GLOBAL STATUS variables related
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Errors'")
            errors_row = self.cursor.fetchone()
            errors = int(errors_row['Value']) if errors_row else 0
            # Additional ManageEngine metrics examples fetched by direct SQL queries
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
            # Buffer Pool Utilization: sum dirty+clean pages / total pages * 100
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_data'")
            pages_data_row = self.cursor.fetchone()
            pages_data = int(pages_data_row['Value']) if pages_data_row else 0
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_total'")
            pages_total_row = self.cursor.fetchone()
            pages_total = int(pages_total_row['Value']) if pages_total_row else 0
            buffer_pool_utilization = 0.0
            if pages_total > 0:
                buffer_pool_utilization = round((pages_data / pages_total) * 100, 2)
            # Add fetched metrics to each DB record as demo; generally these are global but added for visibility
            for dbname, dbdata in db_size_info.items():
                rec = {
                    "name": dbname,
                    "Db_size_MB": self.to_str(dbdata.get("Db_size_MB", 0)),
                    "Index_MB": self.to_str(dbdata.get("Index_MB", 0)),
                    "Number_of_Tables": self.to_str(dbdata.get("Number_of_Tables", 0)),
                    "status": 1,
                    "Open_tables": "0",
                    "Fetch_Latency_ms": self.to_str(fetch_latency),
                    "Insert_Latency_ms": self.to_str(insert_latency),
                    "Throughput_qps": self.to_str(throughput_qps),
                    "Queries_executed": str(queries_executed),
                    "Errors": str(errors),
                    "Version": version,
                    "Connections_attempted": str(connections_attempted),
                    "Threads_connected": str(threads_connected),
                    "Table_open_cache_hit_ratio": str(table_open_cache_hit_ratio),
                    "Buffer_pool_utilization": str(buffer_pool_utilization)
                }
                dbs.append(rec)
        except Exception as e:
            self.maindata["availability"] = 0
            self.maindata["msg"] = f"Database collection error: {e}"
        return dbs
    def collect_session(self):
        sess = []
        try:
            self.cursor.execute("""
                SELECT THREAD_ID, PROCESSLIST_ID
                FROM performance_schema.threads
                WHERE TYPE = 'FOREGROUND'
            """)
            thread_pid_map = {r["THREAD_ID"]: r["PROCESSLIST_ID"] for r in self.cursor.fetchall()}
            self.cursor.execute("SHOW FULL PROCESSLIST")
            sessions = self.cursor.fetchall()
            pid_idx_map = {}
            count = 0
            for s in sessions:
                if count >= 25:
                    break
                pid = s.get("Id", 0)
                pid_str = f"PID_{pid}"
                rec = {
                    "name": pid_str,
                    "User": str(s.get("User") or ""),
                    "db": str(s.get("db") or ""),
                    # "Memory": "0.00",  # commented as requested
                    # "CPU": "0.00",     # commented as requested
                    "Lock_Latency": self.to_str(s.get("Time", 0))
                }
                sess.append(rec)
                pid_idx_map[pid] = count
                count += 1
        except Exception as e:
            self.maindata["availability"] = 0
            self.maindata["msg"] = f"Session collection error: {e}"
        return sess
    def collect_performance(self):
        perf = {}
        try:
            self.cursor.execute("""
                SELECT digest_text, count_star, sum_timer_wait, avg_timer_wait
                FROM performance_schema.events_statements_summary_by_digest
                ORDER BY count_star DESC
                LIMIT 10
            """)
            rows = self.cursor.fetchall()
            for i, row in enumerate(rows, 1):
                perf[f"PS_{i}_count"] = self.safe_int(row.get("count_star", 0))
                perf[f"PS_{i}_sum_timer"] = self.safe_float(row.get("sum_timer_wait", 0.0))
                perf[f"PS_{i}_avg_timer"] = self.safe_float(row.get("avg_timer_wait", 0.0))
        except Exception as e:
            perf["perf_error"] = f"Performance collection error: {e}"
        return perf
    def collect_metrics(self):
        if not self.connect():
            return self.maindata
        try:
            self.cursor.execute("SHOW GLOBAL STATUS")
            status = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
            self.cursor.execute("SHOW GLOBAL VARIABLES")
            variables = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
            # Add Uptime explicitly
            self.maindata["Uptime"] = self.to_str(status.get("Uptime", 0))
            # Add threads_running old metric name as well
            self.maindata["threads_running"] = self.to_str(status.get("Threads_running", 0))
            for tab_name in ["Threads", "Handler", "Query and Storage"]:
                for metric in METRICS_MAPPING[tab_name]:
                    val = status.get(metric) or variables.get(metric)
                    if val is not None:
                        self.maindata[metric] = self.to_str(val)
            max_used = status.get("Max_used_connections")
            self.maindata["Max_used_connections"] = self.to_str(int(max_used)) if max_used else "0.00"
            max_conn = int(variables.get("max_connections", "0"))
            threads = int(status.get("Threads_running", "0"))
            open_files = int(status.get("Open_files", "0"))
            open_files_limit = int(variables.get("open_files_limit", "0"))
            self.maindata["Connection_usage"] = self.to_str(round(threads / max_conn * 100, 2)) if max_conn else "0.00"
            self.maindata["Open_files_usage"] = self.to_str(round(open_files / open_files_limit * 100, 2)) if open_files_limit else "0.00"
            self.maindata["Database"] = self.collect_database()
            self.maindata["Session"] = self.collect_session()
            self.maindata["s247config"] = {
                "childdiscovery": ["Session", "Database"]
            }
            perf = self.collect_performance()
            self.maindata.update(perf)
            self.close()
            return self.maindata
        except Exception as e:
            self.maindata["availability"] = 0
            self.maindata["msg"] = f"Metric collection error: {e}\n{traceback.format_exc()}"
            self.close()
            return self.maindata
def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(i) for i in obj]
    if isinstance(obj, Decimal):
        return float(obj)
    return obj
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=MYSQL_DEFAULTS["host"])
    parser.add_argument("--port", default=MYSQL_DEFAULTS["port"])
    parser.add_argument("--username", default=MYSQL_DEFAULTS["username"])
    parser.add_argument("--password", default=MYSQL_DEFAULTS["password"])
    args = parser.parse_args()
    monitor = MySQLMonitor(args)
    result = monitor.collect_metrics()
    result = normalize(result)
    print(json.dumps(result, indent=2))
