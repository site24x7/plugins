#!/usr/bin/python3

import json
import ibm_db
import traceback
PLUGIN_VERSION = "1"

HEARTBEAT="true"

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
               'total_log_available_kb':'KB',
               'lock_timeouts':'ms',
               'lock_wait_time':'ms'}

class DB2(object):
    
    def __init__(self,args):
        self.DB2_HOST=args.host
        self.DB2_PORT=args.port
        self.DB2_USERNAME=args.username
        self.DB2_PASSWORD=args.password
        self.DB2_SAMPLE_DB=args.sample_db
        self.connection = None

    def getDbConnection(self):
        try:
            url="DATABASE="+self.DB2_SAMPLE_DB+";HOSTNAME="+self.DB2_HOST+";PORT="+self.DB2_PORT+";PROTOCOL=TCPIP;UID="+self.DB2_USERNAME+";PWD="+self.DB2_PASSWORD+";"
            db = ibm_db.connect(url, "", "")  #Connect to an uncataloged database
            self.connection = db
        except Exception as e:
            traceback.print_exc()
            return False
        return True

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
            data['msg']='ibm_db module not installed' + "\n Solution : Use the following command to install ibm_db\n pip install ibm_db \n(or)\n pip3 install ibm_db"
            return data

        if not self.getDbConnection():
            data['status']=0
            data['msg']='Connection Error'
            return data
        

        bufferpool = self.executeQuery(self.connection, 'SELECT COUNT(*) as NO_OF_BUFFERPOOLS FROM syscat.bufferpools')
        if not (bufferpool['NO_OF_BUFFERPOOLS'] is None):
            data['no_of_bufferpools']=bufferpool['NO_OF_BUFFERPOOLS']

        metrics={
        'bufferpool_metric_list' : [  'no_of_bufferpools',
                                    'total_logical_reads',
                                    'total_physical_reads',
                                    'total_hit_ratio_percent',
                                    'data_logical_reads',
                                    'data_physical_reads',
                                    'data_hit_ratio_percent',
                                    'index_logical_reads',
                                    'index_hit_ratio_percent',
                                    'xda_logical_reads',
                                    'xda_hit_ratio_percent'
                                ],


        'logutilization_metric_list' : ["log_utilization_percent",
                                     "total_log_used_kb",
                                     "total_log_available_kb"
                                    ],

        'database_metric_list'   :  ['appls_cur_cons', 
                                    'appls_in_db2', 
                                    'connections_top',
                                    'db_status', 
                                    'deadlocks', 
                                    'lock_list_in_use', 
                                    'lock_timeouts', 
                                    'lock_wait_time', 
                                    'lock_waits', 
                                    'num_locks_held', 
                                    'num_locks_waiting', 
                                    'rows_modified', 
                                    'rows_read', 
                                    'rows_returned', 
                                    'total_cons']
        }

        bufferpool_metrics = self.executeQuery(self.connection, 'SELECT SUM(TOTAL_LOGICAL_READS) as TOTAL_LOGICAL_READS,SUM(TOTAL_PHYSICAL_READS) as TOTAL_PHYSICAL_READS,AVG(TOTAL_HIT_RATIO_PERCENT) as TOTAL_HIT_RATIO_PERCENT,SUM(DATA_LOGICAL_READS) as DATA_LOGICAL_READS,SUM(DATA_PHYSICAL_READS) as DATA_PHYSICAL_READS,AVG(DATA_HIT_RATIO_PERCENT) as DATA_HIT_RATIO_PERCENT,SUM(INDEX_LOGICAL_READS) as INDEX_LOGICAL_READS,AVG(INDEX_HIT_RATIO_PERCENT) as INDEX_HIT_RATIO_PERCENT,SUM(XDA_LOGICAL_READS) as XDA_LOGICAL_READS,AVG(XDA_HIT_RATIO_PERCENT) as XDA_HIT_RATIO_PERCENT FROM SYSIBMADM.BP_HITRATIO')
        for metric in metrics['bufferpool_metric_list']:
            if metric.upper() in bufferpool_metrics:
                data[metric]=bufferpool_metrics[metric.upper()]
            else:
                data[metric]=0            

        logutilization_metrics=self.executeQuery(self.connection,"SELECT AVG(LOG_UTILIZATION_PERCENT) as LOG_UTILIZATION_PERCENT,SUM(TOTAL_LOG_USED_KB) as TOTAL_LOG_USED_KB, SUM(TOTAL_LOG_AVAILABLE_KB) as TOTAL_LOG_AVAILABLE_KB FROM SYSIBMADM.LOG_UTILIZATION")
        for metric in metrics['logutilization_metric_list']:
            if metric.upper() in logutilization_metrics:
                data[metric]=logutilization_metrics[metric.upper()]      
            else:
                data[metric]=0

        database_metric_query=f'SELECT {", ".join(metrics["database_metric_list"])} FROM TABLE(MON_GET_DATABASE(-1))'
        database_metrics=self.executeQuery(self.connection,database_metric_query)
        for metric in metrics['database_metric_list']:
            if metric.upper() in database_metrics:
                data[metric]=database_metrics[metric.upper()]
            else:
                data[metric]=0
        
        ibm_db.close(self.connection)
        

        data['units']=METRICS_UNITS
        return data




if __name__ == "__main__":

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "50000")
    parser.add_argument('--username',help="username", default= "db2inst1")
    parser.add_argument('--password',help="Password", default= "db2inst1")
    parser.add_argument('--sample_db' ,help="Sample db",nargs='?', default= "Sample")
    args=parser.parse_args()
    	
    db2_plugins = DB2(args)

    result = db2_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
    
