#!/usr/bin/python

import json
import argparse
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler


metric_units={
    "Jobs scheduled Rate":"events/minute",
    "Jobs Buildable Duration":"sec",
    "Jobs Blocked Duration":"sec",
    "Jobs Execution Time":"sec",
    "Jobs Queuing Duration":"sec",
    "Jobs Total Duration":"sec",
    "Jobs Waiting Duration":"sec"
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
            self.resultjson["Jobs Count"]=data1["jenkins.job.count.value"]["value"]
            data1=data["meters"]
            self.resultjson["Jobs scheduled Rate"]=data1["jenkins.job.scheduled"]["mean_rate"]
            data1=data["timers"]
            self.resultjson["Jobs Blocked Duration"]=data1["jenkins.job.blocked.duration"]["mean"]
            self.resultjson["Jobs Buildable Duration"]=data1["jenkins.job.buildable.duration"]["mean"]
            self.resultjson["Jobs Execution Time"]=data1["jenkins.job.execution.time"]["mean"]
            self.resultjson["Jobs Queuing Duration"]=data1["jenkins.job.queuing.duration"]["mean"]
            self.resultjson["Jobs Total Duration"]=data1["jenkins.job.total.duration"]["mean"]
            self.resultjson["Jobs Waiting Duration"]=data1["jenkins.job.waiting.duration"]["mean"]

        
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
