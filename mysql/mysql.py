#!/usr/bin/python
"""

Site24x7 MySql Plugin

"""
import traceback
import re
import json
import os
import subprocess
import time

VERSION_QUERY = 'SELECT VERSION()'

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
MYSQL_HOST = "localhost"

MYSQL_PORT="3306"

MYSQL_USERNAME="root"

MYSQL_PASSWORD=""

MYSQL_SOCKET = "/tmp/mysql.sock"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'connection_usage':'%'}

class MySQL(object):
    
    def __init__(self,config):
        self.configurations = config
        self.connection = None
        self.host = os.getenv('MYSQL_HOST', self.configurations.get('host', 'localhost'))
        self.port = os.getenv('MYSQL_PORT', int(self.configurations.get('port', '3306')))
        self.username = os.getenv('MYSQL_USERNAME', self.configurations.get('user', 'root'))
        self.password = os.getenv('MYSQL_PASSWORD', self.configurations.get('password', ''))
    
    @staticmethod
    def get_sock_path():
        _output, _status, _proc = None, False, None
        try:
            _proc = subprocess.Popen("netstat -ln | awk '/mysql(.*)?\.sock/ { print $9 }'" ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(0.5)
            if not _proc.poll() is None:
                _status = True
                _output, error = _proc.communicate()
                _output = _output.strip("\n")
        except Exeception as e:
            if type(_proc) is subprocess.Popen:
                _proc.kill()
                _proc.poll()
        finally:
            return _status, _output
    
    #execute a mysql query and returns a dictionary
    def executeQuery(self, con, query):
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
            db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port))
            self.connection = db
        except Exception as e:
            try:
                import pymysql
                _status, _output = MySQL.get_sock_path()
                if _status:
                    db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port), unix_socket=_output)
                else:
                    db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port), unix_socket=MYSQL_SOCKET)
                self.connection = db
            except Exception as e:
                traceback.print_exc()
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
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT

        bool_result,data = self.checkPreRequisites(data)
        
        if bool_result==False:
            return data
        else:
            try:
                import pymysql
            except Exception:
                data['status']=0
                data['msg']='pymysql module not installed'
                return data

            if not self.getDbConnection():
                data['status']=0
                data['msg']='Connection Error'
                return data
    
            try:
                con = self.connection
                
                # get MySQL version
                try:
                    cursor = con.cursor()
                    cursor.execute(VERSION_QUERY)
                    result = cursor.fetchone()
                    data['version'] = result[0]
                except pymysql.OperationalError as message:
                    return data
    
                global_metrics = self.executeQuery(con, 'SHOW GLOBAL STATUS')
                
                global_variables = self.executeQuery(con, 'SHOW VARIABLES')
    
                cursor.close()

                con.close()
                
                data['uptime'] = global_metrics['Uptime']
                
                data['open_tables'] = global_metrics['Open_tables']
                
                data['slow_queries'] = global_metrics['Slow_queries']
                
                data['threads_connected'] = global_metrics['Threads_connected']
                
                data['threads_running'] = global_metrics['Threads_running']
                
                
                data['max_connections'] = global_variables['max_connections']
                
                data['max_used_connections'] = global_metrics['Max_used_connections']
                
                data['connection_usage'] = ((data['threads_running'] /data['max_connections'])*100)
                
                # Buffer pool
                data['buffer_pool_pages_total'] = global_metrics['Innodb_buffer_pool_pages_total']
                
                data['buffer_pool_pages_free'] = global_metrics['Innodb_buffer_pool_pages_free']
                
                data['buffer_pool_pages_dirty'] = global_metrics['Innodb_buffer_pool_pages_dirty']
                
                data['buffer pool pages data'] = global_metrics['Innodb_buffer_pool_pages_data']
    
                # Query cache items
                data['qcache_hits'] = global_metrics['Qcache_hits']
                
                data['qcache_free_memory'] = global_metrics['Qcache_free_memory']
                
                data['qcache_not_cached'] = global_metrics['Qcache_not_cached']
                
                data['qcache_in_cache'] = global_metrics['Qcache_queries_in_cache']
    
                #no of reads & writes
                writes = (global_metrics['Com_insert'] +global_metrics['Com_replace'] +global_metrics['Com_update'] +global_metrics['Com_delete'])
                data['writes'] = writes
    
                # reads
                reads = global_metrics['Com_select'] + data['qcache_hits']
                data['reads'] = reads
    
                try:
                    data['rw ratio'] = reads/writes
                except ZeroDivisionError:
                    data['rw ratio'] = 0
    
                # transactions
                transactions = (global_metrics['Com_commit'] +global_metrics['Com_rollback'])
                data['transactions'] = transactions
    
                # Aborted connections and clients
                data['aborted_clients'] = global_metrics['Aborted_clients']
                data['aborted_connects'] = global_metrics['Aborted_connects']
    
                # Created temporary tables in memory and on disk
                data['created_tmp_tables'] = global_metrics['Created_tmp_tables']
                data['created_tmp_tables_on_disk'] = global_metrics['Created_tmp_disk_tables']
                
                # select_full_join
                data['select_full_join'] = global_metrics['Select_full_join']
                
                # slave_running
                result = global_metrics['Slave_running']
                if result == 'OFF':
                    result = 0
                else:
                    result = 1
                data['slave_running'] = result
                
                # open files
                data['open_files'] = global_metrics['Open_files']
                data['open_files_limit'] = global_variables['open_files_limit']
                
    
                # table_locks_waited
                data['table_locks_waited'] = global_metrics['Table_locks_waited']
                
                #key reads
                data['key_reads'] = global_metrics['Key_reads']
                
                #Innodb_buffer_pool_wait_free
                data['innodb_buffer_pool_wait_free'] = global_metrics['Innodb_buffer_pool_wait_free']
    
            except Exception as e:
                traceback.format_exc()
    
    
            data['units']=METRICS_UNITS
            
        return data

if __name__ == "__main__":

    configurations = {'host': MYSQL_HOST, 'port': MYSQL_PORT, 'user': MYSQL_USERNAME, 'password': MYSQL_PASSWORD}

    mysql_plugins = MySQL(configurations)
    
    result = mysql_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
