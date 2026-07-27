#!/usr/bin/python

import os
import sys
import re
import json

UNITS = {
    "Avg Request Time": "ms",
    "Avg Upstream Response Time": "ms",
    "Traffic Throughput": "MB",
}

TABS = {
    "HTTP Responses": {
        "order": 1,
        "tablist": [
            "HTTP Status 2xx",
            "HTTP Status 3xx",
            "HTTP Status 4xx",
            "HTTP Status 5xx",
        ]
    },
}

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

            import ssl
            ctx = ssl._create_unverified_context()

            if self._config_data_['username'] and self._config_data_['password']:
                password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(None, url, self._config_data_['username'], self._config_data_['password'])
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                proxy_support = urlconnection.ProxyHandler({})
                opener = urlconnection.build_opener(auth_handler, proxy_support)
                urlconnection.install_opener(opener)

            response = urlconnection.urlopen(url, timeout=self._config_data_['timeout'], context=ctx)
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

        log_path = r"C:\nginx-1.30.4\logs\access.log"
        if os.path.exists(log_path):
            status_2xx = status_3xx = status_4xx = status_5xx = 0
            cache_hit = cache_miss = cache_bypass = cache_expired = 0
            request_times = []
            upstream_times = []
            total_bytes = 0

            # Exact matching patterns for your advanced_text format layout
            STATUS_REGEX = re.compile(r']\s+"[^"\\]*(?:\\.[^"\\]*)*"\s+([1-5]\d{2})')
            BYTES_REGEX = re.compile(r']\s+"[^"\\]*(?:\\.[^"\\]*)*"\s+[1-5]\d{2}\s+(\d+)')
            RT_REGEX = re.compile(r'\brt=([0-9.]+|-)灯?')
            URT_REGEX = re.compile(r'\burt=([0-9., -]+)')
            CS_REGEX = re.compile(r'\bcs=([A-Za-z_-]+|-)')

            with open(log_path, "r", errors="ignore") as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line: continue

                    # 1. Parse Status Codes
                    st_m = STATUS_REGEX.search(clean_line)
                    if st_m:
                        code = st_m.group(1)
                        if code.startswith('2'): status_2xx += 1
                        elif code.startswith('3'): status_3xx += 1
                        elif code.startswith('4'): status_4xx += 1
                        elif code.startswith('5'): status_5xx += 1

                    # 2. Parse Throughput Bandwidth
                    by_m = BYTES_REGEX.search(clean_line)
                    if by_m: total_bytes += int(by_m.group(1))

                    # 3. Parse End-to-End Request Time
                    rt_m = RT_REGEX.search(clean_line)
                    if rt_m and rt_m.group(1) != '-':
                        request_times.append(float(rt_m.group(1)))

                    # 4. Parse Backend Upstream Time
                    urt_m = URT_REGEX.search(clean_line)
                    if urt_m and urt_m.group(1).strip() != '-':
                        for val in urt_m.group(1).replace(" ", "").split(','):
                            try: upstream_times.append(float(val))
                            except ValueError: pass

                    # 5. Parse Cache Status
                    cs_m = CS_REGEX.search(clean_line)
                    if cs_m:
                        state = cs_m.group(1).upper()
                        if 'HIT' in state: cache_hit += 1
                        elif 'MISS' in state: cache_miss += 1
                        elif 'BYPASS' in state: cache_bypass += 1
                        elif 'EXPIRED' in state: cache_expired += 1

            # Populate metrics to JSON structure
            self.data['HTTP Status 2xx'] = status_2xx
            self.data['HTTP Status 3xx'] = status_3xx
            self.data['HTTP Status 4xx'] = status_4xx
            self.data['HTTP Status 5xx'] = status_5xx
            self.data['Traffic Throughput'] = round(total_bytes/(1024*1024),2)
            self.data['Cache Hit Count'] = cache_hit
            self.data['Cache Miss Count'] = cache_miss
            self.data['Cache Bypass Count'] = cache_bypass
            self.data['Cache Expired Count'] = cache_expired
            self.data['Avg Request Time'] = round((sum(request_times)/len(request_times))*1000, 2) if request_times else 0.0
            self.data['Avg Upstream Response Time'] = round((sum(upstream_times)/len(upstream_times))*1000, 2) if upstream_times else 0.0
            self.data['units'] = UNITS
            self.data['tabs']=TABS
        
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
        