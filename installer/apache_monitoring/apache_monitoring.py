#!/usr/bin/python

import sys
import json

'''
Created on 21-Jun-2021
'''

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
    from urllib.request import ProxyHandler
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError
    from httplib import InvalidURL



METRICS = { 'Total Accesses':'total_accesses',
            'Total kBytes':'total_kbytes',
            'CPULoad':'cpu_load',
            'Uptime':'uptime',
            'ReqPerSec':'req_per_sec',
            'BytesPerSec':'bytes_per_sec',
            'BytesPerReq':'bytes_per_req',
            'BusyWorkers':'busy_workers',
            'IdleWorkers':'idle_workers',
            'ServerVersion' : 'version',
            'Load1' : 'load1',
            'Load5' : 'load5',
            'Load15' : 'load15',
            'CPUUser' : 'cpu_user',
            'CPUSystem' : 'cpu_system',
            'ConnsTotal' : 'total_connections',
            'ConnsAsyncWriting' : 'connections_async_writing',
            'ConnsAsyncKeepAlive' : 'connections_async_keep_alive',
            'ConnsAsyncClosing' : 'connections_async_closing',
            'Processes':'Processes'
            
        }

UNITS = {   'total_kbytes':'Bytes',
            'uptime':'Seconds',
            'bytes_per_sec':'Bytes',
            'bytes_per_req':'Bytes',
            'cpu_user':'%',
            'cpu_system':'%',
            'cpu_load':'%'
        }

class ApacheMonitoring(object):
    '''
    Class to monitor Apache webserver
    '''
    def __init__(self, args):
        '''
        Constructor
        '''
        self.url=args.url
        self.username=args.username
        self.password=args.password  
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        
        self.timeout = args.timeout
        
        self.plugin_version=args.plugin_version
        self.heartbeat=args.heartbeat  
        self.data = {}
        
        self._collect_metrics()
        
        self.data['plugin_version'] = self.plugin_version
        self.data['heartbeat_required'] = self.heartbeat
        self.data['units'] = UNITS
        
    
    def _parse_data_(self, _data_):
        try:
            listStatsData = _data_.split('\n')
            for eachStat in listStatsData:
                stats = eachStat.split(':') 
                if str(stats[0]) in METRICS: self.data.setdefault(METRICS[str(stats[0])], str.strip(str(stats[1])))
            
        except TypeError as e:
            self.data['status'] = 0
            self.data['msg'] = 'Error in parsing'
            
        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = 'Exception in parse stats' + str(e)
            
    
    def _collect_metrics(self):
        try:
            auth_handler = None
                            
            if self.username and self.password:
                password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(None, self.url, self.username, self.password)
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)  
            
            if auth_handler is not None :
                opener = urlconnection.build_opener(auth_handler)
                urlconnection.install_opener(opener)
            
            response = urlconnection.urlopen(self.url, timeout=self.timeout)
            #print(self.url)
            
            if response.getcode() == 200:
                response_data = response.read().decode('UTF-8')
                self._parse_data_(response_data)
            else:
                self.data['status'] = 0
                self.data['msg'] = 'Error_code' + str(response.getcode()) 
            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
            else:
                applog["logs_enabled"]=False
            self.data['applog'] = applog
	    
        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = str(e) + ": " + self.url
        return self.data
    
        
if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='apache monitoring url', nargs='?', default="http://localhost:80/server-status?auto")
    parser.add_argument('--username',  help='user name', nargs='?', default= None)
    parser.add_argument('--password', help='password', nargs='?', default= None)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    parser.add_argument('--timeout', help='timeout', nargs='?', type=int, default=30)
    
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    
    
    args = parser.parse_args()
    
    apache = ApacheMonitoring(args)
    data = apache._collect_metrics()
    print(json.dumps(data, indent=4, sort_keys=True))
    
