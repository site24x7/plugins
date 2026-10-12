#!/usr/bin/python3

import datetime
from datetime import datetime, timedelta
import time
import json
import urllib.parse
import os
import glob
import warnings
warnings.filterwarnings("ignore")

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

METRICS_UNITS = {
                 "Opcounters_Insert_per_sec": "operations",
                 "Opcounters_Query_per_sec": "queries",
                 "Opcounters_Update_per_sec": "operations",
                 "Opcounters_Delete_per_sec": "operations",
                 "Opcounters_Getmore_per_sec": "operations",
                 "Opcounters_Command_per_sec": "commands",
                 "OpLatencies_Reads_Latency": "ms",
                 "OpLatencies_Writes_Latency": "ms",
                 "OpLatencies_Commands_Latency": "ms",
                 "Scan_Order_Ratio": "ratio",
                 "Index_Scan_Ratio": "ratio",
                 "InMemory_Sorts": "operations",
                 "Cache_Dirty_Pct": "%",
                 "Cache_Pages_Read": "pages",
                 "Global_Lock_Queue_Readers": "operations",
                 "Global_Lock_Queue_Writers": "operations",
                  "Lock_Wait_Time_Micros": "microseconds",
                  "Connections_Current": "connections",
                  "Connections_Available": "connections",
                  "Network_Bytes_In": "bytes",
                  "Network_Bytes_Out": "bytes",
                  "Active_Reads": "operations",
                  "Active_Writes": "operations",
                  "Oplog_Window_Hours": "hours",
                 "Oplog_Size_MB": "MB",
                 "Oplog_Used_MB": "MB",
                 "Oplog_Used_Pct": "%",
                 }
                 
METRICS_TABS = {}


