#!/usr/bin/python
'''
Site24x7 Plugin to monitor Clickhouse Asynchronous metrics
'''

from clickhouse_driver import Client
import json
import argparse


### Query: SELECT metric,value FROM system.asynchronous_metrics
### Ignored metrics
### "MaxPartCountForPartition", "MemoryCode", "MemoryDataAndStack","UncompressedCacheCells","jemalloc.active","jemalloc.arenas.all.muzzy_purged", 
### "jemalloc.arenas.all.pactive", "jemalloc.arenas.all.pdirty", "jemalloc.arenas.all.pmuzzy", "jemalloc.background_thread.num_runs", 
### "jemalloc.background_thread.run_intervals", "jemalloc.epoch", "jemalloc.mapped", "jemalloc.metadata","jemalloc.metadata_thp",

METRICS = [ "CompiledExpressionCacheCount", "MarkCacheBytes", "MarkCacheFiles", "MemoryResident", 
           "MemoryShared", "MemoryVirtual", "NumberOfDatabases", "NumberOfTables", "ReplicasMaxAbsoluteDelay", "ReplicasMaxInsertsInQueue", "ReplicasMaxMergesInQueue", 
           "ReplicasMaxQueueSize", "ReplicasMaxRelativeDelay", "ReplicasSumInsertsInQueue", "ReplicasSumMergesInQueue", "ReplicasSumQueueSize", "UncompressedCacheBytes",
            "Uptime", "jemalloc.allocated", "jemalloc.arenas.all.dirty_purged", 
            "jemalloc.background_thread.num_threads",  "jemalloc.resident", "jemalloc.retained" ]




class ClickHouse:
    def __init__(self) :
        pass
    
    def _connect_(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--hostname', help='hostname', nargs='?', default='localhost')
        parser.add_argument('--port', help='port number', type=int, nargs='?', default=9000)
        parser.add_argument('--database', help='database',  nargs='?', default='default')
        parser.add_argument('--user', help='user',  nargs='?', default='default')
        parser.add_argument('--password', help='password',  nargs='?', default='')
        parser.add_argument('--timeout', help='connection timeout', type=int,  nargs='?', default=10)
        args = parser.parse_args()
        return Client(host=args.hostname, port=args.port, database=args.database,user=args.user,password=args.password,connect_timeout=args.timeout)
        
    def _get_data_(self):
        QUERY = 'SELECT metric,value FROM system.asynchronous_metrics'
        connection = self._connect_()
        self.metrics = dict(connection.execute(QUERY))
        connection.disconnect()
        
        data = {}
        for key in self.metrics:
            if key in METRICS : data[key] = self.metrics[key]
    
        return dict(data)     
    
if __name__ == '__main__':
    clickhouse = ClickHouse()
    result = clickhouse._get_data_()
    print(json.dumps(result, indent=4, sort_keys=True))
