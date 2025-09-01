#!/usr/bin/python3

import json,sys

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
host = "localhost"
port = "6379"
password = ""
dbs = "1"


### Uncomment/Comment the Attribute Names to be monitored
### Change plugin_version if you edit this section
METRICS = {
    #"_length": "length", 
    
    #"aof_current_rewrite_time_sec": "aof current rewrite time", 
    #"aof_enabled": "aof enabled", 
    "aof_last_bgrewrite_status": "AOF Last Bgrewrite Status", 
    "aof_last_rewrite_time_sec": "AOF Last Rewrite Time", 
    #"aof_last_write_status": "aof last write status", 
    #"aof_rewrite_in_progress": "aof rewrite in progress", 
    #"aof_rewrite_scheduled": "aof rewrite scheduled", 
    "active_defrag_hits": "Active Defrag Hits",
    "active_defrag_misses": "Active Defrag Misses",
    "active_defrag_key_hits": "Active Defrag Key Hits",
    "active_defrag_key_misses": "Active Defrag Key Misses",
    "active_defrag_running": "Active Defrag Running",
    #"arch_bits": "arch bits", 
    "blocked_clients": "Blocked Clients", 
    "client_biggest_input_buf": "Client Biggest Input Buf", 
    "client_longest_output_list": "Client Longest Output List", 
    "cluster_enabled": "Cluster Enabled", 
    "connected_clients": "Connected Clients", 
    "connected_slaves": "Connected Slaves", 
    "evicted_keys": "Evicted Keys", 
    "expired_keys": "Expired Keys", 
    #"hz": "hz", 
    "instantaneous_input_kbps": "Incoming Traffic", 
    "instantaneous_ops_per_sec": "Ops/Sec",
    "instantaneous_output_kbps": "Outgoing Traffic", 
    "keyspace_hits": "Keyspace Hits", 
    "keyspace_misses": "Keyspace Misses", 
    "latest_fork_usec": "Latest Fork Usec", 
    #"loading": "loading", 
    #"lru_clock": "lru clock", 
    "master_repl_offset": "Master Repl Offset", 
    "second_repl_offset": "Second Repl Offset",
    #"mem_allocator": "mem allocator", 
    "mem_fragmentation_ratio": "Fragmentation Ratio", 
    #"migrate_cached_sockets": "migrate cached sockets", 
    #"multiplexing_api": "multiplexing api", 
    "pubsub_channels": "Pubsub Channels", 
    "pubsub_patterns": "Pubsub Patterns", 
    "rdb_bgsave_in_progress": "RDB Bgsave in Progress", 
    "rdb_changes_since_last_save": "RDB Changes Since Last Save", 
    #"rdb_current_bgsave_time_sec": "rdb current bgsave time sec", 
    #"rdb_last_bgsave_status": "rdb last bgsave status", 
    #"rdb_last_bgsave_time_sec": "rdb last bgsave time sec", 
    "rdb_last_save_time": "RDB Last Save Time", 
    #"redis_build_id": "redis build id", 
    #"redis_git_dirty": "redis git dirty", 
    #"redis_git_sha1": "redis git sha1", 
    "rejected_connections": "Rejected Connections", 
    #"repl_backlog_active": "repl backlog active", 
    #"repl_backlog_first_byte_offset": "repl backlog first byte offset", 
    #"repl_backlog_histlen": "repl backlog histlen", 
    #"repl_backlog_size": "repl backlog size", 
    "repl_backlog_histlen": "Repl Backlog Histlen",
    "role": "Role", 
    "connected_slaves": "Connected Slaves",
    #"run_id": "run id", 
    "sync_full": "Sync Full", 
    "sync_partial_err": "Sync Partial Err", 
    "sync_partial_ok": "Sync Partial Ok", 
    "total_commands_processed": "Total Commands Processed", 
    "total_connections_received": "Total Connections Received", 
    #"total_net_input_bytes": "total net input bytes", 
    #"total_net_output_bytes": "total net output bytes", 
    "uptime_in_days": "Uptime in Days", 
    "uptime_in_seconds": "Uptime", 
    "used_cpu_sys": "CPU Sys", 
    "used_cpu_sys_children": "CPU Sys Children", 
    "used_cpu_user": "CPU User", 
    "used_cpu_user_children": "CPU User Children", 
    "used_cpu_sys_main_thread": "CPU Sys Main Thread",
    "used_memory": "Used Memory", 
    #"used_memory_human": "used memory human", 
    "used_memory_lua": "Memory Lua", 
    "used_memory_peak": "Memory Peak", 
    #"used_memory_peak_human": "used memory peak human", 
    "used_memory_rss": "Memory RSS",
    "maxmemory": "Max Memory",
    "used_memory_overhead": "Memory Overhead",
    "used_memory_startup": "Memory Startup",
    "io_threads_active": "IO Threads Active",
    "io_threaded_reads_processed": "IO Threaded Reads Processed",
    "io_threaded_writes_processed": "IO Threaded Writes Processed",
    "redis_version": "Redis Version",
    "redis_mode": "Redis Mode"

}

