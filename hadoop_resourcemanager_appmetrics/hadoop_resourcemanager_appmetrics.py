#!/usr/bin/python3

### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

import urllib.request, json

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

#config section
'''
    Hostname on which the resource manager is running
'''
HOSTNAME = 'localhost'

'''
    Port on which the resource manager is listening to. Default port is 8088
'''
PORT = '8088'

'''
    Each cluster will have a list of applications running and each application will have it's own app id. 
    To get the details about a particular app, we have to pass the necessary application id here. 
    Details about getting the list of applications can be found here
    https://hadoop.apache.org/docs/r2.6.0/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html#Cluster_Applications_API
'''
APP_ID = 'application_1476879916372_0001'

METRICS_UNITS = {'allocatedMB': 'MB',
                 'memorySeconds': 'ms',
                 'vcoreSeconds': 'ms',
                 'preemptedResourceMB':'MB', 
                 'progress': '%',
                 'elapsedTime': 'ms'
                 }

class ResourceManager:
    def __init__(self, appId, hostName="localhost", port="8088"):
        self.url = 'http://%s:%s/ws/v1/cluster/apps/%s' % (hostName, port, appId)
        self.req = urllib.request.Request(self.url)
    
    def metricCollector(self):
        data = {}
        try:
            with urllib.request.urlopen(self.req) as res:
                result = json.loads(res.read().decode())
        except Exception as e:
            data["error"] = str(e)
            return data
        result = result["app"]
        data["allocatedMB"] = result["allocatedMB"]
        data["allocatedVCores"] = result["allocatedVCores"]
        data["elapsedTime"] = result["elapsedTime"]
        data["memorySeconds"] = result["memorySeconds"]
        data["progress"] = result["progress"]
        data["preemptedResourceMB"] = result["preemptedResourceMB"]
        data["preemptedResourceVCores"] = result["preemptedResourceVCores"]
        data["runningContainers"] = result["runningContainers"]
        data['units'] = METRICS_UNITS
        return data
    
if __name__ == "__main__":
    r = ResourceManager(appId=APP_ID, hostName=HOSTNAME, port=PORT)
    
    result = r.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))