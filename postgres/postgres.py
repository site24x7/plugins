#!/usr/bin/python


### This plugin is used for monitoring PostGres Database
### For monitoring the performance metrics of your PostgreSQL database using Site24x7 Server Monitoring Plugins.
### 
### Language : Python
### Tested in Ubuntu

import psycopg2
import json
import traceback 
from collections import OrderedDict

DB = 'postgres'                   #Change the DB name here
USERNAME = 'postgres'             #Change the username here
PASSWORD ='postgres'              #Change the authentication method
HOSTNAME = 'localhost'            #Change this value if it is a remote host
PORT = 5432                       #Change the port number (5432 by default)

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT=True

VERSION = None
tabs=  {
  "tabs": {
    "Transactions and Sessions": {
      "order": "3",
      "tablist": [
        "Tranasctions_and_Session_per_Database",
        "Total Commits",
        "Total Rollbacks",
        "Total Conflicts",
        "Total Sessions",
        "Total Sessions Abandoned",
        "Total Sessions Fatal",
        "Total Sessions Killed",
        "Transactions Idle In Transaction",
        "Transactions Open"
      ]
    },
    "BG Writer": {
      "order": "2",
      "tablist": [
        "Checkpoints Timed",
        "Checkpoints Req",
        "Checkpoint Write Time",
        "Checkpoint Sync Time",
        "Buffers Checkpoint",
        "Buffers Clean",
        "Maxwritten Clean",
        "Buffers Backend",
        "Buffers Backend Fsync",
        "Buffers Alloc"
      ]
    },
    "DB and IO stats": { 
      "order": "1",
      "tablist": [
        "Stats_per_DB",
        "Total Rows Deleted",
        "Total Rows Fetched",
        "Total Rows Inserted",
        "Total Rows Returned",
        "Total Rows Updated",
        "Total Block Hits",
        "Total Block Reads"
      ]
    }
  }
}

units={
  "Active Connections": "connections",
  "Max Connections": "connections",
  "Uptime": "s",
  "Total Rows Deleted": "rows",
  "Total Rows Fetched": "rows",
  "Total Rows Inserted": "rows",
  "Total Rows Returned": "rows",
  "Total Rows Updated": "rows",
  "Total Commits" : "transactions",
  "Total Rollbacks" : "transactions",
  "Total Sessions" : "sessions",
  "Total Sessions Abandoned" : "sessions",
  "Total Sessions Fatal" : "sessions",
  "Total Sessions Killed" : "sessions",
  "Transactions Idle In Transaction" : "transactions",
  "Transactions Open" : "transactions",
  "Locks Count" : "locks",
  "Database Count" : "databases"
}



dict_psqlQueries = OrderedDict({})


