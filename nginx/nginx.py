#!/usr/bin/python

import json
import sys
import os
import traceback

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
NGINX_STATUS_URL = "http://localhost/nginx_status"

USERNAME = None

PASSWORD = None

counterFilePath = '/opt/site24x7/monagent/plugins/nginx/counter.json'

TIME_INTERVAL=300

dictCounterValues = None 

def loadCounterValues():
    file_obj = None
    if not os.path.exists(counterFilePath):
        file_obj = open(counterFilePath,'w')
        file_obj.close()
    else:
        file_obj = open(counterFilePath,'r')
        str_counterValues = file_obj.read()
        if str_counterValues:
            dictCounterValues = json.loads(str_counterValues)
            return dictCounterValues
        file_obj.close()

def updateCounterValues(dict_valuesToUpdate):
    if os.path.exists(counterFilePath):
        file_obj = open(counterFilePath,'w')
        file_obj.write(json.dumps(dict_valuesToUpdate))
        file_obj.close()
        
def metricCollector():
    
    dictCounterValues = loadCounterValues()
    
    data = {}
    #defaults

    data['plugin_version'] = PLUGIN_VERSION

    data['heartbeat_required']=HEARTBEAT
    
    import re
    
    PYTHON_MAJOR_VERSION = sys.version_info[0]
    
    if PYTHON_MAJOR_VERSION == 3:
        import urllib
        import urllib.request as urlconnection
        from urllib.error import URLError, HTTPError
        from http.client import InvalidURL
    elif PYTHON_MAJOR_VERSION == 2:
        import urllib2 as urlconnection
        from urllib2 import HTTPError, URLError
        from httplib import InvalidURL

    response = None
    
    try:
        
        url = NGINX_STATUS_URL
        if USERNAME and PASSWORD:
            password_mgr = urlconnection.HTTPPasswordMgr()
            password_mgr.add_password(None, url, USERNAME, PASSWORD)
            auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
            opener = urlconnection.build_opener(auth_handler)
            urlconnection.install_opener(opener)
        response = urlconnection.urlopen(url, timeout=10)
        output = response.read()
        active_con = re.search(r'Active connections:\s+(\d+)', output)
        if active_con:
            connection = int(active_con.group(1))
            data['active_connection']=connection
            
        read_writes = re.search(r'Reading: (\d+)\s+Writing: (\d+)\s+Waiting: (\d+)', output)
        if read_writes:
            reading, writing, waiting = read_writes.groups()
            data['reading']=reading
            data['writing']=writing
            data['waiting']=waiting
        
        conn=0
        handled=0
        requests=0
        updateDict={}    
        per_s_connections = re.search(r'\s*(\d+)\s+(\d+)\s+(\d+)', output)
        if per_s_connections:
            conn = int(per_s_connections.group(1))
            handled = int(per_s_connections.group(2))
            requests = int(per_s_connections.group(3))
        
        if dictCounterValues:
            if 'request_per_s' in dictCounterValues:
                rps = dictCounterValues['request_per_s']
                data['request_per_s'] = (conn - rps)/TIME_INTERVAL
            if 'connection_opened' in dictCounterValues:
                conn_opened = dictCounterValues['connection_opened']
                data['connection_opened'] = (handled - conn_opened)/TIME_INTERVAL
            if 'connection_dropped' in dictCounterValues:
                conn_dropped = dictCounterValues['connection_dropped']
                data['connection_dropped'] = (requests - conn_dropped)/TIME_INTERVAL
        else:
            data['request_per_s']=0
            data['connection_opened']=0
            data['connection_dropped']=0
            
        updateDict['request_per_s']=conn
        updateDict['connection_opened']=handled
        updateDict['connection_dropped']=requests
        
        updateCounterValues(updateDict)
    
    except HTTPError as e:
        data['status'] = 0
        data['msg'] = 'Error_code : HTTP Error ' + str(e.code)
    except URLError as e:
        data['status'] = 0
        data['msg'] = 'Error_code : URL Error ' + str(e.reason)
    except InvalidURL as e:
        data['status'] = 0
        data['msg'] = 'Error_code : Invalid URL'
    except Exception as e:
        data['status']=0
        data['msg']=str(traceback.format_exc())
    
    return data

if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