tabs= {
  "tabs": {

    "Replication": {
      "order": "5",
      "tablist": [
        "Sync Full",
        "Sync Partial Err",
        "Sync Partial Ok",
        "Master Repl Offset",
        "Second Repl Offset",
        "Repl Backlog Histlen"
      ]
    },

    "Performance": {
      "order": "4",
      "tablist": [
        "AOF Last Rewrite Time",
        "Active Defrag Hits",
        "Active Defrag Key Hits",
        "Active Defrag Key Misses",
        "Active Defrag Misses",
        "Active Defrag Running",
        "RDB Bgsave in Progress",
        "RDB Changes Since Last Save",
        "RDB Last Save Time"
      ]
    },
    
    "CPU": {
      "order": "3",
      "tablist": [
        "CPU Sys",
        "CPU Sys Children",
        "CPU User",
        "CPU User Children",
        "CPU Sys Main Thread"
      ]
    },

    "Memory": {
      "order": "2",
      "tablist": [
        "Used Memory",
        "Max Memory",
        "Memory Lua",
        "Memory Overhead",
        "Memory Peak",
        "Memory RSS",
        "Memory Startup",
        "Fragmentation Ratio"
      ]
    },

    "DB Stats": { 
      "order": "1",
      "tablist": [
        "db",
        "Total Expires",
        "Total Keys",
        "Total Persists"
      ]
    }
  }
}

#Mention the units of your metrics in this dictionary. If any new metrics are added make an entry here for its unit.
METRICS_UNITS={  
    "Uptime in Days": "days",
    "Incoming Traffic": "kbps",
    "Outgoing Traffic": "kbps",
    "Uptime": "s",
    "Used Memory": "KB",
    "Max Memory": "bytes",
    "Memory Lua": "bytes",
    "Memory Overhead": "bytes",
    "Memory Peak": "bytes",
    "Memory RSS": "bytes",
    "Memory Startup": "bytes",
    "AOF Last Rewrite Time": "s",
    "Active Defrag Hits": "operations",
    "Active Defrag Key Misses":"keys",
    "Active Defrag Misses": "operations",
    "Active Defrag Key Hits": "keys",
    "RDB Last Save Time": "s",
    "Total Expires": "keys",
    "Total Keys": "keys",
    "Total Persists": "keys",
    "Repl Backlog Histlen": "bytes",
    "Master Repl Offset": "offset",
    "Second Repl Offset": "offset",
    "Blocked Clients": "connections",
    "Connected Clients":"connections",
    "Connected Slaves": "connections",
    "Rejected Connections": "connections",
    "Max Clients": "connections",
    "Evicted Keys": "keys",
    "Expired Keys": "keys",
    "Keyspace Hits": "keys",
    "Keyspace Misses": "keys",
    "Latest Fork Usec": "ms",
    "Ops/Sec": "operations",
    "Total Connections Received": "connections"
    
}

class Redis(object):
    def __init__(self,args):
        self.args=args
        self.host=args.host
        self.port=args.port
        if args.password:
            self.password=args.password
        else:
            self.password=""
        self.applog={}
        if(args.logs_enabled in ['True', 'true', '1']):
                self.applog["logs_enabled"]=True
                self.applog["log_type_name"]=args.log_type_name
                self.applog["log_file_path"]=args.log_file_path
        else:
                self.applog["logs_enabled"]=False

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        try:
            import redis

        except Exception as e:
            data['status']=0
            if "No module named" in str(e):
                data['msg']="Redis Module Not Installed\nDependency missing:'redis' Python client library\nInstall with command,\n\n pip3 install redis\n"
            else:
                data['msg']=str(e)
            return data 
        stats = None
        try:
            redis_connection = redis.StrictRedis(
                    host=self.host,
                    port=self.port,
                    password=self.password
            )
            stats = redis_connection.info()
            max_clients=redis_connection.config_get('maxclients')
            

        except Exception as e:
            data['status']=0
            data['msg']=str(e)
        if not stats:
            return data
        total_keys=0
        total_expires=0
        total_persist=0
        db=[]
        data["Max Clients"]=str(max_clients["maxclients"])+" Connections"
        for name, value in stats.items():
            try:

                if name in METRICS.keys() :
                    if METRICS[name] == 'Cluster Enabled':
                        value = str(value)+" Count"
                    if METRICS[name] == 'Max Memory':
                        value=str(round(value/1024/1024,2))+" MB"
                    
                    data[METRICS[name]] = value
                if type(value)==dict and "db" in name and "rdb" not in name:
                    db_data=value
                    del db_data['avg_ttl']
                    db_data['name']=name
                    persist=value['keys']-value['expires']
                    db_data['persist']=persist
                    db_data['persist_percent']=round((persist/value['keys'])*100,2)
                    db_data['expires_percent']=round((value['expires']/value['keys'])*100,2)
                    db.append(db_data)
                    total_keys+=value['keys']
                    total_expires+=value['expires']
                    total_persist+=persist

            except (ValueError, TypeError) as e:
                data[name] = value
        try:
            data['Total Keys']=total_keys
            data['Total Expires']=total_expires
            data['Total Persists']=total_persist
            total_key_stats = data['Keyspace Hits'] + data['Keyspace Misses']
            if total_key_stats == 0:
                data['Hit Ratio']=0
            else:
                data['Hit Ratio'] = data['Keyspace Hits'] / total_key_stats
                
                
        except Exception as e:
                data['status']=0
                data['msg']=str(e)
        data['units']=METRICS_UNITS
        data['db']=db
        data["applog"]=self.applog
        data.update(tabs)

        return data


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "6379")
    parser.add_argument('--password',help="Password" , default= password)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="true")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default="Redis Logs")
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default="/var/log/redis/redis*.log")
    args=parser.parse_args()

    redis_plugin = Redis(args)

    result=redis_plugin.metricCollector()
 
    print(json.dumps(result, indent=4, sort_keys=True))
