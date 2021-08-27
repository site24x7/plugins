#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler



metric_units={
    "Request Duration":"seconds"
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
            data1=data["counters"]
            self.resultjson["Total ActiveRequests"]=data1["http.activeRequests"]["count"]
            data1=data["meters"]
            self.resultjson["Total BadRequest"]=data1["http.responseCodes.badRequest"]["count"]
            self.resultjson["Total Responsecode Created"]=data1["http.responseCodes.created"]["count"]
            self.resultjson["Total Forbidden Responsecode"]=data1["http.responseCodes.forbidden"]["count"]
            self.resultjson["NoContent Responsecode"]=data1["http.responseCodes.noContent"]["count"]
            self.resultjson["NotFound Responsecode"]=data1["http.responseCodes.notFound"]["count"]
            self.resultjson["Unmodified Responsecode"]=data1["http.responseCodes.notModified"]["count"]
            self.resultjson["Success Responsecpde"]=data1["http.responseCodes.ok"]["count"]
            self.resultjson["Non Informational Responsecode"]=data1["http.responseCodes.other"]["count"]
            self.resultjson["ServerError Responsecode"]=data1["http.responseCodes.serverError"]["count"]
            self.resultjson["Service Unavailable"]=data1["http.responseCodes.serviceUnavailable"]["count"]
            data1=data["timers"]
            self.resultjson["Request Duration"]=data1["http.requests"]["mean"]
            
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
