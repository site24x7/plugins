#!/usr/bin/python3
import json
import requests

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

        self.url=args.nginx_status_url
        self.username=args.username
        self.password=args.password


    def urlGet(self, endpoint, url, auth):

        maindata={}
        try:
            response=requests.get(self.url+endpoint,auth=(self.username,self.password))
            response.raise_for_status()
        
        except requests.exceptions.HTTPError as err:
            maindata['msg']="HTTP error: "+str(err)
            maindata['status']=0
            return maindata

        except requests.exceptions.RequestException as err:
             maindata['msg']="Requests Exception found: "+str(err)
             maindata['status']=0
             return maindata
             
        except Exception as e:
             maindata['msg']=str(e)
             maindata['status']=0
             return maindata

        result=response.json()
        for key, value in result.items():
            maindata[endpoint.split("/")[-1]+"_"+key]=value

        return maindata

    def metricData(self,endpoints, auth, url):
        
        maindata={}
        for endpoint in endpoints:
             interdata=self.urlGet(endpoint, url, auth)
             maindata.update(interdata)
             if "status" in interdata and interdata['status']==0:
                return maindata
        return maindata
                  

    def metriccollector(self):
        try:
             
            auth=(self.username, self.password)
            api_endpoints=['/connections','/ssl','/http/requests']
            interdata=self.metricData(api_endpoints, self.url, auth)
            self.maindata.update(interdata)
            if "ssl_verify_failures" in self.maindata:
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
    
    nginx_status_url='http://localhost:80/api/3'
    username=None
    password=None

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    parser.add_argument('--nginx_status_url', help='nginx api url', nargs='?', default=nginx_status_url)
    parser.add_argument('--username', help='username', nargs='?', default=username)
    parser.add_argument('--password', help='password', nargs='?', default=password)
    args=parser.parse_args()

    obj=nginx(args)
    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
