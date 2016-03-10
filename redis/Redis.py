#!/usr/bin/python
"""
  
  Site24x7 Redis Plugin
  
"""

import json
import logging
import os
import platform
import sys
import time

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
REDIS_HOST = "localhost"

REDIS_PORT = "6379"

REDIS_USERNAME = "root"

REDIS_PASSWORD = ""

REDIS_DBS = "0"

REDIS_QUEUES = ""

#Mention the units of your metrics in this dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={'instantaneous_input_kbps':'kbps','instantaneous_output_kbps':'kbps',
               'total_net_input_bytes':'bytes','total_net_output_bytes':'bytes'
              }

class Redis(object):
    def __init__(self,config):
        self.configuration = config
        self.host = self.configuration.get('host', 'localhost')
        self.port = int(self.configuration.get('port', '6379'))
        self.dbs = self.configuration.get('dbs', ['0'])
        self.password = self.configuration.get('password', '')
        self.queues = self.configuration.get('queues', '')

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        try:
            import redis
        except Exception:
            #print('Python Redis module not installed, please install https://pypi.python.org/pypi/redis/')
            data['status']=0
            data['msg']='Redis Module Not Installed'
            return data
            
        stats = None
        for db in self.dbs.split(','):
            try:
                redis_connection = redis.StrictRedis(host=self.host,port=self.port,db=int(db),password=self.password)
                stats = redis_connection.info()
            except Exception as e:
                data['status']=0
                data['msg']='Connection Error'

        if not stats:
            return data

        #stats.items() for python version greater than 3 otherwise stats.iteritems()
        for name, value in stats.iteritems():
            try:
                if name in ['used_memory_peak_human', 'used_memory_human']:
                    value = float(value[0:-1])
                if name in ['aof_enabled','aof_rewrite_in_progress','aof_rewrite_scheduled','cluster_enabled','loading','rdb_bgsave_in_progress','redis_git_dirty','tcp_port']:
                    data[name] = value
                else:
                    data[name] = float(value)
            except (ValueError, TypeError) as e:
                #print('error -- {0}'.format(name))
                data[name] = value

        for queueName in self.queues.split(','):
            data[queueName + '_length'] = redis_connection.llen(queueName)
        
        data['units']=METRICS_UNITS
        
        return data


if __name__ == '__main__':
    
    configuration = {'host': REDIS_HOST,'port': REDIS_PORT,'dbs': REDIS_DBS,'password': REDIS_PASSWORD,'queues': REDIS_QUEUES}

    redis_plugin = Redis(configuration)

    result=redis_plugin.metricCollector()
 
    print(json.dumps(result, indent=4, sort_keys=True))