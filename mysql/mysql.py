#!/usr/bin/python3
import json
import pymysql
import traceback
PLUGIN_VERSION = "1"
HEARTBEAT = True

MYSQL_DEFAULTS = {
    "host": "localhost",
    "port": 3306,
    "username": "site24x7",
    "password": "site24x7",
    "logs_enabled": True,
    "log_type_name": "Mysql General Logs",
    "log_file_path": "/var/log/mysql/error.log"
}
METRICS_UNITS = {
    "Uptime": "seconds",
    "Connection_usage": "%",
    "Open_files_usage": "%",
    "Fetch_Latency_ms": "ms",
    "Insert_Latency_ms": "ms",
    "Throughput_qps": "queries/s",
    "Table_open_cache_hit_ratio": "%",
    "Buffer_pool_utilization": "%",
    "Seconds_behind_master": "seconds",
    "Relay_log_space": "bytes",
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
        "open_files_limit",
        "Open_files",
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
    def __init__(self,host,port,username,password,logs_enabled,log_type_name,log_file_path):
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.logs_enabled = logs_enabled
        self.log_type_name = log_type_name
        self.log_file_path = log_file_path
        self.maindata = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            
        }

        applog={}
        if(self.logs_enabled in ['True', 'true', '1']):
            applog["logs_enabled"]=True
            applog["log_type_name"]=self.log_type_name
            applog["log_file_path"]=self.log_file_path
        else:
            applog["logs_enabled"]=False
        self.maindata['applog'] = applog
        self.connection = None
        self.cursor = None
        
    def to_str(self, val):
        try:
            f = float(val)
            return "{:.2f}".format(f)
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
            self.maindata["msg"] = "Connection error: {}".format(repr(e))
            return False
        
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            pass

    def collect_database(self):
        dbs = []
        db_size_info = {}
        
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
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Database size query error: {}; ".format(str(e))
            db_size_info = {}
        
        fetch_latency = 0.0
        try:
            self.cursor.execute("""
                SELECT ROUND(IFNULL(AVG_TIMER_WAIT/1000000000, 0)*1000, 2) AS avg_fetch_latency_ms
                FROM performance_schema.events_statements_summary_by_digest
                WHERE digest_text LIKE 'select%%' AND SCHEMA_NAME IS NOT NULL
                LIMIT 1
            """)
            r = self.cursor.fetchone()
            if r and "avg_fetch_latency_ms" in r:
                fetch_latency = float(r["avg_fetch_latency_ms"])
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Fetch latency query error: {}; ".format(str(e))
            fetch_latency = -1

        insert_latency = 0.0
        try:
            self.cursor.execute("""
                SELECT ROUND(IFNULL(AVG_TIMER_WAIT/1000000000, 0)*1000, 2) AS avg_insert_latency_ms
                FROM performance_schema.events_statements_summary_by_digest
                WHERE digest_text LIKE 'insert%%' AND SCHEMA_NAME IS NOT NULL
                LIMIT 1
            """)
            r = self.cursor.fetchone()
            if r and "avg_insert_latency_ms" in r:
                insert_latency = float(r["avg_insert_latency_ms"])
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Insert latency query error: {}; ".format(str(e))
            insert_latency = -1

        questions = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions'")
            questions_row = self.cursor.fetchone()
            questions = int(questions_row['Value']) if questions_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Questions query error: {}; ".format(str(e))
            questions = -1

        uptime = 1
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Uptime'")
            uptime_row = self.cursor.fetchone()
            uptime = int(uptime_row['Value']) if uptime_row else 1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Uptime query error: {}; ".format(str(e))
            uptime = -1 

        throughput_qps = 0.0
        if questions > 0 and uptime > 0:
            throughput_qps = round(questions / uptime, 2)
        elif questions == -1 or uptime == -1:
            throughput_qps = -1
        queries_executed = questions
        
        errors = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Errors'")
            errors_row = self.cursor.fetchone()
            errors = int(errors_row['Value']) if errors_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Errors query error: {}; ".format(str(e))
            errors = -1
            
        version = ""
        try:
            self.cursor.execute("SELECT VERSION() AS version")
            version_row = self.cursor.fetchone()
            version = version_row.get("version", "") if version_row else ""
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Version query error: {}; ".format(str(e))
            version = "-"
            
        connections_attempted = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Connections'")
            connections_attempted_row = self.cursor.fetchone()
            connections_attempted = int(connections_attempted_row['Value']) if connections_attempted_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Connections query error: {}; ".format(str(e))
            connections_attempted = -1
            
        threads_connected = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Threads_connected'")
            threads_connected_row = self.cursor.fetchone()
            threads_connected = int(threads_connected_row['Value']) if threads_connected_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Threads_connected query error: {}; ".format(str(e))
            threads_connected = -1
            
        table_open_cache_hits = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Table_open_cache_hits'")
            table_open_cache_hits_row = self.cursor.fetchone()
            table_open_cache_hits = int(table_open_cache_hits_row['Value']) if table_open_cache_hits_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Table_open_cache_hits query error: {}; ".format(str(e))
            table_open_cache_hits = -1
            
        table_open_cache_misses = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Table_open_cache_misses'")
            table_open_cache_misses_row = self.cursor.fetchone()
            table_open_cache_misses = int(table_open_cache_misses_row['Value']) if table_open_cache_misses_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Table_open_cache_misses query error: {}; ".format(str(e))
            table_open_cache_misses = -1
            
        table_open_cache_hit_ratio = 0.0
        if table_open_cache_hits >= 0 and table_open_cache_misses >= 0:
            total = table_open_cache_hits + table_open_cache_misses
            if total > 0:
                table_open_cache_hit_ratio = round((table_open_cache_hits / total) * 100, 2)
        else:
            table_open_cache_hit_ratio = -1
            
        pages_data = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_data'")
            pages_data_row = self.cursor.fetchone()
            pages_data = int(pages_data_row['Value']) if pages_data_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Innodb_buffer_pool_pages_data query error: {}; ".format(str(e))
            pages_data = -1
            
        pages_total = 0
        try:
            self.cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_total'")
            pages_total_row = self.cursor.fetchone()
            pages_total = int(pages_total_row['Value']) if pages_total_row else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Innodb_buffer_pool_pages_total query error: {}; ".format(str(e))
            pages_total = -1
            
        buffer_pool_utilization = 0.0
        if pages_data >= 0 and pages_total > 0:
            buffer_pool_utilization = round((pages_data / pages_total) * 100, 2)
        elif pages_data == -1 or pages_total == -1:
            buffer_pool_utilization = -1
        for dbname, dbdata in db_size_info.items():
            rec = {
                "name": dbname,
                "Db_size_MB": self.to_str(dbdata.get("Db_size_MB", 0)),
                "Index_MB": self.to_str(dbdata.get("Index_MB", 0)),
                "Number_of_Tables": self.to_str(dbdata.get("Number_of_Tables", 0)),
                "Fetch_Latency_ms": self.to_str(fetch_latency),
                "Insert_Latency_ms": self.to_str(insert_latency),
                "Throughput_qps": self.to_str(throughput_qps),
                "Queries_executed": str(queries_executed) if queries_executed != -1 else "-1",
                "Errors": str(errors) if errors != -1 else "-1",
                
                # "Version": version,
                # "Connections_attempted": str(connections_attempted),
                # "Threads_connected": str(threads_connected),
                # "Table_open_cache_hit_ratio": str(table_open_cache_hit_ratio),
                # "Buffer_pool_utilization": str(buffer_pool_utilization)
            }
            dbs.append(rec)
        return dbs
    
    def collect_sessions(self):
        sessions = {
            "total_sessions": -1,
            "active_sessions": -1,
            "idle_sessions": -1,
            "killed_sessions": -1
        }
        
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
            if row:
                sessions = {
                    "total_sessions": int(row.get('total_sessions', 0)),
                    "active_sessions": int(row.get('active_sessions', 0)),
                    "idle_sessions": int(row.get('idle_sessions', 0)),
                    "killed_sessions": int(row.get('killed_sessions', 0)) if row.get('killed_sessions') is not None else 0
                }
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Session collection error: {}; ".format(str(e))
            
        return sessions

    def collect_replication_status(self):
        """Collect MySQL replication status metrics"""
        replication_data = {}
        
        try:
            try:
                self.cursor.execute("SHOW REPLICA STATUS")
                replica_status = self.cursor.fetchone()
            except Exception:
                try:
                    self.cursor.execute("SHOW SLAVE STATUS")
                    replica_status = self.cursor.fetchone()
                except Exception as e:
                    if "msg" not in self.maindata:
                        self.maindata["msg"] = ""
                    self.maindata["msg"] += "Replication status query error: {}; ".format(str(e))
                    return replication_data
            
            if replica_status:
                replication_mapping = {
                    "Slave_running": "Replica_IO_Running" if "Replica_IO_Running" in replica_status else "Slave_IO_Running",
                    "Slave_sql_running": "Replica_SQL_Running" if "Replica_SQL_Running" in replica_status else "Slave_SQL_Running", 
                    "Slave_io_running": "Replica_IO_Running" if "Replica_IO_Running" in replica_status else "Slave_IO_Running",
                    "Seconds_behind_master": "Seconds_Behind_Source" if "Seconds_Behind_Source" in replica_status else "Seconds_Behind_Master",
                    "Relay_log_space": "Relay_Log_Space",
                    "Master_host": "Source_Host" if "Source_Host" in replica_status else "Master_Host",
                    "Master_user": "Source_User" if "Source_User" in replica_status else "Master_User",
                    "Master_retry_count": "Source_Retry_Count" if "Source_Retry_Count" in replica_status else "Master_Retry_Count",
                    "Skip_counter": "Skip_Counter"
                }
                
                for metric_name, status_field in replication_mapping.items():
                    try:
                        value = replica_status.get(status_field)
                        if value is not None:
                            if metric_name in ["Slave_running", "Slave_sql_running", "Slave_io_running"]:
                                if str(value).upper() == "YES":
                                    replication_data[metric_name] = "1"  # True
                                elif str(value).upper() == "NO":
                                    replication_data[metric_name] = "0"  # False
                                else:
                                    replication_data[metric_name] = str(value)
                            else:
                                replication_data[metric_name] = self.to_str(value)
                        else:
                            # Return appropriate default based on metric type
                            if metric_name in ["Master_host", "Master_user"]:
                                replication_data[metric_name] = "-"  # String metrics
                            else:
                                replication_data[metric_name] = "-1"  # Numeric metrics
                    except Exception as e:
                        if "msg" not in self.maindata:
                            self.maindata["msg"] = ""
                        self.maindata["msg"] += "Replication metric {} error: {}; ".format(metric_name, str(e))
                        # Return appropriate error value based on metric type
                        if metric_name in ["Master_host", "Master_user"]:
                            replication_data[metric_name] = "-"  # String metrics
                        else:
                            replication_data[metric_name] = "-1"  # Numeric metrics
            else:
                for metric_name in ["Slave_running", "Slave_sql_running", "Slave_io_running", 
                                  "Seconds_behind_master", "Relay_log_space", "Master_host", 
                                  "Master_user", "Master_retry_count", "Skip_counter"]:
                    # Return appropriate default based on metric type
                    if metric_name in ["Master_host", "Master_user"]:
                        replication_data[metric_name] = "-"  # String metrics
                    else:
                        replication_data[metric_name] = "-1"  # Numeric metrics
                    
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Replication collection error: {}; ".format(str(e))
            for metric_name in ["Slave_running", "Slave_sql_running", "Slave_io_running", 
                              "Seconds_behind_master", "Relay_log_space", "Master_host", 
                              "Master_user", "Master_retry_count", "Skip_counter"]:
                # Return appropriate error value based on metric type
                if metric_name in ["Master_host", "Master_user"]:
                    replication_data[metric_name] = "-"  # String metrics
                else:
                    replication_data[metric_name] = "-1"  # Numeric metrics
        
        return replication_data

    def collect_metrics(self):
        if not self.connect():
            return self.maindata
            
        status = {}
        variables = {}
        
        try:
            self.cursor.execute("SHOW GLOBAL STATUS")
            status = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "SHOW GLOBAL STATUS error: {}; ".format(str(e))
            status = {}
            
        try:
            self.cursor.execute("SHOW GLOBAL VARIABLES")
            variables = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "SHOW GLOBAL VARIABLES error: {}; ".format(str(e))
            variables = {}
            
        try:
            uptime_val = status.get("Uptime", "0")
            try:
                self.maindata["Uptime"] = self.to_str(uptime_val)
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Uptime conversion error: {}; ".format(str(e))
                self.maindata["Uptime"] = "-1"
                
            try:
                replication_data = self.collect_replication_status()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Replication data collection error: {}; ".format(str(e))
                replication_data = {}
            
            replication_metrics = {
                "Slave_running", "Slave_sql_running", "Slave_io_running", 
                "Seconds_behind_master", "Relay_log_space", "Master_host", 
                "Master_user", "Master_retry_count", "Skip_counter"
            }
            
            for tab_name in ["Threads", "Handler", "Query and Storage"]:
                for metric in METRICS_MAPPING[tab_name]:
                    try:
                        if metric in replication_metrics:
                            val = replication_data.get(metric, "-")
                            display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                            self.maindata[display_name] = val
                        else:
                            val = status.get(metric) or variables.get(metric)
                            if val is not None:
                                display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                                self.maindata[display_name] = self.to_str(val)
                            else:
                                display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                                # Most metrics are numeric, return -1 for missing values
                                self.maindata[display_name] = "-1"
                    except Exception as e:
                        if "msg" not in self.maindata:
                            self.maindata["msg"] = ""
                        self.maindata["msg"] += "Metric {} collection error: {}; ".format(metric, str(e))
                        display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                        # Most metrics are numeric, return -1 for errors
                        self.maindata[display_name] = "-1"
            try:
                max_used = status.get("Max_used_connections")
                self.maindata["Max_used_connections"] = self.to_str(int(max_used)) if max_used else "0.00"
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Max_used_connections calculation error: {}; ".format(str(e))
                self.maindata["Max_used_connections"] = "-1"
            try:
                max_conn = int(variables.get("max_connections", "0"))
                threads = int(status.get("Threads_running", "0"))
                self.maindata["Connection_usage"] = self.to_str(round(threads / max_conn * 100, 2)) if max_conn else "0.00"
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Connection_usage calculation error: {}; ".format(str(e))
                self.maindata["Connection_usage"] = "-1"
                
            try:
                open_files = int(status.get("Open_files", "0"))
                open_files_limit = int(variables.get("open_files_limit", "0"))
                self.maindata["Open_files_usage"] = self.to_str(round(open_files / open_files_limit * 100, 2)) if open_files_limit else "0.00"
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Open_files_usage calculation error: {}; ".format(str(e))
                self.maindata["Open_files_usage"] = "-1"
            try:
                self.maindata["Database"] = self.collect_database()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Database collection error: {}; ".format(str(e))
                self.maindata["Database"] = []
                
            try:
                session_stats = self.collect_sessions()
                if session_stats: 
                    self.maindata["total_sessions"] = session_stats["total_sessions"]
                    self.maindata["active_sessions"] = session_stats["active_sessions"]
                    self.maindata["idle_sessions"] = session_stats["idle_sessions"]
                    self.maindata["killed_sessions"] = session_stats["killed_sessions"]
                else:
                    self.maindata["total_sessions"] = -1
                    self.maindata["active_sessions"] = -1
                    self.maindata["idle_sessions"] = -1
                    self.maindata["killed_sessions"] = -1
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Session stats collection error: {}; ".format(str(e))
                self.maindata["total_sessions"] = -1
                self.maindata["active_sessions"] = -1
                self.maindata["idle_sessions"] = -1
                self.maindata["killed_sessions"] = -1
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
                        "open_files_limit",
                        "Open_files",
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
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Metric collection error: {}; ".format(str(e))
        finally:
            self.close()
        return self.maindata
    
def run(param={}):
    mysql_params = {**MYSQL_DEFAULTS, **param}
    mysql_params = {
    k: (v.strip('\'"') if isinstance(v, str) else v)
    for k, v in mysql_params.items()
    }
    monitor = MySQLMonitor(**mysql_params)
    result = monitor.collect_metrics()
    return result
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=MYSQL_DEFAULTS["host"])
    parser.add_argument('--port',help="Port",nargs='?', default= MYSQL_DEFAULTS["port"], type=int)
    parser.add_argument("--username", default=MYSQL_DEFAULTS["username"])
    parser.add_argument("--password", default=MYSQL_DEFAULTS["password"])

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default=MYSQL_DEFAULTS["logs_enabled"])
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=MYSQL_DEFAULTS["log_type_name"])
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=MYSQL_DEFAULTS["log_file_path"])
    
    args = parser.parse_args()
    monitor = MySQLMonitor(args.host, args.port, args.username, args.password, args.logs_enabled, args.log_type_name, args.log_file_path)
    result = monitor.collect_metrics()

    print(json.dumps(result, indent=2))
