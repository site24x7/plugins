#!/usr/bin/python3

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler


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
        if public_key and private_key:
            password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None,url, public_key ,private_key)
            auth_handler = urlconnection.HTTPDigestAuthHandler(password_mgr)  
            
        if auth_handler is not None :
            opener = urlconnection.build_opener(auth_handler)
            urlconnection.install_opener(opener)
            
        data = urlconnection.urlopen(url).read()
        data=json.loads(data)
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
        import traceback
        traceback.print_exc()
    return resultjson
    
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--group_id',help="group ID of mongodb_altlas_cluster",type=str)
    parser.add_argument('--host',help="host name of mongodb_atlas",type=str)
    parser.add_argument('--port',help="port number of mongodb_atlas",default="27017")
    parser.add_argument('--public_key',help="public key of mongodb_atlas",type=str)
    parser.add_argument('--private_key',help="Private key of mongodb_atlas",type=str)
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
