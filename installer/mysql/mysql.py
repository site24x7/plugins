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
    "Seconds_behind_master": "seconds",
    "Connection_usage": "%",
    "Open_files_usage": "%",
    "Table_open_cache_hit_ratio": "%",
    "Buffer_pool_utilization": "%",
    "Fetch_Latency_ms": "ms",
    "Insert_Latency_ms": "ms",
    "Throughput_qps": "queries/s",
    "Bytes_received": "bytes",
    "Bytes_sent": "bytes",
    "Relay_log_space": "bytes",
    "Database": {
        "Db_size_MB": "MB",
        "Index_MB": "MB",
    }
}

STATUS_METRICS = [
    "Threads_running", "Threads_connected", "Threads_cached", "Threads_created",
    "Aborted_clients", "Aborted_connects", "Max_used_connections", "Connections",
    
    "Com_select", "Com_insert", "Com_update", "Com_delete", "Com_replace", "Com_load",
    "Handler_read_first", "Handler_read_key", "Handler_read_rnd", "Handler_read_rnd_next",
    "Handler_write", "Handler_update", "Handler_delete", "Handler_commit", "Handler_rollback",
    "Com_delete_multi", "Com_insert_select", "Com_replace_select", "Com_update_multi",
    
    "Queries", "Questions", "Slow_queries", "Opened_tables", "Opened_files",
    "Binlog_cache_use", "Binlog_cache_disk_use", "Bytes_received", "Bytes_sent",
    "Com_commit", "Com_rollback", "Table_locks_waited", "Table_locks_immediate",
    "Created_tmp_files", "Created_tmp_tables", "Created_tmp_disk_tables",
    
    "Innodb_buffer_pool_pages_data", "Innodb_buffer_pool_pages_dirty", "Innodb_buffer_pool_pages_free",
    "Innodb_rows_deleted", "Innodb_rows_inserted", "Innodb_rows_updated",
    "Innodb_buffer_pool_pages_total", "Innodb_pages_read", "Innodb_pages_written",
    "Innodb_log_writes", "Innodb_log_waits", "Innodb_buffer_pool_reads",
    "Innodb_buffer_pool_write_requests", "Innodb_data_reads", "Innodb_data_writes",
    "Innodb_pages_created", "Innodb_row_lock_time_avg", "Innodb_row_lock_time_max",
    "Innodb_row_lock_waits", "Innodb_buffer_pool_wait_free", "Innodb_buffer_pool_pages_flushed",
    "Innodb_buffer_pool_read_ahead_evicted", "Innodb_buffer_pool_read_ahead",
    "Innodb_buffer_pool_read_ahead_rnd", "Innodb_buffer_pool_read_requests",
    "Innodb_data_fsyncs", "Innodb_data_pending_fsyncs", "Innodb_data_pending_reads",
    "Innodb_data_pending_writes", "Innodb_log_write_requests", "Innodb_os_log_fsyncs",
    "Innodb_os_log_pending_fsyncs", "Innodb_os_log_pending_writes", "Innodb_os_log_written",
    "Innodb_rows_read",
    
    "Open_files", "Key_reads", "Key_writes", "Key_blocks_used",
    "Key_blocks_unused", "Key_blocks_not_flushed", "Connection_errors_max_connections",
    "Select_full_join", "Select_full_range_join", "Select_range",
    "Select_range_check", "Select_scan", "Max_execution_time_exceeded",
    "Table_open_cache_hits", "Table_open_cache_misses", "Table_open_cache_overflows",
    "Prepared_stmt_count", "Sort_merge_passes", "Sort_range", "Sort_rows", "Sort_scan",
    "Key_read_requests", "Key_write_requests"
]

VARIABLE_METRICS = [
    "open_files_limit", "max_connections"
]

