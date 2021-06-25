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
    "network.in":"bytes/second",
    "network.out":"bytes/second",
    "network.request":"count/second",
    "opcounter.cmd":"count/second",
    "opcounter.query":"count/second",
    "opcounter.update":"count/second",
    "opcounter.delete":"count/second",
    "opcounter.getmore":"count/second",
    "opcounter.insert":"count/second",
    "logicalsize":"bytes"
}


group_id= ""
host= ""
port= ""
public_key = ""
private_key = ""


def metrics_collector():
    resultjson={}
    try:
        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+group_id+"/processes/"+host+":"+port+"/measurements?granularity=PT5M&period=PT5M&pretty=true" 
        data=json.loads((requests.get(url, auth=HTTPDigestAuth(public_key, private_key)).content))
        new_data = {}
        new_data["groupid"]=data["groupId"]
        new_data["hostid"]=data["hostId"]
        new_data["start"]=data["start"]
        new_data["end"]=data["end"]
        new_data["connections"] = data["measurements"][0]["dataPoints"][0]["value"]
        new_data["network.in"]=data["measurements"][1]["dataPoints"][0]["value"]
        new_data["network.out"]=data["measurements"][2]["dataPoints"][0]["value"]
        new_data["network.request"]=data["measurements"][3]["dataPoints"][0]["value"]
        new_data["opcounter.cmd"]=data["measurements"][4]["dataPoints"][0]["value"]
        new_data["opcounter.query"]=data["measurements"][5]["dataPoints"][0]["value"]
        new_data["opcounter.update"]=data["measurements"][6]["dataPoints"][0]["value"]
        new_data["opcounter.delete"]=data["measurements"][7]["dataPoints"][0]["value"]
        new_data["opcounter.getmore"]=data["measurements"][8]["dataPoints"][0]["value"]
        new_data["opcounter.insert"]=data["measurements"][9]["dataPoints"][0]["value"]
        new_data["logicalsize"]=data["measurements"][10]["dataPoints"][0]["value"]
        

        
        return new_data

        
    
        
        
    except Exception as e:
        resultjson["msg"]=str(e)
        resultjson["status"]=0
    return resultjson




if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--group_id',help="group ID of mongodb_measurement_of_processes",type=str)
    parser.add_argument('--host',help="host name for mongodb_measurement_of_processes",type=str)
    parser.add_argument('--port',help="port name for mongodb_measurement_of_processes",type=str)
    parser.add_argument('--public_key',help="public key of mongodb_measurement_of_processes",type=str)
    parser.add_argument('--private_key',help="Private key for mongodb_measurement_of_processes",type=str)
    args=parser.parse_args()
	
    if args.group_id:
        group_id=args.group_id
    if args.host:
        host=args.host
    if args.port:
        port=args.port
    if args.public_key:
        public_key=args.public_key
    if args.private_key:
        private_key=args.private_key    
    resultjson=metrics_collector() 
    resultjson['plugin_version'] = plugin_version
    resultjson['heartbeat_required'] = heartbeat_required
    resultjson['units'] = metric_units
print(json.dumps(resultjson, indent=4, sort_keys=True))
