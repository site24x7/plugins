#!/usr/bin/python

### This plugin is used for monitoring PostGres Database
### For monitoring the performance metrics of your PostgreSQL database using Site24x7 Server Monitoring Plugins.
### 
### Language : Python
### Tested in Ubuntu

import psycopg2
import json
from collections import OrderedDict

DB = 'postgres'                   #Change the DB name here
USERNAME = 'postgres'             #Change the username here
PASSWORD = None                   #Change the authentication method
HOSTNAME = 'localhost'            #Change this value if it is a remote host
PORT = 5432                       #Change the port number (5432 by default)

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT=True

VERSION = None

dict_psqlQueries = OrderedDict({})

def inititializeQueries():
    global dict_psqlQueries
    major_version = int(VERSION % 1000000 / 10000)
    middle_version = int(VERSION % 10000 / 100)
    minor_version = int(VERSION % 100)
    #Add your queries here
    str_tableStat = "SELECT COUNT(*) AS table_count FROM pg_stat_all_tables;"
    if (major_version >= 9 and middle_version >= 2) or (major_version>=10):
        str_usageActiveStat = "SELECT count(*) - ( SELECT count(*) FROM pg_stat_activity WHERE state = 'idle' ) FROM pg_stat_activity;"
        str_usageIdleStat = "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';"
    else:
        str_usageActiveStat = "SELECT count(*) - ( SELECT count(*) FROM pg_stat_activity WHERE current_query = '<IDLE>' ) FROM pg_stat_activity;"
        str_usageIdleStat = "SELECT count(*) FROM pg_stat_activity WHERE current_query = '<IDLE>';"
    str_lockStat = "SELECT COUNT(*) FROM pg_locks;"
    str_dbStats = "SELECT sum(xact_commit) as commits, sum(xact_rollback) as rollbacks, sum(conflicts) as conflicts, (SUM(blks_hit) / SUM(blks_read)) as cache_usage_ratio FROM pg_stat_database;"
    str_iostats = "SELECT sum(tup_inserted) as tup_inserted, sum(tup_updated) as updated ,sum(tup_deleted) as tup_deleted, sum(tup_fetched) as tup_fetched ,sum(tup_returned) as tup_returned,sum(blks_read) as reads , sum(blks_hit) as hits FROM pg_stat_database;"
    str_bgStats = "SELECT buffers_checkpoint, buffers_backend, maxwritten_clean, checkpoints_req, checkpoints_timed, buffers_alloc FROM pg_stat_bgwriter;"
    
    #Please add any new query designed above to this dictionary also with an appropriate key name
    dict_psqlQueries = {'table_count' : str_tableStat,
                        'users_active_count' : str_usageActiveStat,
                        'users_idle_count' : str_usageIdleStat,
                        'db_stats' : str_dbStats,
                        'bg_stats' : str_bgStats,
                        'locks_count' : str_lockStat,
                        'io_stats' : str_iostats
                        }

class pgsql():
    def __init__(self,host_name,port,username,password,db):
        self._conn = None
        self._uname = username
        self._pwd = password
        self._db = db
        self._hostname = host_name
        self._port = port
        self._results = {}
    def main(self,plugin_version,heartbeat):
        global VERSION
        try: 
            self._results.setdefault('plugin_version' , str(plugin_version))
            self._results.setdefault('heartbeat_required' , str(heartbeat))
            try:
                import psycopg2
            except Exception as e:
                self._results.setdefault('status',0)
                self._results.setdefault('msg', 'psycopg2 not installed')
            self._conn = psycopg2.connect( dbname = self._db, user = self._uname , password = self._pwd, host = self._hostname, port = self._port )
            VERSION = self._conn.server_version
            inititializeQueries()
            self._results.setdefault('VERSION',str(VERSION))
            self._results.setdefault('db_name',str(self._db))
            self.metricCollector()
        except Exception as e:
            self._results.setdefault('status',0)
            self._results.setdefault('msg', str(e)[:50]+ ' ...')
        finally:
            if self._conn:
                self._conn.close()
            print(str(json.dumps(self._results)))
    def metricCollector(self):
        dictResults = {}
        cur = self._conn.cursor()
        for eachQuery in dict_psqlQueries.keys():
                try:
                    cur.execute(dict_psqlQueries[eachQuery])
                    dictResults.setdefault(str(eachQuery),cur.fetchall())
                except Exception as e:
                    pass
        cur.close()   
        for eachKey in dictResults.keys():
            if eachKey == 'db_stats':
                for eachTuple in dictResults[eachKey]:
                    self._results.setdefault('db_commits',int(eachTuple[0]))
                    self._results.setdefault('db_rollbacks',int(eachTuple[1]))
                    self._results.setdefault('db_conflicts',int(eachTuple[2]))
                    self._results.setdefault('db_cache_usage_ratio',int(eachTuple[3]))
                    self._results.setdefault('db_transactions',int(eachTuple[0]) + int(eachTuple[1]))
            elif eachKey == 'bg_stats':
                for eachTuple in dictResults[eachKey]:
                    self._results.setdefault('buffers_checkpoint',int(eachTuple[0]))
                    self._results.setdefault('buffers_backend',int(eachTuple[1]))
                    self._results.setdefault('maxwritten_clean',int(eachTuple[2]))
                    self._results.setdefault('checkpoints_req',int(eachTuple[3]))
                    self._results.setdefault('checkpoints_timed',int(eachTuple[4]))
                    self._results.setdefault('buffers_alloc',int(eachTuple[5]))
            elif eachKey == 'io_stats':
                for eachTuple in dictResults[eachKey]:
                    self._results.setdefault('tup_inserted',int(eachTuple[0]))
                    self._results.setdefault('tup_updated',int(eachTuple[1]))
                    self._results.setdefault('tup_deleted',int(eachTuple[2]))
                    self._results.setdefault('tup_fetched',int(eachTuple[3]))
                    self._results.setdefault('tup_returned',int(eachTuple[4]))
                    self._results.setdefault('blocks_read',int(eachTuple[5]))
                    self._results.setdefault('blocks_hits',int(eachTuple[6]))
            else:
                for eachTuple in dictResults[eachKey]:
                    self._results.setdefault(eachKey,int(eachTuple[0]))
        #self._results.setdefault('Error occured','0')
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=HOSTNAME)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=PORT)
    parser.add_argument('--username', help='user name', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password', nargs='?', default=PASSWORD)
    parser.add_argument('--db', help='database name', nargs='?', default=DB)
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()
        
    host_name=args.host
    port=str(args.port)
    username=args.username
    password=args.password
    db=args.db
    plugin_version=args.plugin_version
    heartbeat=args.heartbeat
        
    psql = pgsql(host_name,port,username,password,db)
    psql.main(plugin_version,heartbeat)
    