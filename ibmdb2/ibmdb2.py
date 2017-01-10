#!/usr/bin/python

### This plugin in python monitors the performance metrics of IBM DB2 servers

### It uses the DB2 query options to get the monitoring data.
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Shobana, Zoho Corp
### Language : Python
### Tested in Ubuntu

### Configure DB2 Server to enable monitoring for Site24x7

import re
import json
import os
import ibm_db
#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:Change DB2 Host,Port,Username,Password and Database name of DB2 server. 
DB2_HOST = "app-w12r2s-7"

DB2_PORT="50000"

DB2_USERNAME="db2admin"

DB2_PASSWORD="administrator@123"

DB2_SAMPLE_DB="SAMPLE"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
#Attribute units
METRICS_UNITS={'no_of_bufferpools':'count',
               'total_logical_reads':'count',
               'total_physical_reads':'count',
               'total_hit_ratio_percent':'%',
               'data_logical_reads':'count',
               'data_physical_reads':'count',
               'data_hit_ratio_percent':'%',
               'index_logical_reads':'count',
               'index_hit_ratio_percent':'%',
               'xda_logical_reads':'count',
               'xda_hit_ratio_percent':'%',
               'log_utilization_percent':'%',
               'total_log_used_kb':'KB',
               'total_log_available_kb':'KB'}

