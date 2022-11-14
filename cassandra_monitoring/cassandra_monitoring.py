#!/usr/bin/python3

import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={
    "CMS garbage collections (time)":"ms",
    "ParNew garbage collections (time)":"ms",
    "Total Latency (Read)":"us",
    "Total Latency (Write)":"us",
    "Cross Node Latency":"us"

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
                "Throughtput (Writes)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency",
                "Throughtput (Read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency",
                "Key cache hit rate":"org.apache.cassandra.metrics:type=Cache,scope=KeyCache,name=Hits/Count",
                "Load":"org.apache.cassandra.metrics:type=Storage,name=Load",
                "Completed compaction tasks":"org.apache.cassandra.metrics:type=Compaction,name=CompletedTasks",
                "Pending campaction tasks":"org.apache.cassandra.metrics:type=Compaction,name=PendingTasks",
                "ParNew garbage collections (count)":"java.lang:type=GarbageCollector,name=ParNew/CollectionCount",
                "ParNew garbage collections (time)":"java.lang:type=GarbageCollector,name=ParNew/CollectionTime",
                "CMS garbage collections (count)":"java.lang:type=GarbageCollector,name=ConcurrentMarkSweep/CollectionCount",
                "CMS garbage collections (time)":"java.lang:type=GarbageCollector,name=ConcurrentMarkSweep/CollectionTime",
                "Exceptions":"org.apache.cassandra.metrics:type=Storage,name=Exceptions",
                "Timeout exceptions (write)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Timeouts/Count",
                "Timeout exception (read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Timeouts/Count",
                "Unavailable exceptions (write)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Unavailables/Count",
                "Unavailable exceptions (read)":"org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Unavailables/Count",
                "Pending tasks" :"org.apache.cassandra.metrics:type=Compaction,name=PendingTasks",
                "Dropped Mutations":"org.apache.cassandra.metrics:type=Table,name=DroppedMutations",
                "Pending Flushes":"org.apache.cassandra.metrics:type=Table,name=PendingFlushes",
                "Blocked On Allocation":"org.apache.cassandra.metrics:type=MemtablePool,name=BlockedOnAllocation/Count",
                "Currently Blocked Tasks":"org.apache.cassandra.metrics:type=ThreadPools,path=internal,scope=MemtableFlushWriter,name=CurrentlyBlockedTasks"
                
            }

            for metric in metric_queries:
                    
                jmxQuery = [jmx.JMXQuery(metric_queries[metric])]
                metric_result = jmxConnection.query(jmxQuery)
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
