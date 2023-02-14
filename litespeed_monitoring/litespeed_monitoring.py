#!/usr/bin/python3
import json
import re

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}

metrics= { 'REQ_PROCESSING': 'ReqProcessing', 
           'REQ_PER_SEC':'ReqPerSec', 
           'TOT_REQS':'TotalRequests', 
           'PUB_CACHE_HITS_PER_SEC':'PublicCacheHitsPerSec', 
           'TOTAL_PUB_CACHE_HITS':'TotalPublicCacheHits', 
           'PRIVATE_CACHE_HITS_PER_SEC':'PrivateCacheHitsPerSec', 
           'TOTAL_PRIVATE_CACHE_HITS':'TotalPrivateCacheHits', 
           'STATIC_HITS_PER_SEC':'StaticHitsPerSec', 
           'TOTAL_STATIC_HITS':'TotalStaticHits'}

class ols:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path

        self.virtual_host=args.virtual_host
        self.metric_path=args.metric_path


    
    def metriccollector(self):
        
        try:

            with open(f"{self.metric_path}.rtreport","r") as f:
                data=f.read()

            match=re.findall(rf"\[{self.virtual_host}\].*",data)

            for metric in metrics:
                data=re.findall(f"{metric}: \d",match[0])[0]
                data=re.findall('\d?\d?\d?\d',data)[0]
                self.maindata[metrics[metric]]=data

        except Exception as e: 
            self.maindata['msg']=str(e)
            self.maindata['status']=0



        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["logs_enabled"]=False
        self.maindata['applog'] = applog


        return self.maindata




if __name__=="__main__":
    
    metric_path="/tmp/lshttpd/"
    virtual_host="_AdminVHost"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--metric_path', help='metric path of openlitespeed',default=metric_path)
    parser.add_argument('--virtual_host', help='virtual host of openlitespeed',default=virtual_host)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=ols(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
