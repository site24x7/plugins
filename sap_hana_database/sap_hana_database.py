#!/usr/bin/python

from hdbcli import dbapi
import simplejson as json
import traceback
from decimal import *

host='localhost'
port=30115
username='SYSTEM'
password='password'

PLUGIN_VERSION = "1"
HEARTBEAT=True

metric_units={
    "Index Server Memory Pool Used Size":"GB",
    "Index Server Memory Pool Heap Used Size":"GB",
    "Index Server Memory Pool Shared Used Size":"GB", 
    "Name Server Memory Pool Used Size":"GB",
    "Name Server Memory Pool Heap Used Size":"GB",
    "Name Server Memory Pool Shared Used Size":"GB",
    "Start Time of Services":"Seconds",
    "Free Physical Memory":"GB",
    "Used Physical Memory":"GB",
    "Total CPU Idle Time":"minutes",
    "CPU Usage":"%",
    "Disk Free Size":"GB",
    "Plan Cache Size":"GB"
}
class Sap_hana(object):
    def __init__(self, args):
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password 
        
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        
        self.resultjson = {}

    def metrics_collector(self):
        try:
            db = dbapi.connect(address=self.host, port=self.port, user=self.username, password=self.password)
            cursor = db.cursor()
            
            cursor.execute('SELECT * FROM "M_CONNECTIONS" WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300')
            result = cursor.fetchall()
            running_connection=0
            idle_connection=0
            queuing_connection=0
            for row in result:
                if row["CONNECTION_STATUS"]=="RUNNING":
                    running_connection +=1
                elif row["CONNECTION_STATUS"]=="IDLE":
                    idle_connection +=1
                if row["CONNECTION_STATUS"]=="QUEUING":
                    queuing_connection +=1
            self.resultjson["Running Connections"]=running_connection
            self.resultjson["Idle Connections"]=idle_connection
            self.resultjson["Queuing Connections"]=queuing_connection
                
            cursor.execute("SELECT * FROM M_DISKS")
            result = cursor.fetchall()
            for row in result:
                self.resultjson[(row["USAGE_TYPE"])+" Disk Free Size"]=str(round((row["TOTAL_SIZE"]-row["USED_SIZE"])/1024.0**3 , 4))+" GB"
                
            cursor.execute("SELECT * FROM M_SERVICE_NETWORK_IO")
            result = cursor.fetchall()
            self.resultjson["Total Network I/O Operations"]=len(result)
            
            cursor.execute("SELECT * FROM M_SERVICE_THREADS")
            result = cursor.fetchall()
            active_thread=0
            for row in result:
                if row["IS_ACTIVE"]:
                    active_thread +=1
            self.resultjson["Active Threads"]=active_thread
            
            cursor.execute("SELECT * FROM M_TRANSACTIONS WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300")
            result = cursor.fetchall()
            active_transaction=0
            inactive_transaction=0
            for row in result:
                if row["TRANSACTION_STATUS"]=="INACTIVE":
                    inactive_transaction +=1
                if row["TRANSACTION_STATUS"]=="ACTIVE":
                    active_transaction +=1
            self.resultjson["Inactive Transactions"]=inactive_transaction
            self.resultjson["Active Transactions"]=active_transaction
            
            cursor.execute("SELECT TOTAL_MEMORY_USED_SIZE, CODE_SIZE,STACK_SIZE, HEAP_MEMORY_ALLOCATED_SIZE, HEAP_MEMORY_USED_SIZE,SHARED_MEMORY_ALLOCATED_SIZE,SHARED_MEMORY_USED_SIZE FROM M_SERVICE_MEMORY where Service_name='indexserver' ")
            result = cursor.fetchall()
            self.resultjson["Index Server Memory Pool Used Size"]=str(round(result[0][0]/1024.0**3 , 4))
            self.resultjson["Index Server Memory Pool Heap Used Size"]=str(round(result[0][4]/1024.0**3 , 4))
            self.resultjson["Index Server Memory Pool Shared Used Size"]=str(round(result[0][6]/1024.0**3 , 4))
            
            cursor.execute("SELECT TOTAL_MEMORY_USED_SIZE, CODE_SIZE,STACK_SIZE, HEAP_MEMORY_ALLOCATED_SIZE, HEAP_MEMORY_USED_SIZE,SHARED_MEMORY_ALLOCATED_SIZE,SHARED_MEMORY_USED_SIZE FROM M_SERVICE_MEMORY where Service_name='nameserver' ")
            result = cursor.fetchall()
            self.resultjson["Name Server Memory Pool Used Size"]=str(round(result[0][0]/1024.0**3 , 4))
            self.resultjson["Name Server Memory Pool Heap Used Size"]=str(round(result[0][4]/1024.0**3 , 4))
            self.resultjson["Name Server Memory Pool Shared Used Size"]=str(round(result[0][6]/1024.0**3 , 4))
            
            cursor.execute("SELECT * FROM M_SERVICE_REPLICATION")
            result = cursor.fetchall()
            error_replication=0
            syncing=0
            for row in result:
                if row["REPLICATION_STATUS"]=="ERROR":
                    error_replication +=1
                elif row["REPLICATION_STATUS"]=="SYNCING":
                    syncing +=1
            self.resultjson["Replication Errors"]=error_replication
            self.resultjson["Replication Syncing"]=syncing
            
            cursor.execute("SELECT * from M_DELTA_MERGE_STATISTICS WHERE TYPE='MERGE' AND SUCCESS='FALSE' AND SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300")
            result = cursor.fetchall()
            self.resultjson["Total Delta Merge Errors"]=len(result)
            
            cursor.execute("SELECT * from M_EXPENSIVE_STATEMENTS WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300")
            result = cursor.fetchall()
            self.resultjson["Total Expensive Statements"]=len(result)
            
            cursor.execute("SELECT * from M_BACKUP_CATALOG WHERE SECONDS_BETWEEN(SYS_START_TIME,CURRENT_TIMESTAMP)<300")
            result = cursor.fetchall()
            self.resultjson["Backup Catalogs"]=len(result)
            
            cursor.execute("SELECT * from M_CS_UNLOADS WHERE SECONDS_BETWEEN(UNLOAD_TIME,CURRENT_TIMESTAMP)<300")
            result = cursor.fetchall()
            self.resultjson["Total Column Unloads"]=len(result)

            cursor.execute("select * from M_PREPARED_STATEMENTS where STATEMENT_STATUS = 'ACTIVE'")
            result = cursor.fetchall()
            self.resultjson["Total Active Statements"]=len(result)

            cursor.execute("select * from M_CACHES")
            result = cursor.fetchall()
            self.resultjson["Total Caches"]=len(result)

            cursor.execute("select (sum(DURATION)/1000) from SYS.M_DEV_RECOVERY_")
            result = cursor.fetchall()
            self.resultjson["Start Time of Services"]=Decimal(result[0][0])

            cursor.execute("SELECT * from _SYS_STATISTICS.STATISTICS_ALERT_THRESHOLDS WHERE SECONDS_BETWEEN(REACHED_AT,CURRENT_TIMESTAMP)<300")
            result = cursor.fetchall()
            self.resultjson["Total Alerts"]=len(result)

            cursor.execute("SELECT FREE_PHYSICAL_MEMORY, USED_PHYSICAL_MEMORY,TOTAL_CPU_IDLE_TIME FROM M_HOST_RESOURCE_UTILIZATION WHERE HOST='"+self.host+"'")
            result = cursor.fetchall()
            self.resultjson["Free Physical Memory"]=str(round(result[0][0]/1024.0**3 , 4))
            self.resultjson["Used Physical Memory"]=str(round(result[0][1]/1024.0**3 , 4))
            self.resultjson["Total CPU Idle Time"]=str(round(result[0][2]/60000))

            cursor.execute("SELECT CPU, DISK_SIZE-DISK_USED FROM M_LOAD_HISTORY_HOST WHERE HOST='"+self.host+"'")
            result = cursor.fetchall()

            self.resultjson["CPU Usage"]=result[len(result)-1][0]
            self.resultjson["Disk Free Size"]=str(round(result[len(result)-1][1]/1024.0**3 , 4))

            cursor.execute("SELECT CACHED_PLAN_SIZE, PLAN_CACHE_HIT_RATIO FROM M_SQL_PLAN_CACHE_OVERVIEW WHERE HOST='"+self.host+"'")
            result = cursor.fetchall()

            self.resultjson["Plan Cache Size"]=str(round(result[0][0]/1024.0**3 , 4))
            self.resultjson["Plan Cache Hit Ratio"]=result[0][1]
            
        except Exception as e:
            self.resultjson["msg"]="Error:" + str(traceback.print_exc())
            self.resultjson["status"]=0
            
        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
            applog["logs_enabled"]=True
            applog["log_type_name"]=self.logtypename
            applog["log_file_path"]=self.logfilepath
        else:
            applog["logs_enabled"]=False
        self.resultjson['applog'] = applog
        
        return self.resultjson
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= host)
    parser.add_argument('--port',help="Port",nargs='?', default= port)
    parser.add_argument('--username',help="username",default=username)
    parser.add_argument('--password',help="Password",default=password)
    
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    
    args=parser.parse_args()
	
    saphana = Sap_hana(args)
    resultjson = saphana.metrics_collector()
    resultjson['plugin_version'] = PLUGIN_VERSION
    resultjson['heartbeat_required'] = HEARTBEAT
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True ))