class MongoDB(object):
    def __init__(self, args):
        self.args=args
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password
        self.dbname=args.dbname
        self.authdb=args.authdb

        self.tls=args.tls
        
        if self.tls=="True":
        
            self.tls=True
            self.tlscertificatekeyfile=args.tlscertificatekeyfile
            self.tlscertificatekeyfilepassword=args.tlscertificatekeyfilepassword
            self.tlsallowinvalidcertificates=args.tlsallowinvalidcertificates
            self.tlsallowinvalidcertificates=args.tlsallowinvalidcertificates
            if self.tlsallowinvalidcertificates=="True":
                self.tlsallowinvalidcertificates=True
            else:
                self.tlsallowinvalidcertificates=False
                
            
            
     
        else:
            self.tls=False

        if(self.username!="None" and self.password!="None" and self.authdb!="None"):
            self.mongod_server = "{0}:{1}@{2}:{3}/{4}".format(self.username,urllib.parse.quote(self.password), self.host, self.port, self.authdb)
        elif(self.username!="None" and self.password!="None"):
            self.mongod_server = "{0}:{1}@{2}:{3}".format(self.username, self.password, self.host, self.port)
        elif(self.authdb!="None"):
            self.mongod_server = "{0}:{1}/{2}".format(self.host, self.port, self.authdb)
        else:
            self.mongod_server = "{0}:{1}".format(self.host, self.port)

    

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        plugin_script_path=os.path.dirname(os.path.realpath(__file__))
        data['applog'] = [
            {
                'logs_enabled': True,
                'log_type_name': 'MongoDB Slow Queries',
                'log_file_path': os.path.join(plugin_script_path, 'slow_query_*.txt')
            },
            {
                'logs_enabled': True,
                'log_type_name': 'MongoDB Long Running Queries',
                'log_file_path': os.path.join(plugin_script_path, 'long_running_query_*.txt')
            }
        ]
        long_query_duration = getattr(self.args, 'long_query_duration', 5)
        slow_query_profile_lookback_minutes = getattr(self.args, 'slow_query_profile_lookback_minutes', 5)

        def per_sec(doc,metric):
            diff = output[doc][metric] - cache_data[doc][metric]
            ps = int(diff / elapsed_time)
            return ps

        try:
            import zipimport
            importer=zipimport.zipimporter(plugin_script_path+"/pymongo.pyz")
            bson=importer.load_module("bson")
            pymongo=importer.load_module("pymongo")
        except:
            data['status']=0
            data['msg']='pymongo module not installed'
            return data

        
        try:

            try:
                mongo_uri = 'mongodb://' + self.mongod_server

                if self.tls:
                    self.connection = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=10000,tls=self.tls,tlscertificatekeyfile=self.tlscertificatekeyfile,tlscertificatekeyfilepassword=self.tlscertificatekeyfilepassword,tlsallowinvalidcertificates=self.tlsallowinvalidcertificates,directConnection=True)
                else:
                    self.connection = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=10000, directConnection=True)



                db = self.connection[self.dbname]

                # Log long-running queries before metrics collection
                log_long_running_queries(self.connection, long_query_duration, plugin_script_path)

                # Log slow queries from system.profile (all DBs, lookback window)
                log_slow_queries(self.connection, slow_query_profile_lookback_minutes, plugin_script_path)

                cache_data = db.command('serverStatus', recordStats=0)
                time.sleep(5)
                output = db.command('serverStatus', recordStats=0)
                elapsed_time=output['uptime']-cache_data['uptime']
                data['Total_no_of_dbs']=len(self.connection.list_database_names())
                stats=db.command('dbstats')

            except pymongo.errors.ServerSelectionTimeoutError:
                data['status']=0
                data['msg']='No mongoDB server is available to connect'
                return data
            except pymongo.errors.ConnectionFailure:
                data['status']=0
                data['msg']='Connection to database failed'
                return data
            except pymongo.errors.ExecutionTimeout:
                data['status']=0
                data['msg']='Execution of database command failed'
                return data

            # Queries Per Second (opcounters)
            try:
                data['Opcounters_Insert_per_sec'] = per_sec('opcounters','insert')
                data['Opcounters_Query_per_sec'] = per_sec('opcounters','query')
                data['Opcounters_Update_per_sec'] = per_sec('opcounters','update')
                data['Opcounters_Delete_per_sec'] = per_sec('opcounters','delete')
                data['Opcounters_Getmore_per_sec'] = per_sec('opcounters','getmore')
                data['Opcounters_Command_per_sec'] = per_sec('opcounters','command')
            except KeyError as ex:
                pass

            # Latency
            try:
                data['OpLatencies_Reads_Latency'] = output['opLatencies']['reads']['latency']
                data['OpLatencies_Writes_Latency'] = output['opLatencies']['writes']['latency']
                data['OpLatencies_Commands_Latency'] = output['opLatencies']['commands']['latency']
            except KeyError as ex:
                pass

            # Query Efficiency & Index Insights
            try:
                metrics_op = output['metrics']['operation']
                total_docs_examined = metrics_op.get('totalDocsExamined', 0)
                total_keys_examined = metrics_op.get('totalKeysExamined', 0)
                nreturned = metrics_op.get('totalDocsReturned', 0)
                scan_and_order = metrics_op.get('scanAndOrder', 0)

                # Scan & Order Ratio: totalDocsExamined / nreturned
                data['Scan_Order_Ratio'] = round(total_docs_examined / nreturned, 2) if nreturned > 0 else 0

                # Index Scan Ratio: totalKeysExamined / nreturned
                data['Index_Scan_Ratio'] = round(total_keys_examined / nreturned, 2) if nreturned > 0 else 0

                # In-Memory Sorts: raw counter from scanAndOrder
                data['InMemory_Sorts'] = scan_and_order

            except KeyError as ex:
                pass

            # WiredTiger Cache Tuning
            try:
                wt_cache = output['wiredTiger']['cache']
                dirty_bytes = wt_cache.get('tracked dirty bytes in the cache', 0)
                max_bytes = wt_cache.get('maximum bytes configured', 1)
                pages_read = wt_cache.get('pages read into cache', 0)

                # Cache Dirty %: (dirty bytes / max bytes) * 100
                data['Cache_Dirty_Pct'] = round((dirty_bytes / max_bytes) * 100, 2) if max_bytes > 0 else 0

                # Cache Pages Read into cache
                data['Cache_Pages_Read'] = pages_read

            except KeyError as ex:
                pass

            # Concurrency & Lock Insights
            try:
                # Global Lock Queue — readers and writers waiting
                locks = output.get('locks', {})
                global_lock = output.get('globalLock', {})
                current_queue = global_lock.get('currentQueue', {})

                data['Global_Lock_Queue_Readers'] = current_queue.get('readers', 0)
                data['Global_Lock_Queue_Writers'] = current_queue.get('writers', 0)

                # Lock Wait Time — collection-level exclusive lock wait (microseconds)
                collection_lock = locks.get('Collection', {})
                time_waiting = collection_lock.get('timeWaitingMicros', {})
                data['Lock_Wait_Time_Micros'] = time_waiting.get('W', 0) + time_waiting.get('w', 0)

                # Connections
                connections = output.get('connections', {})
                data['Connections_Current']   = connections.get('current', 0)
                data['Connections_Available'] = connections.get('available', 0)

                # Network
                network = output.get('network', {})
                data['Network_Bytes_In']  = network.get('bytesIn', 0)
                data['Network_Bytes_Out'] = network.get('bytesOut', 0)

                # Active Clients (from globalLock)
                active_clients = output.get('globalLock', {}).get('activeClients', {})
                data['Active_Reads']  = active_clients.get('readers', 0)
                data['Active_Writes'] = active_clients.get('writers', 0)

            except KeyError as ex:
                pass

            # Oplog Window Metrics (Replica Set PRIMARY only — returns 0 on standalone/mongos)
            try:
                local_db = self.connection['local']
                stats = local_db.command('collStats', 'oplog.rs')
                oplog_size_mb  = round(stats.get('maxSize', 0) / (1024 * 1024), 3)
                oplog_used_mb  = round(stats.get('size', 0) / (1024 * 1024), 3)
                oplog_used_pct = round((oplog_used_mb / oplog_size_mb) * 100, 3) if oplog_size_mb > 0 else 0
                # Get first and last oplog timestamps for window calculation
                oplog_col = local_db['oplog.rs']
                first_doc = oplog_col.find_one(sort=[('$natural', 1)])
                last_doc  = oplog_col.find_one(sort=[('$natural', -1)])
                if first_doc and last_doc:
                    first_ts = first_doc['ts'].time
                    last_ts  = last_doc['ts'].time
                    data['Oplog_Window_Hours'] = round((last_ts - first_ts) / 3600, 3)
                else:
                    data['Oplog_Window_Hours'] = 0
                data['Oplog_Size_MB']  = oplog_size_mb
                data['Oplog_Used_MB']  = oplog_used_mb
                data['Oplog_Used_Pct'] = oplog_used_pct
            except Exception:
                data['Oplog_Window_Hours'] = 0
                data['Oplog_Size_MB']      = 0
                data['Oplog_Used_MB']      = 0
                data['Oplog_Used_Pct']     = 0

            # Replica Set Members (PRIMARY only — returns [] on standalone/mongos)
            try:
                rs_status = self.connection.admin.command('replSetGetStatus')
                replica_set_name = rs_status.get('set', 'unknown')
                members = []
                for member in rs_status.get('members', []):
                    members.append({
                        'name': member.get('name', 'unknown'),
                        'replica_set': replica_set_name,
                        'role': member.get('stateStr', 'unknown')
                    })
                data['replica_set_members'] = members
            except Exception:
                data['replica_set_members'] = []

        except Exception as e:
            data['status']=0
            data['msg']=str(e)

        data['units']=METRICS_UNITS
        data['tabs']=METRICS_TABS

        return data

