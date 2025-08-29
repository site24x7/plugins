#!/usr/bin/python3
import json
import pymysql
import traceback
from decimal import Decimal

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
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
    "Connection_usage": "%",
    "Open_files_usage": "%",
    "Database": {
        "Db_size_MB": "MB",
        "Index_MB": "MB"
    },
    "Session": {
        "Lock_Latency": "ms",
        "CPU": "s",
        "Memory": "KB"
    }
}

METRICS_MAPPING = {
    "Database": ["name", "Db_size_MB", "Index_MB", "Number_of_Tables", "status"],
    "Session": ["name", "User", "db", "Memory", "CPU", "Lock_Latency"],
    "Threads": [
        "Threads_running", "Threads_connected", "Threads_cached",
        "Threads_created", "Aborted_clients", "Aborted_connects",
        "Max_used_connections", "Connections"
    ],
    "Handler": [
        "Com_select", "Com_insert", "Com_update", "Com_delete",
        "Com_replace", "Com_load", "Handler_read_first", "Handler_read_key",
        "Handler_read_rnd", "Handler_read_rnd_next", "Handler_write",
        "Handler_update", "Handler_delete", "Handler_commit", "Handler_rollback"
    ],
    "Query and Storage": [
        "Queries", "Questions", "Slow_queries", "Opened_tables", "Opened_files",
        "Binlog_cache_use", "Binlog_cache_disk_use", "Bytes_received", "Bytes_sent",
        "Com_commit", "Com_rollback", "Table_locks_waited", "Table_locks_immediate",
        "Created_tmp_files", "Created_tmp_tables", "Created_tmp_disk_tables",
        "Commands_per_second", "Avg_query_time", "Max_used_connections", "Connection_usage",
        "Open_files_usage", "Innodb_buffer_pool_pages_data", "Innodb_buffer_pool_pages_dirty",
        "Innodb_buffer_pool_pages_free", "Innodb_rows_deleted", "Innodb_rows_inserted",
        "Innodb_rows_updated", "Slave_running", "Slave_sql_running", "Slave_io_running",
        "Seconds_behind_master", "Relay_log_space", "Master_host", "Master_user",
        "Master_retry_count", "Skip_counter", "Open_files_limit", "Open_files_used",
        "Key_reads", "Key_writes", "Key_blocks_used", "Key_blocks_unused",
        "Key_blocks_not_flushed", "Innodb_buffer_pool_pages_total", "Innodb_pages_read",
        "Innodb_pages_written", "Innodb_log_writes", "Innodb_log_waits",
        "Innodb_buffer_pool_reads", "Innodb_buffer_pool_write_requests", "Innodb_data_reads",
        "Innodb_data_writes", "Innodb_pages_created", "Innodb_row_lock_time_avg",
        "Innodb_row_lock_time_max", "Innodb_row_lock_waits"
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
                "Threads": {"order": 2, "tablist": METRICS_MAPPING["Threads"]},
                "Handler": {"order": 3, "tablist": METRICS_MAPPING["Handler"]},
                "Query and Storage": {"order": 4, "tablist": METRICS_MAPPING["Query and Storage"]}
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
            for row in self.cursor.fetchall():
                dbs.append({k: self.to_str(v) if k != "name" else v for k, v in row.items()})
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
            proc = None
            if HAS_PSUTIL:
                try:
                    procs = [p for p in psutil.process_iter(['pid', 'name']) if 'mysqld' in (p.info.get('name', '') or '')]
                    pid = procs[0].pid if procs else None
                    proc = psutil.Process(pid) if pid else None
                except Exception:
                    proc = None
            pid_idx_map = {}
            count = 0
            for s in sessions:
                if count >= 25:
                    break
                pid = s.get("Id", 0)
                pid_str = f"PID_{pid}"
                rec = {
                    "name": pid_str,  # renamed from Id to name
                    "User": str(s.get("User") or ""),
                    "db": str(s.get("db") or ""),
                    # "Host": str(s.get("Host") or ""),  # commented intentionally
                    # "State": str(s.get("State") or ""),  # commented intentionally
                    "Memory": "0.00",
                    "CPU": "0.00",
                    "Lock_Latency": self.to_str(s.get("Time", 0))
                }
                sess.append(rec)
                pid_idx_map[pid] = count
                count += 1
            if proc:
                for thread in proc.threads():
                    tid = thread.id
                    if tid in thread_pid_map:
                        sid = thread_pid_map[tid]
                        if sid in pid_idx_map:
                            idx = pid_idx_map[sid]
                            sess[idx]["CPU"] = self.to_str(round(thread.user_time + thread.system_time, 2))
                            sess[idx]["Memory"] = self.to_str(int(proc.memory_info().rss / 1024))
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
                "childdiscovery": ["Session"]
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

