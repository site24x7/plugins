#!/usr/bin/python

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler


plugin_version = 1

heartbeat_required = "true"

resultjson={}

metrics_units={
    "disksize":"GB"
}


public_key = ""
private_key = ""
group_id= ""


def metrics_collector():
    resultjson={}
    try:
        url = "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+group_id+"/clusters/Cluster0?pretty=true" 
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
        new_data["clustertype"]=data["clusterType"]
        new_data["disksize"]=data["diskSizeGB"]
        new_data["mongodb_majorversion"]=data["mongoDBMajorVersion"]
        new_data["mongodb_version"]=data["mongoDBVersion"]
        new_data["mongo_uri_updated"]=data["mongoURIUpdated"]
        new_data["name"]=data["name"]
        new_data["numshards"]=data["numShards"]
        new_data["pitenabled"]=data["pitEnabled"]
        new_data["provider_backup_enabled"]=data["providerBackupEnabled"]
        new_data["providername"]=data["providerSettings"]["providerName"]
        new_data["maxinstance_size"]=data["providerSettings"]["autoScaling"]["compute"]["maxInstanceSize"]
        new_data["mininstance_size"]=data["providerSettings"]["autoScaling"]["compute"]["minInstanceSize"]
        new_data["replication_factor"]=data["replicationFactor"]
        new_data["analytics_nodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["analyticsNodes"]
        new_data["electable_nodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["electableNodes"]
        new_data["priority"]=data["replicationSpec"]["ASIA_SOUTH_1"]["priority"]
        new_data["readonly_nodes"]=data["replicationSpec"]["ASIA_SOUTH_1"]["readOnlyNodes"]
        new_data["zonename"]=data["replicationSpecs"][0]["zoneName"]
        new_data["rootcert_type"]=data["rootCertType"]
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

    parser.add_argument('--group_id',help="group ID of mongodb_atlas_cluster",type=str)
    parser.add_argument('--public_key',help="public key of mongodb_atlas",type=str)
    parser.add_argument('--private_key',help="Private key for mongodb_atlas",type=str)
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
    resultjson['units'] = metrics_units
print(json.dumps(resultjson, indent=4, sort_keys=True))

