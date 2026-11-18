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
        
    def get_topics_list(self, jmxConnection):
        try:
            import jmxquery as jmx
            
            query = jmx.JMXQuery('kafka.cluster:*')
            result = jmxConnection.query([query])
            
            topics = set()
            for r in result:
                mbean_name = r.to_query_string()
                if 'topic=' in mbean_name:
                    topic = mbean_name.split('topic=')[1].split(',')[0]
                    if not topic.startswith('__'): # Exclude internal topics
                        topics.add(topic)
            
            return sorted(list(topics))
            
        except Exception as e:
            if 'msg' in self.maindata:
                self.maindata['msg'] += f"; Error getting topics list: {str(e)}"
            else:
                self.maindata['msg'] = f"Error getting topics list: {str(e)}"
            return []

    def get_topics_metrics(self, jmxConnection):
        try:
            import jmxquery as jmx
            
            topics_list = self.get_topics_list(jmxConnection)
            
            if not topics_list:
                return [{
                    "name": "-",
                    "Partition_Count": -1,
                    "Bytes_In_Per_Sec": -1,
                    "Bytes_Out_Per_Sec": -1,
                    "Messages_In_Per_Sec": -1
                }]
            
            topics_data = []
            
            for topic_name in topics_list:
                topic_metrics = {
                    "name": topic_name,
                    "Partition_Count": 0,
                    "Bytes_In_Per_Sec": 0,
                    "Bytes_Out_Per_Sec": 0,
                    "Messages_In_Per_Sec": 0
                }
                
                try:
                    jmxQuery = [jmx.JMXQuery(f"kafka.cluster:type=*,name=ReplicasCount,topic={topic_name},partition=*")]
                    partition_result = jmxConnection.query(jmxQuery)
                    partition_count = len(partition_result)
                    topic_metrics["Partition_Count"] = partition_count if partition_count > 0 else 0
                    
                    jmxQuery = [jmx.JMXQuery(f"kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec,topic={topic_name}")]
                    result = jmxConnection.query(jmxQuery)
                    if result and result[0].value is not None:
                        topic_metrics["Bytes_In_Per_Sec"] = result[0].value
                    
                    jmxQuery = [jmx.JMXQuery(f"kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec,topic={topic_name}")]
                    result = jmxConnection.query(jmxQuery)
                    if result and result[0].value is not None:
                        topic_metrics["Bytes_Out_Per_Sec"] = result[0].value
                    
                    jmxQuery = [jmx.JMXQuery(f"kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic={topic_name}")]
                    result = jmxConnection.query(jmxQuery)
                    if result and result[0].value is not None:
                        topic_metrics["Messages_In_Per_Sec"] = result[0].value
                    
                except Exception as topic_error:
                    if 'msg' in self.maindata:
                        self.maindata['msg'] += f"; Error getting metrics for topic {topic_name}: {str(topic_error)}"
                    else:
                        self.maindata['msg'] = f"Error getting metrics for topic {topic_name}: {str(topic_error)}"
                
                topics_data.append(topic_metrics)
            
            return topics_data if topics_data else [{
                "name": "-",
                "Partition_Count": -1,
                "Bytes_In_Per_Sec": -1,
                "Bytes_Out_Per_Sec": -1,
                "Messages_In_Per_Sec": -1
            }]
            
        except Exception as e:
            if 'msg' in self.maindata:
                self.maindata['msg'] += f"; Error in get_topics_metrics: {str(e)}"
            else:
                self.maindata['msg'] = f"Error in get_topics_metrics: {str(e)}"
            return [{
                "name": "-",
                "Partition_Count": -1,
                "Bytes_In_Per_Sec": -1,
                "Bytes_Out_Per_Sec": -1,
                "Messages_In_Per_Sec": -1
            }]


    def metriccollector(self):

        try:
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.kafka_host}:{self.kafka_jmx_port}/jmxrmi")
            metric_queries={

            "broker_topic_metrics":{
                "Bytes In Per Sec":"kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
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
                "Isr Expands Per Sec":"kafka.server:type=ReplicaManager,name=IsrExpandsPerSec",
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
            
            "purgatory":{
                "Purgatory Size Produce":"kafka.server:type=DelayedOperationPurgatory,delayedOperation=Produce,name=PurgatorySize",
                "Purgatory Size Fetch":"kafka.server:type=DelayedOperationPurgatory,delayedOperation=Fetch,name=PurgatorySize",
                
            },
            "current_control_id":{
                "Current Control ID":"kafka.server:type=MetadataLoader,name=CurrentControllerId",
            },
            "request_handler_average_idle_percent":{
                "Request Handler Avg Idle Percent":"kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent",
            },
            "replicas":{
                 "Replicas In eligible To Delete Count":"kafka.controller:type=KafkaController,name=ReplicasIneligibleToDeleteCount",
                "Replicas To Delete Count":"kafka.controller:type=KafkaController,name=ReplicasToDeleteCount",
            },
            "topics":{
                "Topics Ineligible To Delete Count":"kafka.controller:type=KafkaController,name=TopicsIneligibleToDeleteCount",
                "Topics To Delete Count":"kafka.controller:type=KafkaController,name=TopicsToDeleteCount",
            },
            "zookeeper":{
                "ZooKeeper Disconnects Per Sec":"kafka.server:type=SessionExpireListener,name=ZooKeeperDisconnectsPerSec",
                "Global Partition Count":"kafka.controller:type=KafkaController,name=GlobalPartitionCount"
            }
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

            topics_data = self.get_topics_metrics(jmxConnection)
            self.maindata['Topics'] = topics_data

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata
        
        self.maindata['tabs'] = {
    'Topics':{
        'order': 1,
        'tablist': [
            'Topics'
        ]
    },
    'Traffic': {
        'order': 2,
        'tablist': [
            'Bytes In Per Sec',
            'Bytes Out Per Sec',
            'Total Fetch Requests Per Sec',
            'Total Produce Requests Per Sec',
            'Failed Fetch Requests Per Sec',
            'Failed Produce Requests Per Sec'
        ]
    },
    'Replication': {
        'order': 3,
        'tablist': [
            'Replication Bytes In Per Sec',
            'Replication Bytes Out Per Sec',
            'Reassignment Bytes In Per Sec',
            'Reassignment Bytes Out Per Sec',
            'Under Replicated Partitions',
            'Under Min Isr Partition Count',
            'Replicas In eligible To Delete Count',
            'Replicas To Delete Count'
        ]
    },
    'ISR': {
        'order': 4,
        'tablist': [
            'At Min Isr Partition Count',
            'Isr Expands Per Sec',
            'Isr Shrinks Per Sec',
            'Partitions With Late Transactions Count',
            'Leader Count',
            'Producer Id Count'
        ]
    },
    'Controller and Purgatory': {
        'order': 5,
        'tablist': [
            'Active Controller Count',
            'Offline Partitions Count',
            'Global Partition Count',
            'Leader Election Rate',
            'Total Topics Count',
            'Topics Ineligible To Delete Count',
            'Topics To Delete Count',
            'Purgatory Size Produce',
            'Purgatory Size Fetch',
            'ZooKeeper Disconnects Per Sec'
        ]
    }
}
        
        self.maindata['s247config']={
            "childdiscovery":[
                'Topics'
            ]
        }
        
        return self.maindata



if __name__=="__main__":

    kafka_host = "localhost"
    kafka_jmx_port = "9999"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_host', help='host name to access the kafka server metrics',default=kafka_host)
    parser.add_argument('--kafka_jmx_port', help='jmx port to access the kafka server metrics',default=kafka_jmx_port)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
