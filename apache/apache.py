#!/usr/bin/python

import sys
import json
import socket

'''
Created on 21-Jun-2021
'''
PLUGIN_VERSION = 1

HEARTBEAT = True

TIMEOUT = 30

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
    from urllib.request import ProxyHandler
    from urllib.parse import urlparse
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError
    from httplib import InvalidURL
    from urlparse import urlparse

try:
    import ipaddress
except ImportError:
    ipaddress = None


def resolve_ip_address(host):
    if not host:
        return host
    if host == "localhost":
        return "localhost"
    if ipaddress is not None:
        try:
            ipaddress.ip_address(str(host))
            return host
        except ValueError:
            pass
    else:
        try:
            socket.inet_aton(host)
            return host
        except socket.error:
            pass
    try:
        return socket.gethostbyname(host)
    except Exception:
        return host



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

APACHE_ACCESS_LOGS_LOG_TYPE_NAME = 'Apache Access Logs'

class ApacheMonitoring(object):
    '''
    Class to monitor Apache webserver
    '''
    def __init__(self, args):
        '''
        Constructor
        '''

        self.url = args.url.strip()

        if not self.url.endswith('?auto'):
            if self.url.endswith('/'):
                self.url = self.url[:-1]
            self.url += '?auto'
        
        self.username=args.username
        self.password=args.password  
        self.logsenabled=args.apache_access_logs_enabled
        self.logfilepath=args.apache_access_logs_file_path
        
        self.timeout = TIMEOUT
        
        self.plugin_version=PLUGIN_VERSION
        self.heartbeat=HEARTBEAT  
        self.data = {}
        
        self._collect_metrics()
        
        self.data['plugin_version'] = self.plugin_version
        self.data['heartbeat_required'] = self.heartbeat
        self.data['units'] = UNITS
        
    
    def _parse_data_(self, _data_):
        try:
            metrics_found = 0
            listStatsData = _data_.split('\n')
            for eachStat in listStatsData:
                stats = eachStat.split(':') 
                if str(stats[0]) in METRICS: 
                    self.data.setdefault(METRICS[str(stats[0])], str.strip(str(stats[1])))
                    metrics_found += 1
            
            if metrics_found == 0:
                self.data['status'] = 0
                self.data['msg'] = 'No Apache server status metrics found.'
            
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
                applog["log_type_name"]=APACHE_ACCESS_LOGS_LOG_TYPE_NAME
                applog["log_file_path"]=self.logfilepath
            else:
                applog["logs_enabled"]=False
            self.data['applog'] = applog

            host = urlparse(self.url).hostname
            self.data['s247config'] = {
                "ip_address": resolve_ip_address(host)
            }
	    
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
    parser.add_argument('--apache_access_logs_enabled', help='enable log collection for Apache access logs',default="False")
    parser.add_argument('--apache_access_logs_file_path', help='list of comma separated log file paths', nargs='?', default="/etc/httpd/logs/access_log*,/var/log/httpd/access_log*,/var/log/apache/access.log*,/var/log/apache2/access.log*")
    
    
    args = parser.parse_args()
    
    apache = ApacheMonitoring(args)
    data = apache._collect_metrics()
    print(json.dumps(data, indent=4, sort_keys=True))
