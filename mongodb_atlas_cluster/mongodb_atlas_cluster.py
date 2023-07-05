#!/usr/bin/python3
import json
import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={"disksize":"GB"}


class appname:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        
        self.cluster_name=args.cluster_name
        self.public_key=args.public_key
        self.private_key=args.private_key
        self.group_project_id=args.group_project_id
        

    
    def metriccollector(self):

        try:
            url= "https://cloud.mongodb.com/api/atlas/v1.0/groups/"+self.group_project_id+"/clusters/"+self.cluster_name 
            if self.public_key and self.private_key:
                password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(None,url, self.public_key ,self.private_key)
                auth_handler = urlconnection.HTTPDigestAuthHandler(password_mgr)  
            
            if auth_handler is not None :
                opener = urlconnection.build_opener(auth_handler)
                urlconnection.install_opener(opener)
            try:
                data = urlconnection.urlopen(url).read()
            except HTTPError as e:
                self.maindata['msg']="HTTP Error:", str(e.code), str(e.reason)
                self.maindata['status']=0
                return self.maindata
            
            except URLError as e:
                self.maindata['msg']="Failed to reach the server. Reason:",str(e.reason)
                self.maindata['status']=0
                return self.maindata
            
            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0
                return self.maindata
                            
            data=json.loads(data)

            self.maindata["clustertype"]=data["clusterType"]
            self.maindata["disksize"]=data["diskSizeGB"]
            self.maindata["mongodb_majorversion"]=data["mongoDBMajorVersion"]
            self.maindata["mongodb_version"]=data["mongoDBVersion"]
            self.maindata["mongo_uri_updated"]=data["mongoURIUpdated"]
            self.maindata["name"]=data["name"]
            self.maindata["numshards"]=data["numShards"]
            self.maindata["pitenabled"]=data["pitEnabled"]
            self.maindata["provider_backup_enabled"]=data["providerBackupEnabled"]
            self.maindata["providername"]=data["providerSettings"]["providerName"]
            self.maindata["maxinstance_size"]=data["providerSettings"]["autoScaling"]["compute"]["maxInstanceSize"]
            self.maindata["mininstance_size"]=data["providerSettings"]["autoScaling"]["compute"]["minInstanceSize"]
            self.maindata["replication_factor"]=data["replicationFactor"]


            region_data=data["replicationSpec"]
            for region in region_data:
                self.maindata[region+"_"+"analytics_nodes"]=data["replicationSpec"][region]["analyticsNodes"]
                self.maindata[region+"_"+"electableNodes"]=data["replicationSpec"][region]["electableNodes"]
                self.maindata[region+"_"+"priority"]=data["replicationSpec"][region]["priority"]
                self.maindata[region+"_"+"readOnlyNodes"]=data["replicationSpec"][region]["readOnlyNodes"]



            self.maindata["zonename"]=data["replicationSpecs"][0]["zoneName"]
            self.maindata["rootcert_type"]=data["rootCertType"]
            self.maindata["srvaddress"]=data["srvAddress"]
            self.maindata["statename"]=data["stateName"]            
                    
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
        

        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["logs_enabled"]=False
        self.maindata['applog'] = applog

        self.maindata['tags']=f"mongodb_atlas_cluster:{self.maindata['name']}"

        return self.maindata




if __name__=="__main__":
    
    public_key = None
    private_key = None
    group_project_id= None
    cluster_name='AtlasCluster'

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--cluster_name',help="mongo db atlas cluster name",type=str,default=cluster_name)
    parser.add_argument('--group_project_id',help="group ID of mongodb_atlas_cluster",type=str, default=group_project_id)
    parser.add_argument('--public_key',help="public key of mongodb_atlas",type=str, default=public_key)
    parser.add_argument('--private_key',help="Private key for mongodb_atlas",type=str, default=private_key)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=appname(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
