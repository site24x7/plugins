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
            self.data['master_slave_registrations'] = data['master/slave_registrations']#Number of agents that were able to cleanly re-join the cluster and connect back to the master after the master is disconnected.
            self.data['master_master_slave_reregistrations'] = data['master/slave_reregistrations']#Number of agent re-registrations
            self.data['master_slave_removals'] = data['master/slave_removals']#Number of agent removed for various reasons, including maintenance
            self.data['master_slave_shutdowns_scheduled'] = data['master/slave_shutdowns_scheduled']#Number of agents which have failed their health check and are scheduled to be removed. 
            self.data['master_slave_shutdowns_canceled'] = data['master/slave_shutdowns_canceled']#Number of cancelled agent shutdowns. 
            self.data['master_slave_shutdowns_completed'] = data['master/slave_shutdowns_completed']#Number of agents that failed their health check.
            self.data['master_slaves_active'] = data['master/slaves_active']#Number of active agents
            self.data['master_slaves_connected'] = data['master/slaves_connected']#Number of connected agents	
            self.data['master_slaves_disconnected'] = data['master/slaves_disconnected']#Number of disconnected agents
            self.data['master_slaves_inactive'] = data['master/slaves_inactive']#Number of inactive agents
                
        except Exception as e:
            self.data['msg'] = str(e) 
            self.status = 0
        
        return self.data    
    
 
if __name__ == '__main__':
    mesosagt = MesosAgents()
    result = mesosagt.getData()
    print(json.dumps(result, indent=4, sort_keys=True))
