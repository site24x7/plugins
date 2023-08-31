#!/usr/bin/python3
import json


PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={
    "ISR Shrinks Per Sec":"/sec",
    "ISR Expands Per Sec":"/sec",
    "Leader Election Rate And Time Ms":"/ms",
    "Unclean Leader Elections Per Sec":"/sec",
    "Bytes In Per Sec":"/sec",
    "Bytes Out Per Sec":"/sec",
    "Network Request Rate":"/sec",
    "Network Error Rate":"/sec"
}

class kafka:

    def __init__(self,args):

        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.kafka_host=args.kafka_host
        self.kafka_jmx_port=args.kafka_jmx_port
        self.kafka_consumer_partition=int(args.kafka_consumer_partition)
        self.kafka_topic_name=args.kafka_topic_name
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path


    def metriccollector(self):

        try:
            global jmx
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.kafka_host}:{self.kafka_jmx_port}/jmxrmi")
            metric_queries={

                "Under Replicated Partitions":"kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions",
                "ISR Shrinks Per Sec":"kafka.server:type=ReplicaManager,name=IsrShrinksPerSec/Count",
                "ISR Expands Per Sec":"kafka.server:type=ReplicaManager,name=IsrExpandsPerSec/Count",
                "Active Controller Count" : "kafka.controller:type=KafkaController,name=ActiveControllerCount",
                "Offline Partitions Count" : "kafka.controller:type=KafkaController,name=OfflinePartitionsCount",
                "Leader Election Rate And Time Ms" : "kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs/Count",
                "Unclean Leader Elections Per Sec" : "kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec/Count",
                "Total Time Ms" : "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce/Count",
                "Purgatory Size":"kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,delayedOperation=Produce",
                "Bytes In Per Sec":"kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec/Count",
                "Bytes Out Per Sec":"kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec/Count",
                "Network Request Rate":"kafka.network:type=RequestMetrics,name=RequestsPerSec,request=Produce,version=9/Count",
                "Network Error Rate":"kafka.network:type=RequestMetrics,name=ErrorsPerSec,request=Produce,error=NONE/Count",
                "Total Broker Partitions":"kafka.server:type=ReplicaManager,name=PartitionCount/Value",
                "Young Generation GC Count":"java.lang:type=GarbageCollector,name=G1 Young Generation/CollectionCount",
                "Young Generation GC Time":"java.lang:type=GarbageCollector,name=G1 Young Generation/CollectionTime",
                "Old Generation GC Count":"java.lang:type=GarbageCollector,name=G1 Old Generation/CollectionCount",
                "Old Generation GC Time":"java.lang:type=GarbageCollector,name=G1 Old Generation/CollectionTime",
                f"Log End Offset(Partition : {self.kafka_consumer_partition})":f"kafka.log:type=Log,name=LogEndOffset,topic={self.kafka_topic_name},partition={self.kafka_consumer_partition}"

                }


            for metric in metric_queries:

                jmxQuery = [jmx.JMXQuery(metric_queries[metric])]
                metric_result = jmxConnection.query(jmxQuery)
                if metric_result:
                    self.maindata[metric]=metric_result[0].value

            self.maindata["Topic Name"]=self.kafka_topic_name
            self.maindata["Partition No."]=f"Partition No : {self.kafka_consumer_partition}"



            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                    applog["logs_enabled"]=True
                    applog["log_type_name"]=self.logtypename
                    applog["log_file_path"]=self.logfilepath
            else:
                    applog["logs_enabled"]=False

            self.maindata['applog'] = applog
            self.maindata['tags']=f"Kafka_Broker_Host:{self.kafka_host},Kafka_Topic:{self.kafka_topic_name}"


        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata


        return self.maindata


if __name__=="__main__":

    kafka_host="localhost"
    kafka_jmx_port=9999
    kafka_consumer_partition=0
    kafka_topic_name="quickstart-events"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_host', help='host name to access the kafka server metrics',default=kafka_host)
    parser.add_argument('--kafka_jmx_port', help='jmx port to access the kafka server metrics',default=kafka_jmx_port)
    parser.add_argument('--kafka_consumer_partition', help='partition to monitor the metrics',default=kafka_consumer_partition)
    parser.add_argument('--kafka_topic_name', help='kafka topic name',default=kafka_topic_name)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
