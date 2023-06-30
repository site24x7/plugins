#!/usr/bin/python3
import json
import os
import warnings
warnings.filterwarnings("ignore")

PLUGIN_VERSION=1
HEARTBEAT=True

METRICS_UNITS={
    "SGA Fixed Size":"bytes",
    "SGA Variable Size":"bytes",
    "SGA Database Buffers":"bytes",
    "SGA Redo Buffers":"bytes",
    "SGA Shared Pool Lib Cache Sharable Statement":"bytes",
    "SGA Shared Pool Lib Cache Shareable User":"bytes",
    "Total Memory":"bytes"
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
                "query1":"SELECT sga.name, sga.value FROM GV$SGA sga, GV$INSTANCE inst WHERE sga.inst_id=inst.inst_id",

                "query2":
                """
                SELECT (1 - (phy.value - lob.value - dir.value)/ses.value) as ratio
                FROM GV$SYSSTAT ses, GV$SYSSTAT lob, GV$SYSSTAT dir, GV$SYSSTAT phy, GV$INSTANCE inst
                WHERE ses.name='session logical reads'
                AND dir.name='physical reads direct'
                AND lob.name='physical reads direct (lob)'
                AND phy.name='physical reads'
                AND ses.inst_id=inst.inst_id
                AND lob.inst_id=inst.inst_id
                AND dir.inst_id=inst.inst_id
                AND phy.inst_id=inst.inst_id
                """,

                "query3" :
                """
                SELECT (rbar.value/re.value) as ratio
                FROM GV$SYSSTAT rbar, GV$SYSSTAT re, GV$INSTANCE inst
                WHERE rbar.name like 'redo buffer allocation retries'
                AND re.name like 'redo entries'
                AND re.inst_id=inst.inst_id AND rbar.inst_id=inst.inst_id
                """, 

                "query4":
                """
                SELECT (SUM(rcache.getmisses)/SUM(rcache.gets)) as ratio
                FROM GV$rowcache rcache, GV$INSTANCE inst
                WHERE inst.inst_id=rcache.inst_id
                GROUP BY inst.inst_id
                """,

                "query5":
                """
                SELECT libcache.gethitratio as ratio
                FROM GV$librarycache libcache, GV$INSTANCE inst
                WHERE namespace='SQL AREA' AND inst.inst_id=libcache.inst_id
                """,

                "query6":
                """
                SELECT (sum(libcache.reloads)/sum(libcache.pins)) AS ratio
                FROM GV$librarycache libcache, GV$INSTANCE inst
                WHERE inst.inst_id=libcache.inst_id
                GROUP BY inst.inst_id
                """,

                "query7":
                """
                SELECT SUM(sqlarea.sharable_mem) AS sum
                FROM GV$sqlarea sqlarea, GV$INSTANCE inst
                WHERE sqlarea.executions > 5 AND inst.inst_id=sqlarea.inst_id
                GROUP BY inst.inst_id
                """,

                "query8":
                """
                SELECT SUM(250 * sqlarea.users_opening) AS sum
                FROM GV$sqlarea sqlarea, GV$INSTANCE inst
                WHERE inst.inst_id=sqlarea.inst_id
                GROUP BY inst.inst_id

                """,

                "query9":
                """
                SELECT SUM(value) AS sum
                FROM GV$sesstat, GV$statname, GV$INSTANCE inst
                WHERE name = 'session uga memory max'
                AND GV$sesstat.statistic#=GV$statname.statistic#
                AND GV$sesstat.inst_id=inst.inst_id
                AND GV$statname.inst_id=inst.inst_id
                GROUP BY inst.inst_id
                """
            }


        try:
            import oracledb
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            return self.maindata

        try:
            try:
                conn = oracledb.connect(user=self.username, password=self.password, dsn=f"{self.hostname}:{self.port}/{self.sid}")
                c = conn.cursor()
            except Exception as e:
                self.maindata['status']=0
                self.maindata['msg']='Exception while making connection: '+str(e)
                return self.maindata
        

            c.execute(metric_queries['query1'])
            for row in c:
                metric,value=row
                self.maindata["SGA "+metric]=value

            c.execute(metric_queries['query2'])
            for row in c:
                value=row[0]
                self.maindata["SGA Hit Ratio"]=value
            
            c.execute(metric_queries['query3'])
            for row in c:
                value=row[0]
                self.maindata["SGA Log Alloc Retries"]=value
            
            c.execute(metric_queries['query4'])
            for row in c:
                value=row[0]
                self.maindata["SGA Shared Pool Dict Cache Ratio"]=value

            c.execute(metric_queries['query5'])
            for row in c:
                value=row[0]
                self.maindata["SGA Shared Pool Lib Cache Hit Ratio"]=value        

            c.execute(metric_queries['query6'])
            for row in c:
                value=row[0]
                self.maindata["SGA Shared Pool Lib Cache Reload Ratio"]=value   

            c.execute(metric_queries['query7'])
            for row in c:
                value=row[0]
                self.maindata["SGA Shared Pool Lib Cache Sharable Statement"]=value  

            c.execute(metric_queries['query8'])
            for row in c:
                value=row[0]
                self.maindata["SGA Shared Pool Lib Cache Shareable User"]=value  	

            c.execute(metric_queries['query9'])
            for row in c:
                value=row[0]
                self.maindata["Total Memory"]=value            
            c.close()
            conn.close()

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
