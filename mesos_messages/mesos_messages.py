#!/usr/bin/python

import json
import urllib2

### For monitoring the performance metrics of your Mesos Agents using Site24x7 Server Monitoring Plugins.

### 1. Have the site24x7 server monitoring agent up and running.
### 2. Download the plugin from github 
### 3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
### 4. Place the plugin inside the folder 

### Language : Python
### Author: Anita, Zoho Corp
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
            self.data['messages_deactivate_framework'] = data['master/messages_authenticate']
            self.data['messages_decline_offers'] = data['master/messages_decline_offers']
            self.data['messages_executor_to_framework'] = data['master/messages_executor_to_framework']
            self.data['messages_exited_executor'] = data['master/messages_exited_executor']
            self.data['messages_framework_to_executor'] = data['master/messages_framework_to_executor']
            self.data['messages_kill_task'] = data['master/messages_kill_task']
            self.data['messages_launch_tasks'] = data['master/messages_launch_tasks']
            self.data['messages_operation_status_update'] = data['master/messages_operation_status_update']

            self.data['messages_reconcile_operations'] = data['master/messages_reconcile_operations']
            self.data['messages_reconcile_tasks'] = data['master/messages_reconcile_tasks']
            self.data['messages_register_framework'] = data['master/messages_register_framework']
            self.data['messages_register_slave'] = data['master/messages_register_slave']
            self.data['messages_reregister_framework'] = data['master/messages_reregister_framework']
            self.data['messages_reregister_slave'] = data['master/messages_reregister_slave']
            self.data['messages_deactivate_framework'] = data['master/messages_authenticate']
            self.data['messages_resource_request'] = data['master/messages_resource_request']

            self.data['messages_revive_offers'] = data['master/messages_revive_offers']
            self.data['messages_status_update'] = data['master/messages_status_update']
            self.data['messages_suppress_offers'] = data['master/messages_suppress_offers']
            self.data['messages_unregister_framework'] = data['master/messages_unregister_framework']

            self.data['messages_unregister_slave'] = data['master/messages_unregister_slave']
            self.data['messages_update_slave'] = data['master/messages_update_slave']
            self.data['messages_status_update_acknowledgement'] = data['master/messages_status_update_acknowledgement']
            self.data['messages_operation_status_update_acknowledgement'] = data['master/messages_operation_status_update_acknowledgement']

        except Exception as e:
            self.data['msg'] = str(e) 
            self.status = 0
        
        return self.data    
    
 
if __name__ == '__main__':
    mesosagt = MesosAgents()
    result = mesosagt.getData()
    print(json.dumps(result, indent=4, sort_keys=True))
