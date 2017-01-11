#!/usr/bin/python

import json

import sys

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
RIAK_HOST='127.0.0.1'

RIAK_PORT="8098"

#Riak Status URL
RIAK_STATS_URI="/stats/"

#If any username / password is required to authenticate the stats url kindly mention here.
RIAK_USERNAME=None

RIAK_PASSWORD=None

REALM=None

METRICS_UNITS={'memory_total':'MB','memory_atom':'MB','memory_atom_used':'MB','memory_binary':'MB','memory_code':'MB','memory_ets':'MB',
              'memory_processes':'MB','memory_processes_used':'MB'}

METRICS_TO_BE_PUSHED_TO_SERVER = ["pbc_active","pbc_connects","read_repairs","node_get_fsm_active_60s","node_get_fsm_in_rate","node_get_fsm_out_rate",
                                 "node_get_fsm_rejected_60s","node_gets","node_put_fsm_active_60s","node_put_fsm_in_rate","node_put_fsm_out_rate",
                                 "node_put_fsm_rejected_60s","node_puts","memory_atom","memory_atom_used","memory_binary","memory_code","memory_ets","memory_processes",
                                 "memory_processes_used","memory_total","vnode_gets","vnode_index_deletes",
                                 "vnode_index_reads","vnode_index_writes","vnode_puts"
                                 ]

BYTES_TO_MB_LIST=['memory_total','memory_code','memory_ets','memory_processes','memory_processes_used','memory_atom','memory_atom_used','memory_binary']

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection

def metricCollector():
    data = {}
    
    #defaults
    data['plugin_version'] = PLUGIN_VERSION

    data['heartbeat_required']=HEARTBEAT

    data['units']=METRICS_UNITS
    
    URL = "http://"+RIAK_HOST+":"+RIAK_PORT+"/"+RIAK_STATS_URI
    
    try:
        
        if RIAK_USERNAME and RIAK_PASSWORD:
            password_mgr = urlconnection.HTTPPasswordMgr()
            password_mgr.add_password(REALM, URL, RIAK_USERNAME, RIAK_PASSWORD)
            auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
            opener = urlconnection.build_opener(auth_handler)
            urlconnection.install_opener(opener)

        response = urlconnection.urlopen(URL, timeout=10)
    
        byte_responseData = response.read()
        str_responseData = byte_responseData.decode('UTF-8')

        riak_dict = json.loads(str_responseData)

        for metric in riak_dict:
            if metric in METRICS_TO_BE_PUSHED_TO_SERVER:
                value=riak_dict[metric]
                if metric in BYTES_TO_MB_LIST:
                     value=convertBytesToMB(value)
                data[metric]=value 
    except Exception as e:
            data['status']=0
            data['msg']=str(e)
    
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
