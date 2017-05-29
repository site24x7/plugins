#!/usr/bin/python

import json

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
MEMCACHE_HOST='127.0.0.1'

MEMCACHE_PORT=11211

METRICS_UNITS={'uptime':'seconds','bytes_read':'bytes','bytes_written':'bytes','limit_maxbytes':'MB'}

BYTES_TO_MB_LIST=['bytes','limit_maxbytes']


### Uncomment/Comment the Attribute Names to be monitored
### Change plugin_version if you edit this section
KEYS = {
  "get_hits": "get_hits",
  #"limit_maxbytes": "limit_maxbytes",
  #"listen_disabled_num": "listen_disabled_num",
  #"expired_unfetched": "expired_unfetched",
  #"connection_structures": "connection_structures",
  "delete_misses": "delete_misses",
  #"bytes_read": "bytes_read",
  "reclaimed": "reclaimed",
  "cas_hits": "cas_hits",
  "get_misses": "get_misses",
  "incr_misses": "incr_misses",
  #"version": "version",
  "curr_items": "curr_items",
  #"rusage_user": "rusage_user",
  "incr_hits": "incr_hits",
  #"auth_cmds": "auth_cmds",
  #"pid": "pid",
  #"auth_errors": "auth_errors",
  #"cmd_get": "cmd_get",
  #"bytes": "bytes",
  #"hash_is_expanding": "hash_is_expanding",
  #"lrutail_reflocked": "lrutail_reflocked",
  #"cas_misses": "cas_misses",
  #"delete_hits": "delete_hits",
  "uptime": "uptime",
  #"cmd_touch": "cmd_touch",
  #"decr_hits": "decr_hits",
  #"evicted_unfetched": "evicted_unfetched",
  #"reserved_fds": "reserved_fds",
  #"hash_power_level": "hash_power_level",
  #"evictions": "evictions",
  #"bytes_written": "bytes_written",
  #"crawler_reclaimed": "crawler_reclaimed",
  #"conn_yields": "conn_yields",
  #"malloc_fails": "malloc_fails",
  #"touch_misses": "touch_misses",
  #"total_items": "total_items",
  #"cmd_flush": "cmd_flush",
  #"accepting_conns": "accepting_conns",
  #"touch_hits": "touch_hits",
  #"threads": "threads",
  #"pointer_size": "pointer_size",
  #"cmd_set": "cmd_set",
  #"libevent": "libevent",
  #"cas_badval": "cas_badval",
  #"hash_bytes": "hash_bytes",
  "curr_connections": "curr_connections",
  #"total_connections": "total_connections",
  #"decr_misses": "decr_misses",
  #"rusage_system": "rusage_system"
}

def metricCollector():
    data = {}
    #defaults

    data['plugin_version'] = PLUGIN_VERSION

    data['heartbeat_required']=HEARTBEAT

    data['units']=METRICS_UNITS
    
    try:
        import memcache
    except ImportError:
            data['status']=0
            data['msg']='memcache module not installed'
            return data

    try:
        mc = memcache.Client(["%s:%s"%(MEMCACHE_HOST, MEMCACHE_PORT)])
    except Exception as e:
            data['status']=0
            data['msg']=e
            return data

    stats = mc.get_stats()

    if stats:
        #get the dictionary from tuple
        dct = dict(stats)

        for k,v in dct.items():
            value_dict = v

        if value_dict:
            for k,v in value_dict.items():
                if k in BYTES_TO_MB_LIST and k in KEYS:
                    v=convertBytesToMB(v)
                    data[k]=v
                elif k in KEYS:
                    data[k]=v

    if mc is not None:
            mc.disconnect_all()
            mc == None

    return data

def convertBytesToMB(v):
    try:
        byte_s=float(v)
        kilobytes=byte_s/1024;
        megabytes=kilobytes/1024;
        v=int(megabytes)
    except Exception as e:
        pass
    return v
    
if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
