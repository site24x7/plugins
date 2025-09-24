#!/usr/bin/python3.8
import json
import os
import warnings
warnings.filterwarnings("ignore")

PLUGIN_VERSION = 1
HEARTBEAT = True

# Canonical metric names used in tabs and payload (keep these exact)
METRICS_UNITS = {
    "Buffer Cache Hit Ratio": "%",
    "Cursor Cache Hit Ratio": "%",
    "Library Cache Hit Ratio": "%",
    "Soft Parse Ratio": "%",
    "Memory Sorts Ratio": "%",
    "Session Limit %": "%",
    "Shared Pool Free %": "%",
    "SQL Service Response Time": "sec",
    "Database Wait Time Ratio": "%",
    "Total PGA Allocated": "bytes",
    "Total Freeable PGA Memory": "bytes",
    "Maximum PGA Allocated": "bytes",
    "Total PGA Inuse": "bytes",
    "SGA Fixed Size": "bytes",
    "SGA Variable Size": "bytes",
    "SGA Database Buffers": "bytes",
    "SGA Redo Buffers": "bytes",
    "SGA Shared Pool Lib Cache Sharable Statement": "bytes",
    "SGA Shared Pool Lib Cache Shareable User": "bytes",
    "Total Memory": "bytes",
    "FRA Space Limit": "mb",
    "FRA Space Used": "mb",
    "FRA Space Reclaimable": "mb",
    "Response Time": "ms",
    "Tablespace_List": {
        "Tablespace_Size": "mb",
        "Used_Percent": "%",
        "Used_Space": "mb"
    },
    "Tablespace_Datafile": {
        "Data_File_Size": "mb",
        "Max_Data_File_Size": "mb",
        "Usable_Data_File_Size": "mb"
    },
    "PDB": {
        "PDB_Size": "mb"
    },
    "ASM": {
        "total_gb": "GB",
        "free_gb": "GB",
        "pct_free": "%"
    },

    # Parsing / execution
    "CPU Usage": "seconds",
    "Transactions Per Second": "txn/sec",
    "Queries Per Second": "query/sec",
    "DB Time": "seconds",
    "Rollback Segment Initial Extent": "bytes",
    "Rollback Segment Next Extent": "bytes",
    "Slow Query Latency 95 Percentile": "ms",

    # Waits (canonical names). Use seconds for time keys and count for wait counts.
    "Disk File Operations I/O Time Waited (seconds)": "seconds",
    "Control File Parallel Write Time Waited (seconds)": "seconds",
    "Control File Sequential Read Time Waited (seconds)": "seconds",
    "Db File Parallel Read Time Waited (seconds)": "seconds",
    "Db File Parallel Write Time Waited (seconds)": "seconds",
    "Db File Scattered Read Time Waited (seconds)": "seconds",
    "Db File Sequential Read Time Waited (seconds)": "seconds",
    "Direct Path Read Time Waited (seconds)": "seconds",
    "Direct Path Write Time Waited (seconds)": "seconds",
    "Direct Path Sync Time Waited (seconds)": "seconds",
    "Log File Sync Time Waited (seconds)": "seconds",
    "Log Buffer Space Time Waited (seconds)": "seconds",
    "Write Complete Waits Time Waited (seconds)": "seconds",
    "Library Cache Load Lock Time Waited (seconds)": "seconds",
    "Library Cache Pin Time Waited (seconds)": "seconds",
    "Latch Free Time Waited (seconds)": "seconds"
}

# mapping from lower-cased event name to canonical base label (used to build keys)
_EVENT_TO_CANONICAL = {
    "direct path read": "Direct Path Read",
    "direct path write": "Direct Path Write",
    "db file parallel read": "Db File Parallel Read",
    "db file parallel write": "Db File Parallel Write",
    "control file parallel write": "Control File Parallel Write",
    "control file sequential read": "Control File Sequential Read",
    "log file sync": "Log File Sync",
    "disk file operations i/o": "Disk File Operations I/O",
    "db file sequential read": "Db File Sequential Read",
    "db file scattered read": "Db File Scattered Read",
    "direct path sync": "Direct Path Sync",
    "write complete waits": "Write Complete Waits",
    "library cache pin": "Library Cache Pin",
    "library cache load lock": "Library Cache Load Lock",
    "latch free": "Latch Free",
    "log buffer space": "Log Buffer Space"
}


