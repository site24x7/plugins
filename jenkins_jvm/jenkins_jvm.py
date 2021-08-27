#!/usr/bin/python3

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler



metric_units={
    "Heap Memory Commited":"bytes",
    "Heap Memory Initiated":"bytes",
    "Maximum Heap Memory":"bytes",
    "Heap Memory Used":"bytes",
    "Non-Heap Memory Commited":"bytes",
    "Non-Heap Memory Initiated":"bytes",
    "Maximum Non-Heap Memory":"bytes",
    "Non-Heap Memory Used":"bytes",
    "Total Memory Commited":"bytes",
    "Total Memory Initiated":"bytes",
    "Total Maximum Memory":"bytes",
    "Total Memory Used":"bytes"
}

class Jenkins(object):

    def __init__(self, args):
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password  
        self.apikey=args.apikey
        self.plugin_version=args.plugin_version
        self.heartbeat=args.heartbeat  
        self.resultjson = {}
        
        self.metrics_collector()
        
        self.resultjson['plugin_version'] = self.plugin_version
        self.resultjson['heartbeat_required'] = self.heartbeat
     
    def metrics_collector(self):
        try:
            url="http://"+self.host+":"+self.port+"/metrics/"+self.apikey+"/metrics?pretty=true"
            auth_handler = urlconnection.HTTPBasicAuthHandler((urlconnection.HTTPPasswordMgrWithDefaultRealm()). add_password(None, url, self.username, self.password) )
            data = (urlconnection.urlopen(url)).read().decode('UTF-8')
            data=json.loads(data)
            data1=data["gauges"]
            self.resultjson["Blocked Thread"]=data1["vm.blocked.count"]["value"]
            self.resultjson["Thread Count"]=data1["vm.count"]["value"]
            self.resultjson["Deadlock Count"]=data1["vm.deadlock.count"]["value"]
            self.resultjson["File descriptor Ratio"]=data1["vm.file.descriptor.ratio"]["value"]
            self.resultjson["Heap Memory Commited"]=data1["vm.memory.heap.committed"]["value"]
            self.resultjson["Heap Memory Initiated"]=data1["vm.memory.heap.init"]["value"]
            self.resultjson["Maximum Heap Memory"]=data1["vm.memory.heap.max"]["value"]
            self.resultjson["Heap Memory Used"]=data1["vm.memory.heap.used"]["value"]
            self.resultjson["Non-Heap Memory Commited"]=data1["vm.memory.non-heap.committed"]["value"]
            self.resultjson["Non-Heap Memory Initiated"]=data1["vm.memory.non-heap.init"]["value"]
            self.resultjson["Maximum Non-Heap Memory"]=data1["vm.memory.non-heap.max"]["value"]
            self.resultjson["Non-Heap Memory Used"]=data1["vm.memory.non-heap.used"]["value"]
            self.resultjson["Total Memory Commited"]=data1["vm.memory.total.committed"]["value"]
            self.resultjson["Total Memory Initiated"]=data1["vm.memory.total.init"]["value"]
            self.resultjson["Total Maximum Memory"]=data1["vm.memory.total.max"]["value"]
            self.resultjson["Total Memory Used"]=data1["vm.memory.total.used"]["value"]
            self.resultjson["New Threads"]=data1["vm.new.count"]["value"]
            self.resultjson["Running Threads"]=data1["vm.runnable.count"]["value"]
            self.resultjson["Terminated Threads"]=data1["vm.terminated.count"]["value"]
            self.resultjson["Suspended Threads"]=data1["vm.timed_waiting.count"]["value"]
            self.resultjson["Waiting Threads"]=data1["vm.waiting.count"]["value"]
            
        except Exception as e:
            self.resultjson["msg"]=str(e)
            self.resultjson["status"]=0
        return self.resultjson
      
        
        
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "8080")
    parser.add_argument('--username',help="username")
    parser.add_argument('--password',help="Password")
    parser.add_argument('--apikey' ,help="apikey",nargs='?', default= None)
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args=parser.parse_args()
	
    jenkins = Jenkins(args)
    resultjson = jenkins.metrics_collector()
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
