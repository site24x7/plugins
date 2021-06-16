#!/usr/bin/python3

import sys
import time
import json
import requests
import subprocess
import os
import argparse
from requests.auth import HTTPDigestAuth


PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector

plugin_version = 1

heartbeat_required = "true"

resultjson={}

metric_units={
    "diskSize":"GB"
}


public_key = "jifqsfrc"
private_key = "80d11231-0482-4387-8107-ea0336380452"
group_id="6080fc32b449622900b6612e"


def metrics_collector():
    resultjson={}
    try:
        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+group_id+"/clusters/Cluster0?pretty=true" 
        data=json.loads((requests.get(url, auth=HTTPDigestAuth(public_key, private_key)).content))
        
        new_data = {}
        new_data["clusterType"]=data["clusterType"]
        new_data["diskSize"]=data["diskSizeGB"]
        new_data["mongoDBMajorVersion"]=data["mongoDBMajorVersion"]
        new_data["mongoDBVersion"]=data["mongoDBVersion"]
        new_data["mongoURIUpdated"]=data["mongoURIUpdated"]
        new_data["name"]=data["name"]
        new_data["numShards"]=data["numShards"]
        new_data["pitEnabled"]=data["pitEnabled"]
        new_data["providerBackupEnabled"]=data["providerBackupEnabled"]
        new_data["providerName"]=data["providerSettings"]["providerName"]
        new_data["maxInstanceSize"]=data["providerSettings"]["autoScaling"]["compute"]["maxInstanceSize"]
        new_data["minInstanceSize"]=data["providerSettings"]["autoScaling"]["compute"]["minInstanceSize"]
        new_data["replicationFactor"]=data["replicationFactor"]
        new_data["analyticsNodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["analyticsNodes"]
        new_data["electableNodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["electableNodes"]
        new_data["priority"]=data["replicationSpec"]["ASIA_SOUTH_1"]["priority"]
        new_data["readOnlyNodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["readOnlyNodes"]
        new_data["zoneName"]=data["replicationSpecs"][0]["zoneName"]
        new_data["rootCertType"]=data["rootCertType"]
        new_data["srvAddress"]=data["srvAddress"]
        new_data["stateName"]=data["stateName"]
       
        return new_data

        
        
    
        
        
    except Exception as e:
        resultjson["msg"]=str(e)
        resultjson["status"]=0
    return resultjson




if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--group_id',help="group ID for mongodb_org_event",type=str)
    parser.add_argument('--public_key',help="public key of mongodb_org_event",type=str)
    parser.add_argument('--private_key',help="Private key for mongodb_org_event",type=str)
    args=parser.parse_args()
	

    if args.group_id:
        group_id=args.group_id
    if args.public_key:
        public_key=args.public_key
    if args.private_key:
        private_key=args.private_key
        
    resultjson=metrics_collector() 
    resultjson['plugin_version'] = plugin_version
    resultjson['heartbeat_required'] = heartbeat_required
    resultjson['units'] = metric_units
print(json.dumps(resultjson, indent=4, sort_keys=True))
