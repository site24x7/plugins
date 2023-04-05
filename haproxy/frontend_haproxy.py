#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={ 'frontend_qtime':'ms', 
                'frontend_ctime':'ms', 
                'frontend_bin':'bytes', 
                'frontend_bout':'bytes', 
                'sys_stime':'ms', 
                'sys_ttime_max':'ms',
                'sys_check_duration':'ms'}



sys_metrics=["ttime_max","agent_status","cache_lookups","cache_hits","chkfail","hanafail","throttle","check_status","check_duration","cli_abrt","srv_abrt","comp_in","comp_out","comp_byp","comp_rsp","algo","eint","reuse","wrew","mode"]
frontend_metrics=["qcur","qmax","qtime","ctime","scur","smax","bin","bout","dses","dreq","dcon","ereq","econ","wretr","wredis","rate","rate_max","req_rate","req_rate_max","connect","conn_rate","conn_rate_max","conn_tot","srv_icur","qtime_max","ctime_max","idle_conn_cur","safe_conn_cur","used_conn_cur","need_conn_est"]

class appname:

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
        self.hostname=args.hostname
        self.url=f"http://{args.hostname}:{args.port}/stats;csv"
        

    
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
                response = requests.get(url = self.url,  auth = HTTPBasicAuth(self.username,  self.password))
                if response.status_code==401:
                     self.maindata['msg']="Authentication failed: Invalid credentials"
                     return self.maindata
                elif response.status_code == 403:
                    self.maindata['msg']='Authentication failed: Access denied'
                    return self.maindata

            except requests.exceptions.RequestException as e:
                 self.maindata['msg']=str(e)
                 return self.maindata
            res=response.text
            ha_df=pd.read_csv(io.StringIO(res))
            ha_df=ha_df.fillna(-1)




            # sys metrics
            sys_df=ha_df[ha_df['svname']=="FRONTEND"][sys_metrics]
            sys_numeric_df=sys_df[sys_metrics[:-1]]

            for index, metric in enumerate(sys_metrics):
                 self.maindata["sys_"+metric]=float(sys_numeric_df.iloc[0,index])
                 if index==len(sys_metrics)-2:
                      break
            self.maindata["sys_"+sys_metrics[-1]]=sys_df.iloc[0,len(sys_metrics)-1]

            # frontend metrics
            front_df=ha_df[ha_df['svname']=="FRONTEND"][frontend_metrics]
            for index, metric in enumerate(frontend_metrics):
                 self.maindata["frontend_"+metric]=float(front_df.iloc[0,index])

                      
        except Exception as e:
             self.maindata['msg']=str(e)
             return self.maindata

        self.maindata['tags']=f"HAPROXY_HOST:{self.hostname}"
            
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
    hostname="localhost"
    port=80

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--username', help='haproxy password',default=username)
    parser.add_argument('--password', help='haproxy username',default=password)
    parser.add_argument('--hostname', help='haproxy url hostname',default=hostname)
    parser.add_argument('--port', help='haproxy url port',default=port)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=appname(args)
    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
