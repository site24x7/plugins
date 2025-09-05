#!/usr/bin/python3.8
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
    "Soft Parse Ratio":"%",
    "Memory Sorts Ratio":"%",
    "Session Limit %":"%",
    "Shared Pool Free %":"%",
    "SQL Service Response Time":"sec",
    "Memory Sorts Ratio":"%",
    "Database Wait Time Ratio":"%",
    "Total PGA Allocated":"bytes",
    "Total Freeable PGA Memory":"bytes",
    "Maximum PGA Allocated":"bytes",
    "Total PGA Inuse":"bytes",
    "SGA Fixed Size":"bytes",
    "SGA Variable Size":"bytes",
    "SGA Database Buffers":"bytes",
    "SGA Redo Buffers":"bytes",
    "SGA Shared Pool Lib Cache Sharable Statement":"bytes",
    "SGA Shared Pool Lib Cache Shareable User":"bytes",
    "Total Memory":"bytes",
    "FRA Space Limit":"mb",
    "FRA Space Used":"mb",
    "FRA Space Reclaimable":"mb",
    "Response Time":"ms",
    "Tablespace_List":{
        "Tablespace_Size":"mb",
        "Used_Percent":"%",
        "Used_Space":"mb"
    },
    "Tablespace_Datafile":{
        "Data_File_Size":"mb",
        "Max_Data_File_Size":"mb",
        "Usable_Data_File_Size":"mb"
    },
    "PDB":{
        "PDB_Size":"mb"
    },
    "ASM":{
        "total_gb": "GB",
        "free_gb": "GB",
        "pct_free": "%"
    },
    "CPU Usage":"seconds",
    "Enqueue Deadlocks":"count",
    "Exchange Deadlocks":"count",
    "Logical Reads":"count",
    "Transactions Per Second":"txn/sec",
    "Queries Per Second":"query/sec",
    "DB Time":"seconds",
    "Rollback Segments": "count",
    "Rollback Segment Initial Extent":"bytes",
    "Rollback Segment Next Extent":"bytes",
    "Rollback Segment Max Extents":"count",
    "Slow Query Latency 95 Percentile":"ms",
    "Full Table Scans Short":"count",
    "Full Table Scans Long":"count",
    "Full Table Scans Rowid":"count",
    "Full Table Scans IM":"count",
    "Failed Backups":"count",
    "Alert Log Recent Errors":"count"
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
            oracledb.init_oracle_client()
            self.conn = oracledb.connect(user=self.username, password=self.password, dsn=dsn)
            self.c = self.conn.cursor()
            return (True, "Connected")
        except Exception as e:
            self.conn = None
            self.c = None
            return (False, str(e))

    def close_connection(self):
        try:
            if hasattr(self, 'c') and self.c:
                self.c.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception:
            pass

    def execute_query_row_col(self, query, col_change=False):
        queried_data={}
        try:
            self.c.execute(query)
            col_names = [row[0] for row in self.c.description]
            tot_cols=len(col_names)
            if col_change:
                for row in self.c:
                    for i in range(tot_cols):
                        queried_data[str.title(col_names[i])]=row[i]
                    break
            else:
                for row in self.c:
                    for i in range(tot_cols):
                        queried_data[col_names[i]]=row[i]
                    break
        except Exception as e:
            queried_data["status"]=0
            queried_data['msg']=str(e)
        return queried_data

    def execute_query_bulk(self, query, query_name):
        queried_data={}
        try:
            self.c.execute(query)
            if query_name=="pga_query":
                for row in self.c:
                    value,metric=row
                    metric=str.title(metric).replace("Pga","PGA")
                    if metric=="Maximum PGA Allocated":
                        value=str(value/1024/1024)+" MB"
                    queried_data[metric]=value
            elif query_name=="asm_query":
                asm_list = []
                for row in self.c:
                    asm_name, asm_total_gb, asm_free_gb, asm_pct_free, asm_limit, asm_threshold = row
                    asm_list.append({"name": asm_name, "ASM_TOTAL_GB" :asm_total_gb, "ASM_FREE_GB": asm_free_gb, "ASM_PCT_FREE": asm_pct_free ,"ASM_LIMIT": asm_limit, "ASM_THRESHOLD": asm_threshold})
                queried_data['ASM']=asm_list
            else:
                for row in self.c:
                    value,metric=row
                    queried_data[metric]=value                
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
                queried_data[str.title(name)+" Time Waited (microsec)"]=time_waited
                queried_data[str.title(name)+" Wait Count"]=wait_count
                wait_units[str.title(name)+" Time Waited (microsec)"]='microseconds'
        except Exception as e:
            queried_data['status']=0
            queried_data['msg']=str(e)
        METRICS_UNITS.update(wait_units)
        return  queried_data

    def execute_tablespace_metrics(self):
        db_block_size=8192
        self.c.execute("select value from v$parameter where name = 'db_block_size'")
        for row in self.c:
            db_block_size=row[0]
            break
        queried_data={}
        try:
            self.c.execute(self.metric_queries["Tablespace Queries"]["Tablespace Metrics Query"])        
            tbs_list=[]
            for row in self.c:
                tbs_dict={}
                tbs_dict["name"]=row[0]
                if row[2]:tbs_dict['Used_Space']=int(row[2])*int(db_block_size)/1024/1024
                else:tbs_dict['Used_Space']=0
                if row[3]:tbs_dict['Tablespace_Size']=int(row[3])*int(db_block_size)/1024/1024
                else:tbs_dict['Tablespace_Size']=0
                if row[4]:tbs_dict['Used_Percent']=row[4]
                else:tbs_dict['Used_Percent']=0
                if row[7]=="OFFLINE":
                    tbs_dict['TB_Status']=0
                    tbs_dict['status']=0
                else:
                    tbs_dict['TB_Status']=1
                    tbs_dict['status']=1
                tbs_list.append(tbs_dict)
            queried_data['Tablespace_List']=tbs_list
        except Exception as e:
            queried_data["status"]=0
            queried_data['msg']=str(e)
        return queried_data
        
    def execute_tablespace_datafile(self):
        queried_data={}
        try:
            self.c.execute(self.metric_queries["Tablespace Queries"]["Tablespace Datafile Query"])     
            tbs_list=[]   
            for row in self.c:
                tb_dict={}
                tbs_name=row[0]
                tbs_datafile=row[1].split("/")[-1]
                name=tbs_datafile
                tb_dict["name"]=name
                tb_dict["Data_File_Size"]=row[2]
                tb_dict["Data_File_Blocks"]=row[3]
                if row[4]=="YES":
                    tb_dict["Autoextensible"]=1
                else:
                    tb_dict["Autoextensible"]=0
                tb_dict["Max_Data_File_Size"]=row[5]
                tb_dict["Max_Data_File_Blocks"]=row[6]
                tb_dict["Increment_By"]=row[7]
                tb_dict["Usable_Data_File_Size"]=row[8]
                tb_dict["Usable_Data_File_Blocks"]=row[9]
                tbs_list.append(tb_dict)
            queried_data["Tablespace_Datafile"]=tbs_list
        except Exception as e:
            queried_data["status"]=0
            queried_data['msg']=str(e)
        return queried_data

    def tablespace_complete(self):
        queried_data={}
        try:
            query_output_data=self.execute_tablespace_metrics()
            queried_data.update(query_output_data)
            if 'status' in queried_data and queried_data['status']==0:
                return queried_data
            
            query_output_data=self.execute_tablespace_datafile()
            queried_data.update(query_output_data)
            if 'status' in queried_data and queried_data['status']==0:
                return queried_data
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
                pdb_dict['PDB_ID']=row[1]
                pdb_dict['PDB_Size']=row[2]
                pdb_dict['Block_Size']=row[3]
                pdb_list.append(pdb_dict)
            queried_data['PDB']=pdb_list
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
                "asm_query": "SELECT name AS asm_name, ROUND(total_mb / 1024, 2) AS asm_total_gb, ROUND(free_mb / 1024, 2) AS asm_free_gb, ROUND((free_mb / total_mb) * 100, 2) AS asm_pct_free, USABLE_FILE_MB AS asm_limit, REQUIRED_MIRROR_FREE_MB AS asm_threshold FROM v$asm_diskgroup"
            },
            "Single Queries":{
                "Rman Failed Backup Count":"""SELECT COUNT(*) FROM v$rman_status WHERE operation='BACKUP' AND status='FAILED'""",
                "Dict Cache Hit Ratio":"""SELECT (1 - (SUM(getmisses)/SUM(gets))) * 100 FROM gv$rowcache""",
                "Long Running Queries":"""SELECT COUNT(*) FROM v$session WHERE status='ACTIVE' AND type<>'BACKGROUND' AND last_call_et > 60""",
                "Blocking Locks":"""SELECT COUNT(*) FROM gv$session WHERE blocking_session IS NOT NULL""",
                "SGA Hit Ratio":"""SELECT (1 - (phy.value - lob.value - dir.value)/ses.value) FROM GV$SYSSTAT ses, GV$SYSSTAT lob, GV$SYSSTAT dir, GV$SYSSTAT phy, GV$INSTANCE inst WHERE ses.name='session logical reads' AND dir.name='physical reads direct' AND lob.name='physical reads direct (lob)' AND phy.name='physical reads' AND ses.inst_id=inst.inst_id AND lob.inst_id=inst.inst_id AND dir.inst_id=inst.inst_id AND phy.inst_id=inst.inst_id""",
                "SGA Log Alloc Retries":"""SELECT (rbar.value/re.value) FROM GV$SYSSTAT rbar, GV$SYSSTAT re, GV$INSTANCE inst WHERE rbar.name LIKE 'redo buffer allocation retries' AND re.name LIKE 'redo entries' AND re.inst_id=inst.inst_id AND rbar.inst_id=inst.inst_id""",
                "SGA Shared Pool Dict Cache Ratio":"""SELECT (SUM(rcache.getmisses)/SUM(rcache.gets)) FROM GV$rowcache rcache, GV$INSTANCE inst WHERE inst.inst_id=rcache.inst_id GROUP BY inst.inst_id""",
                "SGA Shared Pool Lib Cache Hit Ratio":"""SELECT libcache.gethitratio FROM GV$librarycache libcache, GV$INSTANCE inst WHERE namespace='SQL AREA' AND inst.inst_id=libcache.inst_id""",
                "SGA Shared Pool Lib Cache Reload Ratio":"""SELECT (SUM(libcache.reloads)/SUM(libcache.pins)) FROM GV$librarycache libcache, GV$INSTANCE inst WHERE inst.inst_id=libcache.inst_id GROUP BY inst.inst_id""",
                "SGA Shared Pool Lib Cache Sharable Statement":"""SELECT SUM(sqlarea.sharable_mem) FROM GV$sqlarea sqlarea, GV$INSTANCE inst WHERE sqlarea.executions > 5 AND inst.inst_id=sqlarea.inst_id GROUP BY inst.inst_id""",
                "SGA Shared Pool Lib Cache Shareable User":"""SELECT SUM(250 * sqlarea.users_opening) FROM GV$sqlarea sqlarea, GV$INSTANCE inst WHERE inst.inst_id=sqlarea.inst_id GROUP BY inst.inst_id""",
                "Total Memory":"""SELECT SUM(value) FROM GV$sesstat, GV$statname, GV$INSTANCE inst WHERE name = 'session uga memory max' AND GV$sesstat.statistic#=GV$statname.statistic# AND GV$sesstat.inst_id=inst.inst_id AND GV$statname.inst_id=inst.inst_id GROUP BY inst.inst_id""",
                "Oracle Database Version":"SELECT version FROM PRODUCT_COMPONENT_VERSION WHERE product LIKE 'Oracle Database%'",
                "Response Time":"""SELECT ROUND(VALUE * 10, 2) FROM GV$SYSMETRIC WHERE METRIC_NAME = 'SQL Service Response Time' ORDER BY INST_ID""",
                "Number of Session Users":"""SELECT COUNT(DISTINCT username) FROM v$session WHERE username IS NOT NULL""",
                "Database Block Size":"""SELECT value FROM v$parameter WHERE name = 'db_block_size'""",
                "Invalid Index Count":"""SELECT COUNT(*) FROM dba_indexes WHERE status = 'INVALID'""",
                "CPU Usage":"SELECT value FROM v$sysstat WHERE name='CPU used by this session'",
                "Enqueue Deadlocks":"SELECT value FROM v$sysstat WHERE name='enqueue deadlocks'",
                "Exchange Deadlocks":"SELECT value FROM v$sysstat WHERE name='exchange deadlocks'",
                "Logical Reads":"SELECT value FROM v$sysstat WHERE name='session logical reads'",
                "Queries Per Second":"""SELECT (value / 60) FROM v$sysstat WHERE name = 'execute count'""",
                "Transactions Per Second":"""SELECT ((SELECT value FROM v$sysstat WHERE name = 'user commits') + (SELECT value FROM v$sysstat WHERE name = 'user rollbacks')) / 60 FROM dual""",
                "DB Time":"""SELECT SUM(value)/100 FROM v$sys_time_model WHERE stat_name = 'DB time'""",
                
                "Slow Query Latency 95 Percentile":"""SELECT ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY elapsed_time/executions)) FROM v$sql WHERE executions > 0""",
                "Full Table Scans Short":"""SELECT value FROM v$sysstat WHERE name = 'table scans (short tables)'""",
                "Full Table Scans Long":"""SELECT value FROM v$sysstat WHERE name = 'table scans (long tables)'""",
                "Full Table Scans Rowid":"""SELECT value FROM v$sysstat WHERE name = 'table scans (rowid ranges)'""",
                "Full Table Scans IM":"""SELECT value FROM v$sysstat WHERE name = 'table scans (IM)'""",
                "Failed Backups":"""SELECT COUNT(*) FROM v$rman_status WHERE operation='BACKUP' AND status='FAILED'""",
                "Alert Log Recent Errors":"""SELECT COUNT(*) FROM V$DIAG_ALERT_EXT WHERE ORIGINATING_TIMESTAMP > SYSDATE - 1""",
                
                "Rollback Segments":"""SELECT COUNT(*) FROM dba_rollback_segs""",
                "Rollback Segment Details":"""SELECT segment_name, tablespace_name, status, initial_extent, next_extent, max_extents FROM dba_rollback_segs"""
            },
            "Tablespace Queries":{
                "Tablespace Metrics Query":"""SELECT b.TABLESPACE_NAME as "dba_tablespace", d.* , b.CONTENTS, b.LOGGING, b.STATUS FROM dba_tablespace_usage_metrics d FULL JOIN dba_tablespaces b ON d.TABLESPACE_NAME = b.TABLESPACE_NAME""",
                "Tablespace Datafile Query":"""SELECT TABLESPACE_NAME, FILE_NAME, (BYTES/1024/1024), BLOCKS, AUTOEXTENSIBLE, (MAXBYTES/1024/1024), (MAXBLOCKS/1024/1024), INCREMENT_BY, (USER_BYTES/1024/1024), USER_BLOCKS FROM DBA_DATA_FILES"""
            },
            "FRA Query":"""SELECT name AS "FRA File Dest", space_limit / (1024 * 1024) AS "FRA Space Limit", space_used / (1024 * 1024) AS "FRA Space Used", space_reclaimable / (1024 * 1024) AS "FRA Space Reclaimable", number_of_files AS "FRA Number of Files" FROM V$RECOVERY_FILE_DEST""",
            "Waits Query":"""SELECT event, time_waited_micro, total_waits FROM v$system_event WHERE wait_class != 'Idle' AND ROWNUM <= 20""",
            "PDB Query":"""SELECT p.name, p.con_id, NVL(SUM(f.bytes),0)/1024/1024 AS pdb_size_mb, p.block_size FROM v$pdbs p LEFT JOIN cdb_data_files f ON f.con_id = p.con_id GROUP BY p.name, p.con_id, p.block_size""",
            "DB Query":"SELECT 1 FROM dual"
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
            self.close_connection()
            return self.maindata
        for query_name ,bulk_query in self.metric_queries['Bulk Queries'].items():
            query_output_data=self.execute_query_bulk(bulk_query, query_name=query_name)
            self.maindata.update(query_output_data)
            if 'status' in self.maindata and self.maindata['status']==0:
                self.close_connection()
                return self.maindata
        for query_name in self.metric_queries['Single Queries']:
            query_output_data=self.execute_query(query_name)
            self.maindata.update(query_output_data)
            if 'status' in self.maindata and self.maindata['status']==0:
                self.close_connection()
                return self.maindata
        query_output_data=self.tablespace_complete()
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
            self.close_connection()
            return self.maindata
        query_output_data=self.execute_waits_query("Waits Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
            self.close_connection()
            return self.maindata
        query_output_data=self.execute_pdb("PDB Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
            self.close_connection()
            return self.maindata
        query_output_data=self.execute_query_row_col(self.metric_queries["DB Query"])
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
            self.close_connection()
            return self.maindata
        query_output_data=self.execute_query_row_col(self.metric_queries["FRA Query"])
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status']==0:
            self.close_connection()
            return self.maindata
        self.maindata['tabs']={
            "Tablespace and PDB":{
                "order":1,
                "tablist":[
                    "Tablespace_List",
                    "Tablespace_Datafile",
                    "PDB"
                ]
            },
            "Buffer Cache and Memory":{
                "order":2,
                "tablist":[
                    "Buffer Cache Hit Ratio",
                    "Database Block Size",
                    "Shared Pool Free %",
                    "Total Freeable PGA Memory",
                    "Maximum PGA Allocated",
                    "Total PGA Allocated",
                    "Total PGA Inuse",
                    "SGA Fixed Size",
                    "SGA Variable Size",
                    "SGA Database Buffers",
                    "SGA Redo Buffers",
                    "SGA Hit Ratio",
                    "SGA Log Alloc Retries",
                    "SGA Shared Pool Dict Cache Ratio",
                    "SGA Shared Pool Lib Cache Hit Ratio",
                    "SGA Shared Pool Lib Cache Reload Ratio",
                    "SGA Shared Pool Lib Cache Sharable Statement",
                    "SGA Shared Pool Lib Cache Shareable User",
                    "CPU Usage",
                    "Logical Reads",
                    "DB Time"
                ]
            },
            "I/O Operations and ASM":{
                "order":3,
                "tablist":[
                    "Physical Reads Per Sec",
                    "Physical Writes Per Sec",
                    "Direct Path Read Time Waited",
                    "Direct Path Read Wait Count",
                    "Direct Path Write Time Waited",
                    "Direct Path Write Wait Count",
                    "Db File Parallel Read Time Waited",
                    "Db File Parallel Read Count",
                    "Db File Parallel Write Time Waited",
                    "Db File Parallel Write Count",
                    "Control File Parallel Write Time Waited",
                    "Control File Parallel Write Count",
                    "Control File Sequential Read Time Waited",
                    "Control File Sequential Read Wait Count",
                    "Log Buffer Space Time Waited",
                    "Log Buffer Space Wait Count",
                    "Log File Sync Time Waited",
                    "Log File Sync Wait Count",
                    "Write Complete Waits Time Waited",
                    "Write Complete Waits Wait Count",
                    "ASM"
                ]
            },
            "Parsing and Execution":{
                "order":4,
                "tablist":[
                    "Cursor Cache Hit Ratio",
                    "Hard Parse Count Per Sec",
                    "Hard Parse Count Per Txn",
                    "Parse Failure Count Per Sec",
                    "Parse Failure Count Per Txn",
                    "Soft Parse Ratio",
                    "Total Parse Count Per Sec",
                    "Total Parse Count Per Txn",
                    "Queries Per Second",
                    "Transactions Per Second",
                    "Slow Query Latency 95 Percentile",
                    "Full Table Scans Short",
                    "Full Table Scans Long",
                    "Full Table Scans Rowid",
                    "Full Table Scans IM"
                ]
            },
            "Locks and Contention":{
                "order":5,
                "tablist":[
                    "Blocking Locks",
                    "Library Cache Pin Time Waited",
                    "Library Cache Pin Wait Count",
                    "Library Cache Load Lock Time Waited",
                    "Library Cache Load Lock Wait Count",
                    "Latch Free Time Waited",
                    "Latch Free Wait Count",
                    "Enqueue Timeouts Per Sec",
                    "Enqueue Deadlocks",
                    "Exchange Deadlocks"
                ]
            }
        }
        self.maindata['units']=METRICS_UNITS
        self.maindata['s247config']={
            "childdiscovery":[
                "Tablespace_List",
                "Tablespace_Datafile",
                "PDB",
                "ASM"
            ]
        }
        self.close_connection()
        return self.maindata

if __name__=="__main__":
    hostname="localhost"
    port="1521"
    sid="ORCL"
    username="ORACLE_USER"
    password="ORACLE_USER"
    tls="False"
    wallet_location=None
    oracle_home="/opt/oracle/product/21c/dbhomeXE"
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
    print(json.dumps(result))
