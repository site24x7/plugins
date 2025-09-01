#!/home/mani-22230/plugins/installer/monagent/.plugin-venv/bin/python
"""
Site24x7 MySql table stats Plugin
"""
import traceback
import re
import json
import os

VERSION_QUERY = 'SELECT VERSION()'

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
MYSQL_HOST = "localhost"

MYSQL_PORT="3306"

MYSQL_USERNAME="user"
MYSQL_PASSWORD=""

METRICS_JSON={
    "Uptime":"uptime",
    "Open_tables":"open_tables",
    "Slow_queries":"slow_queries",
    
    #Threads
    "Threads_connected":"connected",
    "threads_running":"running",
    "Threads_cached":"cached",
    "Threads_created":"created",
    
    # Handler
    "Handler_rollback":"handler_rollback",   
    "Handler_delete":"handler_delete",
    "Handler_read_first":"read_first",
    "Handler_read_key":"read_key",
    "Handler_read_rnd_next":"read_rnd_next",
    "Handler_read_rnd":"read_rnd",
    "Handler_update":"handler_update",
    "Handler_write":"handler_write",
    
    #Buffer pool
    "Innodb_buffer_pool_pages_total":"buffer_pool_pages_total",
    "Innodb_buffer_pool_pages_free":"buffer_pool_pages_free",
    "Innodb_buffer_pool_pages_dirty":"buffer_pool_pages_dirty",
    "Innodb_buffer_pool_pages_data":"buffer_pool_pages_data",
    "Innodb_buffer_pool_wait_free":"buffer_pool_wait_free",
    "Innodb_log_waits":"log_waits",
    "Innodb_row_lock_time_avg":"row_lock_time_avg",
    "Innodb_row_lock_waits":"row_lock_waits",
    "Innodb_buffer_pool_pages_flushed":"buffer_pool_pages_flushed",
    "Innodb_buffer_pool_read_ahead_evicted":"buffer_pool_read_ahead_evicted",
    "Innodb_buffer_pool_read_ahead":"buffer_pool_read_ahead",
    "Innodb_buffer_pool_read_ahead_rnd":"buffer_pool_read_ahead_rnd",
    "Innodb_buffer_pool_read_requests":"buffer_pool_read_requests",
    "Innodb_buffer_pool_reads":"buffer_pool_reads",
    "Innodb_buffer_pool_write_requests":"buffer_pool_write_requests",
    "Innodb_data_fsyncs":"data_fsyncs",
    "Innodb_data_pending_fsyncs":"data_pending_fsyncs",
    "Innodb_data_pending_reads":"data_pending_reads",
    "Innodb_data_pending_writes":"data_pending_writes",
    "Innodb_data_reads":"data_reads",
    "Innodb_data_writes":"data_writes",
    "Innodb_log_write_requests":"log_write_requests",
    "Innodb_log_writes":"log_writes",
    "Innodb_os_log_fsyncs":"os_log_fsyncs",
    "Innodb_os_log_pending_fsyncs":"os_log_pending_fsyncs",
    "Innodb_os_log_pending_writes":"os_log_pending_writes",
    "Innodb_os_log_written":"os_log_written",
    "Innodb_pages_created":"pages_created",
    "Innodb_pages_read":"pages_read",
    "Innodb_pages_written":"pages_written",
    "Innodb_rows_deleted":"rows_deleted",
    "Innodb_rows_inserted":"rows_inserted",
    "Innodb_rows_read":"rows_read",
    "Innodb_rows_updated":"rows_updated",
    # Query cache items    
    # The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation
    "Qcache_hits":"hits",
    "Qcache_free_memory":"free_memory",
    "Qcache_not_cached":"not_cached",
    "Qcache_queries_in_cache":"in_cache",
    "Qcache_free_blocks":"free_blocks",
    "Qcache_inserts":"inserts",
    "Qcache_lowmem_prunes":"lowmem_prunes",
    "Qcache_total_blocks":"total_blocks",
    
    # Aborted connections and clients
    "Aborted_clients":"aborted_clients",
    "Aborted_connects":"aborted_connects",
    # Bytes sent and received
    "Bytes_received":"received",
    "Bytes_sent":"sent",
    
    #Connection 
    
    "Connection_errors_max_connections":"connection_errors_max_connections",
    "max_connections":"max_connections",
    "Max_used_connections":"max_used_connections", 
    
    # Created temporary tables in memory and on disk
    "Created_tmp_tables":"tmp_tables",
    "Created_tmp_disk_tables":"disk_tables",
    "Created_tmp_files":"tmp_files",
    #Select 
    "Select_full_join":"full_join",
    "Select_full_range_join":"full_range_join",
    "Select_range":"select_range",
    "Select_range_check":"range_check",
    "Select_scan":"select_scan",
    "Max_execution_time_exceeded":"max_execution_time_exceeded",
    
    # open files
    "Open_files":"open_files",
    #"open_files_limit":"open_files_limit",
    "Table_locks_waited":"table_locks_waited",
    
    #Table cache
    "Table_open_cache_hits":"open_cache_hits",
    "Table_open_cache_misses":"open_cache_misses",
    "Table_open_cache_overflows":"open_cache_overflows",
    
    #Com
    "Com_commit":"commit",
    "Com_delete":"com_delete",
    "Com_delete_multi":"delete_multi",
    "Com_insert":"com_insert",
    "Com_insert_select":"insert_select",
    "Com_replace_select":"replace_select",
    "Com_rollback":"com_rollback",
    "Com_select":"select",
    "Com_update":"com_update",
    "Com_update_multi":"update_multi",
    #Prepared statement
    "Prepared_stmt_count":"prepared_stmt_count",
    #Queries
    "Queries":"application_queries",
    #Questions
    "Questions":"client_queries",
    #Sort
    "Sort_merge_passes":"merge_passes",
    "Sort_range":"range",
    "Sort_rows":"rows",
    "Sort_scan":"scan",
    #MyISAM Key Cache
    "Key_blocks_not_flushed":"blocks_not_flushed",
    "Key_read_requests":"read_requests",
    "Key_reads":"key_reads",
    "Key_write_requests":"write_requests",
    "Key_writes":"key_writes" 
    }