def flatten_doc(doc, parent_key='', sep='_'):
    items = {}
    for k, v in doc.items():
        new_key = parent_key + sep + k if parent_key else k
        new_key = new_key.lower()  # normalize all keys to lowercase
        if isinstance(v, dict):
            items.update(flatten_doc(v, new_key, sep=sep))
        else:
            # Serialize any non-JSON-native types to string
            if hasattr(v, '__class__') and v.__class__.__name__ in ('ObjectId', 'UUID', 'Binary', 'Decimal128'):
                v = str(v)
            elif isinstance(v, bytes):
                v = v.hex()
            items[new_key] = v
    return items


def log_slow_queries(connection, slow_query_profile_lookback_minutes, plugin_script_path):
    """
    Reads system.profile from all accessible DBs and writes all profiled
    queries recorded in the last slow_query_profile_lookback_minutes minutes
    to slow_query_<date>_<time>.txt — one flattened JSON per line.
    Missing fields are written as "missing".
    """
    now = datetime.now()
    log_file = os.path.join(
        plugin_script_path,
        'slow_query_{}_{}.txt'.format(
            now.strftime('%Y-%m-%d'),
            now.strftime('%H-%M-%S')
        )
    )

    # Delete all previous slow_query_*.txt files
    for old_file in glob.glob(os.path.join(plugin_script_path, 'slow_query_*.txt')):
        os.remove(old_file)

    # ts in system.profile is stored as UTC naive datetime by PyMongo
    # Use utcnow() (naive) to match — avoids timezone-aware comparison errors
    import datetime as _dt
    cutoff_time = _dt.datetime.utcnow() - timedelta(minutes=int(slow_query_profile_lookback_minutes))

    try:
        all_docs = []
        db_names = connection.list_database_names()
        skip_dbs = {'admin', 'local', 'config'}

        for db_name in db_names:
            if db_name in skip_dbs:
                continue
            try:
                db = connection[db_name]
                # Check profiling is enabled (system.profile collection exists)
                if 'system.profile' not in db.list_collection_names():
                    continue
                # ts in system.profile is stored as UTC naive datetime
                cursor = db['system.profile'].find(
                    {"ts": {"$gte": cutoff_time}},
                    sort=[("ts", -1)]
                )
                for doc in cursor:
                    doc['_source_db'] = db_name
                    all_docs.append(doc)
            except Exception:
                continue

        with open(log_file, 'w') as f:
            for doc in all_docs:
                flat = flatten_doc(doc)
                f.write(json.dumps(flat, default=str) + '\n')

    except Exception:
        open(log_file, 'w').close()


