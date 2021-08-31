#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler



metric_units={
    "heap_memory_commited":"bytes",
    "heap_memory_initiated":"bytes",
    "maximum_heap_memory":"bytes",
    "heap_memory_used":"bytes",
    "non-heap_memory_commited":"bytes",
    "non-heap_memory_initiated":"bytes",
    "maximum_non-heap_memory":"bytes",
    "non-heap_memory_used":"bytes",
    "total_memory_commited":"bytes",
    "total_memory_initiated":"bytes",
    "total_maximum_memory":"bytes",
    "total_memory_used":"bytes"
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
            response = (urlconnection.urlopen(url)).read().decode('UTF-8')
            response=json.loads(response)
            data=response["gauges"]
            self.resultjson["blocked_thread"]=data["vm.blocked.count"]["value"]
            self.resultjson["thread_count"]=data["vm.count"]["value"]
            self.resultjson["deadlock_count"]=data["vm.deadlock.count"]["value"]
            self.resultjson["file_descriptor_ratio"]=data["vm.file.descriptor.ratio"]["value"]
            self.resultjson["heap_memory_commited"]=data["vm.memory.heap.committed"]["value"]
            self.resultjson["heap_memory_initiated"]=data["vm.memory.heap.init"]["value"]
            self.resultjson["maximum_heap_memory"]=data["vm.memory.heap.max"]["value"]
            self.resultjson["heap_memory_used"]=data["vm.memory.heap.used"]["value"]
            self.resultjson["non-heap_memory_commited"]=data["vm.memory.non-heap.committed"]["value"]
            self.resultjson["non-heap_memory_initiated"]=data["vm.memory.non-heap.init"]["value"]
            self.resultjson["maximum_non-heap_memory"]=data["vm.memory.non-heap.max"]["value"]
            self.resultjson["non-heap_memory_used"]=data["vm.memory.non-heap.used"]["value"]
            self.resultjson["total_memory_commited"]=data["vm.memory.total.committed"]["value"]
            self.resultjson["total_memory_initiated"]=data["vm.memory.total.init"]["value"]
            self.resultjson["total_maximum_memory"]=data["vm.memory.total.max"]["value"]
            self.resultjson["total_memory_used"]=data["vm.memory.total.used"]["value"]
            self.resultjson["new_threads"]=data["vm.new.count"]["value"]
            self.resultjson["running_threads"]=data["vm.runnable.count"]["value"]
            self.resultjson["terminated_threads"]=data["vm.terminated.count"]["value"]
            self.resultjson["suspended_threads"]=data["vm.timed_waiting.count"]["value"]
            self.resultjson["waiting_threads"]=data["vm.waiting.count"]["value"]
            
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
