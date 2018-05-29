#!/usr/bin/python
"""
  
  Site24x7 Redis Plugin
  
"""

import json


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


### Uncomment/Comment the Attribute Names to be monitored
### Change plugin_version if you edit this section
METRICS = {
    #"_length": "length", 
    
    #"aof_current_rewrite_time_sec": "aof current rewrite time", 
    #"aof_enabled": "aof enabled", 
    #"aof_last_bgrewrite_status": "aof last bgrewrite status", 
    #"aof_last_rewrite_time_sec": "aof last rewrite time", 
    #"aof_last_write_status": "aof last write status", 
    #"aof_rewrite_in_progress": "aof rewrite in progress", 
    #"aof_rewrite_scheduled": "aof rewrite scheduled", 
    
    #"arch_bits": "arch bits", 
    "blocked_clients": "blocked clients", 
    #"client_biggest_input_buf": "client biggest input buf", 
    #"client_longest_output_list": "client longest output list", 
    "cluster_enabled": "cluster enabled", 
    "connected_clients": "connected clients", 
    "connected_slaves": "connected slaves", 
    "evicted_keys": "evicted keys", 
    "expired_keys": "expired keys", 
    #"hz": "hz", 
    #"instantaneous_input_kbps": "instantaneous input kbps", 
    #"instantaneous_ops_per_sec": "instantaneous ops per sec", 
    #"instantaneous_output_kbps": "instantaneous output kbps", 
    #"keyspace_hits": "keyspace hits", 
    #"keyspace_misses": "keyspace misses", 
    #"latest_fork_usec": "latest fork usec", 
    #"loading": "loading", 
    #"lru_clock": "lru clock", 
    #"master_repl_offset": "master repl offset", 
    #"mem_allocator": "mem allocator", 
    #"mem_fragmentation_ratio": "mem fragmentation ratio", 
    #"migrate_cached_sockets": "migrate cached sockets", 
    #"multiplexing_api": "multiplexing api", 
    #"pubsub_channels": "pubsub channels", 
    #"pubsub_patterns": "pubsub patterns", 
    #"rdb_bgsave_in_progress": "rdb bgsave in progress", 
    #"rdb_changes_since_last_save": "rdb changes since last save", 
    #"rdb_current_bgsave_time_sec": "rdb current bgsave time sec", 
    #"rdb_last_bgsave_status": "rdb last bgsave status", 
    #"rdb_last_bgsave_time_sec": "rdb last bgsave time sec", 
    #"rdb_last_save_time": "rdb last save time", 
    #"redis_build_id": "redis build id", 
    #"redis_git_dirty": "redis git dirty", 
    #"redis_git_sha1": "redis git sha1", 
    #"rejected_connections": "rejected connections", 
    #"repl_backlog_active": "repl backlog active", 
    #"repl_backlog_first_byte_offset": "repl backlog first byte offset", 
    #"repl_backlog_histlen": "repl backlog histlen", 
    #"repl_backlog_size": "repl backlog size", 
    #"role": "role", 
    #"run_id": "run id", 
    #"sync_full": "sync full", 
    #"sync_partial_err": "sync partial err", 
    #"sync_partial_ok": "sync partial ok", 
    #"total_commands_processed": "total commands processed", 
    #"total_connections_received": "total connections received", 
    #"total_net_input_bytes": "total net input bytes", 
    #"total_net_output_bytes": "total net output bytes", 
    #"uptime_in_days": "uptime in days", 
    "uptime_in_seconds": "uptime", 
    #"used_cpu_sys": "used cpu sys", 
    #"used_cpu_sys_children": "used cpu sys children", 
    #"used_cpu_user": "used cpu user", 
    #"used_cpu_user_children": "used cpu user children", 
    "used_memory": "used memory", 
    #"used_memory_human": "used memory human", 
    #"used_memory_lua": "used memory lua", 
    #"used_memory_peak": "used memory peak", 
    "used_memory_peak_human": "used memory peak human", 
    #"used_memory_rss": "used memory rss"
}


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
        for name, value in stats.items():
            try:
                if name in METRICS.keys() :
                    if METRICS[name] in ['used_memory_peak_human', 'used_memory_human']:
                        value = float(value[0:-1])
                    data[METRICS[name]] = value
            except (ValueError, TypeError) as e:
                #print('error -- {0}'.format(name))
                data[name] = value

        
        
        data['units']=METRICS_UNITS
        
        return data


if __name__ == '__main__':
    
    configuration = {'host': REDIS_HOST,'port': REDIS_PORT,'dbs': REDIS_DBS,'password': REDIS_PASSWORD,'queues': REDIS_QUEUES}

    redis_plugin = Redis(configuration)

    result=redis_plugin.metricCollector()
 
    print(json.dumps(result, indent=4, sort_keys=True))
