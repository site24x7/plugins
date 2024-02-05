#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={ 'Frontend Qtime':'ms', 
                'Frontend Ctime':'ms', 
                'Frontend Bin':'bytes', 
                'Frontend Bout':'bytes', 
                'Sys Ttime Max':'ms',
                'Sys Check Duration':'ms'}



sys_metrics=["ttime_max","agent_status","cache_lookups","cache_hits","chkfail","hanafail","throttle","check_status","check_duration","cli_abrt","srv_abrt","comp_in","comp_out","comp_byp","comp_rsp","algo","eint","reuse","wrew","mode"]
frontend_metrics=["qcur","qmax","qtime","ctime","scur","smax","bin","bout","dses","dreq","dcon","ereq","econ","wretr","wredis","rate","rate_max","req_rate","req_rate_max","connect","conn_rate","conn_rate_max","conn_tot","srv_icur","qtime_max","ctime_max","idle_conn_cur","safe_conn_cur","used_conn_cur","need_conn_est"]

class haproxy:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        self.username=args.username
        self.password=args.password
        self.url=args.url
        

    
    def metriccollector(self):

        try:
            try:
                import requests
                from requests.auth import HTTPBasicAuth 
                import io
                import pandas as pd

            except Exception as e:
                self.maindata['status']=0
                self.maindata['msg']=str(e)
                return self.maindata
            
            try:
                response = requests.get(url = self.url,  auth = HTTPBasicAuth(self.username,  self.password))
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
                 self.maindata['status']=0
                 self.maindata['msg']=str(e)
                 return self.maindata
            res=response.text
            ha_df=pd.read_csv(io.StringIO(res))
            list_ha_df=list(ha_df)
            [list_ha_df.append(col) for col in sys_metrics if col not in list_ha_df]
            [list_ha_df.append(col) for col in frontend_metrics if col not in list_ha_df]
            ha_df=ha_df.reindex(list_ha_df,axis=1)
            ha_df=ha_df.fillna(-1)




            # sys metrics
            sys_df=ha_df[ha_df['svname']=="FRONTEND"][sys_metrics]
            sys_numeric_df=sys_df[sys_metrics[:-1]]

            for index, metric in enumerate(sys_metrics):
                 metric_name=metric.replace("_"," ").title()
                 self.maindata["Sys "+metric_name]=float(sys_numeric_df.iloc[0,index])
                 if index==len(sys_metrics)-2:
                      break
            self.maindata["Sys "+sys_metrics[-1]]=sys_df.iloc[0,len(sys_metrics)-1]

            # frontend metrics
            front_df=ha_df[ha_df['svname']=="FRONTEND"][frontend_metrics]
            for index, metric in enumerate(frontend_metrics):
                 metric_name=metric.replace("_"," ").title()
                 self.maindata["Frontend "+metric_name]=float(front_df.iloc[0,index])

                      
        except Exception as e:
             self.maindata['status']=0
             self.maindata['msg']=str(e)
             return self.maindata
        
        if "http://" in self.url:
             hostname=self.url.replace("http://","")
        if "https://" in self.url:
             hostname=self.url.replace("https://","")
        hostname=hostname.split("/")
        hostname=hostname[0].split(":")
        self.maindata['tags']=f"HAPROXY_HOST:{hostname[0]}"
            
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

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--username', help='haproxy password',default=username)
    parser.add_argument('--password', help='haproxy username',default=password)
    parser.add_argument('--url', help='haproxy url',default=url)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=haproxy(args)
    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