def inititializeQueries():
    global dict_psqlQueries
    major_version = int(VERSION % 1000000 / 10000)
    middle_version = int(VERSION % 10000 / 100)
    minor_version = int(VERSION % 100)
    #Add your queries here
    waiting=True
    str_tableStat = "SELECT COUNT(*) AS table_count FROM pg_stat_all_tables;"
    str_TransactionsOpen= "SELECT count(*) as transactions_open FROM pg_stat_activity WHERE xact_start IS NOT NULL;"
    str_version="SHOW server_version;"
    if (major_version >= 9 and middle_version >= 2) or (major_version>=10):
        str_usageActiveStat = "SELECT count(*) - ( SELECT count(*) FROM pg_stat_activity WHERE state = 'idle' ) as active_queries FROM pg_stat_activity;"
        str_usageWaitingStat = "SELECT count(*) as active_waiting_queries FROM pg_stat_activity WHERE state = 'active' AND wait_event IS NOT NULL;"
        str_TransactionsIdle="SELECT COUNT(*) as transactions_idle_in_transaction FROM pg_stat_activity WHERE state = 'idle in transaction';"
    else:
        str_usageActiveStat = "SELECT count(*) - ( SELECT count(*) FROM pg_stat_activity WHERE current_query = '<IDLE>' ) as active_queries FROM pg_stat_activity;"
        str_TransactionsIdle="SELECT COUNT(*) as transactions_idle_in_transaction FROM pg_stat_activity WHERE state = '<IDLE> in transaction';"
        
        waiting=False

    str_lockStat = "SELECT COUNT(*) as locks_count FROM pg_locks;"
    str_MaxConn = "select setting::int max_connections from pg_settings where name=$$max_connections$$;"
    str_dbStats = "SELECT sum(numbackends) as active_connections, sum(xact_commit) as total_commits, sum(xact_rollback) as total_rollbacks, sum(conflicts) as total_conflicts FROM pg_stat_database;"
    str_iostats = "SELECT sum(tup_inserted) as total_rows_inserted, sum(tup_updated) as total_rows_updated ,sum(tup_deleted) as total_rows_deleted, sum(tup_fetched) as total_rows_fetched ,sum(tup_returned) as total_rows_returned,sum(blks_read) as total_block_reads , sum(blks_hit) as total_block_hits FROM pg_stat_database;"
    str_bgStats = "SELECT checkpoints_timed,checkpoints_req,checkpoint_write_time,checkpoint_sync_time,buffers_checkpoint,buffers_clean,maxwritten_clean,buffers_backend,buffers_backend_fsync,buffers_alloc FROM pg_stat_bgwriter;"
    str_idxStats = "SELECT sum(idx_scan) as index_scans,sum(idx_tup_read) as index_rows_read, sum(idx_tup_fetch) as index_rows_fetched FROM pg_stat_user_indexes;"
    str_uptime ="SELECT FLOOR(EXTRACT(EPOCH FROM current_timestamp - pg_postmaster_start_time())) as uptime;"
    str_databaseCount = "SELECT COUNT(*) AS database_count FROM pg_database WHERE datname <> 'template0' AND datname <> 'template1';"
    str_Sessions = "SELECT SUM(sessions) as total_sessions, SUM(sessions_abandoned) as total_sessions_abandoned, SUM(sessions_fatal) as total_sessions_fatal, SUM(sessions_killed) as total_sessions_killed FROM pg_stat_database;"
    str_heap = "SELECT sum(heap_blks_read) as heap_blocks_read, sum(heap_blks_hit)  as heap_blocks_hit, CASE WHEN (sum(heap_blks_hit) + sum(heap_blks_read)) = 0 THEN 0 ELSE sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) END as cache_hit_ratio FROM pg_statio_user_tables;"
    
    #Please add any new query designed above to this dictionary also with an appropriate key name
    dict_psqlQueries = {'table_count' : str_tableStat,
                        'active_queries' : str_usageActiveStat,
                        'transactions_open':str_TransactionsOpen,
                        'transacttions_idle':str_TransactionsIdle,
                        'db_stats' : str_dbStats,
                        'bg_stats' : str_bgStats,
                        'locks_count' : str_lockStat,
                        'max_conn' : str_MaxConn,
                        'io_stats' : str_iostats,
                        'idx_stats' :str_idxStats,
                        'version' : str_version,
                        'uptime' : str_uptime,
                        'no of databases' : str_databaseCount,
                        'session' : str_Sessions,
                        'heap_and_cache' : str_heap
                        }
    if waiting:
        dict_psqlQueries['active_waiting_queries']= str_usageWaitingStat

    # table queries

    global conn_details,db_details
    conn_details="SELECT datname as name,xact_commit as commits, xact_rollback as rollbacks, conflicts, sessions, sessions_abandoned, sessions_fatal, sessions_killed, session_time, active_time as sessions_active_time, idle_in_transaction_time as session_idle_in_transaction_time FROM pg_stat_database;"
    db_details = "SELECT d.datname AS name, s.numbackends as active_connections, ROUND(pg_database_size(d.datname) / 1024 / 1024,2) AS size_in_mb,tup_inserted as rows_inserted, tup_updated as rows_updated, tup_deleted as rows_deleted, tup_fetched as rows_fetched , tup_returned as rows_returned, blks_read as block_reads , blks_hit as block_hits FROM pg_database d JOIN pg_stat_database s ON d.oid = s.datid;"

