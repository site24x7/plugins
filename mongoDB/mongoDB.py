#!/usr/bin/python3

import collections
import datetime
import traceback
import time
import json
import urllib.parse
import os
import warnings
warnings.filterwarnings("ignore")

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

METRICS_UNITS = {
                 
                 "Heap Usage":'MB',
                 "Memory Resident":'MB',
                 "Memory Virtual":'MB',
                 "Memory Mapped":'MB',
                 "Memory Bits":'bits',
                 "Network Bytes In per sec":'bytes',
                 "Network Bytes Out per sec":'bytes',
                 "Network Num Requests per sec":'requests',
                 "Asserts Msg per sec":'assertions',
                 "Asserts User per sec":'assertions',
                 "Asserts Regular per sec":'assertions',
                 "Asserts Warning per sec":'assertions',
                 "OpLatencies Reads Latency":'ms',
                 "OpLatencies Writes Latency":'ms',
                 "OpLatencies Commands Latency":'ms',
                 "Opcounters Insert per sec":'operations',
                 "Opcounters Update per sec":'operations',
                 "Opcounters Delete per sec":'operations',
                 "Opcounters Getmore per sec":'operations',
                 "Opcounters Command per sec":'commands',
                 "Opcounters Query per sec":'queries',
                 "Document Deleted per sec":'documents',
                 "Document Inserted per sec":'documents',
                 "Document Returned per sec":'documents',
                 "Document Updated per sec":'documents',
                 "Concurrent Transactions Read Available":'tickets',
                 "Concurrent Transactions Read Out":'tickets',
                 "Concurrent Transactions Read Total Tickets":'tickets',
                 "Concurrent Transactions Write Available":'tickets',
                 "Concurrent Transactions Write Out":'tickets',
                 "Concurrent Transactions Write Total Tickets":'tickets',
                 "Bytes Currently in the Cache":'bytes',
                 "Extra Info Page Faults per sec":'faults',
                 "Total Page Faults":'faults',
                 "Total no of dbs":'databases',
                 "Cursors Total Open":'cursors',
                 "Cursors Timedout":'cursors',
                 "Metrics cursor Timed Out":'cursors',
                 "Metrics cursor Open NoTimeout":'cursors',
                 "Metrics cursor Open Pinned":'cursors',
                 "Metrics cursor Open Total":'cursors',
                 "Current Connections":'connections',
                 "Total Connections Created":'connections',
                 "Stats Objects":'objects',
                 "Stats Collections":'collections',
                 "Stats Storage Size":'bytes',
                 "Stats Indexes":'indexes',
                 "Stats Index Size":'bytes',
                 "Stats Data Size":'bytes',
                 "Uptime":'s',
                 "Health": "health",
	         "ID": "_id",
	         "Opcounters Repl Command per sec": "commands",
	         "Opcounters Repl Delete per sec": "operations",
	         "Opcounters Repl Getmore per sec": "operations",
	         "Opcounters Repl Insert per sec": "operations",
	         "Opcounters Repl Query per sec": "queries",
	         "Opcounters Repl Update per sec": "operations",
	         "Oplog Log Size MB": "MB",
	         "Oplog timeDiff": "s",
	         "Oplog used MB": "MB",
	         "Repl Apply Batches Total millis per sec": "fractions",
	         "Repl Apply ops per sec": "operations",
	         "Repl Buffer Count per sec": "operations",
	         "Repl Buffer Max Size Bytes": "bytes",
	         "Repl Buffer Size Bytes": "bytes",
	         "Repl Network Bytes per sec": "bytes",
	         "Repl Network Getmores Num per sec": "operations",
	         "Repl Network Getmores Total millis per sec": "fractions",
	         "Repl Network Readers Created per sec": "processes",
	         "Repl Network ops per sec": "fractions",
	         "Replication Lag": "s",
	         "State": "state",
	         "TTL Deleted Documents per sec": "documents",
	         "TTL Passes per sec": "operations",
	         "Voting Members Count": "members"


                 }
                 
