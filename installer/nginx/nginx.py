#!/usr/bin/python

import sys
import re
import json

class NginxServerMonitoring():
    def __init__(self, config_data) :
        self.data = {}
        self._config_data_ = config_data
        self.data['plugin_version'] = self._config_data_['plugin_version']
        self.data['heartbeat_required'] = self._config_data_['heartbeat_required']
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

            response = urlconnection.urlopen(url, timeout=self._config_data_['timeout'])
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
        
        return self.data


def _load_args_():
    _config_data_ = {}
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--nginx_status_url', help="nginx_status_url",type=str,default="http://localhost/nginx_status")
    parser.add_argument('--username', help='username', type=str, default=None)
    parser.add_argument('--password', help='password', type=str, default=None)
    
    parser.add_argument('--timeout', help ="timeout",type=int,default=60)
    
    parser.add_argument('--plugin_version', help='plugin_version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='is heartbeat enabled', type=bool, nargs='?', default=True)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)

    args = parser.parse_args()
    
    _config_data_['url'] = args.nginx_status_url
    _config_data_['username'] = args.username
    _config_data_['password'] = args.password
    _config_data_['timeout'] = args.timeout
    _config_data_['plugin_version'] = args.plugin_version
    _config_data_['heartbeat_required'] = args.heartbeat
    
    logsenabled=args.logs_enabled
    logtypename=args.log_type_name
    logfilepath=args.log_file_path
    
    
    applog={}
    if(logsenabled in ['True', 'true', '1']):
        applog["logs_enabled"]=True
        applog["log_type_name"]=logtypename
        applog["log_file_path"]=logfilepath
    else:
        applog["logs_enabled"]=False
    _config_data_['applog'] = applog

    
    return _config_data_
    
if __name__ == '__main__':
    _config_data_ =  _load_args_()
    nginx = NginxServerMonitoring(_config_data_)
    result = nginx._collect_metrics_()
    print(json.dumps(result, indent=4, sort_keys=True))
        
