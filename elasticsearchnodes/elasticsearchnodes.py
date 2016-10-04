#!/usr/bin/python

import json
import urllib2

### For monitoring the performance metrics of your Elasticsearch cluster using Site24x7 Server Monitoring Plugins.

### 1. Have the site24x7 server monitoring agent up and running.
### 2. Download the plugin from github https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/
### 3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
### 4. Place the plugin inside the folder 

### Author: Tarun, Zoho Corp
### Language : Python
### Tested in Ubuntu


# Change the Elasticsearch stats accordingly here.
URL = "http://localhost:9200/_nodes/stats"
USERNAME = None
PASSWORD = None
NODE = 'Node Name' # Name of the node

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

### Attribute Names
KEYS = {'host':'host', # ESCluster Host
        'transport_address':'transport_address',# ESClusted address
        'cpu_used':'cpu_used', # CPU Used
        'cpu_percent':'cpu_percent', # CPU Used Percent
        'mem_used':'mem_used', # Memory Used
        'mem_free':'mem_free', # Memory Free
        'mem_resident_in_bytes':'resident_mem', # Resident Memory in Bytes
        'mem_share_in_bytes':'shared_mem', # Shared Memory in Bytes
        'mem_total_virtual_in_bytes':'vitual_mem', # Total Virtual Memory in Bytes    
}
UNITS = {
        'cpu_percent':'%',
        'resident_mem':'Bytes', # number of data nodes in the cluster
        'shared_mem':'Bytes', # number of nodes in a cluster
        'vitual_mem':'Bytes', # number of shards that are currently moving from one node to another node      
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
        try:
            data = json.loads(output.decode('UTF-8'))
            nodes = data['nodes'].keys()
            
            for _ in nodes :
                node = data['nodes'][_]
                nodename = node['name']
                if NODE == nodename : 
                    self.data['host'] = node['host']
                    self.data['transport_address'] = node['transport_address']
                    self.data['cpu_used'] = node['os']['cpu']['usage']
                    self.data['mem_used'] = node['os']['mem']['used_percent']
                    self.data['mem_free'] = node['os']['mem']['free_percent']
                    
                    self.data['cpu_percent'] = node['process']['cpu']['percent']
                    self.data['mem_resident_in_bytes'] = node['process']['mem']['resident_in_bytes']
                    self.data['mem_share_in_bytes'] = node['process']['mem']['share_in_bytes']
                    self.data['mem_total_virtual_in_bytes'] = node['process']['mem']['total_virtual_in_bytes']
                    
                else : 
                    self.data['msg'] = "node not present"
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