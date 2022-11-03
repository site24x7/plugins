#!/usr/bin/python

from hdbcli import dbapi
import json
import traceback

host='localhost'
port=39041
username='system'
password=''

PLUGIN_VERSION = "1"
HEARTBEAT=True

metric_units={
    "INDEX_SERVER_MEMORY_POOL_USED_SIZE":"GB",
    "INDEX_SERVER_MEMORY_POOL_HEAP_USED_SIZE":"GB",
    "INDEX_SERVER_MEMORY_POOL_SHARED_USED_SIZE":"GB",
    "NAMESERVER_MEMORY_POOL_USED_SIZE":"GB",
    "NAMESERVER_MEMORY_POOL_HEAP_USED_SIZE":"GB",
    "NAMESERVER_MEMORY_POOL_SHARED_USED_SIZE":"GB"
}
class Sap_hana(object):
    def __init__(self, args):
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password 
        self.resultjson = {}

    def metrics_collector(self):
        try:
            db = dbapi.connect(address=self.host, port=self.port, user=self.username, password=self.password)
            cursor = db.cursor()
            
            cursor.execute('SELECT * FROM "M_CONNECTIONS" WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIME)<300')
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
            self.resultjson["RUNNING_CONNECTIONS"]=running_connection
            self.resultjson["IDLE_CONNECTIONS"]=idle_connection
            self.resultjson["QUEUING_CONNECTIONS"]=queuing_connection
                
            cursor.execute("SELECT * FROM M_DISKS")
            result = cursor.fetchall()
            for row in result:
                self.resultjson[(row["USAGE_TYPE"])+"_DISK_FREE_SIZE"]=str(round((row["TOTAL_SIZE"]-row["USED_SIZE"])/1024.0**3 , 4))+" GB"
                
            cursor.execute("SELECT * FROM M_SERVICE_NETWORK_IO")
            result = cursor.fetchall()
            self.resultjson["TOTAL_NETWORK_IO_OPERATIONS"]=len(result)
            
            cursor.execute("SELECT * FROM M_SERVICE_THREADS")
            result = cursor.fetchall()
            active_thread=0
            for row in result:
                if row["IS_ACTIVE"]:
                    active_thread +=1
            self.resultjson["ACTIVE_THREADS"]=active_thread
            
            cursor.execute("SELECT * FROM M_TRANSACTIONS WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIME)<300")
            result = cursor.fetchall()
            active_transaction=0
            inactive_transaction=0
            for row in result:
                if row["TRANSACTION_STATUS"]=="INACTIVE":
                    inactive_transaction +=1
                if row["TRANSACTION_STATUS"]=="ACTIVE":
                    active_transaction +=1
            self.resultjson["INACTIVE_TRANSACTIONS"]=inactive_transaction
            self.resultjson["ACTIVE_TRANSACTIONS"]=active_transaction
            
            cursor.execute("SELECT TOTAL_MEMORY_USED_SIZE, CODE_SIZE,STACK_SIZE, HEAP_MEMORY_ALLOCATED_SIZE, HEAP_MEMORY_USED_SIZE,SHARED_MEMORY_ALLOCATED_SIZE,SHARED_MEMORY_USED_SIZE FROM M_SERVICE_MEMORY where Service_name='indexserver' ")
            result = cursor.fetchall()
            self.resultjson["INDEX_SERVER_MEMORY_POOL_USED_SIZE"]=str(round(result[0][0]/1024.0**3 , 4))
            self.resultjson["INDEX_SERVER_MEMORY_POOL_HEAP_USED_SIZE"]=str(round(result[0][4]/1024.0**3 , 4))
            self.resultjson["INDEX_SERVER_MEMORY_POOL_SHARED_USED_SIZE"]=str(round(result[0][6]/1024.0**3 , 4))
            
            cursor.execute("SELECT TOTAL_MEMORY_USED_SIZE, CODE_SIZE,STACK_SIZE, HEAP_MEMORY_ALLOCATED_SIZE, HEAP_MEMORY_USED_SIZE,SHARED_MEMORY_ALLOCATED_SIZE,SHARED_MEMORY_USED_SIZE FROM M_SERVICE_MEMORY where Service_name='nameserver' ")
            result = cursor.fetchall()
            self.resultjson["NAMESERVER_MEMORY_POOL_USED_SIZE"]=str(round(result[0][0]/1024.0**3 , 4))
            self.resultjson["NAMESERVER_MEMORY_POOL_HEAP_USED_SIZE"]=str(round(result[0][4]/1024.0**3 , 4))
            self.resultjson["NAMESERVER_MEMORY_POOL_SHARED_USED_SIZE"]=str(round(result[0][6]/1024.0**3 , 4))
            
            cursor.execute("SELECT * FROM M_SERVICE_REPLICATION")
            result = cursor.fetchall()
            error_replication=0
            syncing=0
            for row in result:
                if row["REPLICATION_STATUS"]=="ERROR":
                    error_replication +=1
                elif row["REPLICATION_STATUS"]=="SYNCING":
                    syncing +=1
            self.resultjson["REPLICATION_ERRORS"]=error_replication
            self.resultjson["REPLICATION_SYNCING"]=syncing
            
            cursor.execute("SELECT * from M_DELTA_MERGE_STATISTICS WHERE TYPE='MERGE' AND SUCCESS='FALSE' AND SECONDS_BETWEEN(START_TIME,CURRENT_TIME)<300")
            result = cursor.fetchall()
            self.resultjson["TOTAL_DELTA_MERGE_ERRORS"]=len(result)
            
            cursor.execute("SELECT * from M_EXPENSIVE_STATEMENTS WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIME)<300")
            result = cursor.fetchall()
            self.resultjson["TOTAL_EXPENSIVE_STATEMENTS"]=len(result)
            
            cursor.execute("SELECT * from M_BACKUP_CATALOG WHERE SECONDS_BETWEEN(SYS_START_TIME,CURRENT_TIME)<300")
            result = cursor.fetchall()
            self.resultjson["BACKUP_CATALOGS"]=len(result)
            
        except Exception as e:
            self.resultjson["msg"]="Error:" + str(traceback.print_exc())
            self.resultjson["status"]=0
        return self.resultjson
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= host)
    parser.add_argument('--port',help="Port",nargs='?', default= port)
    parser.add_argument('--username',help="username",default=username)
    parser.add_argument('--password',help="Password",default=password)
    args=parser.parse_args()
	
    saphana = Sap_hana(args)
    resultjson = saphana.metrics_collector()
    resultjson['plugin_version'] = PLUGIN_VERSION
    resultjson['heartbeat_required'] = HEARTBEAT
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
