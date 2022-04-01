#!/usr/bin/python

import collections
import datetime
import traceback
import time
import json

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

METRICS_UNITS = {'heap_usage':'MB',
                 'memory_resident':'MB',
                 'memory_virtual':'MB',
                 'memory_mapped':'MB'
                 }

host ="localhost"
port ="27017"
username ="none"
password ="none"
dbstats ="yes"
replset ="no"
dbname ="test"

class MongoDB(object):
    def __init__(self, args):
        self.args=args
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password
        self.dbstats=args.dbstats
        self.replset=args.replset
        self.dbname=args.dbname
        if(self.username!=None and self.password!=None and self.dbname!=None):
            self.mongod_server = "{0}:{1}@{2}:{3}/{4}".format(self.username, self.password, self.host, self.port, self.dbname)
        elif(self.username!=None and self.password!=None):
            self.mongod_server = "{0}:{1}@{2}:{3}".format(self.username, self.password, self.host, self.port)
        elif(self.dbname!=None):
            self.mongod_server = "{0}:{1}/{2}".format(self.host, self.port, self.dbname)
        else:
            self.mongod_server = "{0}:{1}".format(self.host, self.port)


    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        try:
            import pymongo
            from pymongo import MongoClient
        except ImportError:
            data['status']=0
            data['msg']='pymongo module not installed'
            return data
        
        try:

            try:
                mongo_uri = 'mongodb://' + self.mongod_server
                self.connection = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
                db = self.connection['local']
                output = db.command('serverStatus', recordStats=0)
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

            #Memory
            try:
                data['memory_resident'] = output['mem']['resident']
                data['memory_virtual'] = output['mem']['virtual']
                data['memory_mapped'] = output['mem']['mapped']

            except KeyError as ex:
                pass

            # Connections
            try:
                data['connections_current'] = output['connections']['current']
                data['connections_available'] = output['connections']['available']

            except KeyError as ex:
                pass

            try:
                data['heap_usage'] = round((float(output['extra_info']['heap_usage_bytes'])/(1024*1024)),2)
                data['page_faults'] = output['extra_info']['page_faults']

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
                data['cursors_total_open'] = output['cursors']['totalOpen']
            except KeyError as ex:
                pass

            # Replica set status
            if 'self.replset' in self.args and self.args.get('self.replset') =='yes':
                # isMaster (to get state
                isMaster = db.command('isMaster')

                data['replSet_setName'] = isMaster['setName']
                data['replSet_isMaster'] = isMaster['ismaster']
                data['replSet_isSecondary'] = isMaster['secondary']

                if 'arbiterOnly' in isMaster:
                    data['replSet_isArbiter'] = isMaster['arbiterOnly']

                # rs.status()
                db = self.connection['admin']
                repl_set = db.command('replSetGetStatus')

                data['replSet_myState'] = repl_set['myState']

                data['replSet'] = {}
                data['replSet']['members'] = {}

                for member in repl_set['members']:

                    data['replSet']['members'][str(member['_id'])] = {
                        'name': member['name'],
                        'state': member['state']
                    }
                    
            # db.stats()
            if 'self.dbstats' in self.args and self.args.get('self.dbstats')=='yes':
                for database in self.connection.database_names():
                    if database != 'config' and database != 'local' and database != 'admin' and database != 'test':

                        dbstats_database = 'dbStats_{0}'.format(database)
                        dbstats_database_namespaces = 'dbStats_{0}_namespaces'.format(database)

                        master = self.connection[database].command('isMaster')

                        dt={}
                        dt[dbstats_database] = self.connection[database].command('dbstats')

                        for key in dt[dbstats_database].keys():
                                data[dbstats_database+'_'+key] = str(dt[dbstats_database][key])

                        # if master['ismaster']:
                        #     namespaces = (self.connection[database]['system']['namespaces'])
                        #     data[dbstats_database_namespaces] = (namespaces.count())
        except Exception:
            data['msg']=traceback.format_exc()

        data['units']=METRICS_UNITS

        return data

if __name__ == "__main__":
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "27017")
    parser.add_argument('--username',help="username", default= username)
    parser.add_argument('--password',help="Password", default= password)
    parser.add_argument('--dbstats' ,help="dbstats",nargs='?', default= dbstats)
    parser.add_argument('--replset' ,help="replset",nargs='?', default= replset)
    parser.add_argument('--dbname' ,help="dbname",nargs='?', default= dbname)
    args=parser.parse_args()
	
    mongo_check = MongoDB(args)
    
    result = mongo_check.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
