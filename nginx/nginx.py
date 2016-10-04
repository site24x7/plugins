#!/usr/bin/python

import json

import os

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
NGINX_STATUS_URL = "http://localhost/nginx_status"

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
    
    import requests
    
    import re
    
    from requests.exceptions import ConnectionError

    from urlparse import urljoin
    
    req_headers={}

    req_headers['Accept'] = 'application/text'

    credentials = None
    
    response = None
    
    try:
        
        url = NGINX_STATUS_URL
        response = requests.get(url, auth=credentials, headers=req_headers,timeout=int(30))
        
        if response.status_code == 404:
            data['status']=0
            data['msg']='received status code 404'
            return data

        if response.status_code == 400:
            data['status']=0
            data['msg']='received status code 400'
            return data

    except ConnectionError as e:
            data['status']=0
            data['msg']='Connection Error'
    
    output = response.content
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
    
    return data

if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
