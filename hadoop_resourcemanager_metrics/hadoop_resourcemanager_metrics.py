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

# Config Section:
HADOOP_HOST = "localhost"

HADOOP_PORT = "8088"


METRICS_UNITS = {'allocatedMB': 'MB',
                 'totalMB': 'MB',
                 'availableMB': 'MB',
                 'appsSubmitted':'Units',
                 'appsCompleted':'Units',
                 'appsPending':'Units',
                 'totalVirtualCores': 'Units', 
                 'allocatedVirtualCores': 'Units',
                 'availableVirtualCores': 'Units',
                 'totalNodes': 'Units',   
                 }

class ResourceManager:
    def __init__(self, hostName="localhost", port="8088"):
        self.url = 'http://%s:%s/ws/v1/cluster/metrics' % (hostName, port)
        self.req = urllib.request.Request(self.url)
    
    def metricCollector(self):
        data = {}
        with urllib.request.urlopen(self.req) as res:
            result = json.loads(res.read().decode())
        result = result["clusterMetrics"]
        result['units'] = METRICS_UNITS
        return result

    
if __name__ == "__main__":
    r = ResourceManager(hostName=HADOOP_HOST, port=HADOOP_PORT)
    
    result = r.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))