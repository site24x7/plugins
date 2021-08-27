#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler



metric_units={
    "Health-check Duration":"sec",
    "Builds Blocked Duration":"sec",
    "Builds Buildable Duration":"sec",
    "Builds Execution Duration":"sec",
    "Builds Queuing Duration":"sec",
    "Builds Waiting Duration":"sec"
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
            self.resultjson["Total Executors Count"]=data1["jenkins.executor.count.value"]["value"]
            self.resultjson["Executors Free Count"]=data1["jenkins.executor.free.value"]["value"]
            self.resultjson["Executors inuse Count"]=data1["jenkins.executor.in-use.value"]["value"]
            self.resultjson["NodeCount"]=data1["jenkins.node.count.value"]["value"]
            self.resultjson["Nodes Offline"]=data1["jenkins.node.offline.value"]["value"]
            self.resultjson["Nodes Online"]=data1["jenkins.node.online.value"]["value"]
            self.resultjson["Projects Count"]=data1["jenkins.project.count.value"]["value"]
            self.resultjson["Projects Disabled"]=data1["jenkins.project.disabled.count.value"]["value"]
            self.resultjson["Projects Enabled"]=data1["jenkins.project.disabled.count.value"]["value"]
            self.resultjson["Queues Blocked"]=data1["jenkins.queue.blocked.value"]["value"]
            self.resultjson["Jobs in Queue"]=data1["jenkins.queue.buildable.value"]["value"]
            self.resultjson["Queues Pending"]=data1["jenkins.queue.pending.value"]["value"]
            self.resultjson["Queues Size"]=data1["jenkins.queue.size.value"]["value"]
            self.resultjson["Queues Stuck"]=data1["jenkins.queue.stuck.value"]["value"]
            self.resultjson["Health-check Count"]=data1["jenkins.health-check.count"]["value"]
            self.resultjson["Plugins Active"]=data1["jenkins.plugins.active"]["value"]
            self.resultjson["Plugins Failed"]=data1["jenkins.plugins.failed"]["value"]
            self.resultjson["Plugins Inactive"]=data1["jenkins.plugins.inactive"]["value"]
            self.resultjson["Plugins Withupdate"]=data1["jenkins.plugins.withUpdate"]["value"]
            data1=data["timers"]
            self.resultjson["Health-check Duration"]=data1["jenkins.health-check.duration"]["mean"]
            self.resultjson["Builds Blocked Duration"]=data1["jenkins.task.blocked.duration"]["mean"]
            self.resultjson["Build Creation Time"]=data1["jenkins.task.buildable.duration"]["mean"]
            self.resultjson["Builds Execution Duration"]=data1["jenkins.task.execution.duration"]["mean"]
            self.resultjson["Builds Queuing Duration"]=data1["jenkins.task.queuing.duration"]["mean"]
            self.resultjson["Builds Waiting Duration"]=data1["jenkins.task.waiting.duration"]["mean"]
            
        
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
