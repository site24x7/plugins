#!/usr/bin/python

import json
import urllib2

### For monitoring the performance metrics of your Mesos Agents using Site24x7 Server Monitoring Plugins.

### 1. Have the site24x7 server monitoring agent up and running.
### 2. Download the plugin from github 
### 3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
### 4. Place the plugin inside the folder 

### Language : Python
### Tested in Ubuntu


# Change the mesos agents stats accordingly here.
HOST="localhost"
PORT="5050"
URL = "http://"+HOST+":"+PORT+"/metrics/snapshot"
USERNAME = None
PASSWORD = None

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

class MesosAgents():
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
            self.data['cpus_percent'] = data['master/cpus_percent']
            self.data['cpus_total'] = data['system/cpus_total']
            self.data['cpus_used'] = data['master/cpus_used']
            
            self.data['disk_percent'] = data['master/disk_percent']
            self.data['disk_total'] = data['master/disk_total']
            self.data['disk_used'] = data['master/disk_used']

            self.data['gpus_percent'] = data['master/gpus_percent']
            self.data['gpus_total'] = data['master/gpus_total']
            self.data['gpus_used'] = data['master/gpus_used']

            self.data['mem_percent'] = data['master/mem_percent']
            self.data['mem_total'] = data['master/mem_total']
            self.data['mem_used'] = data['master/mem_used']

            self.data['mem_free_bytes'] = data['system/mem_free_bytes']
            self.data['mem_total_bytes'] = data['system/mem_total_bytes']

            self.data['load_1min'] = data['system/load_1min']
            self.data['load_5min'] = data['system/load_5min']
            self.data['load_15min'] = data['system/load_15min']


            self.data['http_cache_hits'] = data['master/http_cache_hits']
            self.data['uptime_secs'] = data['master/uptime_secs']
            self.data['invalid_status_updates'] = data['master/invalid_status_updates']
            self.data['valid_status_updates'] = data['master/valid_status_updates']

            self.data['logs_ensemble_size'] = data['registrar/log/ensemble_size']
            self.data['logs_recovered'] = data['registrar/log/recovered']
            self.data['queued_operations'] = data['registrar/queued_operations']
            self.data['registry_size_bytes'] = data['registrar/registry_size_bytes']
            self.data['state_fetch_ms'] = data['registrar/state_fetch_ms']
            self.data['state_store_ms'] = data['registrar/state_store_ms']

        except Exception as e:
            self.data['msg'] = str(e) 
            self.status = 0
        
        return self.data    
    
if __name__ == '__main__':
    mesosagt = MesosAgents()
    result = mesosagt.getData()
    print(json.dumps(result, indent=4, sort_keys=True))
