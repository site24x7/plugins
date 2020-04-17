#!/usr/bin/python
"""

Site24x7 Oracle DB Plugin

"""

import json
# if any changes are done to the metrics or units, increment the plugin version number here
PLUGIN_VERSION = "1"
HEARTBEAT = "true"

# Config Section: Enter your configuration details to connect to the oracle database
ORACLE_HOST = "oracle_hostname_here"

ORACLE_PORT = "1521"

ORACLE_SID = "XE"

ORACLE_USERNAME = "sys"

ORACLE_PASSWORD = "password"

# Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS = {'processes_usage': '%','sessions_usage':'%','response_time':'ms','pga_cache_hit_percentage':'%'}
#oracle_status = 1 denotes UP and 0 denotes down

#for invalid_objects count - to get count of particular owner, update the below field with owner name
#leave this field empty to get overall invalid_objects count
INVALID_OBJECTS_OWNER=""

##Metrics enable/disable
SESSIONS=True
PGA_CACHE_HIT=True
FAILED_JOBS=True
RMAN_FAILED_BACKUP=True
FAILED_LOGIN=True
INVALID_OBJECTS=True
SESSION_PROCESS_USAGE=True
SQL_RESPONSE_TIME=True
DISK_MEMORY_SORT_RATIO=True
BUFFER_CACHE_HIT_RATIO=True

class Oracle(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '1521'))
        self.sid = self.configurations.get('sid', 'XE')
        self.username = self.configurations.get('user', 'sys')
        self.password = self.configurations.get('password', 'admin')
        self.data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT, 'units':METRICS_UNITS}

    def metricCollector(self):
        c=None
        conn=None
        try:
            import cx_Oracle
        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = str(e)
            return self.data

        try:
            try:
                #dsnStr = cx_Oracle.makedsn(self.host, self.port, self.sid)
                conn = cx_Oracle.connect(self.username,self.password,self.host+':'+str(self.port)+'/'+self.sid)
                c = conn.cursor()
            except Exception as e:
                self.data['status']=0
                self.data['msg']='Exception while making connection: '+str(e)
                return self.data

            c.execute("SELECT  status  FROM v$instance")
            for row in c:
                status = row[0]
                self.data['oracle_status'] = 1 if status == 'OPEN' else 0
                break

            if SESSIONS:
                c.execute("select s.status name,count(s.status) session_count  from gv$session s, v$process p where  p.addr=s.paddr and s.status in ('INACTIVE','ACTIVE') group by s.status")
                for row in c:
                    name, value = row
                    if name == 'ACTIVE':
                        self.data['active_sessions'] = value
                    if name =='INACTIVE':
                        self.data['inactive_sessions'] = value

            if PGA_CACHE_HIT:
                c.execute("select value from v$pgastat where name='cache hit percentage'")
                for row in c:
                    self.data['pga_cache_hit_percentage'] = row[0]

            if FAILED_JOBS:
                c.execute("select count(*) failed_jobs from dba_scheduler_job_log where STATUS='FAILED' and log_date >= sysdate-(5/(24*60))")
                for row in c:
                    self.data['failed_jobs'] = row[0]

            if RMAN_FAILED_BACKUP:
                c.execute("SELECT COUNT(*) failed FROM v$rman_status WHERE operation = 'BACKUP' AND status = 'FAILED' AND END_TIME >= sysdate-(5/(24*60))")
                for row in c:
                    self.data['rman_failed_backup_count'] = row[0]

            if FAILED_LOGIN:
                #this will work only if audit trail is enabled
                c.execute("select count(*) failed_logins from dba_audit_trail where timestamp >= sysdate-(5/(24*60))")
                for row in c:
                    self.data['failed_login_count'] = row[0]

            if INVALID_OBJECTS:
                invalid_object_query="select count(*) invalid_objects from dba_objects where status = 'INVALID'"
                if INVALID_OBJECTS_OWNER and INVALID_OBJECTS_OWNER.strip():
                    invalid_object_query = invalid_object_query + " AND owner='"+INVALID_OBJECTS_OWNER+"'"
                c.execute(invalid_object_query)
                for row in c:
                    self.data['invalid_objects_count'] = row[0]

            if SESSION_PROCESS_USAGE:
                c.execute("SELECT resource_name name, 100*DECODE(initial_allocation, ' UNLIMITED', 0, current_utilization / initial_allocation) usage FROM v$resource_limit WHERE LTRIM(limit_value) != '0' AND LTRIM(initial_allocation) != '0' AND resource_name in('sessions','processes')")
                for row in c:
                    resource,usage = row
                    self.data[resource+'_usage']= round(usage,2)

            if SQL_RESPONSE_TIME:
                c.execute("SELECT to_char(begin_time, 'hh24:mi'),round(value * 10, 2) FROM v$sysmetric WHERE metric_name = 'SQL Service Response Time'")
                for row in c:
                    self.data['sql_response_time'] = float(row[1])
                    break

            # Disk to memory sort ratio
			# http://oln.oracle.com/DBA/OLN_OPTIMIZING_SORTS/sorts/html/lesson2/124_01a.htm
            if DISK_MEMORY_SORT_RATIO:
                c.execute("SELECT disk.value, mem.value,(disk.value / mem.value) * 100  FROM v$sysstat mem, v$sysstat disk WHERE mem.name = 'sorts (memory)' AND disk.name = 'sorts (disk)'")
                for row in c:
                    disk_sort, memory_sort, ratio = row
                    self.data['disk_memory_sort_ratio'] = ratio

            # Calculate buffer cache hit ratio
            # https://docs.oracle.com/database/121/TGDBA/tune_buffer_cache.htm#TGDBA533
            if BUFFER_CACHE_HIT_RATIO:
                c.execute(
                    "SELECT name, value FROM V$SYSSTAT "
                    "WHERE name IN ('db block gets from cache', 'consistent gets from cache', 'physical reads cache')")
                for row in c:
                    name, value = row
                    if name == 'db block gets from cache':
                        db_blocks = value
                    if name == 'consistent gets from cache':
                        consistent_gets = value
                    if name == 'physical reads cache':
                        physical_reads = value

                buffer_cache_hit_ratio = 1 - (physical_reads / float(consistent_gets + db_blocks))
                self.data['buffer_cache_hit_ratio'] = round(buffer_cache_hit_ratio,2)  # formatting to two decimals

        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = str(e)
        finally:
            if c!= None : c.close()
            if conn != None : conn.close()
            return self.data

if __name__ == "__main__":
    configurations = {'host': ORACLE_HOST, 'port': ORACLE_PORT,
                      'user': ORACLE_USERNAME, 'password': ORACLE_PASSWORD, 'sid': ORACLE_SID}

    oracle_plugin = Oracle(configurations)

    result = oracle_plugin.metricCollector()

print(json.dumps(result, indent=4, sort_keys=True))
