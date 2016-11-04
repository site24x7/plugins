#!/usr/bin/python3

### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Plugin for getting the metrics of node in a cluster
### For more info refer,
### https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Node_API

import urllib.request, json

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

#config section
'''
    hostname on which the resource manager is running
'''
HOSTNAME = 'localhost'

'''
    port on which the resource manager is listening to. Default port is 8088
'''
PORT = '8088'

'''
    Each cluster will have a list of nodes and this plugin will get the details
    of a single node. So, to get the details of a single node, we have to pass
    the correct nodeId below. We can get the details of each node using the 
    below url,
    GET http://<rm http address:port>/ws/v1/cluster/nodes
    
    If wrong NODE_ID is given, the following error will be displayed,
    {
    "error": "HTTP Error 404: Not Found"
    }
'''
NODE_ID = 'vinoth-2277.csez.zohocorpin.com:52086'

METRICS_UNITS = {'lastHealthUpdate': 'ms',
                 'numContainers': 'units',
                 'usedMemoryMB': 'MB',
                 'availMemoryMB':'MB', 
                 'usedVirtualCores': 'units',
                 'availableVirtualCores': 'units'
                 }

class ResourceManager:
    def __init__(self, nodeId, hostName="localhost", port="8088"):
        self.url = 'http://%s:%s/ws/v1/cluster/nodes/%s' % (hostName, port, nodeId)
        self.req = urllib.request.Request(self.url)
    
    def metricCollector(self):
        data = {}
        try:
            with urllib.request.urlopen(self.req) as res:
                result = json.loads(res.read().decode())
        except Exception as e:
            data["error"] = str(e)
            return data
        result = result["node"]
        data["lastHealthUpdate"] = result["lastHealthUpdate"]
        data["numContainers"] = result["numContainers"]
        data["usedMemoryMB"] = result["usedMemoryMB"]
        data["availMemoryMB"] = result["availMemoryMB"]
        data["usedVirtualCores"] = result["usedVirtualCores"]
        data["availableVirtualCores"] = result["availableVirtualCores"]
        data['units'] = METRICS_UNITS
        return data
    
if __name__ == "__main__":
    r = ResourceManager(nodeId=NODE_ID, hostName=HOSTNAME, port=PORT)
    
    result = r.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))