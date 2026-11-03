#!/usr/bin/python3

import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={
    "CMS garbage collections (time)":"ms",
    "ParNew garbage collections (time)":"ms",
    "Total Latency (Read)":"us",
    "Total Latency (Write)":"us",
    "Cross Node Latency":"us",
    "Read Latency 75th Percentile":"us",
    "Read Latency 95th Percentile":"us",
    "Read Latency 99th Percentile":"us",
    "Write Latency 75th Percentile":"us",
    "Write Latency 95th Percentile":"us",
    "Write Latency 99th Percentile":"us",
    "CAS Commit Latency 75th Percentile":"us",
    "CAS Commit Latency 95th Percentile":"us",
    "CAS Prepare Latency 75th Percentile":"us",
    "CAS Prepare Latency 95th Percentile":"us",
    "CAS Propose Latency 75th Percentile":"us",
    "CAS Propose Latency 95th Percentile":"us",
    "View Lock Acquire Time 75th Percentile":"us",
    "View Lock Acquire Time 95th Percentile":"us",
    "View Read Time 75th Percentile":"us",
    "View Read Time 95th Percentile":"us",
    "Col Update Time Delta 75th Percentile":"us",
    "Col Update Time Delta 95th Percentile":"us",
    "Col Update Time Delta Min":"us",
    "Live Disk Space Used":"bytes",
    "Total Disk Space Used":"bytes",
    "Compaction Bytes Written":"bytes",
    "Bytes Flushed":"bytes",
    "Max Partition Size":"bytes",
    "Max Row Size":"bytes",
    "Mean Partition Size":"bytes",
    "Mean Row Size":"bytes",
    "Total Commit Log Size":"bytes",
    "Snapshots Size":"bytes",
    "Oldest Task Queue Time":"ms"
}


