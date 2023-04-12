#!/usr/bin/python3

import json
import ibm_db
import traceback
PLUGIN_VERSION = "1"

HEARTBEAT="true"

METRICS_UNITS={'tbsp_page_size':'bytes'}

class DB2(object):
    
    def __init__(self,args):
        self.DB2_HOST=args.host
        self.DB2_PORT=args.port
        self.DB2_USERNAME=args.username
        self.DB2_PASSWORD=args.password
        self.DB2_SAMPLE_DB=args.sample_db
        self.DB2_TBSP_NAME=args.tbsp_name
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
            data['msg']='ibm_db module not installed'
            return data

        if not self.getDbConnection():
            data['status']=0
            data['msg']='Connection Error'
            return data

        tablespace_metrics = [
            'tbsp_name',
            'tbsp_page_size',
            'tbsp_state',
            'tbsp_total_pages',
            'tbsp_usable_pages',
            'tbsp_used_pages',
        ]

        metric_string=", ".join(tablespace_metrics)
        tablespace_metric_query=f"SELECT {metric_string} FROM TABLE(MON_GET_TABLESPACE(NULL, -1)) WHERE TBSP_NAME='{self.DB2_TBSP_NAME}'"
        database_metrics=self.executeQuery(self.connection,tablespace_metric_query)
        for metric in tablespace_metrics:
            if metric.upper() in database_metrics:
                data[metric] = database_metrics[metric.upper()]
            
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
    parser.add_argument('--tbsp_name' ,help="tablespace name ",nargs='?', default= "SYSCATSPACE")

    args=parser.parse_args()
    	
    db2_plugins = DB2(args)

    result = db2_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
    
