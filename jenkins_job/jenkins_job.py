#!/usr/bin/python3

import json
import argparse
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler


metric_units={
    "jobs_scheduled_rate":"events/minute",
    "jobs_buildable_duration":"sec",
    "jobs_blocked_duration":"sec",
    "jobs_execution_time":"sec",
    "jobs_queuing_duration":"sec",
    "jobs_total_duration":"sec",
    "jobs_waiting_duration":"sec"
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
            import ssl
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            url="https://"+self.host+":"+self.port+"/metrics/"+self.apikey+"/metrics?pretty=true"
            auth_handler = urlconnection.HTTPBasicAuthHandler((urlconnection.HTTPPasswordMgrWithDefaultRealm()). add_password(None, url, self.username, self.password) )
            response = (urlconnection.urlopen(url,context=context)).read().decode('UTF-8')
            response=json.loads(response)
            data=response["gauges"]
            self.resultjson["jobs_count"]=data["jenkins.job.count.value"]["value"]
            data=response["meters"]
            self.resultjson["jobs_scheduled_rate"]=data["jenkins.job.scheduled"]["mean_rate"]
            data=response["timers"]
            self.resultjson["jobs_blocked_duration"]=data["jenkins.job.blocked.duration"]["mean"]
            self.resultjson["jobs_buildable_duration"]=data["jenkins.job.buildable.duration"]["mean"]
            self.resultjson["jobs_execution_time"]=data["jenkins.job.execution.time"]["mean"]
            self.resultjson["jobs_queuing_duration"]=data["jenkins.job.queuing.duration"]["mean"]
            self.resultjson["jobs_total_duration"]=data["jenkins.job.total.duration"]["mean"]
            self.resultjson["jobs_waiting_duration"]=data["jenkins.job.waiting.duration"]["mean"]

        
        except Exception as e:
            self.resultjson["msg"]=str(e)
            self.resultjson["status"]=0
        return self.resultjson
      
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "8080")
    parser.add_argument('--username',help="user")
    parser.add_argument('--password',help="password")
    parser.add_argument('--apikey' ,help="apikey",nargs='?', default= None)
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args=parser.parse_args()
	
    jenkins = Jenkins(args)
    resultjson = jenkins.metrics_collector()
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