class cassandra:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        self.hostname=args.hostname
        self.port=args.port
        
    def metriccollector(self):

        try:
            global jmx
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.hostname}:{self.port}/jmxrmi")
            metric_queries={
                
                "Total Latency (Read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=TotalLatency",
                "Total Latency (Write)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=TotalLatency",
                "Cross Node Latency":"org.apache.cassandra.metrics:type=Messaging,name=CrossNodeLatency/Count",
                "Total Hints":"org.apache.cassandra.metrics:type=Storage,name=TotalHints",
                "Throughput (Writes)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/Count",
                "Throughput (Read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/Count",
                "Key Cache Hit Rate":"org.apache.cassandra.metrics:type=Cache,scope=KeyCache,name=HitRate/Value",
                "Load":"org.apache.cassandra.metrics:type=Storage,name=Load",
                "Completed Compaction Tasks":"org.apache.cassandra.metrics:type=Compaction,name=CompletedTasks",
                "Pending Compaction Tasks":"org.apache.cassandra.metrics:type=Compaction,name=PendingTasks",
                "ParNew garbage collections (count)":"java.lang:type=GarbageCollector,name=ParNew/CollectionCount",
                "ParNew garbage collections (time)":"java.lang:type=GarbageCollector,name=ParNew/CollectionTime",
                "CMS garbage collections (count)":"java.lang:type=GarbageCollector,name=ConcurrentMarkSweep/CollectionCount",
                "CMS garbage collections (time)":"java.lang:type=GarbageCollector,name=ConcurrentMarkSweep/CollectionTime",
                "Exceptions":"org.apache.cassandra.metrics:type=Storage,name=Exceptions",
                "Timeout Exceptions (Write)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Timeouts/Count",
                "Timeout Exceptions (Read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Timeouts/Count",
                "Unavailable Exceptions (Write)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Unavailables/Count",
                "Unavailable Exceptions (Read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Unavailables/Count",
                "Dropped Mutations":"org.apache.cassandra.metrics:type=Table,name=DroppedMutations",
                "Pending Flushes":"org.apache.cassandra.metrics:type=Table,name=PendingFlushes",
                "Blocked On Allocation":"org.apache.cassandra.metrics:type=MemtablePool,name=BlockedOnAllocation/Count",
                "Currently Blocked Tasks":"org.apache.cassandra.metrics:type=ThreadPools,path=internal,scope=MemtableFlushWriter,name=CurrentlyBlockedTasks",

                "Read Latency 75th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/75thPercentile",
                "Read Latency 95th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/95thPercentile",
                "Read Latency 99th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/99thPercentile",
                "Read Requests One Minute Rate":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/OneMinuteRate",
                "Write Latency 75th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/75thPercentile",
                "Write Latency 95th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/95thPercentile",
                "Write Latency 99th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/99thPercentile",
                "Write Requests One Minute Rate":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/OneMinuteRate",

                "Active Tasks":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=ActiveTasks/Value",
                "Completed Tasks":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=CompletedTasks/Value",
                "Currently Blocked Tasks (Transport)":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=CurrentlyBlockedTasks/Count",
                "Max Pool Size":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=MaxPoolSize/Value",
                "Max Tasks Queued":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=MaxTasksQueued/Value",
                "Oldest Task Queue Time":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=OldestTaskQueueTime/Value",
                "Pending Tasks":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=PendingTasks/Value",
                "Total Blocked Tasks":"org.apache.cassandra.metrics:type=ThreadPools,path=transport,scope=Native-Transport-Requests,name=TotalBlockedTasks/Count",
                "Dropped One Minute Rate":"org.apache.cassandra.metrics:type=DroppedMessage,scope=MUTATION,name=Dropped/OneMinuteRate",

                "Live Disk Space Used":"org.apache.cassandra.metrics:type=Table,name=LiveDiskSpaceUsed",
                "Total Disk Space Used":"org.apache.cassandra.metrics:type=Table,name=TotalDiskSpaceUsed",
                "Live SSTable Count":"org.apache.cassandra.metrics:type=Table,name=LiveSSTableCount",
                "Compression Ratio":"org.apache.cassandra.metrics:type=Table,name=CompressionRatio",
                "Total Commit Log Size":"org.apache.cassandra.metrics:type=CommitLog,name=TotalCommitLogSize/Value",
                
                "Row Cache Hits":"org.apache.cassandra.metrics:type=Cache,scope=RowCache,name=Hits/Count",
                "Row Cache Misses":"org.apache.cassandra.metrics:type=Cache,scope=RowCache,name=Misses/Count",
                "Row Cache Hit Out Of Range":"org.apache.cassandra.metrics:type=ColumnFamily,name=RowCacheHitOutOfRange/Value",
                
                "Compaction Bytes Written":"org.apache.cassandra.metrics:type=Compaction,name=BytesCompacted/Count",
                "Bytes Flushed":"org.apache.cassandra.metrics:type=Table,name=BytesFlushed/Value",
                "SSTables Per Read 75th Percentile":"org.apache.cassandra.metrics:type=Table,name=SSTablesPerReadHistogram/75thPercentile",
                "SSTables Per Read 95th Percentile":"org.apache.cassandra.metrics:type=Table,name=SSTablesPerReadHistogram/95thPercentile",
                "Max Partition Size":"org.apache.cassandra.metrics:type=Table,name=MaxPartitionSize/Value",
                "Max Row Size":"org.apache.cassandra.metrics:type=ColumnFamily,name=MaxRowSize/Value",
                "Mean Partition Size":"org.apache.cassandra.metrics:type=Table,name=MeanPartitionSize/Value",
                "Mean Row Size":"org.apache.cassandra.metrics:type=ColumnFamily,name=MeanRowSize/Value",
                
                "Tombstone Scanned 75th Percentile":"org.apache.cassandra.metrics:type=Table,name=TombstoneScannedHistogram/75thPercentile",
                "Tombstone Scanned 95th Percentile":"org.apache.cassandra.metrics:type=Table,name=TombstoneScannedHistogram/95thPercentile",
                "Bloom Filter False Ratio":"org.apache.cassandra.metrics:type=Table,name=BloomFilterFalseRatio",
                
                "Timeout One Minute Rate (Read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Timeouts/OneMinuteRate",
                "Timeout One Minute Rate (Write)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Timeouts/OneMinuteRate",
                
                "Snapshots Size":"org.apache.cassandra.metrics:type=Table,name=SnapshotsSize",
                
                "CAS Commit Latency 75th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASWrite,name=Latency/75thPercentile",
                "CAS Commit Latency 95th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASWrite,name=Latency/95thPercentile",
                "CAS Commit One Minute Rate":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASWrite,name=Latency/OneMinuteRate",
                "CAS Prepare Latency 75th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASRead,name=Latency/75thPercentile",
                "CAS Prepare Latency 95th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASRead,name=Latency/95thPercentile",
                "CAS Prepare One Minute Rate":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASRead,name=Latency/OneMinuteRate",
                "CAS Propose Latency 75th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASWrite,name=ContentionHistogram/75thPercentile",
                "CAS Propose Latency 95th Percentile":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASWrite,name=ContentionHistogram/95thPercentile",
                "CAS Propose One Minute Rate":"org.apache.cassandra.metrics:type=ClientRequest,scope=CASWrite,name=ContentionHistogram/Count",
            
                "View Lock Acquire Time 75th Percentile":"org.apache.cassandra.metrics:type=Table,name=ViewLockAcquireTime/75thPercentile",
                "View Lock Acquire Time 95th Percentile":"org.apache.cassandra.metrics:type=Table,name=ViewLockAcquireTime/95thPercentile",
                "View Lock Acquire One Minute Rate":"org.apache.cassandra.metrics:type=Table,name=ViewLockAcquireTime/OneMinuteRate",
                "View Read Time 75th Percentile":"org.apache.cassandra.metrics:type=Table,name=ViewReadTime/75thPercentile",
                "View Read Time 95th Percentile":"org.apache.cassandra.metrics:type=Table,name=ViewReadTime/95thPercentile",
                "View Read One Minute Rate":"org.apache.cassandra.metrics:type=Table,name=ViewReadTime/OneMinuteRate",
                
                "Col Update Time Delta 75th Percentile":"org.apache.cassandra.metrics:type=Table,name=ColUpdateTimeDeltaHistogram/75thPercentile",
                "Col Update Time Delta 95th Percentile":"org.apache.cassandra.metrics:type=Table,name=ColUpdateTimeDeltaHistogram/95thPercentile",
                "Col Update Time Delta Min":"org.apache.cassandra.metrics:type=Table,name=ColUpdateTimeDeltaHistogram/Min"
                
            }

            for metric in metric_queries:
                    
                jmxQuery = [jmx.JMXQuery(metric_queries[metric])]
                metric_result = jmxConnection.query(jmxQuery)
                if metric_result:
                    self.maindata[metric]=metric_result[0].value
            self.maindata["Cassandra Host Name"]=self.hostname

            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                    applog["logs_enabled"]=True
                    applog["log_type_name"]=self.logtypename
                    applog["log_file_path"]=self.logfilepath
            else:
                    applog["logs_enabled"]=False
            self.maindata['applog'] = applog
            self.maindata['tabs']={    
                    "Latency":{
                        "order":1,
                        "tablist":[
                            "Read Latency 75th Percentile",
                            "Read Latency 95th Percentile",
                            "Read Latency 99th Percentile",
                            "Write Latency 75th Percentile",
                            "Write Latency 95th Percentile",
                            "Write Latency 99th Percentile",
                            "Read Requests One Minute Rate",
                            "Write Requests One Minute Rate",
                            "Total Latency (Read)",
                            "Total Latency (Write)",
                            "Cross Node Latency",
                            "CAS Commit Latency 75th Percentile",
                            "CAS Commit Latency 95th Percentile",
                            "CAS Commit One Minute Rate",
                            "CAS Prepare Latency 75th Percentile",
                            "CAS Prepare Latency 95th Percentile",
                            "CAS Prepare One Minute Rate",
                            "CAS Propose Latency 75th Percentile",
                            "CAS Propose Latency 95th Percentile",
                            "CAS Propose One Minute Rate",
                            "View Lock Acquire Time 75th Percentile",
                            "View Lock Acquire Time 95th Percentile",
                            "View Lock Acquire One Minute Rate",
                            "View Read Time 75th Percentile",
                            "View Read Time 95th Percentile",
                            "View Read One Minute Rate",
                            "Col Update Time Delta 75th Percentile",
                            "Col Update Time Delta 95th Percentile",
                            "Col Update Time Delta Min"
                        ]
                    },
                    
                    "Storage":{
                        "order":2,
                        "tablist":[
                            "Live Disk Space Used",
                            "Total Disk Space Used",
                            "Live SSTable Count",
                            "Compression Ratio",
                            "Total Commit Log Size",
                            "Snapshots Size",
                            "Compaction Bytes Written",
                            "Bytes Flushed",
                            "Completed Compaction Tasks",
                            "Pending Compaction Tasks",
                            "Max Partition Size",
                            "Mean Partition Size",
                            "Max Row Size",
                            "Mean Row Size",
                            "SSTables Per Read 75th Percentile",
                            "SSTables Per Read 95th Percentile",
                            "Tombstone Scanned 75th Percentile",
                            "Tombstone Scanned 95th Percentile",
                            "Bloom Filter False Ratio"
                        ]
                    },
                    
                    "Cache":{
                        "order":3,
                        "tablist":[
                            "Key Cache Hit Rate",
                            "Row Cache Hits",
                            "Row Cache Misses",
                            "Row Cache Hit Out Of Range"
                        ]
                    },
                    
                    "Threads":{
                        "order":4,
                        "tablist":[
                            "Active Tasks",
                            "Completed Tasks",
                            "Pending Tasks",
                            "Currently Blocked Tasks (Transport)",
                            "Currently Blocked Tasks",
                            "Total Blocked Tasks",
                            "Max Pool Size",
                            "Max Tasks Queued",
                            "Oldest Task Queue Time",
                            "Blocked On Allocation",
                            "Dropped Mutations",
                            "Pending Flushes",
                            "Total Hints"
                        ]
                    },
                    
                    "Errors":{
                        "order":5,
                        "tablist":[
                            "Exceptions",
                            "Timeout Exceptions (Read)",
                            "Timeout Exceptions (Write)",
                            "Unavailable Exceptions (Read)",
                            "Unavailable Exceptions (Write)",
                            "Timeout One Minute Rate (Read)",
                            "Timeout One Minute Rate (Write)",
                            "Dropped One Minute Rate",
                            "ParNew garbage collections (count)",
                            "ParNew garbage collections (time)",
                            "CMS garbage collections (count)",
                            "CMS garbage collections (time)"
                        ]
                    }
                }
            

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata


if __name__=="__main__":
    
    hostname="localhost"
    port="7199"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--hostname', help='host of cassandra',default=hostname)
    parser.add_argument('--port', help='enable log collection for this plugin application',default=port)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=cassandra(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
