#!/usr/bin/python3

import json

PLUGIN_VERSION = 1
HEARTBEAT = True

METRICS_UNITS = {
    'Network Read': 'MB',
    'Network Written': 'MB',
    'Cache Memory Used': 'MB',
    'User CPU Time': 'minutes',
    'System CPU Time': 'minutes',
    'Hash Table Memory': 'MB',
    'Avg Item Size': 'MB',
    'Memory Usage Percent': '%',
    'Cache Hit Rate': '%',
    'Oldest Item Age': 'minutes',
    'Last Evicted Item Age': 'minutes',
    'Slab Memory Allocated': 'MB',
    'Slab Memory Requested': 'MB',
    'Uptime': 'minutes',
    'Slabs Chunk Size': 'MB'
}

BYTES_TO_MB_LIST = ['limit_maxbytes', 'bytes_read', 'bytes_written', 'bytes', 'hash_bytes']
STRING_KEYS = {'version', 'libevent'}

KEYS = {
    "get_hits": "GET Hits",
    "limit_maxbytes": "Max Memory Limit",
    "listen_disabled_num": "Listener Disabled Count",
    "expired_unfetched": "Expired Unfetched",
    "connection_structures": "Connection Structures",
    "delete_misses": "DELETE Misses",
    "bytes_read": "Network Read",
    "reclaimed": "Expired Items Reclaimed",
    "cas_hits": "CAS Hits",
    "get_misses": "GET Misses",
    "incr_misses": "INCREMENT Misses",
    "version": "Memcached Version",
    "curr_items": "Current Items",
    "rusage_user": "User CPU Time",
    "incr_hits": "INCREMENT Hits",
    "auth_cmds": "AUTH Commands",
    "pid": "PID",
    "auth_errors": "AUTH Errors",
    "cmd_get": "GET Commands",
    "bytes": "Cache Memory Used",
    "hash_is_expanding": "Hash Is Expanding",
    "lrutail_reflocked": "LRU Tail Relocked",
    "cas_misses": "CAS Misses",
    "delete_hits": "DELETE Hits",
    "cmd_touch": "TOUCH Commands",
    "decr_hits": "DECREMENT Hits",
    "evicted_unfetched": "Evicted Unfetched",
    "reserved_fds": "Reserved File Descriptors",
    "hash_power_level": "Hash Power Level",
    "evictions": "Evictions",
    "bytes_written": "Network Written",
    "crawler_reclaimed": "LRU Crawler Reclaimed",
    "conn_yields": "Connection Yields",
    "malloc_fails": "Memory Allocation Failures",
    "touch_misses": "TOUCH Misses",
    "total_items": "Total Items",
    "cmd_flush": "FLUSH Commands",
    "accepting_conns": "Accepting Connections",
    "touch_hits": "TOUCH Hits",
    "threads": "Worker Threads",
    "pointer_size": "Architecture Bits",
    "cmd_set": "SET Commands",
    "libevent": "Libevent Version",
    "cas_badval": "CAS Value Mismatches",
    "hash_bytes": "Hash Table Memory",
    "curr_connections": "Current Connections",
    "total_connections": "Total Connections",
    "decr_misses": "DECREMENT Misses",
    "rusage_system": "System CPU Time",
    "max_connections": "Max Connections",
    "direct_reclaims": "Direct Reclaims",
    "moves_to_cold": "Moves To Cold",
    "moves_to_warm": "Moves To Warm",
    "moves_within_lru": "Moves Within LRU",
    "rejected_connections": "Rejected Connections",
    "store_no_memory": "Store No Memory",
    "store_too_large": "Store Too Large",
    "uptime": "Uptime",
    "evicted_active": "Evicted Active",
    "lru_crawler_starts": "LRU Crawler Starts",
    "crawler_items_checked": "Crawler Items Checked"
}


