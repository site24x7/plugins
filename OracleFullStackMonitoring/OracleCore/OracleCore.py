#!/usr/bin/python3
import json
import os

PLUGIN_VERSION=1
HEARTBEAT=True

METRICS_UNITS={
    
    "Buffer Cache Hit Ratio":"%",
    "Cursor Cache Hit Ratio":"%",
    "Library Cache Hit Ratio":"%",
    "Shared Pool Free %":"%",
    "SQL Service Response Time":"sec",
    "Memory Sorts Ratio":"%",
    "Database Wait Time Ratio":"%",
    "Total PGA Allocated":"byte",
    "Total Freeable PGA Memory":"byte",
    "Maximum PGA Allocated":"byte",
    "Total PGA Inuse":"byte"
}

# Reference
metrics = {

    "System Metrics":

    [   
        'Soft Parse Ratio',
        'Total Parse Count Per Sec',
        'Total Parse Count Per Txn',
        'Hard Parse Count Per Sec',
        'Hard Parse Count Per Txn',
        'Parse Failure Count Per Sec',
        'Parse Failure Count Per Txn',
        'Temp Space Used',
        'Session Count',
        'Session Limit %',
        'Database Wait Time Ratio',
        'Memory Sorts Ratio',
        'Disk Sort Per Sec',
        'Rows Per Sort',
        'Total Sorts Per User Call',
        'User Rollbacks Per Sec',
        'SQL Service Response Time',
        'Long Table Scans Per Sec',
        'Average Active Sessions',
        'Logons Per Sec',
        'Global Cache Blocks Los',
        'Global Cache Blocks Corrupted',
        'GC CR Block Received Per Second',
        'Enqueue Timeouts Per Sec',
        'Physical Writes Per Sec',
        'Physical Reads Per Sec',
        'Shared Pool Free %',
        'Library Cache Hit Ratio',
        'Cursor Cache Hit Ratio',
        'Buffer Cache Hit Ratio'
    ],

    
    "PGA Metrics":

    [ "Total PGA Allocated",
      "Total Freeable PGA Memory",
      "Maximum PGA Allocated",
      "Total PGA Inuse"]

}



class oracle:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.username=args.username
        self.password=args.password
        self.sid=args.sid
        self.hostname=args.hostname
        self.port=args.port

        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        




    def metriccollector(self):
        

        metric_queries={
                "system_query":"SELECT VALUE, METRIC_NAME FROM GV$SYSMETRIC WHERE METRIC_NAME IN ( 'Soft Parse Ratio', 'Total Parse Count Per Sec', 'Total Parse Count Per Txn', 'Hard Parse Count Per Sec', 'Hard Parse Count Per Txn', 'Parse Failure Count Per Sec', 'Parse Failure Count Per Txn', 'Temp Space Used', 'Session Count', 'Session Limit %', 'Database Wait Time Ratio', 'Memory Sorts Ratio', 'Disk Sort Per Sec', 'Rows Per Sort', 'Total Sorts Per User Call', 'User Rollbacks Per Sec', 'SQL Service Response Time', 'Long Table Scans Per Sec', 'Average Active Sessions', 'Logons Per Sec', 'Global Cache Blocks Los', 'Global Cache Blocks Corrupted', 'GC CR Block Received Per Second', 'Enqueue Timeouts Per Sec', 'Physical Writes Per Sec', 'Physical Reads Per Sec', 'Shared Pool Free %', 'Library Cache Hit Ratio', 'Cursor Cache Hit Ratio', 'Buffer Cache Hit Ratio' )",
                "pga_query":"SELECT VALUE, NAME FROM gv$pgastat where NAME IN ('total PGA allocated', 'total freeable PGA memory', 'maximum PGA allocated','total PGA inuse')"
                
            }


        try:
            import cx_Oracle
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            return self.maindata

        try:
            try:
                conn = cx_Oracle.connect(self.username,self.password,self.hostname+':'+str(self.port)+'/'+self.sid)
                c = conn.cursor()
            except Exception as e:
                self.maindata['status']=0
                self.maindata['msg']='Exception while making connection: '+str(e)
                return self.maindata
        

            c.execute(metric_queries['system_query'])                
            for row in c:
                value,metric=row
                self.maindata[metric]=value

            c.execute(metric_queries['pga_query'])
            for row in c:
                value,metric=row
                
                #Formatting
                if metric=="total PGA allocated":
                    metric="Total PGA Allocated"
                elif metric=="total freeable PGA memory":
                    metric="Total Freeable PGA Memory"
                elif metric=="maximum PGA allocated":
                    metric="Maximum PGA Allocated"
                elif metric=="total PGA inuse":
                    metric="Total PGA Inuse"

                self.maindata[metric]=value
                



            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                    applog["logs_enabled"]=True
                    applog["log_type_name"]=self.logtypename
                    applog["log_file_path"]=self.logfilepath
            else:
                    applog["logs_enabled"]=False
            self.maindata['applog'] = applog
            self.maindata['tags']=f"oracle_hostname:{self.hostname},oracle_sid:{self.sid}"
            

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0

        


        return self.maindata




if __name__=="__main__":
    
    hostname="localhost"
    port="1521"
    sid="ORCLCDB"
    username=None
    password=None

    oracle_home='/opt/oracle/product/19c/dbhome_1'

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--hostname', help='hostname for oracle',default=hostname)
    parser.add_argument('--port', help='port number for oracle',default=port)
    parser.add_argument('--sid', help='sid for oracle',default=sid)
    parser.add_argument('--username', help='username for oracle',default=username)
    parser.add_argument('--password', help='password for oracle',default=password)

    parser.add_argument('--oracle_home',help='oracle home path',default=oracle_home)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    os.environ['ORACLE_HOME']=args.oracle_home
    obj=oracle(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
