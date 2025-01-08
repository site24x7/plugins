#!/usr/bin/python

import json
try:
    import urllib2
except Exception as e:
    import urllib.request as urllib2

### For monitoring the performance metrics of your Elasticsearch cluster using Site24x7 Server Monitoring Plugins.

### 1. Have the site24x7 server monitoring agent up and running.
### 2. Download the plugin from github https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/
### 3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
### 4. Place the plugin inside the folder 

### Language : Python
### Tested in Ubuntu

'''
This is Default configuration. 
Change the Elasticsearch configuration accordingly
in the configuration file elasticsearchnodes.cfg.

Configuration File will have more Priority
'''

HOST='localhost'
PORT='9200'
USERNAME = None
PASSWORD = None
TIMEOUT=10

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT =True

### Attribute Names
KEYS = {'active_primary_shards':'active_primary_shards', # number of primary shards in the cluster
        'active_shards':'active_shards',# an aggregate total of all shards across all indices, which includes replica shards
        'cluster_name':'cluster_name', # Name of the cluster
        'delayed_unassigned_shards':'delayed_unassigned_shards', # number of currently active connections
        'initializing_shards':'initializing_shards', # number of shards that are being freshly created
        'number_of_data_nodes':'number_of_data_nodes', # number of data nodes in the cluster
        'number_of_nodes':'number_of_nodes', # number of nodes in a cluster
        'relocating_shards':'relocating_shards', # number of shards that are currently moving from one node to another node
        'status':'status', #
        'unassigned_shards':'unassigned_shards', # number of shards in the cluster state, but cannot be found in the cluster itself        
}
   

class Elasticsearch():
    def __init__(self,host_name,port,username,password):
        self.data = {}
        self._url = "http://"+host_name+':'+port+"/_cluster/health"
        self._userName = username
        self._userPass = password
                        
    def getData(self):
        try:
            ### Create Authentication Handler for the HTTP Request
            pwdmgr = urllib2.HTTPPasswordMgr()
            pwdmgr.add_password(None, self._url, self._userName, self._userPass)
            auth = urllib2.HTTPBasicAuthHandler(pwdmgr)
            
            ### Create Proxy Handler for the HTTP Request
            proxy = urllib2.ProxyHandler({}) # Uses NO Proxy
            
            ### Create a HTTP Request with the authentication and proxy handlers
            opener = urllib2.build_opener(proxy, auth)
            urllib2.install_opener(opener)
            
            ### Get HTTP Response
            response = urllib2.urlopen(self._url, timeout=TIMEOUT)
            
            ### Parse the response data
            if response.getcode() == 200:
                bytedata = response.read()
                output = bytedata.decode()
                self.data = self.parseClusterData(output)
                
            else:
                self.data['msg'] = str(response.getcode())
                self.data['status'] = 0
        
        except Exception as e:
            self.data['msg'] = str(e)
            self.data['status'] = 0
        
        return self.data
    
    def parseClusterData(self, output):
        try:
            data = json.loads(output)
            for _ in data:
                key = str(data['cluster_name']) 
                if _ in KEYS.keys():
                    key = key+"_"+_ 
                    if _ == 'status' : 
                        if data[_] == 'red' : self.data[key] = 0 
                        elif data[_] == "yellow" : self.data[key] = 2
                        else: self.data[key] = 1
                         
                    else : self.data[key] = str(data[_])
                    
        except Exception as e:            
            self.data['msg'] = str(e) 
            self.data['status'] = 0
        
        return self.data    
    
 
if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=HOST)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=PORT)
    parser.add_argument('--username', help='user name of the elasticsearch', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password of the elasticsearch', nargs='?', default=PASSWORD)
    
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()
    
    host_name=args.host
    port=str(args.port)
    username=args.username
    password=args.password
        
    es = Elasticsearch(host_name,port,username,password)    
    result = es.getData()
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat
    
    print(json.dumps(result, indent=4, sort_keys=True))
