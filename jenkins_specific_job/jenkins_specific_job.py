#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler


metric_units={
    "job_lastbuild_duration":"ms",
    "job_lastbuild_estimated_duration":"ms"
}


class Jenkins(object):

    def __init__(self, args):
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password  
        self.jobname=args.jobname
        self.plugin_version=args.plugin_version
        self.heartbeat=args.heartbeat  
        self.resultjson = {}
        
        self.metrics_collector()
        
        self.resultjson['plugin_version'] = self.plugin_version
        self.resultjson['heartbeat_required'] = self.heartbeat
        
    def url_data_collector(self, url):
        auth_handler = urlconnection.HTTPBasicAuthHandler((urlconnection.HTTPPasswordMgrWithDefaultRealm()). add_password(None, url, self.username, self.password) )
        data = (urlconnection.urlopen(url)).read().decode('UTF-8')
        data=json.loads(data)
     
        return data
    
    def metrics_collector(self):
        successful_build=0
        failed_build=0
        aborted_build=0
        try:
            url="http://"+self.host+":"+self.port+"/job/"+self.jobname+"/lastBuild/api/json"
            data=self.url_data_collector(url)
            self.resultjson["job_lastbuild_queueid"]=data["queueId"]
            self.resultjson["job_lastbuild_duration"]=data["duration"]
            self.resultjson["job_lastbuild_estimated_duration"]=data["estimatedDuration"]
            self.resultjson["job_lastbuildid"]=data["id"]
            self.resultjson["job_lastbuildnumber"]=data["number"]
            url="http://"+self.host+":"+self.port+"/job/"+self.jobname+"/api/json?tree=builds[*]"
            data=self.url_data_collector(url)
            self.resultjson["build_count"]=len(data["builds"])
            for build in  (data["builds"]):
                if(build["result"]=="SUCCESS"):
                    successful_build=successful_build+1
                elif(build["result"]=="FAILURE"):
                    failed_build=failed_build+1
                else:
                    aborted_build=aborted_build+1
                    
            self.resultjson["build_failed"]=failed_build
            self.resultjson["build_success"]=successful_build
            self.resultjson["build_aborted"]=aborted_build
            
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
    parser.add_argument('--jobname' ,help="apikey",nargs='?', default= None)
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args=parser.parse_args()
	
    jenkins = Jenkins(args)
    resultjson = jenkins.metrics_collector()
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