class oracle:
    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.maindata['units'] = METRICS_UNITS.copy()
        self.username = args.username
        self.password = args.password
        self.sid = args.sid
        self.hostname = args.hostname
        self.port = args.port
        self.tls = args.tls.lower()
        self.wallet_location = args.wallet_location
        self.conn = None
        self.c = None

    def connect(self, dsn):
        try:
            import oracledb
            try:
                oracledb.init_oracle_client()
            except Exception:
                # init may fail in thin mode, ignore if so
                pass
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
        queried_data = {}
        try:
            self.c.execute(query)
            col_names = [row[0] for row in self.c.description] if self.c.description else []
            tot_cols = len(col_names)
            if col_change:
                for row in self.c:
                    for i in range(tot_cols):
                        queried_data[str(col_names[i]).title()] = row[i]
                    break
            else:
                for row in self.c:
                    for i in range(tot_cols):
                        queried_data[col_names[i]] = row[i]
                    break
        except Exception as e:
            queried_data["status"] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def execute_table_query(self, query, col_aliases=None):
        """
        Execute a query that returns multiple rows/columns and return a list of dicts.
        If col_aliases is provided (list), use those as dict keys; otherwise use cursor.description names.
        """
        try:
            self.c.execute(query)
            desc = [d[0] for d in self.c.description] if self.c.description else []
            results = []
            for row in self.c:
                rowd = {}
                for i, val in enumerate(row):
                    key = None
                    if col_aliases and i < len(col_aliases):
                        key = col_aliases[i]
                    elif i < len(desc):
                        key = desc[i]
                    else:
                        key = f"col_{i}"
                    rowd[key] = val
                results.append(rowd)
            return results
        except Exception as e:
            return {"status": 0, "msg": str(e)}

    def execute_query_bulk(self, query, query_name):
        queried_data = {}
        try:
            self.c.execute(query)
            if query_name == "pga_query":
                for row in self.c:
                    value, metric = row
                    metric = str(metric).title().replace("Pga", "PGA")
                    if metric == "Maximum PGA Allocated":
                        value = str(value / 1024 / 1024) + " MB"
                    queried_data[metric] = value
            elif query_name == "asm_query":
                asm_list = []
                for row in self.c:
                    asm_name, asm_total_gb, asm_free_gb, asm_pct_free, asm_limit, asm_threshold = row
                    asm_list.append({
                        "name": asm_name,
                        "ASM_TOTAL_GB": asm_total_gb,
                        "ASM_FREE_GB": asm_free_gb,
                        "ASM_PCT_FREE": asm_pct_free,
                        "ASM_LIMIT": asm_limit,
                        "ASM_THRESHOLD": asm_threshold
                    })
                queried_data['ASM'] = asm_list
            else:
                # generic bulk: expect VALUE, METRIC_NAME pairs
                for row in self.c:
                    try:
                        value, metric = row
                        queried_data[metric] = value
                    except Exception:
                        # fallback if ordering different
                        if len(row) >= 2:
                            queried_data[row[1]] = row[0]
                        elif len(row) == 1:
                            queried_data[query_name] = row[0]
        except Exception as e:
            queried_data["status"] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def _canonical_for_event(self, event_name):
        if not event_name:
            return None
        lk = event_name.strip().lower()
        return _EVENT_TO_CANONICAL.get(lk, None)

    def execute_waits_query(self, metric_query_name):
        """
        Runs waits query (left-joined event names to system_event),
        converts time (microseconds) -> seconds and writes canonical keys.
        """
        queried_data = {}
        wait_units = {}
        try:
            self.c.execute(self.metric_queries[metric_query_name])
            for row in self.c:
                ename, time_waited_micro, total_waits = row
                if ename is None:
                    continue
                canonical = self._canonical_for_event(str(ename))
                # if not in our explicit map, try to derive a readable canonical name
                if not canonical:
                    canonical = " ".join([w.capitalize() for w in str(ename).replace("/", " ").split()])
                # normalize micro -> seconds (safe guard None)
                time_waited_micro = 0 if time_waited_micro is None else time_waited_micro
                total_waits = 0 if total_waits is None else total_waits
                time_seconds = float(time_waited_micro) / 1_000_000.0
                time_key = f"{canonical} Time Waited (seconds)"
                count_key = f"{canonical} Wait Count"
                queried_data[time_key] = time_seconds
                queried_data[count_key] = total_waits
                wait_units[time_key] = 'seconds'
                wait_units[count_key] = 'count'
        except Exception as e:
            queried_data['status'] = 0
            queried_data['msg'] = str(e)
        # update units so payload has units for these dynamic keys
        self.maindata['units'].update(wait_units)
        return queried_data

    def execute_tablespace_metrics(self):
        # Use aliased query to avoid ambiguous column names
        db_block_size = 8192
        try:
            self.c.execute("select value from v$parameter where name = 'db_block_size'")
            for row in self.c:
                db_block_size = row[0]
                break
        except Exception:
            db_block_size = 8192

        queried_data = {}
        try:
            # This query aliases b.STATUS etc to avoid ambiguous names
            q = self.metric_queries["Tablespace Queries"]["Tablespace Metrics Query"]
            self.c.execute(q)
            desc = [d[0].upper() for d in self.c.description]
            tbs_list = []
            for row in self.c:
                rowd = dict(zip(desc, row))
                # pick the tablespace name from known aliases
                name = rowd.get('DBA_TABLESPACE') or rowd.get('TABLESPACE_NAME') or rowd.get('TABLESPACE')
                tbs_dict = {"name": name}
                # used_space and tablespace_size fields (these names come from dba_tablespace_usage_metrics)
                used_space_blocks = rowd.get('USED_SPACE') or rowd.get('BYTES') or rowd.get('USER_BYTES') or rowd.get('USER_BLOCKS')
                tablespace_size_blocks = rowd.get('TABLESPACE_SIZE') or rowd.get('TABLESPACE_SIZE_BYTES') or rowd.get('BLOCKS')
                used_percent = rowd.get('USED_PERCENT') or rowd.get('USED_PCT') or rowd.get('USED_PCT_PERCENT')
                if used_space_blocks is None:
                    try:
                        used_space_blocks = row[2]
                    except Exception:
                        used_space_blocks = 0
                if tablespace_size_blocks is None:
                    try:
                        tablespace_size_blocks = row[3]
                    except Exception:
                        tablespace_size_blocks = 0
                if used_percent is None:
                    try:
                        used_percent = row[4]
                    except Exception:
                        used_percent = 0
                try:
                    tbs_dict['Used_Space'] = int(used_space_blocks) * int(db_block_size) / 1024 / 1024 if used_space_blocks else 0
                except Exception:
                    tbs_dict['Used_Space'] = 0
                try:
                    tbs_dict['Tablespace_Size'] = int(tablespace_size_blocks) * int(db_block_size) / 1024 / 1024 if tablespace_size_blocks else 0
                except Exception:
                    tbs_dict['Tablespace_Size'] = 0
                tbs_dict['Used_Percent'] = used_percent or 0
                # determine status from aliased B_STATUS or STATUS
                status_val = rowd.get('B_STATUS') or rowd.get('STATUS') or rowd.get('b_STATUS')
                # map to Site24x7: 1=online, 0=offline
                if isinstance(status_val, str):
                    tbs_dict['TB_Status'] = 0 if status_val.upper() == 'OFFLINE' else 1
                    tbs_dict['status'] = 0 if status_val.upper() == 'OFFLINE' else 1
                else:
                    try:
                        tbs_dict['TB_Status'] = 1 if int(status_val or 0) != 0 else 1
                        tbs_dict['status'] = 1 if int(status_val or 0) != 0 else 1
                    except Exception:
                        tbs_dict['TB_Status'] = 1
                        tbs_dict['status'] = 1
                tbs_list.append(tbs_dict)
            queried_data['Tablespace_List'] = tbs_list
        except Exception as e:
            queried_data["status"] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def execute_tablespace_datafile(self):
        queried_data = {}
        try:
            self.c.execute(self.metric_queries["Tablespace Queries"]["Tablespace Datafile Query"])
            tbs_list = []
            for row in self.c:
                tb_dict = {}
                tbs_name = row[0]
                tbs_datafile = row[1].split("/")[-1]
                name = tbs_datafile
                tb_dict["name"] = name
                tb_dict["Data_File_Size"] = row[2]
                tb_dict["Data_File_Blocks"] = row[3]
                tb_dict["Autoextensible"] = 1 if row[4] == "YES" else 0
                tb_dict["Max_Data_File_Size"] = row[5]
                tb_dict["Max_Data_File_Blocks"] = row[6]
                tb_dict["Increment_By"] = row[7]
                tb_dict["Usable_Data_File_Size"] = row[8]
                tb_dict["Usable_Data_File_Blocks"] = row[9]
                tbs_list.append(tb_dict)
            queried_data["Tablespace_Datafile"] = tbs_list
        except Exception as e:
            queried_data["status"] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def tablespace_complete(self):
        queried_data = {}
        try:
            query_output_data = self.execute_tablespace_metrics()
            queried_data.update(query_output_data)
            if 'status' in queried_data and queried_data['status'] == 0:
                return queried_data
            query_output_data = self.execute_tablespace_datafile()
            queried_data.update(query_output_data)
            if 'status' in queried_data and queried_data['status'] == 0:
                return queried_data
        except Exception as e:
            queried_data["status"] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def execute_pdb(self, metric_query_name):
        queried_data = {}
        try:
            self.c.execute(self.metric_queries[metric_query_name])
            pdb_list = []
            for row in self.c:
                pdb_dict = {}
                pdb_dict['name'] = row[0]
                pdb_dict['PDB_ID'] = row[1]
                pdb_dict['PDB_Size'] = row[2]
                pdb_dict['Block_Size'] = row[3]
                pdb_list.append(pdb_dict)
            queried_data['PDB'] = pdb_list
        except Exception as e:
            queried_data['status'] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def metriccollector(self):
        self.metric_queries = {
            "Bulk Queries": {
                "system_query": "SELECT VALUE, METRIC_NAME FROM GV$SYSMETRIC WHERE METRIC_NAME IN ( 'Soft Parse Ratio', 'Total Parse Count Per Sec', 'Total Parse Count Per Txn', 'Hard Parse Count Per Sec', 'Hard Parse Count Per Txn', 'Parse Failure Count Per Sec', 'Parse Failure Count Per Txn', 'Temp Space Used', 'Session Count', 'Session Limit %', 'Database Wait Time Ratio', 'Memory Sorts Ratio', 'Disk Sort Per Sec', 'Rows Per Sort', 'Total Sorts Per User Call', 'User Rollbacks Per Sec', 'SQL Service Response Time', 'Long Table Scans Per Sec', 'Average Active Sessions', 'Logons Per Sec', 'Global Cache Blocks Los', 'Global Cache Blocks Corrupted', 'GC CR Block Received Per Second', 'Enqueue Timeouts Per Sec', 'Physical Writes Per Sec', 'Physical Reads Per Sec', 'Shared Pool Free %', 'Library Cache Hit Ratio', 'Cursor Cache Hit Ratio', 'Buffer Cache Hit Ratio' )",
                "pga_query": "SELECT VALUE, NAME FROM gv$pgastat where NAME IN ('total PGA allocated', 'total freeable PGA memory', 'maximum PGA allocated','total PGA inuse')",
                "sga_query": """SELECT sga.value, CONCAT('SGA ',sga.name) AS name FROM GV$SGA sga INNER JOIN GV$INSTANCE inst ON sga.inst_id = inst.inst_id""",
                "asm_query": "SELECT name AS asm_name, ROUND(total_mb / 1024, 2) AS asm_total_gb, ROUND(free_mb / 1024, 2) AS asm_free_gb, ROUND((free_mb / total_mb) * 100, 2) AS asm_pct_free, USABLE_FILE_MB AS asm_limit, REQUIRED_MIRROR_FREE_MB AS asm_threshold FROM v$asm_diskgroup"
            },
            "Single Queries": {
                "Rman Failed Backup Count": "SELECT COUNT(*) FROM v$rman_status WHERE operation='BACKUP' AND status='FAILED'",
                "Dict Cache Hit Ratio": "SELECT (1 - (SUM(getmisses)/SUM(gets))) * 100 FROM gv$rowcache",
                "Long Running Queries": "SELECT COUNT(*) FROM v$session WHERE status='ACTIVE' AND type<>'BACKGROUND' AND last_call_et > 60",
                "Blocking Locks": "SELECT COUNT(*) FROM gv$session WHERE blocking_session IS NOT NULL",
                "SGA Hit Ratio": "SELECT (1 - (phy.value - lob.value - dir.value)/ses.value) FROM GV$SYSSTAT ses, GV$SYSSTAT lob, GV$SYSSTAT dir, GV$SYSSTAT phy, GV$INSTANCE inst WHERE ses.name='session logical reads' AND dir.name='physical reads direct' AND lob.name='physical reads direct (lob)' AND phy.name='physical reads' AND ses.inst_id=inst.inst_id AND lob.inst_id=inst.inst_id AND dir.inst_id=inst.inst_id AND phy.inst_id=inst.inst_id",
                "SGA Log Alloc Retries": "SELECT (rbar.value/re.value) FROM GV$SYSSTAT rbar, GV$SYSSTAT re, GV$INSTANCE inst WHERE rbar.name LIKE 'redo buffer allocation retries' AND re.name LIKE 'redo entries' AND re.inst_id=inst.inst_id AND rbar.inst_id=inst.inst_id",
                "SGA Shared Pool Dict Cache Ratio": "SELECT (SUM(rcache.getmisses)/SUM(rcache.gets)) FROM GV$rowcache rcache, GV$INSTANCE inst WHERE inst.inst_id=rcache.inst_id GROUP BY inst.inst_id",
                "SGA Shared Pool Lib Cache Hit Ratio": "SELECT libcache.gethitratio FROM GV$librarycache libcache, GV$INSTANCE inst WHERE namespace='SQL AREA' AND inst.inst_id=libcache.inst_id",
                "SGA Shared Pool Lib Cache Reload Ratio": "SELECT (SUM(libcache.reloads)/SUM(libcache.pins)) FROM GV$librarycache libcache, GV$INSTANCE inst WHERE inst.inst_id=libcache.inst_id GROUP BY inst.inst_id",
                "SGA Shared Pool Lib Cache Sharable Statement": "SELECT SUM(sqlarea.sharable_mem) FROM GV$sqlarea sqlarea, GV$INSTANCE inst WHERE sqlarea.executions > 5 AND inst.inst_id=sqlarea.inst_id GROUP BY inst.inst_id",
                "SGA Shared Pool Lib Cache Shareable User": "SELECT SUM(250 * sqlarea.users_opening) FROM GV$sqlarea sqlarea, GV$INSTANCE inst WHERE inst.inst_id=sqlarea.inst_id GROUP BY inst.inst_id",
                "Total Memory": "SELECT SUM(value) FROM GV$sesstat, GV$statname, GV$INSTANCE inst WHERE name = 'session uga memory max' AND GV$sesstat.statistic#=GV$statname.statistic# AND GV$sesstat.inst_id=inst.inst_id AND GV$statname.inst_id=inst.inst_id GROUP BY inst.inst_id",
                "Oracle Database Version": "SELECT version FROM PRODUCT_COMPONENT_VERSION WHERE product LIKE 'Oracle Database%'",
                #"DB ID": "SELECT dbid FROM v$database",
                "Response Time": "SELECT ROUND(VALUE * 10, 2) FROM GV$SYSMETRIC WHERE METRIC_NAME = 'SQL Service Response Time' ORDER BY INST_ID",
                "Number of Session Users": "SELECT COUNT(DISTINCT username) FROM v$session WHERE username IS NOT NULL",
                "Database Block Size": "SELECT value FROM v$parameter WHERE name = 'db_block_size'",
                "Invalid Index Count": "SELECT COUNT(*) FROM dba_indexes WHERE status = 'INVALID'",
                "CPU Usage": "SELECT value FROM v$sysstat WHERE name='CPU used by this session'",
                "Enqueue Deadlocks": "SELECT value FROM v$sysstat WHERE name='enqueue deadlocks'",
                "Exchange Deadlocks": "SELECT value FROM v$sysstat WHERE name='exchange deadlocks'",
                "Logical Reads": "SELECT value FROM v$sysstat WHERE name='session logical reads'",
                "Queries Per Second": "SELECT (value / 60) FROM v$sysstat WHERE name = 'execute count'",
                "Transactions Per Second": "SELECT ((SELECT value FROM v$sysstat WHERE name = 'user commits') + (SELECT value FROM v$sysstat WHERE name = 'user rollbacks')) / 60 FROM dual",
                "DB Time": "SELECT SUM(value)/100 FROM v$sys_time_model WHERE stat_name = 'DB time'",
                "Slow Query Latency 95 Percentile": "SELECT ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY elapsed_time/executions)) FROM v$sql WHERE executions > 0",
                "Full Table Scans Short": "SELECT value FROM v$sysstat WHERE name = 'table scans (short tables)'",
                "Full Table Scans Long": "SELECT value FROM v$sysstat WHERE name = 'table scans (long tables)'",
                "Full Table Scans Rowid": "SELECT value FROM v$sysstat WHERE name = 'table scans (rowid ranges)'",
                "Full Table Scans IM": "SELECT value FROM v$sysstat WHERE name = 'table scans (IM)'",
                "Failed Backups": "SELECT COUNT(*) FROM v$rman_status WHERE operation='BACKUP' AND status='FAILED'",
                "Alert Log Recent Errors": "SELECT COUNT(*) FROM V$DIAG_ALERT_EXT WHERE ORIGINATING_TIMESTAMP > SYSDATE - 1",
                "Rollback Segments": "SELECT COUNT(*) FROM dba_rollback_segs",
                # detailed rollback segment table (alias segment_name as name)
                "Rollback_Segment_Details": "SELECT segment_name AS name, tablespace_name, status, initial_extent, next_extent, max_extents FROM dba_rollback_segs"
            },
            "Tablespace Queries": {
                # alias b.STATUS etc to avoid ambiguous column names that caused ORA-00918
                "Tablespace Metrics Query": """SELECT b.TABLESPACE_NAME AS DBA_TABLESPACE, d.* , b.CONTENTS AS B_CONTENTS, b.LOGGING AS B_LOGGING, b.STATUS AS B_STATUS
FROM dba_tablespace_usage_metrics d
FULL JOIN dba_tablespaces b ON d.TABLESPACE_NAME = b.TABLESPACE_NAME""",
                "Tablespace Datafile Query": "SELECT TABLESPACE_NAME, FILE_NAME, (BYTES/1024/1024), BLOCKS, AUTOEXTENSIBLE, (MAXBYTES/1024/1024), (MAXBLOCKS/1024/1024), INCREMENT_BY, (USER_BYTES/1024/1024), USER_BLOCKS FROM DBA_DATA_FILES"
            },
            # FRA
            "FRA Query": "SELECT name AS \"FRA File Dest\", space_limit / (1024 * 1024) AS \"FRA Space Limit\", space_used / (1024 * 1024) AS \"FRA Space Used\", space_reclaimable / (1024 * 1024) AS \"FRA Space Reclaimable\", number_of_files AS \"FRA Number of Files\" FROM V$RECOVERY_FILE_DEST",
            # waits: select canonical events from v$event_name left joined with v$system_event
            "Waits Query": """
SELECT en.name AS event,
       NVL(se.time_waited_micro,0) AS time_waited_micro,
       NVL(se.total_waits,0)      AS total_waits
FROM v$event_name en
LEFT JOIN v$system_event se
  ON LOWER(se.event) = LOWER(en.name)
WHERE LOWER(en.name) IN (
  'direct path read',
  'direct path write',
  'db file parallel read',
  'db file parallel write',
  'control file parallel write',
  'control file sequential read',
  'log file sync',
  'disk file operations i/o',
  'db file sequential read',
  'db file scattered read',
  'direct path sync',
  'write complete waits',
  'library cache pin',
  'library cache load lock',
  'latch free',
  'log buffer space'
)
ORDER BY en.name
""",
            "PDB Query": "SELECT p.name, p.con_id, NVL(SUM(f.bytes),0)/1024/1024 AS pdb_size_mb, p.block_size FROM v$pdbs p LEFT JOIN cdb_data_files f ON f.con_id = p.con_id GROUP BY p.name, p.con_id, p.block_size"
        }

        # Build DSN
        if self.tls == "True":
            dsn = f"""(DESCRIPTION=
                    (ADDRESS=(PROTOCOL=tcps)(HOST={self.hostname})(PORT={self.port}))
                    (CONNECT_DATA=(SERVICE_NAME={self.sid}))
                    (SECURITY=(MY_WALLET_DIRECTORY={self.wallet_location}))
                    )"""
        else:
            dsn = f"{self.hostname}:{self.port}/{self.sid}"

        connection_status = self.connect(dsn)
        if not connection_status[0]:
            self.maindata['status'] = 0
            self.maindata['msg'] = connection_status[1]
            self.close_connection()
            return self.maindata

        # Bulk queries (system metrics, pga, sga, asm)
        for query_name, bulk_query in self.metric_queries['Bulk Queries'].items():
            query_output_data = self.execute_query_bulk(bulk_query, query_name=query_name)
            self.maindata.update(query_output_data)
            if 'status' in self.maindata and self.maindata['status'] == 0:
                self.close_connection()
                return self.maindata

        # Single scalar queries (skip rollback details here)
        for query_name in self.metric_queries['Single Queries']:
            if query_name == "Rollback_Segment_Details":
                continue
            query_output_data = self.execute_query(query_name)
            self.maindata.update(query_output_data)
            if 'status' in self.maindata and self.maindata['status'] == 0:
                self.close_connection()
                return self.maindata

        # Tablespace lists and datafiles
        query_output_data = self.tablespace_complete()
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status'] == 0:
            self.close_connection()
            return self.maindata

        # Waits (I/O + locks) - convert microsec -> seconds inside handler
        query_output_data = self.execute_waits_query("Waits Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status'] == 0:
            self.close_connection()
            return self.maindata

        # PDBs
        query_output_data = self.execute_pdb("PDB Query")
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status'] == 0:
            self.close_connection()
            return self.maindata

        # FRA
        query_output_data = self.execute_query_row_col(self.metric_queries["FRA Query"])
        self.maindata.update(query_output_data)
        if 'status' in self.maindata and self.maindata['status'] == 0:
            self.close_connection()
            return self.maindata

        # Rollback Segment Details (table) - we use execute_table_query and alias first column as 'name'
        rollback_rows = self.execute_table_query(self.metric_queries["Single Queries"]["Rollback_Segment_Details"],
                                                 col_aliases=['name', 'tablespace_name', 'status', 'initial_extent', 'next_extent', 'max_extents'])
        if isinstance(rollback_rows, dict) and rollback_rows.get('status') == 0:
            self.maindata.update(rollback_rows)
            self.close_connection()
            return self.maindata

        # Process rollback rows:
        # - remove 'status' column from each rollback row
        # - strip leading underscores from the name
        processed_rollback = []
        for r in rollback_rows:
            try:
                name_val = r.get('name') if isinstance(r, dict) else None
                if name_val is None:
                    name_val = r.get('segment_name') if isinstance(r, dict) else None
                # strip leading underscores
                if isinstance(name_val, str):
                    cleaned_name = name_val.lstrip('_')
                else:
                    cleaned_name = name_val
                rr = {
                    "name": cleaned_name,
                    "tablespace_name": r.get('tablespace_name'),
                    "initial_extent": r.get('initial_extent'),
                    "next_extent": r.get('next_extent'),
                    "max_extents": r.get('max_extents')
                }
                processed_rollback.append(rr)
            except Exception:
                # in case of unexpected shape, skip the row gracefully
                continue

        # Attach rollback details without 'status' field under the new key name
        self.maindata["Rollback_Segment_Details"] = processed_rollback

        # Tabs & organization: make sure tab metric names exactly match keys produced above
        self.maindata['tabs'] = {
            "Tablespace and PDB": {
                "order": 1,
                "tablist": [
                    "Tablespace_List",
                    "Tablespace_Datafile",
                    "PDB",
                    "Rollback_Segment_Details"
                ]
            },
            "Buffer Cache and Memory": {
                "order": 2,
                "tablist": [
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
            "I/O Operations and ASM": {
                "order": 3,
                "tablist": [
                    "Physical Reads Per Sec",
                    "Physical Writes Per Sec",
                    "Direct Path Read Time Waited (seconds)",
                    "Direct Path Read Wait Count",
                    "Direct Path Write Time Waited (seconds)",
                    "Direct Path Write Wait Count",
                    "Db File Parallel Read Time Waited (seconds)",
                    "Db File Parallel Read Wait Count",
                    "Db File Parallel Write Time Waited (seconds)",
                    "Db File Parallel Write Wait Count",
                    "Control File Parallel Write Time Waited (seconds)",
                    "Control File Parallel Write Count",
                    "Control File Sequential Read Time Waited (seconds)",
                    "Control File Sequential Read Wait Count",
                    "Log Buffer Space Time Waited (seconds)",
                    "Log Buffer Space Wait Count",
                    "Log File Sync Time Waited (seconds)",
                    "Log File Sync Wait Count",
                    "Write Complete Waits Time Waited (seconds)",
                    "Write Complete Waits Wait Count",
                    "Disk File Operations I/O Time Waited (seconds)",
                    "Disk File Operations I/O Wait Count",
                    "Db File Scattered Read Time Waited (seconds)",
                    "Db File Scattered Read Wait Count",
                    "Direct Path Sync Time Waited (seconds)",
                    "Direct Path Sync Wait Count",
                    "ASM"
                ]
            },
            "Parsing and Execution": {
                "order": 4,
                "tablist": [
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
            "Locks and Contention": {
                "order": 5,
                "tablist": [
                    "Blocking Locks",
                    "Library Cache Pin Time Waited (seconds)",
                    "Library Cache Pin Wait Count",
                    "Library Cache Load Lock Time Waited (seconds)",
                    "Library Cache Load Lock Wait Count",
                    "Latch Free Time Waited (seconds)",
                    "Latch Free Wait Count",
                    "Enqueue Timeouts Per Sec",
                    "Enqueue Deadlocks",
                    "Exchange Deadlocks"
                ]
            }
        }

        # finalize units (already updated dynamically)
        self.maindata['units'] = self.maindata.get('units', METRICS_UNITS.copy())

        # child discovery
        self.maindata['s247config'] = {
            "childdiscovery": [
                "Tablespace_List",
                "Tablespace_Datafile",
                "PDB",
                "ASM",
                "Rollback_Segment_Details"
            ]
        }

        self.close_connection()
        return self.maindata

    def execute_query(self, metric_query_name):
        queried_data = {}
        try:
            self.c.execute(self.metric_queries["Single Queries"][metric_query_name])
            for row in self.c:
                queried_data[metric_query_name] = row[0]
        except Exception as e:
            queried_data["status"] = 0
            queried_data['msg'] = str(e)
        return queried_data


if __name__ == "__main__":
    hostname = "localhost"
    port = "1521"
    sid = "ORCL"
    username = "ORACLE_USER"
    password = "ORACLE_USER"
    tls = "False"
    wallet_location = None
    oracle_home = "/opt/oracle/product/21c/dbhomeXE"

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='hostname for oracle', default=hostname)
    parser.add_argument('--port', help='port number for oracle', default=port)
    parser.add_argument('--sid', help='sid for oracle', default=sid)
    parser.add_argument('--username', help='username for oracle', default=username)
    parser.add_argument('--password', help='password for oracle', default=password)
    parser.add_argument('--tls', help='tls support for oracle', default=tls)
    parser.add_argument('--wallet_location', help='oracle wallet location', default=wallet_location)
    parser.add_argument('--oracle_home', help='oracle home path', default=oracle_home)
    args = parser.parse_args()

    os.environ['ORACLE_HOME'] = args.oracle_home
    obj = oracle(args)
    result = obj.metriccollector()
    print(json.dumps(result))
