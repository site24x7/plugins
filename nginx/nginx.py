#!/usr/bin/python

import sys
import re
import json
import socket
import ipaddress

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

PLUGIN_VERSION = 1
HEARTBEAT_REQUIRED = True

NGINX_ACCESS_LOGS_LOG_TYPE_NAME = "Nginx Logs"
NGINX_ERROR_LOGS_LOG_TYPE_NAME = "Nginx Error Logs"


def resolve_ip_address(host):
    if not host:
        return host
    if host == "localhost":
        return "localhost"
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    try:
        return socket.gethostbyname(host)
    except Exception:
        return host

class NginxServerMonitoring():
    def __init__(self, config_data) :
        self.data = {}
        self._config_data_ = config_data
        self.data['plugin_version'] = PLUGIN_VERSION
        self.data['heartbeat_required'] = HEARTBEAT_REQUIRED
        self.data['applog']=self._config_data_['applog']
    
    def _get_request_data_(self):
        PYTHON_MAJOR_VERSION = sys.version_info[0]    
        if PYTHON_MAJOR_VERSION == 3:
            import urllib.request as urlconnection
        elif PYTHON_MAJOR_VERSION == 2:
            import urllib2 as urlconnection
            
        try:
            url = self._config_data_['url']

            if self._config_data_['username'] and self._config_data_['password']:
                password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(None, url, self._config_data_['username'], self._config_data_['password'])
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                proxy_support = urlconnection.ProxyHandler({})
                opener = urlconnection.build_opener(auth_handler, proxy_support)
                urlconnection.install_opener(opener)

            response = urlconnection.urlopen(url)
            return response.read()
        except Exception as e:
            self.data['status'] = 0
            #self.data['msg'] = str(e.code) + " " + str(e.reason)
            self.data['msg'] = str(e)
                

                
    def _collect_metrics_(self):
        output = self._get_request_data_()
        if output == None : return self.data
        
        output = output.decode('utf-8')
        active_con = re.search(r'Active connections:\s+(\d+)', output)
        read_writes = re.search(r'Reading: (\d+)\s+Writing: (\d+)\s+Waiting: (\d+)', output)
        per_s_connections = re.search(r'\s*(\d+)\s+(\d+)\s+(\d+)', output)
        
        if not active_con and not read_writes and not per_s_connections:
            self.data['status'] = 0
            self.data['msg'] = "Invalid nginx status URL - no status data found"
            return self.data
        
        if active_con: self. data['Currently active client connections'] = int(active_con.group(1)) # current active client connections including Waiting connections.        
        if read_writes:
            reading, writing, waiting = read_writes.groups()
            self.data['Number of connections where nginx is reading the request header']=reading # The current number of connections where nginx is reading the request header.
            self.data['Number of connections where nginx is writing the response back to the client']=writing # The current number of connections where nginx is writing the response back to the client.
            self.data['Number of idle client connections waiting for a request']=waiting # The current number of idle client connections waiting for a request.
            
        if per_s_connections:
            conn = int(per_s_connections.group(1)) # The total number of accepted client connections.
            handled = int(per_s_connections.group(2)) # The total number of handled connections. Generally, same as accepts unless some resource limits have been reached (for example, the worker_connections limit).
            requests = int(per_s_connections.group(3)) # The total number of client requests.

            self.data['Count of client requests'] = requests
            self.data['Count of successful client connections']= handled
            self.data['Count of dropped connections '] = (conn - handled)
        
        host = urlparse(self._config_data_['url']).hostname
        self.data['s247config'] = {
            "ip_address": resolve_ip_address(host)
        }
        
        return self.data


def _load_args_():
    _config_data_ = {}
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--nginx_status_url', help="nginx_status_url",type=str,default="http://localhost/nginx_status")
    parser.add_argument('--username', help='username', type=str, default=None)
    parser.add_argument('--password', help='password', type=str, default=None)
    
    parser.add_argument('--nginx_access_logs_enabled', help='enable log collection for Nginx access logs',default="False")
    parser.add_argument('--nginx_access_logs_file_path', help='list of comma separated log file paths', nargs='?', default="/var/log/nginx*/access*.log")
    parser.add_argument('--nginx_error_logs_enabled', help='enable log collection for Nginx error logs',default="False")
    parser.add_argument('--nginx_error_logs_file_path', help='list of comma separated log file paths', nargs='?', default="/var/log/nginx*/error*.log")

    args = parser.parse_args()
    
    _config_data_['url'] = args.nginx_status_url
    _config_data_['username'] = args.username
    _config_data_['password'] = args.password
    
    applog=[]

    access_log_entry = {}
    if(args.nginx_access_logs_enabled in ['True', 'true', '1']):
        access_log_entry["logs_enabled"]=True
        access_log_entry["log_type_name"]=NGINX_ACCESS_LOGS_LOG_TYPE_NAME
        access_log_entry["log_file_path"]=args.nginx_access_logs_file_path
    else:
        access_log_entry["logs_enabled"]=False
    applog.append(access_log_entry)

    error_log_entry = {}
    if(args.nginx_error_logs_enabled in ['True', 'true', '1']):
        error_log_entry["logs_enabled"]=True
        error_log_entry["log_type_name"]=NGINX_ERROR_LOGS_LOG_TYPE_NAME
        error_log_entry["log_file_path"]=args.nginx_error_logs_file_path
    else:
        error_log_entry["logs_enabled"]=False
    applog.append(error_log_entry)

    _config_data_['applog'] = applog

    
    return _config_data_
    
if __name__ == '__main__':
    _config_data_ =  _load_args_()
    nginx = NginxServerMonitoring(_config_data_)
    result = nginx._collect_metrics_()
    print(json.dumps(result, indent=4, sort_keys=True))
        
