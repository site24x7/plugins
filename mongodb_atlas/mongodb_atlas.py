#!/usr/bin/python3

import collections
import datetime
import traceback
import time
import json
import urllib.parse


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
                 "Uptime":'s'

                 }



class MongoDB(object):
    def __init__(self, args):
        self.args=args
        self.connect_string=args.mongo_connect_string
        self.dbname=args.dbname


    

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT

        def per_sec(doc,metric):
            diff = output[doc][metric] - cache_data[doc][metric]
            ps = int(diff / elapsed_time)
            return ps
        def per_sec_metric(root,doc,metric):
            diff = output[root][doc][metric] - cache_data[root][doc][metric]
            ps = int(diff / elapsed_time)
            return ps
        try:

            import pymongo
            from pymongo import MongoClient

        except ImportError:
            data['status']=0
            data['msg']='pymongo module not installed'
            return data
        
        try:

            try:
                self.connection = MongoClient(self.connect_string, serverSelectionTimeoutMS=10000)
                db = self.connection[self.dbname]
                cache_data = db.command('serverStatus', recordStats=0)
                time.sleep(5)
                output = db.command('serverStatus', recordStats=0)
                elapsed_time=output['uptime']-cache_data['uptime']
                data['Uptime']=output['uptime']
                data['Total no of dbs']=len(self.connection.list_database_names())
                stats=db.command('dbstats')
                self.connection.close()

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
                data['version'] = output['version']
            except KeyError as ex:
                pass
 
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


        except Exception:
            data['msg']=traceback.format_exc()

        data['units']=METRICS_UNITS

        return data

if __name__ == "__main__":

    mongo_connect_string ="mongodb+srv://test:test123@atlascluster.xyltq3c.mongodb.net/?retryWrites=true&w=majority"
    dbname="Admin"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--mongo_connect_string',help="mongo_connect_string",nargs='?', default= mongo_connect_string)
    parser.add_argument('--dbname' ,help="dbname",nargs='?', type=str,default= dbname)

    
    args=parser.parse_args()
    mongo_check = MongoDB(args)
    
    result = mongo_check.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))