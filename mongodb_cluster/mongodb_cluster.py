#!/usr/bin/python3

import sys
import json
import requests
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
    "disksize":"GB"
}


public_key = ""
private_key = ""
group_id= ""


def metrics_collector():
    resultjson={}
    try:
        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+group_id+"/clusters/Cluster0?pretty=true" 
        data=json.loads((requests.get(url, auth=HTTPDigestAuth(public_key, private_key)).content))
        
        new_data = {}
        new_data["clustertype"]=data["clusterType"]
        new_data["disksize"]=data["diskSizeGB"]
        new_data["mongodb.majorversion"]=data["mongoDBMajorVersion"]
        new_data["mongodb.version"]=data["mongoDBVersion"]
        new_data["mongo.uri.updated"]=data["mongoURIUpdated"]
        new_data["name"]=data["name"]
        new_data["numshards"]=data["numShards"]
        new_data["pitenabled"]=data["pitEnabled"]
        new_data["provider.backup.enabled"]=data["providerBackupEnabled"]
        new_data["providername"]=data["providerSettings"]["providerName"]
        new_data["maxinstance.size"]=data["providerSettings"]["autoScaling"]["compute"]["maxInstanceSize"]
        new_data["mininstance.size"]=data["providerSettings"]["autoScaling"]["compute"]["minInstanceSize"]
        new_data["replication.factor"]=data["replicationFactor"]
        new_data["analytics.nodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["analyticsNodes"]
        new_data["electable.nodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["electableNodes"]
        new_data["priority"]=data["replicationSpec"]["ASIA_SOUTH_1"]["priority"]
        new_data["readonly.nodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["readOnlyNodes"]
        new_data["zonename"]=data["replicationSpecs"][0]["zoneName"]
        new_data["rootcert.type"]=data["rootCertType"]
        new_data["srvaddress"]=data["srvAddress"]
        new_data["statename"]=data["stateName"]
       
        return new_data

        
        
    
        
        
    except Exception as e:
        resultjson["msg"]=str(e)
        resultjson["status"]=0
    return resultjson




if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--group_id',help="group ID for mongodb_cluster",type=str)
    parser.add_argument('--public_key',help="public key of mongodb_cluster",type=str)
    parser.add_argument('--private_key',help="Private key for mongodb_cluster",type=str)
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
