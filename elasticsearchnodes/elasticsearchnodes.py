#!/usr/bin/python

import json
import urllib2
import socket

### For monitoring the performance metrics of your Elasticsearch cluster using Site24x7 Server Monitoring Plugins.

### 1. Have the site24x7 server monitoring agent up and running.
### 2. Download the plugin from github https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/
### 3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
### 4. Place the plugin inside the folder 

### Author: Tarun, Zoho Corp
### Language : Python
### Tested in Ubuntu, CentOS 6


### Modified By: Pierce Fortin, SmashFly Technologies
### Changes Made: Modified for Elastic 2.4.2, Added integration for the ability to have hostname and IP address dynamically generated based on eth0 IP address and system hostname to align with common Elastic automation 

# Change the Elasticsearch stats accordingly here.
URL = "http://127.0.0.1:9200/_nodes/stats"
USERNAME = None
PASSWORD = None
NODE = 'NODE_NAME' # Name of the node
nodecount = 0
### If you want to use Dynamic IP and Node Naming, Comment NODE = and URL = above and uncomment lines below: 

#IP = socket.gethostbyname(socket.gethostname()) # Get local IP address
#URL = "http://%s:9200/_nodes/stats" % IP        # Set URL as IP address found in IP line
#USERNAME = None
#PASSWORD = None
#NODE = socket.gethostname()                     #Sets node name to local hostname of server

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "3"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

### Attribute Names
KEYS = {'host':'host', # ESCluster Host
        'transport_address':'transport_address',# ESClusted address
        'cpu_percent':'cpu_percent', # CPU Used Percent
        'mem_used':'mem_used', # Memory Used
        'mem_free':'mem_free', # Memory Free
        'non_heap_used_in_bytes':'non_heap_used_in_bytes', # Non Heap Used In Bytes
        'non_heap_committed_in_bytes':'non_heap_comitted_in_bytes', # Non Heap Commited in Bytes
        'mem_total_virtual_in_bytes':'vitual_mem', # Total Virtual Memory in Bytes
        'heap_used_percent':'heap_used_percent', # JVM Heap Utilization
}
UNITS = {
        'cpu_percent':'%',
        'mem_used':'%',
        'mem_free':'%',      
        'non_heap_used_in_bytes':'Bytes', 
        'non_heap_committed_in_bytes':'Bytes', 
        'vitual_mem':'Bytes',
        'heap_used_percent':'%',       
         }
   

class Elasticsearch():
    def __init__(self):
        self.data = {}
        self.data['plugin_version'] = PLUGIN_VERSION
        self.data['heartbeat_required'] = HEARTBEAT
        
    def getData(self):
        try:
            ### Create Authentication Handler for the HTTP Request
            pwdmgr = urllib2.HTTPPasswordMgr()
            pwdmgr.add_password(None, URL, USERNAME, PASSWORD)
            auth = urllib2.HTTPBasicAuthHandler(pwdmgr)
            
            ### Create Proxy Handler for the HTTP Request
            proxy = urllib2.ProxyHandler({}) # Uses NO Proxy
            
            ### Create a HTTP Request with the authentication and proxy handlers
            opener = urllib2.build_opener(proxy, auth)
            urllib2.install_opener(opener)
            
            ### Get HTTP Response
            response = urllib2.urlopen(URL, timeout=10)
            
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
        global nodecount
        try:
            data = json.loads(output.decode('UTF-8'))
            nodes = data['nodes'].keys()
            
            for _ in nodes :
                node = data['nodes'][_]
                nodename = node['name']
                if NODE == nodename : 
                    self.data['host'] = node['host']
                    self.data['transport_address'] = node['transport_address']
                    self.data['mem_used'] = node['os']['mem']['used_percent']
                    self.data['mem_free'] = node['os']['mem']['free_percent']
                    
                    self.data['cpu_percent'] = node['process']['cpu']['percent']
                    self.data['non_heap_used_in_bytes'] = node['jvm']['mem']['non_heap_used_in_bytes']
                    self.data['non_heap_committed_in_bytes'] = node['jvm']['mem']['non_heap_committed_in_bytes']
                    self.data['mem_total_virtual_in_bytes'] = node['process']['mem']['total_virtual_in_bytes']
                    self.data['heap_used_percent'] = node['jvm']['mem']['heap_used_percent']
                    nodecount = 1
                
                else :
                   continue #Continue the loop until all nodes are enumerated
            if nodecount != 1: #After loop is completed, Do basic error handling. If NODE variable was not found in JSON document, Return node not found in cluster and status 0
               self.data['msg'] = "Node not found in cluster"
               self.data['status'] = 0


                
        except Exception as e:
            print e
            self.data['msg'] = str(e) 
            self.status = 0
        
        return self.data    
    
 
if __name__ == '__main__':
    es = Elasticsearch()
    result = es.getData()
    print(json.dumps(result, indent=4, sort_keys=True))