REPLICATION_JSON = {
    "Slave_IO_State": "slave_IO_state",
    "Replica_IO_State": "slave_IO_state",
    "Master_Host": "master_host",
    "Source_Host": "master_host",
    "Master_User": "master_user",
    "Source_User": "master_user",
    "Connect_Retry": "connect_retry",
    "Master_Server_Id": "master_server_id",
    "Source_Server_Id": "master_server_id",
    "Master_Retry_Count": "master_retry_count",
    "Source_Retry_Count": "master_retry_count",
    "Skip_Counter": "skip_counter",
    "Relay_Log_Space": "relay_log_space",
    "Seconds_Behind_Master": "seconds_behind_master",  # For MySQL 5.7
    "Seconds_Behind_Source": "seconds_behind_master",  # For MySQL 8.0+
    "Last_IO_Errno": "last_IO_errno",
    "Last_SQL_Errno": "last_sql_errno",
    "Slave_IO_Running": "slave_IO_running",
    "Replica_IO_Running": "slave_IO_running",
    "Slave_SQL_Running": "slave_sql_running",
    "Replica_SQL_Running": "slave_sql_running"
}
    
#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'uptime':'seconds',
               'row_length':'bytes',
               'data_length': 'bytes', 
               'max_data_length': 'bytes',
               'index_length': 'bytes',
               'row_count': 'units',
               'connection_usage':'%',
               'open_files_usage':'%',
               'row_lock_time_avg':'ms',
               'received':'bytes',
               'sent':'bytes',
               'relay_log_space':'bytes',
               'os_log_written':'bytes',
               'free_memory':'bytes',
               'seconds_behind_master':'seconds'
               }
               