class MemcachedMonitor:

    def __init__(self, args):
        self.maindata = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
            'units': METRICS_UNITS,
            'tabs': {
                'Memory & Storage': {
                    'order': 1,
                    'tablist': [
                        'Active Slab Classes',
                        'Slab Memory Allocated',
                        'Slabs Total Pages',
                        'Slabs Total Chunks',
                        'Slabs Used Chunks',
                        'Slabs Free Chunks',
                        'Slabs Free Chunks End',
                        'Slab Memory Requested',
                        'Hash Table Memory',
                        'Hash Power Level',
                        'Hash Is Expanding',
                        'Memory Allocation Failures',
                        'Store No Memory',
                        'Store Too Large',
                        'Slabs Chunk Size',
                        'Slabs Chunks Per Page'
                    ]
                },
                'Operations': {
                    'order': 2,
                    'tablist': [
                        'GET Commands',
                        'SET Commands',
                        'FLUSH Commands',
                        'TOUCH Commands',
                        'GET Hits',
                        'GET Misses',
                        'DELETE Hits',
                        'DELETE Misses',
                        'INCREMENT Hits',
                        'INCREMENT Misses',
                        'DECREMENT Hits',
                        'DECREMENT Misses',
                        'CAS Hits',
                        'CAS Misses',
                        'CAS Value Mismatches',
                        'TOUCH Hits',
                        'TOUCH Misses',
                        'Total Items',
                        'AUTH Commands',
                        'AUTH Errors'
                    ]
                },
                'Eviction': {
                    'order': 3,
                    'tablist': [
                        'Evicted Active',
                        'Evicted Unfetched',
                        'Expired Unfetched',
                        'Expired Items Reclaimed',
                        'Evicted With Expiry',
                        'Last Evicted Item Age',
                        'Out Of Memory Errors'
                    ]
                },
                'LRU': {
                    'order': 4,
                    'tablist': [
                        'Moves To Cold',
                        'Moves To Warm',
                        'Moves Within LRU',
                        'Hot LRU Items',
                        'Warm LRU Items',
                        'Cold LRU Items',
                        'Non-Expiring Items',
                        'Oldest Item Age',
                        'LRU Tail Repairs',
                        'LRU Crawler Starts',
                        'LRU Tail Relocked',
                        'LRU Crawler Reclaimed',
                        'Crawler Items Checked',
                        'Direct Reclaims'
                    ]
                },
                'Connections': {
                    'order': 5,
                    'tablist': [
                        'Total Connections',
                        'Rejected Connections',
                        'Connection Structures',
                        'Connection Yields',
                        'Accepting Connections',
                        'Reserved File Descriptors',
                        'Listener Disabled Count'
                    ]
                }
            }
        }
        self.host = args.host
        self.port = args.port
        self.username = getattr(args, 'username', None)
        self.password = getattr(args, 'password', None)

    def append_error(self, msg):
        self.maindata['status'] = 0
        if 'msg' in self.maindata:
            self.maindata['msg'] = self.maindata['msg'] + '; ' + msg
        else:
            self.maindata['msg'] = msg

    def metriccollector(self):
        try:
            import bmemcached
        except ImportError as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            return self.maindata

        try:
            server = '%s:%s' % (self.host, self.port)
            if self.username and self.password:
                mc = bmemcached.Client((server,), username=self.username, password=self.password)
            else:
                mc = bmemcached.Client((server,))

            all_stats = mc.stats()

            if all_stats:
                # bmemcached returns {server: {key: val}}
                value_dict = {}
                for server_key, data in all_stats.items():
                    value_dict = data

                if value_dict:
                    for k, v in value_dict.items():
                        k = k if isinstance(k, str) else k.decode()
                        v = v if isinstance(v, str) else v.decode()
                        if k in BYTES_TO_MB_LIST and k in KEYS:
                            v = self.convertBytesToMB(v)
                            self.maindata[KEYS[k]] = v
                        elif k in KEYS:
                            if k not in STRING_KEYS:
                                try:
                                    v = int(v)
                                except ValueError:
                                    try:
                                        v = float(v)
                                    except ValueError:
                                        pass
                            self.maindata[KEYS[k]] = v

                if 'PID' in self.maindata:
                    self.maindata['PID'] = 'Process_' + str(self.maindata['PID'])

                # Convert seconds to minutes
                for sec_key in ['User CPU Time', 'System CPU Time', 'Uptime']:
                    if sec_key in self.maindata:
                        self.maindata[sec_key] = round(self.maindata[sec_key] / 60, 2)

                # Convert configuration values to descriptive strings
                if 'Max Memory Limit' in self.maindata:
                    self.maindata['Max Memory Limit'] = str(self.maindata['Max Memory Limit']) + ' MB'
                if 'Max Connections' in self.maindata:
                    self.maindata['Max Connections'] = str(self.maindata['Max Connections']) + ' Connections'
                if 'Architecture Bits' in self.maindata:
                    self.maindata['Architecture Bits'] = str(self.maindata['Architecture Bits']) + ' bits'
                if 'Worker Threads' in self.maindata:
                    self.maindata['Worker Threads'] = str(self.maindata['Worker Threads']) + ' Threads'

                # Computed metrics
                try:
                    bytes_used = float(value_dict.get('bytes', 0))
                    curr_items = float(value_dict.get('curr_items', 0))
                    limit_maxbytes = float(value_dict.get('limit_maxbytes', 0))
                    get_hits = float(value_dict.get('get_hits', 0))
                    get_misses = float(value_dict.get('get_misses', 0))

                    if curr_items > 0:
                        avg_bytes = bytes_used / curr_items
                        self.maindata['Avg Item Size'] = round(avg_bytes / (1024 * 1024), 2)
                    else:
                        self.maindata['Avg Item Size'] = 0

                    if limit_maxbytes > 0:
                        self.maindata['Memory Usage Percent'] = round((bytes_used / limit_maxbytes) * 100, 2)
                    else:
                        self.maindata['Memory Usage Percent'] = 0

                    total_gets = get_hits + get_misses
                    if total_gets > 0:
                        self.maindata['Cache Hit Rate'] = round((get_hits / total_gets) * 100, 2)
                    else:
                        self.maindata['Cache Hit Rate'] = 0
                except Exception as e:
                    self.append_error('Error computing metrics: ' + str(e))
                    return self.maindata

                # Items stats (aggregated across all slab classes)
                ITEMS_KEYS = {
                    'age': 'Oldest Item Age',
                    'evicted_nonzero': 'Evicted With Expiry',
                    'evicted_time': 'Last Evicted Item Age',
                    'number_cold': 'Cold LRU Items',
                    'number_hot': 'Hot LRU Items',
                    'number_noexp': 'Non-Expiring Items',
                    'number_warm': 'Warm LRU Items',
                    'outofmemory': 'Out Of Memory Errors',
                    'tailrepairs': 'LRU Tail Repairs'
                }

                for item_display in ITEMS_KEYS.values():
                    self.maindata[item_display] = 0

                try:
                    items_stats = mc.stats('items')
                    if items_stats:
                        max_keys = {'age', 'evicted_time'}
                        for server_key, iv in items_stats.items():
                            for item_key, item_val in iv.items():
                                item_key = item_key if isinstance(item_key, str) else item_key.decode()
                                item_val = item_val if isinstance(item_val, str) else item_val.decode()
                                # Keys are like 'items:1:age', extract the metric name
                                parts = item_key.split(':')
                                if len(parts) == 3:
                                    metric = parts[2]
                                    if metric in ITEMS_KEYS:
                                        val = int(item_val)
                                        display = ITEMS_KEYS[metric]
                                        if metric in max_keys:
                                            self.maindata[display] = max(self.maindata[display], val)
                                        else:
                                            self.maindata[display] += val
                except Exception as e:
                    self.append_error('Error fetching items stats: ' + str(e))
                    return self.maindata

                # Convert items time metrics from seconds to minutes
                for sec_key in ['Oldest Item Age', 'Last Evicted Item Age']:
                    if sec_key in self.maindata:
                        self.maindata[sec_key] = round(self.maindata[sec_key] / 60, 2)

                # Slabs stats (aggregated across all slab classes)
                SLABS_KEYS = {
                    'free_chunks': 'Slabs Free Chunks',
                    'free_chunks_end': 'Slabs Free Chunks End',
                    'total_chunks': 'Slabs Total Chunks',
                    'total_pages': 'Slabs Total Pages',
                    'used_chunks': 'Slabs Used Chunks',
                    'mem_requested': 'Slab Memory Requested',
                    'chunk_size': 'Slabs Chunk Size',
                    'chunks_per_page': 'Slabs Chunks Per Page'
                }

                self.maindata['Active Slab Classes'] = 0
                self.maindata['Slab Memory Allocated'] = 0
                for slab_display in SLABS_KEYS.values():
                    self.maindata[slab_display] = 0

                try:
                    slabs_stats = mc.stats('slabs')
                    if slabs_stats:
                        for server_key, sv in slabs_stats.items():
                            for slab_key, slab_val in sv.items():
                                slab_key = slab_key if isinstance(slab_key, str) else slab_key.decode()
                                slab_val = slab_val if isinstance(slab_val, str) else slab_val.decode()
                                if slab_key == 'active_slabs':
                                    self.maindata['Active Slab Classes'] = int(slab_val)
                                elif slab_key == 'total_malloced':
                                    self.maindata['Slab Memory Allocated'] = self.convertBytesToMB(slab_val)
                                else:
                                    parts = slab_key.split(':')
                                    if len(parts) == 2:
                                        metric = parts[1]
                                        if metric in SLABS_KEYS:
                                            val = int(slab_val)
                                            self.maindata[SLABS_KEYS[metric]] += val

                    self.maindata['Slab Memory Requested'] = self.convertBytesToMB(self.maindata['Slab Memory Requested'])
                    self.maindata['Slabs Chunk Size'] = self.convertBytesToMB(self.maindata['Slabs Chunk Size'])

                except Exception as e:
                    self.append_error('Error fetching slabs stats: ' + str(e))
                    return self.maindata
            else:
                self.append_error('Unable to fetch memcached stats')

            if mc is not None:
                mc.disconnect_all()
                mc = None

        except Exception as e:
            self.append_error(str(e))

        return self.maindata

    def convertBytesToMB(self, v):
        try:
            byte_s = float(v)
            kilobytes = byte_s / 1024
            megabytes = kilobytes / 1024
            v = round(megabytes, 2)
        except Exception as e:
            v = 0
        return v


if __name__ == "__main__":
    host = "127.0.0.1"
    port = "11211"

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Memcached host', default=host)
    parser.add_argument('--port', help='Memcached port', default=port)
    parser.add_argument('--username', help='SASL username', default=None)
    parser.add_argument('--password', help='SASL password', default=None)
    args = parser.parse_args()

    obj = MemcachedMonitor(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=4, sort_keys=True))
