#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler



metric_units={
    "request_duration":"seconds"
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
            data=response["counters"]
            self.resultjson["total_activerequests"]=data["http.activeRequests"]["count"]
            data=response["meters"]
            self.resultjson["total_badrequest"]=data["http.responseCodes.badRequest"]["count"]
            self.resultjson["total_responsecode_created"]=data["http.responseCodes.created"]["count"]
            self.resultjson["total_forbidden_responsecode"]=data["http.responseCodes.forbidden"]["count"]
            self.resultjson["nocontent_responsecode"]=data["http.responseCodes.noContent"]["count"]
            self.resultjson["notfound_responsecode"]=data["http.responseCodes.notFound"]["count"]
            self.resultjson["unmodified_responsecode"]=data["http.responseCodes.notModified"]["count"]
            self.resultjson["success_responsecpde"]=data["http.responseCodes.ok"]["count"]
            self.resultjson["non_informational_responsecode"]=data["http.responseCodes.other"]["count"]
            self.resultjson["servererror_responsecode"]=data["http.responseCodes.serverError"]["count"]
            self.resultjson["service_unavailable"]=data["http.responseCodes.serviceUnavailable"]["count"]
            data=response["timers"]
            self.resultjson["request_duration"]=data["http.requests"]["mean"]
            
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
