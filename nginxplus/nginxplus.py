#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class nginx:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path

        self.domain_name=args.domain_name
        self.username=args.username
        self.password=args.password


    
    
    def metriccollector(self):
        
        api_endpoints=['/connections','/ssl','/http/requests']
        try:
             
            try:
                import requests

            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0
                return self.maindata

            url="http://"+self.domain_name+"/api/3"

            for api_endpoint in api_endpoints:

                response=requests.get(url+api_endpoint,auth=(self.username,self.password))
                result=response.json()
                for key, value in result.items():
                    self.maindata[api_endpoint.split("/")[-1]+"_"+key]=value
            
            del self.maindata['ssl_verify_failures']
                

        except Exception as e:
             self.maindata['msg']=str(e)
             self.maindata['status']=0
             return self.maindata
             
        
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
    
    domain_name='localhost:80'
    username=None
    password=None
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    parser.add_argument('--domain_name', help='name of the nginx domain', nargs='?', default=domain_name)
    parser.add_argument('--username', help='username', nargs='?', default=username)
    parser.add_argument('--password', help='password', nargs='?', default=password)
    args=parser.parse_args()

    obj=nginx(args)
    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