class pgsql():
    def __init__(self,host_name,port,username,password):
        self._conn = None
        self._uname = username
        self._pwd = password
        self._hostname = host_name
        self._port = port
        self._results = {}
        self._msg=""
    def main(self,plugin_version,heartbeat):
        global VERSION
        try: 
            self._results.setdefault('plugin_version' , str(plugin_version))
            self._results.setdefault('heartbeat_required' , str(heartbeat))
            import psycopg2
            self._conn = psycopg2.connect(  user = self._uname , password = self._pwd, host = self._hostname, port = self._port )
            VERSION = self._conn.server_version
            
            inititializeQueries()
            self.metricCollector()
        except ImportError as e:
            self._results.setdefault('status',0)
            self._results.setdefault('msg', "psycopg2 Module Not Installed\nDependency missing:'psycopg2' Python client library\nInstall with command,\n\n pip3 install psycopg2-binary\n")
            #traceback.print_exc() 
        except Exception as e:
            self._results.setdefault('status',0)
            self._results.setdefault('msg', str(e))
            #traceback.print_exc() 
        finally:
            if self._conn:
                self._conn.close()
            self._results.update(tabs)
            self._results["units"]=units
            if self._msg != "":
                self._results["msg"]=self._msg
            print(str(json.dumps(self._results, indent=4, sort_keys=True)))

    def metricCollector(self):
        dictResults = {}
        cur = self._conn.cursor()
        conn_result=[]
        db_result=[]
        for eachQuery in dict_psqlQueries.keys():
                try:
                    cur.execute(dict_psqlQueries[eachQuery])
                    column_names = [desc[0] for desc in cur.description]
                    dictResults.setdefault(str(eachQuery),[column_names,cur.fetchall()])
                    
                    
                except Exception as e:
                    self._msg=self._msg+","+str(e)
                    self._conn.rollback()

        try: 
            cur.execute(conn_details)
            conn_column_names = [desc[0] for desc in cur.description]
            conn_table_result=cur.fetchall()
            conn_table_result.pop(0)

        except Exception as e:
            self._msg=self._msg+","+str(e)
            self._conn.rollback()
        
        try: 
            cur.execute(db_details)
            db_column_names = [desc[0] for desc in cur.description]
            db_table_result=cur.fetchall()

        except Exception as e:
            self._msg=self._msg+","+str(e)
            self._conn.rollback()

        cur.close()   
        
        for eachKey in dictResults.keys():
            query_result=dictResults[eachKey]
            columns=query_result[0]
            rows=query_result[1]
            rows=rows[0]
            for i,j in enumerate(columns):
                self._results[j.replace("_", " ").title()]= str(rows[i])
        for row in conn_table_result:
            tab_result={}
            for i,j in enumerate(row):
                tab_result[conn_column_names[i]]=j
            conn_result.append(tab_result)
        
        for row in db_table_result:
            tab_result={}
            for i,j in enumerate(row):
                tab_result[db_column_names[i]]=str(j)
            db_result.append(tab_result)

        self._results["Tranasctions_and_Session_per_Database"]=conn_result
        self._results["Stats_per_DB"]=db_result

        

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=HOSTNAME)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=PORT)
    parser.add_argument('--username', help='user name', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password', nargs='?', default=PASSWORD)
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()
        
    host_name=args.host
    port=str(args.port)
    username=args.username
    password=args.password
    plugin_version=args.plugin_version
    heartbeat=args.heartbeat
        
    psql = pgsql(host_name,port,username,password)
    psql.main(plugin_version,heartbeat)
