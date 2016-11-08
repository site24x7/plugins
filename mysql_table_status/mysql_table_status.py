#!/usr/bin/python3
"""

Site24x7 MySql table stats Plugin

"""
import traceback
import re
import json
import os
from configparser import ConfigParser

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

'''
    give the database name over which the table information has to be generated.
    The list of database can be retrived using,
    show databases;
'''
DATABASE = "jbossdb"

'''
    select the table name for which the information has to be returned.
    The list of tables in a database can be retrived using,
    show tables;
'''
TABLE = "SASAccounts"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'row_lenth':'bytes', 
               'data_length': 'bytes', 
               'max_data_length': 'bytes',
               'index_length': 'bytes',
               'row_count': 'units'}

class MySQL(object):
    
    def __init__(self,config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '3306'))
        self.username = self.configurations.get('user', 'root')
        self.password = self.configurations.get('password', '')
        self.database = self.configurations.get('database')
        self.table = self.configurations.get('table')

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

    def getDbConnection(self):
        try:
            import pymysql
            db = pymysql.connect(host=self.host,user=self.username,passwd=self.password,port=int(self.port))
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
                    traceback.print_exc()
                    return data
                
                global_metrics = self.executeQuery('select * from information_schema.tables where table_schema="' + self.database + '" and table_name="'+self.table+'"')
                data["row_length"] = global_metrics["AVG_ROW_LENGTH"]
                data["data_length"] = global_metrics["DATA_LENGTH"]
                data["index_length"] = global_metrics["INDEX_LENGTH"]
                data["max_data_length"] = global_metrics["MAX_DATA_LENGTH"]
                data["rows_count"] = global_metrics["TABLE_ROWS"]
            except Exception as e:
                data["error"] = repr(e)
                return data
        data['units']=METRICS_UNITS
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        return data

if __name__ == "__main__":

    configurations = {'host': MYSQL_HOST,
                      'port': MYSQL_PORT,
                      'user': MYSQL_USERNAME,
                      'password': MYSQL_PASSWORD,
                      'database': DATABASE,
                      'table': TABLE}

    mysql_plugins = MySQL(configurations)
    
    #mysql_plugins.getDbConnection()
    #print(mysql_plugins.executeQuery("select * from information_schema.tables where table_schema = 'jbossdb'"));
    result = mysql_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
