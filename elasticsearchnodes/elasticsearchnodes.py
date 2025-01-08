#!/usr/bin/python

import json,sys
import base64

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib.request as urllib2    
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2


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
NODE = 'Node name' # Name of the node
TIMEOUT=10

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT =True

### Attribute Names
KEYS = {
            'host':{'node' : None, 'key' : 'host'}, # ESCluster Host
            'transport_address':{'node' : None, 'key' : 'transport_address'},# ESClusted address
            
            'percent':{'node' : 'os:cpu', 'key' : 'cpu_percent'}, # CPU Used Percent
            'used_percent':{'node' : 'os:mem', 'key' :'mem_used'}, # Memory Used
            'free_percent':{'node' : 'os:mem', 'key' :'mem_free'}, # Memory Free
            'heap_committed_in_bytes' : {'node' :'jvm:mem','key':'heap_committed_in_bytes'},
            'heap_used_in_bytes' : {'node' :'jvm:mem','key':'heap_used_in_bytes'},
            'heap_used_percent' : {'node' :'jvm:mem','key':'heap_used_percent'},
            
            
            'count' : {'node' :'indices:docs','key':'count'},
            'deleted' : {'node' :'indices:docs','key':'deleted'},
            'fetch_total' : {'node' :'indices:search','key':'fetch_total'},
            'query_total' : {'node' :'indices:search','key':'query_total'},
            'total' : {'node' :'indices:flush','key':'total'},
            
            'evictions' : {'node' :'indices:fielddata','key':'evictions'},
            
            'request_cache:hit_count' : {'node' :'indices:request_cache','key':'request_cache_hit_count'},
            'request_cache:memory_size_in_bytes' : {'node' :'indices:request_cache','key':'request_cache_memory_size_in_bytes'},
            'request_cache:miss_count' : {'node' :'indices:request_cache','key':'request_cache_miss_count'},
            
            'query_cache:memory_size_in_bytes' : {'node' :'indices:query_cache','key':'query_cache_memory_size_in_bytes'},
            'query_cache:hit_count' : {'node' :'indices:query_cache','key':'query_cache_hit_count'},
            'query_cache:miss_count' : {'node' :'indices:query_cache','key':'query_cache_miss_count'},
}           

UNITS = {
        'cpu_percent':'%',
        'mem_used':'%', 
        'mem_free':'%'
}

class Elasticsearch():
    def __init__(self,host_name,port,node_name,username,password):
        self.data = {}
        self._url = "http://"+host_name+':'+port+"/_nodes/stats"
        self._userName = username
        self._userPass = password
        self._node_name=node_name
                
    def getData(self):
        try:
            
            ### Create Proxy Handler for the HTTP Request
            proxy = urllib2.ProxyHandler({}) # Uses NO Proxy
            
            ### Create a HTTP Request with the authentication and proxy handlers
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            
            ### Get HTTP Response            
            request = urllib2.Request(self._url)
            base64string = base64.b64encode(('%s:%s' % (self._userName,self._userPass)).encode("utf-8"))
            request.add_header("Authorization", "Basic %s" % base64string)
            response = urllib2.urlopen(request,timeout=TIMEOUT)
            
            ### Parse the response data
            if response.getcode() == 200:
                bytedata = response.read()
                output = bytedata.decode()
                self.data = self.parseClusterData(output)
            else:
                self.data['msg'] = str(response.getcode())
                self.status = 0
        
        except Exception as e:
            self.data['msg'] = str(e)
            self.status = 0
        
        return self.data
    
    def parseClusterData(self, output):
        try:
            is_node_present=False        
            data = json.loads(output)
            nodes = data['nodes'].keys()                    
            for _ in nodes :
                node = data['nodes'][_]
                nodename = node['name']
                if self._node_name == nodename : 
                    for __ in KEYS :
                        try:                            
                            keynodes = KEYS[__]['node']                            
                            key = KEYS[__]['key']
                            mynode = node
                            if keynodes is not None:
                                keynode = keynodes.split(':')
                                for item in keynode:
                                    mynode = mynode[item]                                    
                            self.data[key] = mynode[__.split(':')[-1]] 
                        except Exception as ee:                            
                            self.data['msg'] = str(ee)
                    is_node_present=True
            if not is_node_present:
                self.data['msg'] = "node not present"
                self.data['status'] = 0 
                
        except Exception as e:
            self.data['msg'] = str(e) 
            self.status = 0
        
        return self.data    
    
 
if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=HOST)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=PORT)
    parser.add_argument('--node_name', help='Node name to be monitored', nargs='?', default=NODE)
    parser.add_argument('--username', help='user name of the elasticsearch', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password of the elasticsearch', nargs='?', default=PASSWORD)
    
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()
    
    host_name=args.host
    port=str(args.port)
    node_name=args.node_name    
    username=args.username
    password=args.password    
        
    es = Elasticsearch(host_name,port,node_name,username,password)    
    result = es.getData()
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat
    
    print(json.dumps(result, indent=4, sort_keys=True))
