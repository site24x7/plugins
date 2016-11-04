#!/usr/bin/python3
"""

Site24x7 Hadoop datanode Plugin
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

"""
import os
import json
import urllib.request

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "2"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
HADOOP_HOST = "172.20.9.130"

HADOOP_PORT = "50075"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'total_space_': 'GB', 
                 'remaining_space_': 'GB',
                 'dfs_used_space_': 'GB', 
                 'non_dfs_used_space_': 'GB',  
                 }


class HadoopDataNodeInfo:
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '50075'))

    def metricCollector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}

        url = 'http://%s:%s/jmx?qry=Hadoop:service=DataNode,name=FSDatasetState-null' % (
            self.host, self.port)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode())
        bean = result['beans'][0]
        non_dfs_used = float(bean['Capacity']) - (float(bean['DfsUsed']) + float(bean['Remaining']))
        
        non_dfs_used = 0 if non_dfs_used <=0 else non_dfs_used
        
        data['total_space_'] = self.convertBytesToGB(bean['Capacity'])
        data['remaining_space_'] = self.convertBytesToGB(bean['Remaining'])
        data['dfs_used_space_'] = self.convertBytesToGB(bean['DfsUsed'])
        data['non_dfs_used_space_'] = self.convertBytesToGB(non_dfs_used)
        data['num_failed_volumes_'] = bean['NumFailedVolumes']
        data['num_blocks_cached_'] = bean['NumBlocksCached']
        data['num_blocks_failed_to_cache_'] = bean['NumBlocksFailedToCache']
        data['num_blocks_failed_to_uncache_'] = bean['NumBlocksFailedToUncache']
        data['units'] = METRICS_UNITS

        return data
    
    def convertBytesToGB(self, v):
        try:
            byte_s=float(v)
            kilobytes=byte_s/1024;
            megabytes=kilobytes/1024;
            gigabytes = megabytes/1024;
            v=round(gigabytes,2)
        except Exception as e:
            pass
        return v 
        


if __name__ == "__main__":
    configurations = {'host': HADOOP_HOST, 'port': HADOOP_PORT}

    hadoop_plugins = HadoopDataNodeInfo(configurations)

    result = hadoop_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
