#! /usr/bin/python3

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
            import pymongo
            from pymongo import MongoClient
        except ImportError as e:
            data['status']=0
            data['msg']='pymongo module not installed\n Solution : Use the following command to install pymongo\n pip install pymongo \n(or)\n pip3 install pymongo'
            return data
        
        try:

            try:
                mongo_uri = 'mongodb://' + self.mongod_server

                if self.tls:
                    self.connection = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000,tls=self.tls,tlscertificatekeyfile=self.tlscertificatekeyfile,tlscertificatekeyfilepassword=self.tlscertificatekeyfilepassword,tlsallowinvalidcertificates=self.tlsallowinvalidcertificates)
                else:
                    self.connection = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)



                db = self.connection[self.dbname]
                db_admin = self.connection["admin"]
                cache_data = db.command('serverStatus', recordStats=0)
                time.sleep(5)
                output = db.command('serverStatus', recordStats=0)
                #print(self.connection.getReplicationInfo())
                elapsed_time=output['uptime']-cache_data['uptime']
                replication_data = db_admin.command({'replSetGetStatus'  :1})
                #print(replication_data)
                
                oplog=get_replication_info()
                self.connection.close()

            except pymongo.errors.ServerSelectionTimeoutError as e:
                data['status']=0
                data['msg']='No mongoDB server is available to connect.\n '+str(e)
                return data
            except pymongo.errors.ConnectionFailure as e:
                data['status']=0
                data['msg']='Connection to database failed. '+str(e)
                return data
            except pymongo.errors.ExecutionTimeout as e:
                data['status']=0
                data['msg']='Execution of database command failed'+str(e)
                return data

 
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


            except KeyError as ex:
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
                data['Voting Members Count']=replication_data["votingMembersCount"]
                for member in replication_data["members"]:

                    host_id=[self.host]
                    if self.host=="127.0.0.1":
                        host_id.append("localhost")
                    elif self.host=="localhost":
                        host_id.append("127.0.0.1")
                    for i in host_id:
                        if member["name"]==i+":"+str(self.port):
                            data["Health"]=int(member["health"])
                            data["State"]=member["state"]
                            data["State Str"]=member["stateStr"]
                            data["ID"]=member["_id"]
                            optime=member["optimeDate"]
                            
                    if member["stateStr"]=="PRIMARY":
                        primary_optime=member["optimeDate"]

                data["Replication Lag"]=(primary_optime-optime).total_seconds()

            except KeyError as ex:
                pass


        except Exception as e:
            data['msg']=str(e)
            #traceback.print_exc()

        data['units']=METRICS_UNITS

        return data

if __name__ == "__main__":


    host ="127.0.0.1"
    port ="27083"
    username ="None"
    password ="None"
    dbname ="local"
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
    #traceback.print_exc()
    
    print(json.dumps(result, indent=4, sort_keys=True, default=str))