class MySQL(object):
    
    def __init__(self,args):
        self.connection = None
        self.host = args.host
        self.port = args.port
        self.username = args.username
        self.password = args.password
        
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
       

    #execute a mysql query and returns a dictionary
    def executeQuery(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            metric = {}
            field_names = [i[0] for i in cursor.description]
            for entry in cursor:    
                for i in range(len(entry)):
                    metric[field_names[i]] = entry[i]
            return metric
        except Exception as e:
            metric["error"] = str(e)
            return metric
    def executeQuery_replica(self, query):
        try:
            cursor = self.connection.cursor()
        except Exception as e:
            metric["error"] = str(e)
            return metric
    def executeQuery_mysql(self, con, query):
        try:
            cursor = con.cursor()
            cursor.execute(query)
            metric = {}
            for entry in cursor:
                try:
                    metric[entry[0]] = float(entry[1])
                except ValueError as e:
                    metric[entry[0]] = entry[1]

            return metric
        except pymysql.OperationalError as message:
            pass
            
    def getDbConnection(self):
        try:
            import pymysql
            db = pymysql.connect(host=self.host,user=self.username,passwd=self.password,port=int(self.port))
            self.connection = db
        except Exception as e:
            global con_error
            con_error=str(e)
            #traceback.print_exc()
            return False
        return True

    def checkPreRequisites(self,data):
        bool_result = True
        try:
            import pymysql
        except Exception:
            data['status']=0
            data['msg']='pymysql module not installed'
            bool_result=False
            pymysql_returnVal=os.system('pip install pymysql >/dev/null 2>&1')
            if pymysql_returnVal==0:
                bool_result=True
                data.pop('status')
                data.pop('msg')
        return bool_result,data

    def metricCollector(self):
        data = {}

        #bool_result,data = self.checkPreRequisites(data)
        bool_result = True
        
        if bool_result==False:
            return data
        else:
            try:
                import pymysql
            except Exception:
                data['status']=0
                data['msg']='pymysql module not installed\n Solution : Use the following command to install pymysql\n pip install pymysql \n(or)\n pip3 install pymysql'
                return data

            if not self.getDbConnection():
                data['status']=0
                data['msg']='Connection Error: '+con_error
                return data
    
            try:
                con = self.connection
                # get MySQL version
                try:
                    cursor = con.cursor()
                    cursor.execute(VERSION_QUERY)
                    result = cursor.fetchone()
                    data['mysql_version'] = result[0]
                    version=result[0].split(".")
                    if int(version[0]) >=8:
                         slave_query="SHOW REPLICA STATUS"
                         #master_query="SHOW BINARY LOG STATUS"
                    else:
                         slave_query='SHOW SLAVE STATUS'
                    master_query='SHOW MASTER STATUS'
                         
                except pymysql.OperationalError as message:
                    data["msg"] = repr(e)
                    data["status"]=0
                    return data
                
                cursor.execute(slave_query)
                myresult_slave_key=cursor.description
                myresult_slave=cursor.fetchall()
                try:
                    cursor.execute(master_query)
                except pymysql.ProgrammingError as e:
                    if int(version[0]) >=8:
                        cursor.execute('SHOW BINARY LOG STATUS')
                    else:
                        data["msg"] = repr(e)
                        data["status"]=0
                         
                myresult_master=cursor.fetchall()
                if myresult_master and myresult_slave:
                        data['mysql_node_type']='Master & slave'
                        for i in range(len(myresult_slave[0])):
                            if REPLICATION_JSON.get(myresult_slave_key[i][0]):
                                
                                data[REPLICATION_JSON[myresult_slave_key[i][0]]]=myresult_slave[0][i]
                        #data['mysql_node_type']='Slave'
                elif myresult_master:
                        data['mysql_node_type']='Master'
                elif myresult_slave : 
                    for i in range(len(myresult_slave[0])):
                        if REPLICATION_JSON.get(myresult_slave_key[i][0]):
                            
                            data[REPLICATION_JSON[myresult_slave_key[i][0]]]=myresult_slave[0][i]
                    data['mysql_node_type']='Slave'
                else:
                        data['mysql_node_type']='Standalone'

                        
                json_file={} 
                #MySQL Replication
                
                file_name="mysql_info_"+self.host+".json"
                if os.path.exists(file_name):
                        if os.stat(file_name).st_size == 0:
                                json_file['MySQLNodeType']=data['mysql_node_type']
                                with open(file_name, 'w') as f:
                                        json.dump(json_file, f)
                        f = open(file_name)
                        json_val = json.load(f)
                        json_data = json_val["MySQLNodeType"]
                        if(json_data != data['mysql_node_type'] and (json_data in ['Slave', 'Master', 'Standalone'])):
                                json_file['MySQLNodeType']=data['mysql_node_type']
                                with open(file_name, 'w') as f:
                                        json.dump(json_file, f)
                                data["msg"] = "Failover happened -"+json_data+" was Switched to "+data['mysql_node_type']
                                data["status"] = 0
                                return data
                        else:
                                json_file['MySQLNodeType']=data['mysql_node_type']
                                with open(file_name, 'w') as f:
                                        json.dump(json_file, f)
                else:
                        json_file['MySQLNodeType']=data['mysql_node_type']
                        with open(file_name, 'w') as f:
                                json.dump(json_file, f)
                #global_table = self.executeQuery('select * from information_schema.tables where table_schema="' + self.database + '" and table_name="'+self.table+'"')
                data["row_length"] = 0
                data["data_length"] = 0
                data["index_length"] = 0
                data["max_data_length"] = 0
                data["rows_count"] = 0
                global_metrics = self.executeQuery_mysql(con,'SHOW GLOBAL STATUS')
                global_variables = self.executeQuery_mysql(con,'SHOW VARIABLES') 
                """global_db = self.executeQuery_mysql(con, 'SELECT table_schema "DB Name",ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" FROM information_schema.tables GROUP BY table_schema;')
       
                for k,v in global_db.items():
                    db_list = {}
                    db_list["name"]=k
                    db_list["size"]=v
                    db.append(db_list)"""
                    #data[k]=v
                    #METRICS_UNITS[k] = "MB"
                for attribute_keys in METRICS_JSON:
                    if attribute_keys in global_metrics:
                        data[METRICS_JSON[attribute_keys]]=global_metrics[attribute_keys]
                    elif attribute_keys in global_variables:
                        data[METRICS_JSON[attribute_keys]]=global_variables[attribute_keys]
                    else:
                        data[METRICS_JSON[attribute_keys]]=0
                if 'threads_running' in data and  'max_connections' in global_variables:
                    data['connection_usage'] = ((data['threads_running'] /global_variables['max_connections'])*100)
                else:
                    data['connection_usage'] = 0
                if 'open_files' in data and  'open_files_limit' in global_variables:
                    data['open_files_usage'] = ((data['open_files'] /global_variables['open_files_limit'])*100)                                                                                                                                                                                        
                else:
                    data['open_files_usage'] = 0 
                #no of reads & writes
                if 'Com_insert' in global_metrics and  'Com_replace' in global_metrics and 'Com_update' in global_metrics and  'Com_delete' in global_metrics:
                    writes = (global_metrics['Com_insert'] +global_metrics['Com_replace'] +global_metrics['Com_update'] +global_metrics['Com_delete'])
                    data['writes'] = writes
                else:
                    data['writes'] = 0
                # reads
                if 'Com_select' in global_metrics and  'qcache_hits' in data:
                    reads = global_metrics['Com_select'] + data['qcache_hits']
                    data['reads'] = reads
                else:
                    data['reads'] = 0
                    reads = 0
                try:
                    data['rw_ratio'] = reads/writes
                except ZeroDivisionError:
                    data['rw_ratio'] = 0
                except Exception as e:
                    data["msg"] = repr(e)
                    data["status"]=0
    
                # transactions
                if 'Com_commit' in global_metrics and  'Com_rollback' in global_metrics:
                    transactions = (global_metrics['Com_commit'] +global_metrics['Com_rollback'])
                    data['transactions'] = transactions
                else:
                    data['transactions'] = 0                                                                                                             
                # slave_running
                if 'Slave_running' in global_metrics:
                    result = global_metrics['Slave_running']
                    if result == 'OFF':
                        result = 0
                    else:
                        result = 1
                    data['slave_running'] = result
                else:
                    if myresult_slave:
                        data['slave_running'] = 1
                    else:
                        data['slave_running'] = 0
                
                cursor.execute('SHOW VARIABLES LIKE "wsrep_cluster_name"')
                cluster=cursor.fetchall()
                if cluster:
                    data['tags']="MYSQL_CLUSTER:"+cluster[0][1]+",MYSQL_NODE:"+self.host+""
            except Exception as e:
                data["error"] = repr(e)
                cursor.close()
                con.close()
                return data
        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
            applog["logs_enabled"]=True
            applog["log_type_name"]=self.logtypename
            applog["log_file_path"]=self.logfilepath
        else:
            applog["logs_enabled"]=False
        data['applog'] = applog
        #data['tags']="Node Type:"+data['mysql_node_type']+""
        data['units']=METRICS_UNITS
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        cursor.close()
        con.close()
        return data

if __name__ == "__main__":
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= MYSQL_HOST)
    parser.add_argument('--port',help="Port",nargs='?', default= MYSQL_PORT)
    parser.add_argument('--username',help="username", default= MYSQL_USERNAME)
    parser.add_argument('--password',help="Password", default= MYSQL_PASSWORD)
    
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    
    args=parser.parse_args()
    mysql_plugins = MySQL(args)
    result = mysql_plugins.metricCollector()
    print(json.dumps(result))
