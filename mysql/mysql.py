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
import sys

VERSION_QUERY = 'SELECT VERSION()'

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT=True

#Config Section: 
#Use either True | False - enabled True will read mysql configurations from my.cnf file , Please provide the my.cnf path below
USE_MYSQL_CONF_FILE=False

#Used only when USE_MYSQL_CONF_FILE is set to True , We have provided the default path change it as it is in your server
MY_CNF_FILE_LOCATION='/etc/mysql/my.cnf'

'''
1.This is Default configuration.
2.For password encryption or Need to monitor more than one host 
use configuration file mysql.cfg 
3.Change the mysql configuration accordingly
in the configuration file mysql.cfg.
4.Configuration File will have more Priority
'''

MYSQL_HOST = "localhost"

MYSQL_PORT=3306

MYSQL_USERNAME="test"

MYSQL_PASSWORD=""

MYSQL_SOCKET = "/tmp/mysql.sock"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'connection_usage':'%','uptime':'seconds','open_files_usage':'%'}

METRICS_JSON={
    "Uptime":"uptime",
    "Open_tables":"open_tables",
    "Slow_queries":"slow_queries",
    "Threads_connected":"threads_connected",
    "Threads_running":"threads_running",
    "max_connections":"max_connections",
    "Max_used_connections":"max_used_connections",    
    # Buffer pool
    "Innodb_buffer_pool_pages_total":"buffer_pool_pages_total",
    "Innodb_buffer_pool_pages_free":"buffer_pool_pages_free",
    "Innodb_buffer_pool_pages_dirty":"buffer_pool_pages_dirty",
    "Innodb_buffer_pool_pages_data":"buffer pool pages data",
    #Innodb_buffer_pool_wait_free
    "Innodb_buffer_pool_wait_free":"innodb_buffer_pool_wait_free",
    # Query cache items    
    # The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL 8.0. Deprecation
    "Qcache_hits":"qcache_hits",
    "Qcache_free_memory":"qcache_free_memory",
    "Qcache_not_cached":"qcache_not_cached",
    "Qcache_queries_in_cache":"qcache_in_cache",
    # Aborted connections and clients
    "Aborted_clients":"aborted_clients",
    "Aborted_connects":"aborted_connects",
    # Created temporary tables in memory and on disk
    "Created_tmp_tables":"created_tmp_tables",
    "Created_tmp_disk_tables":"created_tmp_tables_on_disk",
    
    "Select_full_join":"select_full_join",
    
    # open files
    "Open_files":"open_files",
    #"open_files_limit":"open_files_limit",
    
    "Table_locks_waited":"table_locks_waited",
    "Key_reads":"key_reads"
    }

             
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
            if USE_MYSQL_CONF_FILE:
                db = pymysql.connect(read_default_file=MY_CNF_FILE_LOCATION)
            else:
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
                
                for attribute_keys in METRICS_JSON:
                    if attribute_keys in global_metrics:
                        data[METRICS_JSON[attribute_keys]]=global_metrics[attribute_keys]
                    elif attribute_keys in global_variables:
                        data[METRICS_JSON[attribute_keys]]=global_variables[attribute_keys]
                
                                                              
                if 'threads_running' in data and  'max_connections' in global_variables:
                    data['connection_usage'] = ((data['threads_running'] /global_variables['max_connections'])*100)
                
                if 'open_files' in data and  'open_files_limit' in global_variables:
                    data['open_files_usage'] = ((data['open_files'] /global_variables['open_files_limit'])*100)                                                                                                                                                                                        
    
                #no of reads & writes
                if 'Com_insert' in global_metrics and  'Com_replace' in global_metrics and 'Com_update' in global_metrics and  'Com_delete' in global_metrics:
                    writes = (global_metrics['Com_insert'] +global_metrics['Com_replace'] +global_metrics['Com_update'] +global_metrics['Com_delete'])
                    data['writes'] = writes
    
                # reads
                if 'Com_select' in global_metrics and  'qcache_hits' in data:
                    reads = global_metrics['Com_select'] + data['qcache_hits']
                    data['reads'] = reads
    
                try:
                    data['rw ratio'] = reads/writes
                except ZeroDivisionError:
                    data['rw ratio'] = 0
                except Exception as e:
                    traceback.format_exc()
    
                # transactions
                if 'Com_commit' in global_metrics and  'Com_rollback' in global_metrics:
                    transactions = (global_metrics['Com_commit'] +global_metrics['Com_rollback'])
                    data['transactions'] = transactions
                                                                                                                                            
                # slave_running
                if 'Slave_running' in global_metrics:
                    result = global_metrics['Slave_running']
                    if result == 'OFF':
                        result = 0
                    else:
                        result = 1
                    data['slave_running'] = result                                                                                                                                                                   
            except Exception as e:
                data['msg']=str(e)
    
    
            data['units']=METRICS_UNITS
            
        return data

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=MYSQL_HOST)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=MYSQL_PORT)
    parser.add_argument('--username', help='user name of the elasticsearch', nargs='?', default=MYSQL_USERNAME)
    parser.add_argument('--password', help='password of the elasticsearch', nargs='?', default=MYSQL_PASSWORD)
    
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()
    
    host_name=args.host
    port=str(args.port)
    username=args.username
    password=args.password                

    configurations = {'host': host_name, 'port': port, 'user': username, 'password': password}

    mysql_plugins = MySQL(configurations)
    
    result = mysql_plugins.metricCollector()
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat
    
    print(json.dumps(result, indent=4, sort_keys=True))