class DB2(object):
    
    def __init__(self,config):
        self.configurations = config
        self.connection = None

    def getDbConnection(self):
        try:
            url="DATABASE="+DB2_SAMPLE_DB+";HOSTNAME="+DB2_HOST+";PORT="+DB2_PORT+";PROTOCOL=TCPIP;UID="+DB2_USERNAME+";PWD="+DB2_PASSWORD+";"
            db = ibm_db.connect(url, "", "")  #Connect to an uncataloged database
            self.connection = db
        except Exception as e:
            traceback.print_exc()
            return False
        return True

    #execute a query and returns a dictionary
    def executeQuery(self, con, query):
        try:
            stmt = ibm_db.exec_immediate(con, query)
            result = ibm_db.fetch_both(stmt)
            return result

        except Exception as message:
            pass

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
   
        try:
            import ibm_db
        except Exception:
            data['status']=0
            data['msg']='ibm_db module not installed'
            return data

        if not self.getDbConnection():
            data['status']=0
            data['msg']='Connection Error'
            return data
        
        #No of bufferpools available

        bufferpool = self.executeQuery(self.connection, 'SELECT COUNT(*) as NO_OF_BUFFERPOOLS FROM syscat.bufferpools')

		#The BP_HITRATIO administrative view returns bufferpool hit ratios, including total hit ratio, data hit ratio, XDA hit ratio and index hit 
         #ratio, for all bufferpools and all database partitions in the the currently connected database
		
        bufferpool_metrics = self.executeQuery(self.connection, 'SELECT SUM(TOTAL_LOGICAL_READS) as TOTAL_LOGICAL_READS,SUM(TOTAL_PHYSICAL_READS) as TOTAL_PHYSICAL_READS,AVG(TOTAL_HIT_RATIO_PERCENT) as TOTAL_HIT_RATIO_PERCENT,SUM(DATA_LOGICAL_READS) as DATA_LOGICAL_READS,SUM(DATA_PHYSICAL_READS) as DATA_PHYSICAL_READS,AVG(DATA_HIT_RATIO_PERCENT) as DATA_HIT_RATIO_PERCENT,SUM(INDEX_LOGICAL_READS) as INDEX_LOGICAL_READS,AVG(INDEX_HIT_RATIO_PERCENT) as INDEX_HIT_RATIO_PERCENT,SUM(XDA_LOGICAL_READS) as XDA_LOGICAL_READS,AVG(XDA_HIT_RATIO_PERCENT) as XDA_HIT_RATIO_PERCENT FROM SYSIBMADM.BP_HITRATIO')
       
        #Overall DB2 log utilization parameters.

        logutilization_metrics=self.executeQuery(self.connection,"SELECT AVG(LOG_UTILIZATION_PERCENT) as LOG_UTILIZATION_PERCENT,SUM(TOTAL_LOG_USED_KB) as TOTAL_LOG_USED_KB, SUM(TOTAL_LOG_AVAILABLE_KB) as TOTAL_LOG_AVAILABLE_KB FROM SYSIBMADM.LOG_UTILIZATION")
      
        if not (bufferpool['NO_OF_BUFFERPOOLS'] is None):
            data['no_of_bufferpools']=bufferpool['NO_OF_BUFFERPOOLS']    #the current number of bufferpools
   
        if not (bufferpool_metrics['TOTAL_LOGICAL_READS'] is None):
            data['total_logical_reads']=int(bufferpool_metrics['TOTAL_LOGICAL_READS'])     #Total logical reads from bufferpool which is the total of data,index and xda logical reads

        if not (bufferpool_metrics['TOTAL_PHYSICAL_READS'] is None):
            data['total_physical_reads']=int(bufferpool_metrics['TOTAL_PHYSICAL_READS'])   #Total physical reads from bufferpool which is the total phyiscal reads of data,index and XDA.

        if not (bufferpool_metrics['TOTAL_HIT_RATIO_PERCENT'] is None):
            data['total_hit_ratio_percent']=float(bufferpool_metrics['TOTAL_HIT_RATIO_PERCENT'])  #Buffer pool hit ratio is a measure of how often a page access (a getpage) is satisfied without requiring an I/O operation.

        if not (bufferpool_metrics['DATA_LOGICAL_READS'] is None): 
            data['data_logical_reads']=int(bufferpool_metrics['DATA_LOGICAL_READS'])  #Bufferpool data logical reads

        if not (bufferpool_metrics['DATA_PHYSICAL_READS'] is None):
            data['data_physical_reads']=int(bufferpool_metrics['DATA_PHYSICAL_READS'])   #Bufferpool data physical reads

        if not (bufferpool_metrics['DATA_HIT_RATIO_PERCENT'] is None):
            data['data_hit_ratio_percent']=float(bufferpool_metrics['DATA_HIT_RATIO_PERCENT'])   #Individual hit ratio for data bufferpool

        if not (bufferpool_metrics['INDEX_LOGICAL_READS'] is None):
            data['index_logical_reads']=int(bufferpool_metrics['INDEX_LOGICAL_READS'])   #Bufferpool index logical reads

        if not (bufferpool_metrics['INDEX_HIT_RATIO_PERCENT'] is None):
            data['index_hit_ratio_percent']=float(bufferpool_metrics['INDEX_HIT_RATIO_PERCENT'])   #Bufferpool index hit ratio

        if not (bufferpool_metrics['XDA_LOGICAL_READS'] is None):
            data['xda_logical_reads']=int(bufferpool_metrics['XDA_LOGICAL_READS'])    #Bufferpool XDA logical reads

        if not (bufferpool_metrics['XDA_HIT_RATIO_PERCENT'] is None):
            data['xda_hit_ratio_percent']=float(bufferpool_metrics['XDA_HIT_RATIO_PERCENT'])     #Bufferpool XDA hit ratio percent
      
        if not (logutilization_metrics['LOG_UTILIZATION_PERCENT'] is None):
            data['log_utilization_percent']=float(logutilization_metrics['LOG_UTILIZATION_PERCENT'])     #The LOG_UTILIZATION administrative view returns information about log utilization for the currently connected database.Percent utilization of total log space.

        if not (logutilization_metrics['TOTAL_LOG_USED_KB'] is None):
            data['total_log_used_kb']=int(logutilization_metrics['TOTAL_LOG_USED_KB'])    #Total log space used

        if not (logutilization_metrics['TOTAL_LOG_AVAILABLE_KB'] is None):
            data['total_log_available_kb']=int(logutilization_metrics['TOTAL_LOG_AVAILABLE_KB'])     #Total log space available

        data['units']=METRICS_UNITS
        return data

if __name__ == "__main__":

    configurations = {'database': DB2_SAMPLE_DB,'port': DB2_PORT ,'user': DB2_USERNAME ,'password': DB2_PASSWORD}

    db2_plugins = DB2(configurations)

    result = db2_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
    
