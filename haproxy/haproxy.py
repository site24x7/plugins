#!/usr/bin/python3
import json
import csv

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={ 'Frontend Qtime':'ms',
                'Frontend Ctime':'ms',
                'Frontend Bin':'bytes',
                'Frontend Bout':'bytes',
                'Sys Ttime Max':'ms',
                'Sys Check Duration':'ms',
                'BACKEND Rtime': 'ms',
                'BACKEND Rtime Max': 'ms',
                'BACKEND Lastsess': 'ms'}

sys_metrics=["ttime_max","agent_status","cache_lookups","cache_hits","chkfail","hanafail","throttle","check_status","check_duration","cli_abrt","srv_abrt","comp_in","comp_out","comp_byp","comp_rsp","algo","eint","reuse","wrew","mode"]
frontend_metrics=["qcur","qmax","qtime","ctime","scur","smax","bin","bout","dses","dreq","dcon","ereq","econ","wretr","wredis","rate","rate_max","req_rate","req_rate_max","connect","conn_rate","conn_rate_max","conn_tot","srv_icur","qtime_max","ctime_max","idle_conn_cur","safe_conn_cur","used_conn_cur","need_conn_est"]
backend_metrics=["rtime","rtime_max","dresp","eresp","act","bck","chkdown","lastchg","downtime","lbtot","hrsp_5xx","hrsp_4xx","hrsp_3xx","hrsp_2xx","hrsp_1xx","hrsp_other","lastsess","cookie"]

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
            except Exception as e:
                self.maindata['status'] = 0
                self.maindata['msg'] = str(e)
                return self.maindata

            try:
                response = requests.get(url=self.url, auth=HTTPBasicAuth(self.username, self.password))
            except Exception as e:
                self.maindata['status'] = 0
                self.maindata['msg'] = str(e)
                return self.maindata

            if response.status_code == 200:
                res = response.text
            elif response.status_code == 400:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error 400: Bad Request.\nURL: " + self.url
                return self.maindata
            elif response.status_code == 401:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error 401: Unauthorized Access, Incorrect Username or Password"
                return self.maindata
            elif response.status_code == 403:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error 403: Access Denied for User, Insufficient Privileges.\nURL: " + self.url
                return self.maindata
            elif response.status_code == 404:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error 404: The Requested URL is Not Found.\nURL: " + self.url
                return self.maindata
            elif response.status_code == 500:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error 500: Internal Server Error.\nAn Unexpected condition was encountered on the server, and couldn't handle the request. Try again later, and maybe it'll feel better."
                return self.maindata
            elif response.status_code == 503:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error 503: Service Unavailable. Please try again later."
                return self.maindata
            else:
                self.maindata['status'] = 0
                self.maindata['msg'] = "HTTP Error {}: Something went wrong".format(response.status_code)
                return self.maindata

            ha_rows = list(csv.DictReader(io.StringIO(res)))
            
            for row in ha_rows:
                for key in sys_metrics + frontend_metrics + backend_metrics:
                    if key not in row:
                        row[key] = -1

            sys_rows = [row for row in ha_rows if row.get('svname') == "FRONTEND"]
            if sys_rows:
                sys_row = sys_rows[0]
                for metric in sys_metrics:
                    metric_name = metric.replace("_", " ").title()
                    value = sys_row.get(metric, -1)
                    if value == "" or value is None:
                        value = -1
                    
                    if metric == "mode":
                        self.maindata["Sys " + metric_name] = value
                    else:
                        try:
                            self.maindata["Sys " + metric_name] = float(value)
                        except (ValueError, TypeError):
                            self.maindata["Sys " + metric_name] = -1

            front_rows = [row for row in ha_rows if row.get('svname') == "FRONTEND"]
            if front_rows:
                front_row = front_rows[0]
                for metric in frontend_metrics:
                    metric_name = metric.replace("_", " ").title()
                    value = front_row.get(metric, -1)
                    if value == "" or value is None:
                        value = -1
                    try:
                        self.maindata["Frontend " + metric_name] = float(value)
                    except (ValueError, TypeError):
                        self.maindata["Frontend " + metric_name] = -1

            back_rows = [row for row in ha_rows if row.get('svname') == "BACKEND"]
            if back_rows:
                back_row = back_rows[0]
                for metric in backend_metrics:
                    metric_name = metric.replace("_", " ").title()
                    value = back_row.get(metric, -1)
                    if value == "" or value is None:
                        value = -1
                    
                    if metric == "cookie":
                        self.maindata["BACKEND " + metric_name] = value
                    else:
                        try:
                            self.maindata["BACKEND " + metric_name] = int(value)
                        except (ValueError, TypeError):
                            self.maindata["BACKEND " + metric_name] = -1

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

        tabs = {
            "Frontend":{
                "order": 1,
                "tablist": [
                    "Frontend Qcur", "Frontend Qmax", "Frontend Qtime", "Frontend Ctime", 
                    "Frontend Scur", "Frontend Smax", "Frontend Bin", "Frontend Bout", 
                    "Frontend Dses", "Frontend Dreq", "Frontend Dcon", "Frontend Ereq", 
                    "Frontend Econ", "Frontend Wretr", "Frontend Wredis", "Frontend Rate", 
                    "Frontend Rate Max", "Frontend Req Rate", "Frontend Req Rate Max", 
                    "Frontend Connect", "Frontend Conn Rate", "Frontend Conn Rate Max", 
                    "Frontend Conn Tot", "Frontend Srv Icur", "Frontend Qtime Max", 
                    "Frontend Ctime Max", "Frontend Idle Conn Cur", "Frontend Safe Conn Cur", 
                    "Frontend Used Conn Cur", "Frontend Need Conn Est"
                ]
            },
            "Backend":{
                "order": 2,
                "tablist": [
                    "BACKEND Rtime", "BACKEND Rtime Max", "BACKEND Dresp", "BACKEND Eresp", 
                    "BACKEND Act", "BACKEND Bck", "BACKEND Chkdown", "BACKEND Lastchg", 
                    "BACKEND Downtime", "BACKEND Lbtot", "BACKEND Hrsp 5Xx", "BACKEND Hrsp 4Xx", 
                    "BACKEND Hrsp 3Xx", "BACKEND Hrsp 2Xx", "BACKEND Hrsp 1Xx", "BACKEND Hrsp Other", 
                    "BACKEND Lastsess", "BACKEND Cookie"
                ]
            }
        }
        self.maindata['tabs'] = tabs

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
    username="None"
    password="None"
    url="http://localhost:8080/stats;csv"
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