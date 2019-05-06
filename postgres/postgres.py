#!/usr/bin/python


#import psycopg2
#=======
### This plugin is used for monitoring PostGres Database
### For monitoring the performance metrics of your PostgreSQL database using Site24x7 Server Monitoring Plugins.
### 
### Author: Tarun, Zoho Corp
### Language : Python
### Tested in Ubuntu

import psycopg2
import json
from collections import OrderedDict

db = None
userName = None             #Change the username here
passWord = None             #Change the authentication method
hostName = None             #Change this value if it is a remote host
port = None                 #Change the port number (5432 by default)

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

VERSION = None

dict_psqlQueries = OrderedDict({})

def inititializeQueries():
    global dict_psqlQueries
    major_version = int(VERSION % 1000000 / 10000)
    middle_version = int(VERSION % 10000 / 100)
    minor_version = int(VERSION % 100)
    #Add your queries here
    str_tableStat = "SELECT COUNT(*) AS table_count FROM pg_stat_all_tables;"
    if (major_version >= 9 and middle_version >= 2) or (major_version>10):
        str_usageActiveStat = "SELECT count(*) - ( SELECT count(*) FROM pg_stat_activity WHERE state = 'idle' ) FROM pg_stat_activity;"
        str_usageIdleStat = "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';"
    else:
        str_usageActiveStat = "SELECT count(*) - ( SELECT count(*) FROM pg_stat_activity WHERE current_query = '<IDLE>' ) FROM pg_stat_activity;"
        str_usageIdleStat = "SELECT count(*) FROM pg_stat_activity WHERE current_query = '<IDLE>';"
    str_lockStat = "SELECT COUNT(*) FROM pg_locks;"
    str_dbStats = "SELECT sum(xact_commit) as commits, sum(xact_rollback) as rollbacks, sum(conflicts) as conflicts, (SUM(blks_hit) / SUM(blks_read)) as cache_usage_ratio FROM pg_stat_database;"
    str_bgStats = "SELECT buffers_checkpoint, buffers_backend, maxwritten_clean, checkpoints_req, checkpoints_timed, buffers_alloc FROM pg_stat_bgwriter;"
    #Please add any new query designed above to this dictionary also with an appropriate key name
    dict_psqlQueries = {'table_count' : str_tableStat,
                        'users_active_count' : str_usageActiveStat,
                        'users_idle_count' : str_usageIdleStat,
                        'db_stats' : str_dbStats,
                        'bg_stats' : str_bgStats,
                        'locks_count' : str_lockStat
                        }

class pgsql():
    def __init__(self):
        self._conn = None
        self._uname = userName
        self._pwd = passWord
        self._db = db
        self._hostname = hostName
        self._port = port
        self._results = {}
    def main(self):
        global VERSION
        try: 
            self._results.setdefault('plugin_version' , str(PLUGIN_VERSION))
            self._results.setdefault('heartbeat_required' , str(HEARTBEAT))
            try:
                import psycopg2
            except Exception as e:
                self._results.setdefault('status',0)
                self._results.setdefault('msg', 'psycopg2 not installed')
            self._conn = psycopg2.connect( dbname = self._db, user = self._uname , password = self._pwd, host = self._hostname, port = self._port )
            VERSION = self._conn.server_version
            inititializeQueries()
            self._results.setdefault('VERSION',str(VERSION))
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
            elif eachKey == 'bg_stats':
                for eachTuple in dictResults[eachKey]:
                    self._results.setdefault('buffers_checkpoint',int(eachTuple[0]))
                    self._results.setdefault('buffers_backend',int(eachTuple[1]))
                    self._results.setdefault('maxwritten_clean',int(eachTuple[2]))
                    self._results.setdefault('checkpoints_req',int(eachTuple[3]))
                    self._results.setdefault('checkpoints_timed',int(eachTuple[4]))
                    self._results.setdefault('buffers_alloc',int(eachTuple[5]))
            else:
                for eachTuple in dictResults[eachKey]:
                    self._results.setdefault(eachKey,int(eachTuple[0]))
        #self._results.setdefault('Error occured','0')
    
if __name__ == '__main__':
    psql = pgsql()
    psql.main()