METRICS_TABS = {
            "Database":{
                "order":1,
                "tablist":[
                    "Opcounters Insert per sec",
                    "Opcounters Query per sec",
                    "Opcounters Update per sec",
                    "Opcounters Delete per sec",
                    "Opcounters Getmore per sec",
                    "Opcounters Command per sec",
                    "Document Deleted per sec",
                    "Document Inserted per sec",
                    "Document Returned per sec",
                    "Document Updated per sec",
                    "TTL Deleted Documents per sec",
                    "TTL Passes per sec"
                ]},
                "Performance":{
                "order":2,
                "tablist":[
                    "Network Bytes In per sec",
                    "Network Bytes Out per sec",
                    "Network Num Requests per sec",
                    "Stats Objects",
                    "Stats Collections",
                    "Stats Storage Size",
                    "Stats Indexes",
                    "Stats Index Size",
                    "Stats Data Size",
                    "Memory Resident",
                    "Memory Virtual"
                ]},
                "Connection":{
                "order":3,
                "tablist":[
                    "Connections Available",
                    "Current Connections",
                    "Concurrent Transactions Read Available",
                    "Concurrent Transactions Read Out",
                    "Concurrent Transactions Read Total Tickets",
                    "Concurrent Transactions Write Available",
                    "Concurrent Transactions Write Out",
                    "Concurrent Transactions Write Total Tickets"
                ]},
                "Cursor":{
                "order":4,
                "tablist":[
                    "Metrics cursor Timed Out",
                    "Metrics cursor Open NoTimeout",
                    "Metrics cursor Open Pinned",
                    "Metrics cursor Open Total"
                ]},
                "Replication":{
                "order":5,
                "tablist":[
                    "Repl Apply ops per sec",
                    "Repl Buffer Count per sec",
                    "Repl Network Bytes per sec",
                    "Repl Network Readers Created per sec",
                    "Repl Network ops per sec",
                    "Repl Apply Batches Total millis per sec",
                    "Repl Network Getmores Num per sec",
                    "Repl Network Getmores Total millis per sec",
		    "Repl Buffer Max Size Bytes",
		    "Repl Buffer Size Bytes",
                    "Opcounters Repl Insert per sec",
                    "Opcounters Repl Query per sec",
                    "Opcounters Repl Update per sec",
                    "Opcounters Repl Delete per sec",
                    "Opcounters Repl Getmore per sec",
                    "Opcounters Repl Command per sec"
                ]}
}


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

        def per_sec(doc,metric):
            diff = output[doc][metric] - cache_data[doc][metric]
            ps = int(diff / elapsed_time)
            return ps
        def per_sec_metric(root,doc,metric):
            diff = output[root][doc][metric] - cache_data[root][doc][metric]
            ps = int(diff / elapsed_time)
            return ps
            
        def get_replication_info():

            local_db = self.connection['local']

            for collection_name in ("oplog.rs", "oplog.$main"):
                try:
                    ol_options = local_db[collection_name].options()

                    if ol_options and 'size' in ol_options:
                       break

                except Exception as e:
                    pass

            timestamp = local_db[collection_name]
            first_oplog_entry = timestamp.find({"ts": {"$exists": 1}}).sort("$natural", pymongo.ASCENDING).limit(1)
            last_oplog_entry = timestamp.find({"ts": {"$exists": 1}}).sort("$natural", pymongo.DESCENDING).limit(1)
            time_diff = last_oplog_entry[0]['ts'].as_datetime() - first_oplog_entry[0]['ts'].as_datetime()


            replication_info = {
            'logSizeMB': round(ol_options['size'] / 2.0**20, 2),
            'usedMB':  round(local_db.command("collstats", collection_name)['size'] / 2.0**20, 2),
            'timeDiff': int(time_diff.total_seconds()),
            'tFirst': first_oplog_entry[0]['ts'].as_datetime(),
            'tLast': last_oplog_entry[0]['ts'].as_datetime()
            }

            return replication_info

        def per_sec_2(doc,metric):
            diff = output[doc][metric] - cache_data[doc][metric]
            ps = int(diff / elapsed_time)
            return ps
        def per_sec_3(root,doc,metric):
            diff = output[root][doc][metric] - cache_data[root][doc][metric]
            ps = int(diff / elapsed_time)
            return ps     
        def per_sec_4(root,doc,node,metric):
            diff = output[root][doc][node][metric] - cache_data[root][doc][node][metric]
            ps = int(diff / elapsed_time)
            return ps
        def per_sec_5(root,doc,node,node1,metric):
            diff = output[root][doc][node][node1][metric] - cache_data[root][doc][node][node1][metric]
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
                db_admin = self.connection[self.authdb]
                cache_data = db.command('serverStatus', recordStats=0)
                time.sleep(5)
                output = db.command('serverStatus', recordStats=0)
                elapsed_time=output['uptime']-cache_data['uptime']
                data['Uptime']=output['uptime']
                data['Total no of dbs']=len(self.connection.list_database_names())
                stats=db.command('dbstats')
                
                try:
                    replication_data = db_admin.command({'replSetGetStatus'  :1})
                    oplog=get_replication_info()
                    self.connection.close()
                except Exception as e:
                    if 'not running with --replSet' in str(e):
                        pass
                    else:
                        data['msg'] = str(e)

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

            #Version
            try:
                data['MongoDB Version'] = output['version']
            except KeyError as ex:
                pass
 
            #Asserts,extra info,network,opcounters,fsynclocked
            try:
                data['Asserts Msg per sec']=per_sec('asserts','msg')
                data['Asserts User per sec']=per_sec('asserts','user')
                data['Asserts Regular per sec']=per_sec('asserts','regular')
                data['Asserts Warning per sec']=per_sec('asserts','warning')
                data['Extra Info Page Faults per sec'] = per_sec('extra_info','page_faults')
                data['Network Bytes In per sec'] = per_sec('network','bytesIn')
                data['Network Bytes Out per sec'] = per_sec('network','bytesOut')
                data['Network Num Requests per sec'] = per_sec('network','numRequests')
                data['Opcounters Insert per sec'] = per_sec('opcounters','insert')
                data['Opcounters Query per sec'] = per_sec('opcounters','query')
                data['Opcounters Update per sec'] = per_sec('opcounters','update')
                data['Opcounters Delete per sec'] = per_sec('opcounters','delete')
                data['Opcounters Getmore per sec'] = per_sec('opcounters','getmore')
                data['Opcounters Command per sec'] = per_sec('opcounters','command')
                data['Document Deleted per sec']=per_sec_metric('metrics','document','deleted')
                data['Document Inserted per sec']=per_sec_metric('metrics','document','inserted')
                data['Document Returned per sec']=per_sec_metric('metrics','document','returned')
                data['Document Updated per sec']=per_sec_metric('metrics','document','updated')
                data['Fsynclocked']= output['fsynclocked']

            except KeyError as ex:
                pass

            #Stats
            try:
                data['Stats Objects'] = stats['objects']
                data['Stats Collections'] = stats['collections']
                data['Stats Storage Size'] = stats['storageSize']
                data['Stats Indexes'] = stats['indexes']
                data['Stats Index Size'] = stats['indexSize']
                data['Stats Data Size'] = stats['dataSize']

            except KeyError as ex:
                pass

            #Memory
            try:
                data['Memory Resident'] = output['mem']['resident']
                data['Memory Virtual'] = output['mem']['virtual']
                data['Memory Mapped'] = output['mem']['mapped']
                data['Memory Bits'] = output['mem']['bits']

            except KeyError as ex:
                pass
            #oplatencies
            try:
                data['OpLatencies Reads Latency'] = output['opLatencies']['reads']['latency']
                data['OpLatencies Writes Latency'] = output['opLatencies']['writes']['latency']
                data['OpLatencies Commands Latency'] = output['opLatencies']['commands']['latency']
                
            except KeyError as ex:
                pass


            #WiredTiger
            try:
                data['Bytes Currently in the Cache'] = output['wiredTiger']['cache']['bytes currently in the cache']
                data['Concurrent Transactions Read Available'] = output['wiredTiger']['concurrentTransactions']['read']['available']
                data['Concurrent Transactions Read Out'] = output['wiredTiger']['concurrentTransactions']['read']['out']
                data['Concurrent Transactions Read Total Tickets'] = output['wiredTiger']['concurrentTransactions']['read']['totalTickets']
                data['Concurrent Transactions Write Available'] = output['wiredTiger']['concurrentTransactions']['write']['available']
                data['Concurrent Transactions Write Out'] = output['wiredTiger']['concurrentTransactions']['write']['out']
                data['Concurrent Transactions Write Total Tickets'] = output['wiredTiger']['concurrentTransactions']['write']['totalTickets']

            except KeyError as ex:
                pass

            # Metrics.cursor
            try:
                data['Metrics cursor Timed Out'] = output['metrics']['cursor']['timedOut']
                data['Metrics cursor Open NoTimeout'] = output['metrics']['cursor']['open']['noTimeout']
                data['Metrics cursor Open Pinned'] = output['metrics']['cursor']['open']['pinned']
                data['Metrics cursor Open Total'] = output['metrics']['cursor']['open']['total']

            except KeyError as ex:
                pass

            # Connections
            try:
                data['Current Connections'] = output['connections']['current']
                data['Connections Available'] = output['connections']['available']
                data['Total Connections Created'] = output['connections']['totalCreated']

            except KeyError as ex:
                pass

            try:
                data['Heap Usage'] = round((float(output['extra_info']['heap_usage_bytes'])/(1024*1024)),2)
                data['Total Page Faults'] = output['extra_info']['page_faults']

            except KeyError as ex:
                pass

            # flushing
            try:
                delta = (datetime.datetime.utcnow()-output['backgroundFlushing']['last_finished'])
                data['seconds_since_lastflush'] = delta.seconds
                data['last_flush_length'] = output['backgroundFlushing']['last_ms']
                data['flush_length_avrg'] = output['backgroundFlushing']['average_ms']
            except KeyError as ex:
                pass

            # Cursors
            try:
                data['Cursors Total Open'] = output['cursors']['totalOpen']
                data['Cursors Timedout'] = output['cursors']['timedOut']

            except KeyError as ex:
                pass
                
            
            #OpCounters Repl, Metrics 
            try:
                data['Opcounters Repl Insert per sec'] = per_sec_2('opcountersRepl','insert')
                data['Opcounters Repl Query per sec'] = per_sec_2('opcountersRepl','query')
                data['Opcounters Repl Update per sec'] = per_sec_2('opcountersRepl','update')
                data['Opcounters Repl Delete per sec'] = per_sec_2('opcountersRepl','delete')
                data['Opcounters Repl Getmore per sec'] = per_sec_2('opcountersRepl','getmore')
                data['Opcounters Repl Command per sec'] = per_sec_2('opcountersRepl','command')
                data['TTL Deleted Documents per sec']=per_sec_3('metrics','ttl','deletedDocuments')
                data['TTL Passes per sec']=per_sec_3('metrics','ttl','passes')
                data['Repl Apply ops per sec']=per_sec_4('metrics','repl','apply','ops')
                data['Repl Buffer Count per sec']=per_sec_4('metrics','repl','buffer','count')
                data['Repl Network Bytes per sec']=per_sec_4('metrics','repl','network','bytes')
                data['Repl Network Readers Created per sec']=per_sec_4('metrics','repl','network','readersCreated')
                data['Repl Network ops per sec']=per_sec_4('metrics','repl','network','ops')
                data['Repl Apply Batches Total millis per sec']=per_sec_5('metrics','repl','apply','batches','totalMillis')
                data['Repl Network Getmores Num per sec']=per_sec_5('metrics','repl','network','getmores','num')
                data['Repl Network Getmores Total millis per sec']=per_sec_5('metrics','repl','network','getmores','totalMillis')
                data['Repl Preload Indexes Total millis per sec']=per_sec_5('metrics','repl','preload','indexes','totalMillis')
                data['Repl Preload Indexes Num per sec']=per_sec_5('metrics','repl','preload','indexes','num')
                data['Repl Preload Doc Total millis per sec']=per_sec_5('metrics','repl','preload','docs','totalMillis')
                data['Repl Preload Doc Num per sec']=per_sec_5('metrics','repl','preload','docs','num')
                


            except KeyError as ex:
                pass

            #Oplog
            
            try:
                data['Oplog Log Size MB'] = oplog['logSizeMB']
                data['Oplog used MB'] = oplog['usedMB']
                data['Oplog timeDiff'] = oplog['timeDiff']
                tfirst= str(oplog['tFirst']).split(" ")
                data['Oplog First Entry Date'] =tfirst[0]
                data['Oplog First Entry Time'] =tfirst[-1]
                tlast= str(oplog['tLast']).split(" ")
                data['Oplog Last Entry Date'] =tlast[0]
                data['Oplog Last Entry Time'] =tlast[-1]


            except Exception as ex:
                pass
            
            #Repl
            try:
                data['Repl Buffer Max Size Bytes'] = output['metrics']['repl']['buffer']['maxSizeBytes']
                data['Repl Buffer Size Bytes'] = output['metrics']['repl']['buffer']['sizeBytes']


            except KeyError as ex:
                pass

            #Repl Set
            try:
                optime=None
                primary_optime=None
                
                if 'votingMembersCount' in replication_data:
                    data['Voting Members Count']=replication_data["votingMembersCount"]
                
                for member in replication_data["members"]:
                    if member["stateStr"]=="PRIMARY":
                        primary_optime=member["optimeDate"]
                        break
                
                current_member = None
                for member in replication_data["members"]:
                    if member.get("self", False):
                        current_member = member
                        break
                
                if current_member:
                    data["Health"]=int(current_member["health"])
                    data["State Str"]=current_member["stateStr"]
                    data["State"]=current_member["state"] 
                    data["ID"]=str(current_member["_id"])
                    optime=current_member["optimeDate"]
                    
                    if primary_optime and optime:
                        data["Replication Lag"]=(primary_optime-optime).total_seconds()
                    else:
                        data["Replication Lag"]=0.0

            except Exception as ex:
                pass

            try:
                if 'sharding' in output:
                    config_conn_string = output['sharding'].get('configsvrConnectionString', '')
                    
                    cluster_name = config_conn_string.split('/')[0] if '/' in config_conn_string else 'unknown'
                    
                    data["tags"] = "MONGODB_CLUSTER:{},MONGODB_NODE:{}".format(cluster_name, self.host)
            except KeyError as ex:
                pass



        except Exception as e:
            data['status']=0
            data['msg']=str(e)

        data['units']=METRICS_UNITS
        data['tabs']=METRICS_TABS

        return data

if __name__ == "__main__":


    host ="127.0.0.1"
    port ="27017"
    username ="None"
    password ="None"
    dbname ="mydatabase"
    authdb="admin"

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

    parser.add_argument('--tls' ,help="tls setup (True or False)",nargs='?',default= tls)
    parser.add_argument('--tlscertificatekeyfile' ,help="tlscertificatekeyfile file path",default= tlscertificatekeyfile)
    parser.add_argument('--tlscertificatekeyfilepassword' ,help="tlscertificatekeyfilepassword",default= tlscertificatekeyfilepassword)
    parser.add_argument('--tlsallowinvalidcertificates' ,help="tlsallowinvalidcertificates",default= tlsallowinvalidcertificates)
    
    args=parser.parse_args()
    mongo_check = MongoDB(args)
    
    result = mongo_check.metricCollector()
    
    print(json.dumps(result))
