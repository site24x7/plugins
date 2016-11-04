#!/usr/bin/python3
"""

Site24x7 Hadoop namenode Plugin
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu
"""
import os
import json
import urllib.request

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
HADOOP_HOST = "172.20.11.106"

HADOOP_PORT = "50070"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'configured_capacity': 'GB', 
                 'used_space': 'GB', 
                 'free_space': 'GB', 
                 'percent_remaining': '%', 
                 'total_blocks': 'Units', 
                 'total_files': 'units',
                 'missing_blocks': 'units',
                 'number_of_threads': 'units'}


class HadoopNameNodeInfo:
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '50070'))

    def metricCollector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}

        url = 'http://%s:%s/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo' % (
            self.host, self.port)
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode())
        bean = result['beans'][0]
        
        data['configured_capacity'] = self.convertBytesToGB(bean['Total'])
        data['used_space'] = self.convertBytesToGB(bean['Used'])
        data['free_space'] = self.convertBytesToGB(bean['Free'])
        data['percent_remaining'] = bean['PercentRemaining']
        data['total_blocks'] = bean['TotalBlocks']
        data['total_files'] = bean['TotalFiles']
        data['missing_blocks'] = bean['NumberOfMissingBlocks']
        data['number_of_threads'] = bean['Threads']
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

    hadoop_plugins = HadoopNameNodeInfo(configurations)

    result = hadoop_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
