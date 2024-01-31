#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}

backend_metrics=["rtime","rtime_max","dresp","eresp","act","bck","chkdown","lastchg","downtime","lbtot","hrsp_5xx","hrsp_4xx","hrsp_3xx","hrsp_2xx","hrsp_1xx","hrsp_other","lastsess","cookie"]
class appname:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        self.username=args.username
        self.password=args.password
        self.url=args.url
        self.svname=args.svname
        

    
    def metriccollector(self):

        try:
            try:
                import requests
                from requests.auth import HTTPBasicAuth 
                import io
                import pandas as pd

            except Exception as e:
                self.maindata['msg']=str(e)
                return self.maindata
            
            try:
                response = requests.get(url = self.url,  auth = (self.username,  self.password))
                if response.status_code== 200:
                     pass
                elif response.status_code == 400:
                    self.maindata['status']=0
                    self.maindata['msg']="HTTP Error 400: Bad Request\nURL: "+self.url
                    return self.maindata
                elif response.status_code==401:
                     self.maindata['status']=0
                     self.maindata['msg']="HTTP Error 401: Unauthorized Access, Incorrect Username or Password"
                     return self.maindata
                elif response.status_code == 403:
                    self.maindata['status']=0
                    self.maindata['msg']="HTTP Error 403: Access Denied for User, Insufficient Privileges\nURL: " + self.url
                    return self.maindata
                elif response.status_code == 404:
                    self.maindata['status']=0
                    self.maindata['msg']="HTTP Error 404: The Requested URL is Not Found\nURL: "+self.url
                    return self.maindata
                elif response.status_code == 500:
                    self.maindata['status']=0
                    self.maindata['msg']="HTTP Error 500: Internal Server Error\nAn Unexpected condition was encountered on the server, and couldn't handle the request. Try again later, and maybe it'll feel better."
                    return self.maindata
                else:
                    self.maindata['status']=0
                    self.maindata['msg']="HTTP Error {}: Oops! Something went wrong".format(response.status_code)
                    return self.maindata


            except requests.exceptions.RequestException as e:
                 self.maindata['msg']=str(e)
                 return self.maindata
            
            res=response.text
            ha_df=pd.read_csv(io.StringIO(res))
            ha_df=ha_df.fillna(-1)          

            back_df=ha_df[ha_df.svname==self.svname][backend_metrics]
            for index, metric in enumerate(backend_metrics):
                 metric_name=metric.replace("_"," ").title()
                 self.maindata[f"{self.svname} "+metric_name]=int(back_df.iloc[0,index])
            
            
            units={
                 f'{self.svname} Rtime':'ms',
                 f'{self.svname} Rtime Max':'ms',
                 f'{self.svname} Lastsess':'ms'

            }
            self.maindata['units']=units


                                
        except Exception as e:
             self.maindata['msg']=str(e)
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
    
    username=None
    password=None
    url="http://localhost:80/stats;csv"
    svname="BACKEND"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--username', help='haproxy password',default=username)
    parser.add_argument('--password', help='haproxy username',default=password)
    parser.add_argument('--url', help='haproxy stats url',default=url)
    parser.add_argument('--svname', help='haproxy backend svname',default=svname)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=appname(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