REPLICATION_METRICS = [
    "Slave_running", "Slave_sql_running", "Slave_io_running", "Seconds_behind_master",
    "Relay_log_space", "Master_host", "Master_user", "Master_retry_count", "Skip_counter"
]


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
        self.maindata["Database"] = []
        
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

        for dbname, dbdata in db_size_info.items():
            rec = {
                "name": dbname,
                "Db_size_MB": str(dbdata.get("Db_size_MB", 0)),
                "Index_MB": str(dbdata.get("Index_MB", 0)),
                "Number_of_Tables": str(dbdata.get("Number_of_Tables", 0)),
            }
            dbs.append(rec)
        
        self.maindata["Database"] = dbs
    
    def collect_sessions(self):

        self.maindata["total_sessions"] = -1
        self.maindata["active_sessions"] = -1
        self.maindata["idle_sessions"] = -1
        self.maindata["killed_sessions"] = -1
        
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
                self.maindata["total_sessions"] = int(row.get('total_sessions', 0)) if row.get('total_sessions') is not None else 0
                self.maindata["active_sessions"] = int(row.get('active_sessions', 0)) if row.get('active_sessions') is not None else 0
                self.maindata["idle_sessions"] = int(row.get('idle_sessions', 0)) if row.get('idle_sessions') is not None else 0
                self.maindata["killed_sessions"] = int(row.get('killed_sessions', 0)) if row.get('killed_sessions') is not None else 0
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Session collection error: {}; ".format(str(e))

    def collect_replication_status(self):
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
        
                    for metric_name in REPLICATION_METRICS:
                        if metric_name in ["Master_host", "Master_user"]:
                            self.maindata[metric_name] = "-"
                        else:
                            self.maindata[metric_name] = "-1"
                    return
            
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
                                    self.maindata[metric_name] = "1" 
                                elif str(value).upper() == "NO":
                                    self.maindata[metric_name] = "0"  
                                else:
                                    self.maindata[metric_name] = str(value)
                            else:
                                self.maindata[metric_name] = value
                        else:
                            if metric_name in ["Master_host", "Master_user"]:
                                self.maindata[metric_name] = "-" 
                            else:
                                self.maindata[metric_name] = "-1"  
                    except Exception as e:
                        if "msg" not in self.maindata:
                            self.maindata["msg"] = ""
                        self.maindata["msg"] += "Replication metric {} error: {}; ".format(metric_name, str(e))
                        if metric_name in ["Master_host", "Master_user"]:
                            self.maindata[metric_name] = "-"  
                        else:
                            self.maindata[metric_name] = "-1"
            else:
                for metric_name in REPLICATION_METRICS:
                    if metric_name in ["Master_host", "Master_user"]:
                        self.maindata[metric_name] = "-"  
                    else:
                        self.maindata[metric_name] = "-1"
                    
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Replication collection error: {}; ".format(str(e))
            for metric_name in REPLICATION_METRICS:
                if metric_name in ["Master_host", "Master_user"]:
                    self.maindata[metric_name] = "-"  
                else:
                    self.maindata[metric_name] = "-1"

    def get_mysql_status(self):
        try:
            self.cursor.execute("SHOW GLOBAL STATUS")
            status = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
            
        
            for metric in STATUS_METRICS:
                try:
                    if metric in status:
                        display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                        self.maindata[display_name] = status[metric]
                    else:
                        display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                        self.maindata[display_name] = "-1"
                except Exception as e:
                    if "msg" not in self.maindata:
                        self.maindata["msg"] = ""
                    self.maindata["msg"] += "Status metric {} collection error: {}; ".format(metric, str(e))
                    display_name = metric.replace("Com_", "Command_") if metric.startswith("Com_") else metric
                    self.maindata[display_name] = "-1"
            
        
            try:
                uptime_val = status.get("Uptime", "0")
                self.maindata["Uptime"] = uptime_val
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Uptime conversion error: {}; ".format(str(e))
                self.maindata["Uptime"] = "-1"
            
            return status
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "SHOW GLOBAL STATUS error: {}; ".format(str(e))
            return {}

    def get_mysql_variables(self):
        try:
            self.cursor.execute("SHOW GLOBAL VARIABLES")
            variables = {row["Variable_name"]: row["Value"] for row in self.cursor.fetchall()}
            
            for metric in VARIABLE_METRICS:
                try:
                    if metric in variables:
                        self.maindata[metric] = variables[metric]
                    else:
                        self.maindata[metric] = "-1"
                except Exception as e:
                    if "msg" not in self.maindata:
                        self.maindata["msg"] = ""
                    self.maindata["msg"] += "Variable metric {} collection error: {}; ".format(metric, str(e))
                    self.maindata[metric] = "-1"
            
            return variables
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "SHOW GLOBAL VARIABLES error: {}; ".format(str(e))
            return {}

    def collect_latency_metrics(self):
        
        try:
            
            self.cursor.execute("""
                SELECT 
                    ROUND(IFNULL(AVG(CASE WHEN UPPER(digest_text) LIKE 'SELECT %' 
                                     AND digest_text NOT LIKE '%SHOW%' 
                                     AND digest_text NOT LIKE '%performance_schema%'
                                     AND digest_text NOT LIKE '%information_schema%'
                                     THEN AVG_TIMER_WAIT/1000000000 END), 0)*1000, 2) AS avg_fetch_latency_ms,
                    ROUND(IFNULL(AVG(CASE WHEN UPPER(digest_text) LIKE 'INSERT %' 
                                     THEN AVG_TIMER_WAIT/1000000000 END), 0)*1000, 2) AS avg_insert_latency_ms,
                    COUNT(CASE WHEN UPPER(digest_text) LIKE 'SELECT %' 
                               AND digest_text NOT LIKE '%SHOW%' 
                               AND digest_text NOT LIKE '%performance_schema%'
                               AND digest_text NOT LIKE '%information_schema%'
                               THEN 1 END) AS select_count,
                    COUNT(CASE WHEN UPPER(digest_text) LIKE 'INSERT %' THEN 1 END) AS insert_count
                FROM performance_schema.events_statements_summary_by_digest
                WHERE digest_text IS NOT NULL 
                AND COUNT_STAR > 0
            """)
            r = self.cursor.fetchone()
            if r:
                
                select_count = r.get("select_count", 0) if r.get("select_count") is not None else 0
                insert_count = r.get("insert_count", 0) if r.get("insert_count") is not None else 0
                
                if select_count > 0 and r.get("avg_fetch_latency_ms") is not None:
                    self.maindata["Fetch_Latency_ms"] = float(r["avg_fetch_latency_ms"])
                else:
                    self.maindata["Fetch_Latency_ms"] = -1 
                    
                if insert_count > 0 and r.get("avg_insert_latency_ms") is not None:
                    self.maindata["Insert_Latency_ms"] = float(r["avg_insert_latency_ms"])
                else:
                    self.maindata["Insert_Latency_ms"] = -1 
                    
                if select_count == 0 and insert_count == 0:
                    if "msg" not in self.maindata:
                        self.maindata["msg"] = ""
                    self.maindata["msg"] += "No user SELECT/INSERT statements found in performance schema; "
            else:
                self.maindata["Fetch_Latency_ms"] = -1
                self.maindata["Insert_Latency_ms"] = -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Server latency query error: {}; ".format(str(e))
            self.maindata["Fetch_Latency_ms"] = -1
            self.maindata["Insert_Latency_ms"] = -1

    def collect_calculated_metrics(self, status, variables):

        try:
            max_used = status.get("Max_used_connections")
            self.maindata["Max_used_connections"] = max_used if max_used else "0"
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Max_used_connections calculation error: {}; ".format(str(e))
            self.maindata["Max_used_connections"] = "-1"
        
        try:
            max_conn = int(variables.get("max_connections", "0"))
            threads = int(status.get("Threads_running", "0"))
            self.maindata["Connection_usage"] = "{:.2f}".format(round(threads / max_conn * 100, 2)) if max_conn else "0.00"
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Connection_usage calculation error: {}; ".format(str(e))
            self.maindata["Connection_usage"] = "-1"
            
        try:
            open_files = int(status.get("Open_files", "0"))
            open_files_limit = int(variables.get("open_files_limit", "0"))
            self.maindata["Open_files_usage"] = "{:.2f}".format(round(open_files / open_files_limit * 100, 2)) if open_files_limit else "0.00"
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Open_files_usage calculation error: {}; ".format(str(e))
            self.maindata["Open_files_usage"] = "-1"
        
        try:
            questions = status.get('Questions', -1) if 'Questions' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Questions retrieval error: {}; ".format(str(e))
            questions = -1
            
        try:
            uptime = status.get('Uptime', -1) if 'Uptime' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Uptime retrieval error: {}; ".format(str(e))
            uptime = -1

        if questions != -1 and uptime != -1:
            try:
                throughput_qps = round(float(questions) / float(uptime), 2)
            except:
                throughput_qps = -1
        else:
            throughput_qps = -1
        
        self.maindata["Throughput_qps"] = throughput_qps
        self.maindata["Queries_executed"] = questions
        
        try:
            connections_attempted = status.get('Connections', -1) if 'Connections' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Connections retrieval error: {}; ".format(str(e))
            connections_attempted = -1
        
        self.maindata["Connections_attempted"] = connections_attempted
        
        try:
            table_open_cache_hits = status.get('Table_open_cache_hits', -1) if 'Table_open_cache_hits' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Table_open_cache_hits retrieval error: {}; ".format(str(e))
            table_open_cache_hits = -1
            
        try:
            table_open_cache_misses = status.get('Table_open_cache_misses', -1) if 'Table_open_cache_misses' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Table_open_cache_misses retrieval error: {}; ".format(str(e))
            table_open_cache_misses = -1
            
        if table_open_cache_hits != -1 and table_open_cache_misses != -1:
            try:
                total = float(table_open_cache_hits) + float(table_open_cache_misses)
                table_open_cache_hit_ratio = round((float(table_open_cache_hits) / total) * 100, 2)
            except:
                table_open_cache_hit_ratio = -1
        else:
            table_open_cache_hit_ratio = -1
        
        self.maindata["Table_open_cache_hit_ratio"] = table_open_cache_hit_ratio
        
        try:
            pages_data = status.get('Innodb_buffer_pool_pages_data', -1) if 'Innodb_buffer_pool_pages_data' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Innodb_buffer_pool_pages_data retrieval error: {}; ".format(str(e))
            pages_data = -1
            
        try:
            pages_total = status.get('Innodb_buffer_pool_pages_total', -1) if 'Innodb_buffer_pool_pages_total' in status else -1
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Innodb_buffer_pool_pages_total retrieval error: {}; ".format(str(e))
            pages_total = -1
            
        if pages_data != -1 and pages_total != -1:
            try:
                buffer_pool_utilization = round((float(pages_data) / float(pages_total)) * 100, 2)
            except:
                buffer_pool_utilization = -1
        else:
            buffer_pool_utilization = -1
        
        self.maindata["Buffer_pool_utilization"] = buffer_pool_utilization

    def collect_version_info(self):
        try:
            self.cursor.execute("SELECT VERSION() AS version")
            version_row = self.cursor.fetchone()
            version = version_row.get("version", "") if version_row else ""
            self.maindata["MySQL_Version"] = version if version else "-"
        except Exception as e:
            if "msg" not in self.maindata:
                self.maindata["msg"] = ""
            self.maindata["msg"] += "Version query error: {}; ".format(str(e))
            self.maindata["MySQL_Version"] = "-"

    def collect_metrics(self):
        if not self.connect():
            return self.maindata
            
        try:

            try:
                status = self.get_mysql_status()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "MySQL status collection error: {}; ".format(str(e))
                status = {}
                
            try:
                variables = self.get_mysql_variables()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "MySQL variables collection error: {}; ".format(str(e))
                variables = {}
            
            try:
                self.collect_replication_status()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Replication data collection error: {}; ".format(str(e))

            try:
                self.collect_calculated_metrics(status, variables)
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Calculated metrics collection error: {}; ".format(str(e))
            try:
                self.collect_database()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Database collection error: {}; ".format(str(e))

            try:
                self.collect_latency_metrics()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Latency metrics collection error: {}; ".format(str(e))

            try:
                self.collect_version_info()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Version collection error: {}; ".format(str(e))
                
            try:
                self.collect_sessions()
            except Exception as e:
                if "msg" not in self.maindata:
                    self.maindata["msg"] = ""
                self.maindata["msg"] += "Session stats collection error: {}; ".format(str(e))

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
                        "Fetch_Latency_ms",
                        "Insert_Latency_ms",
                        "Throughput_qps", 
                        "Queries_executed",
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
