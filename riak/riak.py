#!/usr/bin/python

import json

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
RIAK_HOST='127.0.0.1'

RIAK_PORT="8098"

RIAK_STATS_URI="/stats/"

RIAK_USERNAME=None

RIAK_PASSWORD=None

METRICS_UNITS={'memory_total':'MB','memory_atom':'MB','memory_atom_used':'MB','memory_binary':'MB','memory_code':'MB','memory_ets':'MB',
              'memory_processes':'MB','memory_processes_used':'MB'}

METRICS_TO_BE_PUSHED_TO_SERVER = ["pbc_active","pbc_connects","read_repairs","node_get_fsm_active_60s","node_get_fsm_in_rate","node_get_fsm_out_rate",
                                 "node_get_fsm_rejected_60s","node_gets","node_put_fsm_active_60s","node_put_fsm_in_rate","node_put_fsm_out_rate",
                                 "node_put_fsm_rejected_60s","node_puts","memory_atom","memory_atom_used","memory_binary","memory_code","memory_ets","memory_processes",
                                 "memory_processes_used","memory_total","vnode_gets","vnode_index_deletes",
                                 "vnode_index_reads","vnode_index_writes","vnode_puts"
                                 ]

BYTES_TO_MB_LIST=['memory_total','memory_code','memory_ets','memory_processes','memory_processes_used','memory_atom','memory_atom_used','memory_binary']



def metricCollector():
    data = {}
    #defaults

    data['plugin_version'] = PLUGIN_VERSION

    data['heartbeat_required']=HEARTBEAT

    data['units']=METRICS_UNITS
    
    import requests
    
    from requests.exceptions import ConnectionError

    from urlparse import urljoin
    
    server = "http://"+RIAK_HOST+":"+RIAK_PORT+"/"
    
    url = urljoin(server, RIAK_STATS_URI)
    
    credentials = None
    
    if RIAK_USERNAME and RIAK_PASSWORD:
        credentials = (RIAK_USERNAME,RIAK_PASSWORD)

    req_headers={}

    req_headers['Accept'] = 'application/json'

    try:
        response = requests.get(url, auth=credentials, headers=req_headers,timeout=int(30))
        
        if response.status_code == 404:
            data['status']=0
            data['msg']='received status code 404'
            return data

        if response.status_code == 400:
            data['status']=0
            data['msg']='received status code 400'
            return data

        riak_dict = response.json()

        for metric in riak_dict:
            if metric in METRICS_TO_BE_PUSHED_TO_SERVER:
                value=riak_dict[metric]
                if metric in BYTES_TO_MB_LIST:
                     value=convertBytesToMB(value)
                data[metric]=value 
    except ConnectionError as e:
            data['status']=0
            data['msg']='Connection Error'  
    
    return data

def convertBytesToMB(v):
    try:
        byte_s=float(v)
        kilobytes=byte_s/1024;
        megabytes=kilobytes/1024;
        v=round(megabytes,2)
    except Exception as e:
        pass
    return v  

if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))