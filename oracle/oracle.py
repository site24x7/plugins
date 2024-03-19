#!/usr/bin/python3
import json
import os
import warnings
warnings.filterwarnings("ignore")
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
    "Total PGA Inuse":"byte",
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
        self.tls=args.tls.lower()
        self.wallet_location=args.wallet_location
        

    def connect(self, dsn):
        try:
            import oracledb
            conn = oracledb.connect(user=self.username, password=self.password, dsn=dsn)
            self.c = conn.cursor()
            return (True, "Connected")
        except Exception as e:
            return (False, str(e))


    def execute_query_bulk(self, query):
        queried_data={}
        try:
            self.c.execute(query)
            for row in self.c:
                value,metric=row
                queried_data[metric.title()]=value
        except Exception as e:
            queried_data["status"]=0
            queried_data['msg']=str(e)
        return queried_data


    def execute_query(self,metric_query_name):
        queried_data={}
        try:
            self.c.execute(self.metric_queries["Single Queries"][metric_query_name])
            for row in self.c:
                queried_data[metric_query_name]=row[0]
        except Exception as e:
            queried_data["status"]=0
            queried_data['msg']=str(e)
        return queried_data
    
    
    def execute_waits_query(self,metric_query_name):
        queried_data={}
        wait_units={}
        try:
            self.c.execute(self.metric_queries[metric_query_name])
            for row in self.c:
                name,time_waited,wait_count=row
                queried_data[name+"_time_waited"]=time_waited/100
                queried_data[name+"_wait_count"]=wait_count
                wait_units[name+"_time_waited"]='sec'
        except Exception as e:
            queried_data['status']=0
            queried_data['msg']=str(e)
        METRICS_UNITS.update(wait_units)
        return  queried_data


    def execute_tablespace_query(self, metric_query_name):

        db_block_size=8192
        self.c.execute("select value from v$parameter where name = 'db_block_size'")
        for row in self.c:
            db_block_size=row[0]
            break

        queried_data={}
        try:
            self.c.execute(self.metric_queries[metric_query_name])        
            tbs_list=[]
            for row in self.c:
                tbs_dict={}
                tbs_dict["name"]=row[0]
                if row[2]:tbs_dict['Used_Space']=int(row[2])*int(db_block_size)/1024/1024
                else:tbs_dict['Used_Space']=0

                if row[3]:tbs_dict['Tablespace_Size']=int(row[3])*int(db_block_size)/1024/1024
                else:tbs_dict['Tablespace Size']=0

                if row[4]:tbs_dict['Used_Percent']=row[4]
                else:tbs_dict['Used_Percent']=0
                if row[7]=="OFFLINE":
                    tbs_dict['TB_Status']=0
                    tbs_dict['status']=0
                else:
                    tbs_dict['TB_Status']=1
                    tbs_dict['status']=1

                tbs_list.append(tbs_dict)
            queried_data['Tablespace_Details']=tbs_list

        except Exception as e:
            queried_data["status"]=0
            queried_data['msg']=str(e)

        return queried_data        

    def execute_pdb(self, metric_query_name):
        queried_data={}
        try:
            self.c.execute(self.metric_queries[metric_query_name])    
            pdb_list=[]    
            for row in self.c:
                pdb_dict={}
                pdb_dict['name']=row[0]
                pdb_dict['pdb_id']=row[1]
                pdb_list.append(pdb_dict)
            queried_data['pdb_details']=pdb_list

        except Exception as e:
            queried_data['status']=0
            queried_data['msg']=str(e)
        return queried_data



    def metriccollector(self):


        self.metric_queries={
            "Bulk Queries":{

                "system_query":"SELECT VALUE, METRIC_NAME FROM GV$SYSMETRIC WHERE METRIC_NAME IN ( 'Soft Parse Ratio', 'Total Parse Count Per Sec', 'Total Parse Count Per Txn', 'Hard Parse Count Per Sec', 'Hard Parse Count Per Txn', 'Parse Failure Count Per Sec', 'Parse Failure Count Per Txn', 'Temp Space Used', 'Session Count', 'Session Limit %', 'Database Wait Time Ratio', 'Memory Sorts Ratio', 'Disk Sort Per Sec', 'Rows Per Sort', 'Total Sorts Per User Call', 'User Rollbacks Per Sec', 'SQL Service Response Time', 'Long Table Scans Per Sec', 'Average Active Sessions', 'Logons Per Sec', 'Global Cache Blocks Los', 'Global Cache Blocks Corrupted', 'GC CR Block Received Per Second', 'Enqueue Timeouts Per Sec', 'Physical Writes Per Sec', 'Physical Reads Per Sec', 'Shared Pool Free %', 'Library Cache Hit Ratio', 'Cursor Cache Hit Ratio', 'Buffer Cache Hit Ratio' )",
                "pga_query":"SELECT VALUE, NAME FROM gv$pgastat where NAME IN ('total PGA allocated', 'total freeable PGA memory', 'maximum PGA allocated','total PGA inuse')",
                "sga_query":"""SELECT sga.value, CONCAT('SGA ',sga.name) AS name FROM GV$SGA sga INNER JOIN GV$INSTANCE inst ON sga.inst_id = inst.inst_id""",
                },
    
            "Single Queries":{

                "Rman Failed Backup Count":"""SELECT COUNT(*) as "Rman Failed Backup Count" FROM v$rman_status WHERE operation = 'BACKUP' AND status = 'FAILED' AND END_TIME >= sysdate-(5/(24*60))""",
                "Dict Cache Hit Ratio":"""select (1-(sum(getmisses)/sum(gets)))*100 as " DICT CACHE HIT RATIO" from gv$rowcache""",
                "Long Running Queries":"""SELECT sum(num) AS total FROM (( SELECT i.inst_id, 1 AS num FROM gv$session s, gv$instance i WHERE i.inst_id=s.inst_id AND s.status='ACTIVE' AND s.type <>'BACKGROUND' AND s.last_call_et > 60 GROUP BY i.inst_id ) UNION ( SELECT i.inst_id, 0 AS num FROM gv$session s, gv$instance i WHERE i.inst_id=s.inst_id)) GROUP BY inst_id""",
                "Blocking Locks":"""SELECT count(*) FROM gv$session WHERE blocking_session IS NOT NULL""",
                "SGA Hit Ratio":"""SELECT (1 - (phy.value - lob.value - dir.value)/ses.value) as ratio FROM GV$SYSSTAT ses, GV$SYSSTAT lob, GV$SYSSTAT dir, GV$SYSSTAT phy, GV$INSTANCE inst WHERE ses.name='session logical reads' AND dir.name='physical reads direct' AND lob.name='physical reads direct (lob)' AND phy.name='physical reads' AND ses.inst_id=inst.inst_id AND lob.inst_id=inst.inst_id AND dir.inst_id=inst.inst_id AND phy.inst_id=inst.inst_id""",
                "SGA Log Alloc Retries":"""SELECT (rbar.value/re.value) as ratio FROM GV$SYSSTAT rbar, GV$SYSSTAT re, GV$INSTANCE inst WHERE rbar.name like 'redo buffer allocation retries' AND re.name like 'redo entries' AND re.inst_id=inst.inst_id AND rbar.inst_id=inst.inst_id""",
                "SGA Shared Pool Dict Cache Ratio":"""SELECT (SUM(rcache.getmisses)/SUM(rcache.gets)) as ratio FROM GV$rowcache rcache, GV$INSTANCE inst WHERE inst.inst_id=rcache.inst_id GROUP BY inst.inst_id""",
                "SGA Shared Pool Lib Cache Hit Ratio":"""SELECT libcache.gethitratio as ratio FROM GV$librarycache libcache, GV$INSTANCE inst WHERE namespace='SQL AREA' AND inst.inst_id=libcache.inst_id""",
                "SGA Shared Pool Lib Cache Reload Ratio":"""SELECT (sum(libcache.reloads)/sum(libcache.pins)) AS ratio FROM GV$librarycache libcache, GV$INSTANCE inst WHERE inst.inst_id=libcache.inst_id GROUP BY inst.inst_id""",
                "SGA Shared Pool Lib Cache Sharable Statement":"""SELECT SUM(sqlarea.sharable_mem) AS sum FROM GV$sqlarea sqlarea, GV$INSTANCE inst WHERE sqlarea.executions > 5 AND inst.inst_id=sqlarea.inst_id GROUP BY inst.inst_id""",
                "SGA Shared Pool Lib Cache Shareable User":"""SELECT SUM(250 * sqlarea.users_opening) AS sum FROM GV$sqlarea sqlarea, GV$INSTANCE inst WHERE inst.inst_id=sqlarea.inst_id GROUP BY inst.inst_id""",
                "Total Memory":"""SELECT SUM(value) AS sum FROM GV$sesstat, GV$statname, GV$INSTANCE inst WHERE name = 'session uga memory max' AND GV$sesstat.statistic#=GV$statname.statistic# AND GV$sesstat.inst_id=inst.inst_id AND GV$statname.inst_id=inst.inst_id GROUP BY inst.inst_id"""
                    },

            "Tablespace Query":f"""  SELECT b.TABLESPACE_NAME as "dba_tablespace", d.* , b.CONTENTS, b.LOGGING, b.STATUS FROM dba_tablespace_usage_metrics d FULL JOIN dba_tablespaces b ON d.TABLESPACE_NAME = b.TABLESPACE_NAME""",
            "Waits Query":"""select n.name , round(m.time_waited,3) time_waited, m.wait_count from v$eventmetric m, v$event_name n where m.event_id=n.event_id and n.name in ( 'free buffer waits' , 'buffer busy waits', 'latch free', 'library cache pin', 'library cache load lock', 'log buffer space', 'library object reloads count', 'enqueue waits', 'db file parallel read', 'db file parallel write', 'control file sequential read', 'control file parallel write', 'write complete waits', 'log file sync', 'sort segment request', 'direct path read', 'direct path write')""",
            "PDB Query":"""SELECT a.PDB_NAME, a.PDB_ID,  a.STATUS, b.OPEN_MODE, b.RESTRICTED, b.OPEN_TIME FROM DBA_PDBS a join V$PDBS b on a.PDB_NAME=b.NAME"""
                }

        if self.tls=="True":
            dsn=f"""(DESCRIPTION=
                    (ADDRESS=(PROTOCOL=tcps)(HOST={self.hostname})(PORT={self.port}))
                    (CONNECT_DATA=(SERVICE_NAME={self.sid}))
                    (SECURITY=(MY_WALLET_DIRECTORY={self.wallet_location}))
                    )"""
        else:
            dsn=f"{self.hostname}:{self.port}/{self.sid}"


        connection_status=self.connect(dsn)
        if not connection_status[0]:
            self.maindata['status']=0
            self.maindata['msg']=connection_status[1]
            return self.maindata

        for _ ,bulk_query in self.metric_queries['Bulk Queries'].items():
            query_output_data=self.execute_query_bulk(bulk_query)
            self.maindata.update(query_output_data)
            if 'status' in self.maindata and self.maindata['status']==0:
                return self.maindata

        for query_name in self.metric_queries['Single Queries']:
            query_output_data=self.execute_query(query_name)
            self.maindata.update(query_output_data)
            if 'status' in self.maindata and self.maindata['status']==0:
                return self.maindata
        
        query_output_data=self.execute_tablespace_query("Tablespace Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
                return self.maindata

        query_output_data=self.execute_waits_query("Waits Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
                return self.maindata        

        query_output_data=self.execute_pdb("PDB Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
                return self.maindata 

        self.maindata['tabs']={
            "Tablespace Details":{
                "order":1,
                "tablist":[
                    "Tablespace_Details"
                ]},
            "PDB Details":{
                "order":2,
                "tablist":[
                    "pdb_details"
                ]
            }
            }
        

        self.maindata['units']=METRICS_UNITS
        return self.maindata



if __name__=="__main__":
    
    hostname="localhost"
    port="1521"
    sid="ORCLCDB"
    username="oracle_user"
    password="oracle_password"
    tls="False"
    wallet_location=None
    oracle_home="/opt/oracle/product/19c/dbhome_1/"

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--hostname', help='hostname for oracle',default=hostname)
    parser.add_argument('--port', help='port number for oracle',default=port)
    parser.add_argument('--sid', help='sid for oracle',default=sid)
    parser.add_argument('--username', help='username for oracle',default=username)
    parser.add_argument('--password', help='password for oracle',default=password)
    parser.add_argument('--tls', help='tls support for oracle',default=tls)
    parser.add_argument('--wallet_location', help='oracle wallet location',default=wallet_location)
    parser.add_argument('--oracle_home',help='oracle home path',default=oracle_home)

    args=parser.parse_args()

    os.environ['ORACLE_HOME']=args.oracle_home
    obj=oracle(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
