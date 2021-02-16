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

MYSQL_HOST = "localhost"

MYSQL_PORT="3306"

MYSQL_USERNAME="test"

MYSQL_PASSWORD=""

MYSQL_SOCKET = "/tmp/mysql.sock"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
SLAVE_METRICS = {
    "Slave_IO_State" : {"key" : "Slave_IO_State" ,"unit" : ""},
    "Last_Errno" : {"key" : "Last_Errno" ,"unit" : ""},
    "Skip_Counter" : {"key" : "Skip_Counter" ,"unit" : ""},
    "Relay_Log_Space" : {"key" : "Relay_Log_Space" ,"unit" : ""},
    "Seconds_Behind_Master" : {"key" : "Seconds_Behind_Master" ,"unit" : ""},
    "Last_IO_Errno" : {"key" : "Last_IO_Errno" ,"unit" : ""},
    "Last_SQL_Errno" : {"key" : "Last_SQL_Errno" ,"unit" : ""},


    "Slave_IO_Running" : {"key" : "Slave_IO_Running" ,"unit" : ""},
    "Slave_SQL_Running" : {"key" : "Slave_SQL_Running" ,"unit" : ""}
}
METRICS = {
    "Slave_heartbeat_period" : {"key" : "Slave_heartbeat_period" ,"unit" : ""},
    "Slave_open_temp_tables" : {"key" : "Slave_open_temp_tables" ,"unit" : ""},
    "Slave_received_heartbeats" : {"key" : "Slave_received_heartbeats" ,"unit" : ""},
    "Slave_retried_transactions" : {"key" : "Slave_retried_transactions" ,"unit" : ""}
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
    
    def getDbConnection(self):
        try:
            import pymysql
            if USE_MYSQL_CONF_FILE:
                db = pymysql.connect(default_read_file=MY_CNF_FILE_LOCATION)
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
            
            METRICS_UNITS = {}

            try:
                con = self.connection
                
                try :

                    cursor = con.cursor()
                    cursor.execute('SHOW SLAVE STATUS')
                    myresult = cursor.fetchall()

                    if myresult : 
                        for entry in myresult:
                            data[SLAVE_METRICS['Slave_IO_State']['key']] = entry[0]
                            data[SLAVE_METRICS['Last_Errno']['key']] = entry[18]
                            data[SLAVE_METRICS['Skip_Counter']['key']] = entry[20]
                            data[SLAVE_METRICS['Relay_Log_Space']['key']] = entry[22]
                            data[SLAVE_METRICS['Seconds_Behind_Master']['key']] = entry[32] if entry[32] is not None else 0
                            data[SLAVE_METRICS['Last_IO_Errno']['key']] = entry[34]
                            data[SLAVE_METRICS['Last_SQL_Errno']['key']] = entry[36]
                            data[SLAVE_METRICS['Slave_IO_Running']['key']] = 0 if entry[10] == 'No' else 1
                            data[SLAVE_METRICS['Slave_SQL_Running']['key']] = 0 if entry[11] == 'No' else 1
                    else : 
                            data[SLAVE_METRICS['Slave_IO_State']['key']] = ""
                            data[SLAVE_METRICS['Last_Errno']['key']] = 0
                            data[SLAVE_METRICS['Skip_Counter']['key']] = 0
                            data[SLAVE_METRICS['Relay_Log_Space']['key']] = 0
                            data[SLAVE_METRICS['Seconds_Behind_Master']['key']] = 0
                            data[SLAVE_METRICS['Last_IO_Errno']['key']] = 0
                            data[SLAVE_METRICS['Last_SQL_Errno']['key']] = 0
                            data[SLAVE_METRICS['Slave_IO_Running']['key']] = 0
                            data[SLAVE_METRICS['Slave_SQL_Running']['key']] = 0

                            data[METRICS['Slave_heartbeat_period']['key']] = 0
                            data[METRICS['Slave_received_heartbeats']['key']] = 0
                            data[METRICS['Slave_retried_transactions']['key']] = 0
                            data['Slave_running'] = 0
                except Exception as message:
                    data['msg'] = message
                finally :
                    cursor.close()
                    
                try:
                    cursor = con.cursor()
                    cursor.execute('SHOW GLOBAL STATUS')
                    for entry in cursor:
                        if entry[0] in METRICS :
                            key = METRICS[entry[0]]['key']
                            unit = METRICS[entry[0]]['unit']
                            try:
                                value = float(entry[1])
                            except ValueError as e:
                                value = entry[1]
                            data[key] = value

                        elif entry[0] == 'Slave_running' :
                            if entry[1] == 'OFF': result = 0
                            else: result = 1
                            data['Slave_running'] = result
                except Exception as message:
                    data['msg'] = message
                finally : 
                    cursor.close()

                
     
            except Exception as e:
                data['msg'] = str(e)
            finally :
                con.close()
        
        return data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=MYSQL_HOST)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=MYSQL_PORT)
    parser.add_argument('--username', help='user name', nargs='?', default=MYSQL_USERNAME)
    parser.add_argument('--password', help='password', nargs='?', default=MYSQL_PASSWORD)
    
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
