#!/usr/bin/python
"""

Site24x7 MySql Plugin

"""
import traceback
import re
import json
import os
"""import subprocess
import time
import sys
"""
VERSION_QUERY = 'SELECT VERSION()'

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section: 
#Use either True | False - enabled True will read mysql configurations from my.cnf file , Please provide the my.cnf path below
USE_MYSQL_CONF_FILE=False

#Used only when USE_MYSQL_CONF_FILE is set to True , We have provided the default path change it as it is in your server
MY_CNF_FILE_LOCATION='/etc/mysql/my.cnf'

MYSQL_HOST = "localhost"

MYSQL_PORT="3306"

MYSQL_USERNAME="root"

MYSQL_PASSWORD=""

MYSQL_SOCKET = "/tmp/s.sock"

#Update the DBname 
MYSQL_DB="sys"

#Update the query need to be executed
MYSQL_QUERY = "select * from metrics LIMIT 1"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={}

class MySQL(object):
    
    def __init__(self,config):
        self.configurations = config
        self.connection = None
        self.host = os.getenv('MYSQL_HOST', self.configurations.get('host', 'localhost'))
        self.port = os.getenv('MYSQL_PORT', int(self.configurations.get('port', '3306')))
        self.username = os.getenv('MYSQL_USERNAME', self.configurations.get('user', 'root'))
        self.password = os.getenv('MYSQL_PASSWORD', self.configurations.get('password', ''))
        self.db = os.getenv('MYSQL_DB', self.configurations.get('db', ''))
        self.query = os.getenv('MYSQL_QUERY', self.configurations.get('query', ''))
        self.data = {}
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
        except Exception as e:
            if type(_proc) is subprocess.Popen:
                _proc.kill()
                _proc.poll()
        finally:
            return _status, _output
    
    #execute a mysql query and returns only the first row as adictionary
    def executeQuery(self, con, query, metric):
        try:
            cursor = con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = cursor.description             
            result = [{columns[index][0]:str(column)[:25] for index, column in enumerate(value)} for value in rows]            
            cursor.close()
            if len(result) > 0 :
                try:
                    metric = result[0]
                    #metric['msg'] = str(len(result)) + " rows returned"
                except Exception as ee:
                    metric['status'] = 0
                    metric['msg'] = ee
                    traceback.print_exc()
            else :
                empty_rows = [{column[0]:'-' for column in columns}] 
                metric=empty_rows[0]              
                metric['msg'] = "No rows returned"
            #metric['No of rows returned']=len(result)
            return metric
        except Exception as e:
            traceback.print_exc()
            metric['status'] = 0
            metric['msg'] = e
        return metric

    def getDbConnection(self):
        try:
            import pymysql
            if USE_MYSQL_CONF_FILE:
                db = pymysql.connect(read_default_file=MY_CNF_FILE_LOCATION)
            else:
                db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port),db=self.db)
            self.connection = db
        except Exception as e:
            try:
                import pymysql
                _status, _output = MySQL.get_sock_path()
                if _status:
                    db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port),db=self.db, unix_socket=_output)
                else:
                    db = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=int(self.port),db=self.db, unix_socket=MYSQL_SOCKET)
                self.connection = db
            except Exception as e:
                #traceback.print_exc()
                self.data['status'] = 0
                self.data['msg'] = e
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

        bool_result,self.data = self.checkPreRequisites(self.data)
        
        if bool_result==False:
            return self.data
        else:
            try:
                import pymysql
            except Exception:
                self.data['status']=0
                self.data['msg']='pymysql module not installed'
                return self.data

            if not self.getDbConnection():
                self.data['status']=0
                self.data['msg']='Connection Error'
                return self.data
    
            try:
                con = self.connection
                self.data = self.executeQuery(con, self.query, self.data)               
                con.close()
            except Exception as e:
                #traceback.format_exc()
                self.data['status'] = 0
                self.data['msg'] = e

            self.data['plugin_version'] = PLUGIN_VERSION
            self.data['heartbeat_required']=HEARTBEAT
            if len(METRICS_UNITS) > 0 :  self.data['units'] = METRICS_UNITS

        return self.data

if __name__ == "__main__":

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= MYSQL_HOST)
    parser.add_argument('--port',help="Port",nargs='?', default= MYSQL_PORT)
    parser.add_argument('--username',help="username", default= MYSQL_USERNAME)
    parser.add_argument('--password',help="Password", default= MYSQL_PASSWORD)
    
    parser.add_argument('--db', help='db name',default=MYSQL_DB)
    parser.add_argument('--query', help='mysql query', nargs='?', default=MYSQL_QUERY)
    args=parser.parse_args()

    configurations = {'host': args.host, 'port': args.port, 'user': args.username, 'password': args.password, 'db' : args.db, 'query' : args.query}

    mysql_plugins = MySQL(configurations)
    
    result = mysql_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
