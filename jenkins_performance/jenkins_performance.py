#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler



metric_units={
    "health-check_duration":"sec",
    "builds_blocked_duration":"sec",
    "builds_buildable_duration":"sec",
    "builds_execution_duration":"sec",
    "builds_queuing_duration":"sec",
    "builds_waiting_duration":"sec"
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
            self.resultjson["total_executors_count"]=data["jenkins.executor.count.value"]["value"]
            self.resultjson["executors_free_count"]=data["jenkins.executor.free.value"]["value"]
            self.resultjson["executors_inuse_count"]=data["jenkins.executor.in-use.value"]["value"]
            self.resultjson["node_count"]=data["jenkins.node.count.value"]["value"]
            self.resultjson["nodes_offline"]=data["jenkins.node.offline.value"]["value"]
            self.resultjson["nodes_online"]=data["jenkins.node.online.value"]["value"]
            self.resultjson["projects_count"]=data["jenkins.project.count.value"]["value"]
            self.resultjson["projects_disabled"]=data["jenkins.project.disabled.count.value"]["value"]
            self.resultjson["projects_enabled"]=data["jenkins.project.disabled.count.value"]["value"]
            self.resultjson["queues_blocked"]=data["jenkins.queue.blocked.value"]["value"]
            self.resultjson["jobs_in_queue"]=data["jenkins.queue.buildable.value"]["value"]
            self.resultjson["queues_pending"]=data["jenkins.queue.pending.value"]["value"]
            self.resultjson["queues_size"]=data["jenkins.queue.size.value"]["value"]
            self.resultjson["queues_stuck"]=data["jenkins.queue.stuck.value"]["value"]
            self.resultjson["health-check_count"]=data["jenkins.health-check.count"]["value"]
            self.resultjson["plugins_active"]=data["jenkins.plugins.active"]["value"]
            self.resultjson["plugins_failed"]=data["jenkins.plugins.failed"]["value"]
            self.resultjson["plugins_inactive"]=data["jenkins.plugins.inactive"]["value"]
            self.resultjson["plugins_withupdate"]=data["jenkins.plugins.withUpdate"]["value"]
            data=response["timers"]
            self.resultjson["health-check_duration"]=data["jenkins.health-check.duration"]["mean"]
            self.resultjson["builds_blocked_duration"]=data["jenkins.task.blocked.duration"]["mean"]
            self.resultjson["build_creation_time"]=data["jenkins.task.buildable.duration"]["mean"]
            self.resultjson["builds_execution_duration"]=data["jenkins.task.execution.duration"]["mean"]
            self.resultjson["builds_queuing_duration"]=data["jenkins.task.queuing.duration"]["mean"]
            self.resultjson["builds_waiting_duration"]=data["jenkins.task.waiting.duration"]["mean"]
            
        
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
