#!/usr/bin/python3
import json
import subprocess

PLUGIN_VERSION=1
HEARTBEAT=True

class kafka:

    def __init__(self,args):

        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.kafka_home=args.kafka_home
        self.kafka_host=args.kafka_host
        self.kafka_jmx_port=args.kafka_jmx_port
        
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path


    def execute_command(self,cmd, need_out=False):
        try:
            if not isinstance(cmd, list):
                cmd=cmd.split()
            
            result=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(f"    {cmd} execution failed with return code {result.returncode}")
                print(f"    {str(result.stderr)}")
                return False
            if need_out:
                return result.stdout
            return True
        except Exception as e:
            return False
        


    def metriccollector(self):

        try:
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.kafka_host}:{self.kafka_jmx_port}/jmxrmi")
            metric_queries={

            "broker_topic_metrics":{
                "Bytes In Per Sec":"kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec/Count (Long)",
                "Bytes Out Per Sec":"kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec",
                "Bytes Rejected Per Sec":"kafka.server:type=BrokerTopicMetrics,name=BytesRejectedPerSec",
                "Failed Fetch Requests Per Sec":"kafka.server:type=BrokerTopicMetrics,name=FailedFetchRequestsPerSec",
                "Failed Produce Requests Per Sec":"kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec",
                "Fetch Message Conversions Per Sec":"kafka.server:type=BrokerTopicMetrics,name=FetchMessageConversionsPerSec",
                "Invalid Magic Number Records Per Sec":"kafka.server:type=BrokerTopicMetrics,name=InvalidMagicNumberRecordsPerSec",
                "Invalid Message Crc Records Per Sec":"kafka.server:type=BrokerTopicMetrics,name=InvalidMessageCrcRecordsPerSec",
                "Invalid Offset Or Sequence Records Per Sec":"kafka.server:type=BrokerTopicMetrics,name=InvalidOffsetOrSequenceRecordsPerSec",
                "No Key Compacted Topic Records Per Sec":"kafka.server:type=BrokerTopicMetrics,name=NoKeyCompactedTopicRecordsPerSec",
                "Produce Message Conversions Per Sec":"kafka.server:type=BrokerTopicMetrics,name=ProduceMessageConversionsPerSec",
                "Reassignment Bytes In Per Sec":"kafka.server:type=BrokerTopicMetrics,name=ReassignmentBytesInPerSec",
                "Reassignment Bytes Out Per Sec":"kafka.server:type=BrokerTopicMetrics,name=ReassignmentBytesOutPerSec",
                "Replication Bytes In Per Sec":"kafka.server:type=BrokerTopicMetrics,name=ReplicationBytesInPerSec",
                "Total Fetch Requests Per Sec":"kafka.server:type=BrokerTopicMetrics,name=TotalFetchRequestsPerSec",
                "Total Produce Requests Per Sec":"kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec"
            },

            "replication_manager":{
                "At Min Isr Partition Count":"kafka.server:type=ReplicaManager,name=AtMinIsrPartitionCount",
                "Failed Isr Updates Per Sec":"kafka.server:type=ReplicaManager,name=FailedIsrUpdatesPerSec",
                "Isr Shrinks Per Sec":"kafka.server:type=ReplicaManager,name=IsrShrinksPerSec",
                "Leader Count":"kafka.server:type=ReplicaManager,name=LeaderCount",
                "Partition Count":"kafka.server:type=ReplicaManager,name=PartitionCount",
                "Partitions With Late Transactions Count":"kafka.server:type=ReplicaManager,name=PartitionsWithLateTransactionsCount",
                "Producer Id Count":"kafka.server:type=ReplicaManager,name=ProducerIdCount",
                "Reassigning Partitions":"kafka.server:type=ReplicaManager,name=ReassigningPartitions",
                "Under Min Isr Partition Count":"kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount",
                "Under Replicated Partitions":"kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions"
            },

            "controller_metrics":{
                "Active Controller Count":"kafka.controller:type=KafkaController,name=ActiveControllerCount",
                "Offline Partitions Count":"kafka.controller:type=KafkaController,name=OfflinePartitionsCount",
                "Leader Election Rate ":"kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs/Count",
                "Total Topics Count": "kafka.controller:type=KafkaController,name=GlobalTopicCount",
            },
            }

            for metric_type in metric_queries:
                 for metrics in metric_queries[metric_type]:
                      query=metric_queries[metric_type][metrics]
                      jmxQuery = [jmx.JMXQuery(query)]
                      metric_result = jmxConnection.query(jmxQuery)
                      if metric_result:
                        self.maindata[metrics]=metric_result[0].value

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
        
        self.maindata['tabs'] = {
    'General Stats': {
        'order': 1,
        'tablist': [
            'Total Topics Count',
            'Partition Count',
            'Leader Count',
            'Active Controller Count',
            'Fetch Message Conversions Per Sec',
            'Produce Message Conversions Per Sec'
        ]
    },
    'Request Metrics': {
        'order': 2,
        'tablist': [
            'Total Fetch Requests Per Sec',
            'Total Produce Requests Per Sec',
            'Bytes Out Per Sec'
        ]
    },
    'Errors & Failures': {
        'order': 3,
        'tablist': [
            'Failed Fetch Requests Per Sec',
            'Failed Produce Requests Per Sec',
            'Failed Isr Updates Per Sec',
            'Invalid Magic Number Records Per Sec',
            'Invalid Message Crc Records Per Sec',
            'Invalid Offset Or Sequence Records Per Sec',
            'No Key Compacted Topic Records Per Sec',
            'Partitions With Late Transactions Count',
            'Reassigning Partitions',
            'Under Min Isr Partition Count',
            'Under Replicated Partitions',
            'Offline Partitions Count'
        ]
    },
    'Reassignment & Replication': {
        'order': 4,
        'tablist': [
            'Reassignment Bytes In Per Sec',
            'Reassignment Bytes Out Per Sec',
            'Replication Bytes In Per Sec'
        ]
    },
    'ISR Metrics': {
        'order': 5,
        'tablist': [
            'At Min Isr Partition Count',
            'Isr Shrinks Per Sec',
            'Leader Election Rate',
            'Producer Id Count'
        ]
    }
}
        return self.maindata



if __name__=="__main__":

    kafka_host="localhost"
    kafka_jmx_port=9999
    kafka_home="/home/s247-lin-plugin/Documents/kafka/kafka_2.13-3.8.0"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_host', help='host name to access the kafka server metrics',default=kafka_host)
    parser.add_argument('--kafka_jmx_port', help='jmx port to access the kafka server metrics',default=kafka_jmx_port)
    parser.add_argument('--kafka_home', help='kafka home path', default=kafka_home)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