def log_long_running_queries(connection, long_query_duration_secs, plugin_script_path):
    now = datetime.now()
    log_file = os.path.join(
        plugin_script_path,
        'long_running_query_{}_{}.txt'.format(
            now.strftime('%Y-%m-%d'),
            now.strftime('%H-%M-%S')
        )
    )

    for old_file in glob.glob(os.path.join(plugin_script_path, 'long_running_query_*.txt')):
        os.remove(old_file)

    if os.path.exists(log_file):
        os.remove(log_file)

    secs_threshold = int(long_query_duration_secs)

    pipeline = [
        {
            "$currentOp": {
                "allUsers": True,
                "idleConnections": False
            }
        },
        {
            "$match": {
                "active": True,
                "secs_running": {"$gte": secs_threshold}
            }
        }
    ]

    try:
        admin_db = connection["admin"]
        long_running = list(admin_db.aggregate(pipeline))

        with open(log_file, 'w') as f:
            for op in long_running:
                flat = flatten_doc(op)
                f.write(json.dumps(flat, default=str) + '\n')

    except Exception:
        open(log_file, 'w').close()


if __name__ == "__main__":


    host ="127.0.0.1"
    port ="27017"
    username ="None"
    password ="None"
    dbname ="mydatabase"
    authdb="admin"
    long_query_duration ="5"
    slow_query_profile_lookback_minutes = "5"

    # TLS/SSL Details
    tls="False"
    tlscertificatekeyfile=None
    tlscertificatekeyfilepassword=None
    tlsallowinvalidcertificates="True"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= host)
    parser.add_argument('--port',help="Port",nargs='?', default= port)
    parser.add_argument('--username',help="username", default= username)
    parser.add_argument('--password',help="Password", default= password)
    parser.add_argument('--dbname' ,help="dbname",nargs='?', type=str,default= dbname)
    parser.add_argument('--authdb' ,help="authdb",nargs='?',type=str, default= authdb)
    parser.add_argument('--long_query_duration', help="Long running query threshold in seconds", nargs='?', default=long_query_duration)
    parser.add_argument('--slow_query_profile_lookback_minutes', help="Lookback window in minutes for slow query profiler", nargs='?', default=slow_query_profile_lookback_minutes)

    parser.add_argument('--tls' ,help="tls setup (True or False)",nargs='?',default= tls)
    parser.add_argument('--tlscertificatekeyfile' ,help="tlscertificatekeyfile file path",default= tlscertificatekeyfile)
    parser.add_argument('--tlscertificatekeyfilepassword' ,help="tlscertificatekeyfilepassword",default= tlscertificatekeyfilepassword)
    parser.add_argument('--tlsallowinvalidcertificates' ,help="tlsallowinvalidcertificates",default= tlsallowinvalidcertificates)
    
    args=parser.parse_args()
    mongo_check = MongoDB(args)
    
    result = mongo_check.metricCollector()
    
    print(json.dumps(result, indent=4))