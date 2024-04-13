#!/usr/bin/python3
import json
import subprocess


PLUGIN_VERSION=3
HEARTBEAT=True


class kafka:

    def __init__(self,args):

        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.kafka_home=args.kafka_home
        self.kafka_host=args.kafka_host
        self.kafka_jmx_port=args.kafka_jmx_port
        self.kafka_topic_name=args.kafka_topic_name
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
        

    def cmd_lag_metric(self):
        
        out=self.execute_command(f"""bash {self.kafka_home}/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092  --describe --all-groups --all-topics """, True).decode()
        cmd_metrics=out.split("\n")[2:-1]

        data={}
        for cmd_metric in cmd_metrics:
            
            cmd_metric=cmd_metric.split()
            if cmd_metric[1]== self.kafka_topic_name:
                partition_no=cmd_metric[2]
                current_offset=cmd_metric[3]
                if current_offset=="-":current_offset=0
                log_end_offset=cmd_metric[3]
                if log_end_offset=="-":log_end_offset=0
                consumer_lag=cmd_metric[4]
                if consumer_lag=="-":consumer_lag=0

                data[f"Partition_No_{partition_no}"]={"CurrentOffset":current_offset, "LogEndOffset":log_end_offset, "ConsumerLag": consumer_lag}
            
        return data

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
                "Messages In Per Sec":"kafka.server:type=BrokerTopicMetrics,name=Messages In Per Sec",
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
            },

            "topic_metrics":{
                f"Bytes In Per Sec ({self.kafka_topic_name})":f"kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec,topic={self.kafka_topic_name}",
                f"Bytes Out Per Sec ({self.kafka_topic_name})":f"kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec,topic={self.kafka_topic_name}",
                f"Messages In Per Sec ({self.kafka_topic_name})":f"kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic={self.kafka_topic_name}",
            },
            }

            jmxQuery = [jmx.JMXQuery("kafka.cluster:type=*,name=AtMinIsr,topic=quickstart-events,partition=*")]
            partition_count= len(jmxConnection.query(jmxQuery))
            if partition_count>25:partition_count=25
            self.maindata[f'Partition Count ({self.kafka_topic_name})']=partition_count
            

            for metric_type in metric_queries:
                 for metrics in metric_queries[metric_type]:
                      query=metric_queries[metric_type][metrics]
                      jmxQuery = [jmx.JMXQuery(query)]
                      metric_result = jmxConnection.query(jmxQuery)
                      if metric_result:
                        self.maindata[metrics]=metric_result[0].value
            
            try:
                lag_data=self.cmd_lag_metric()
            except Exception as e:
                self.maindata["status"]=0
                self.maindata['msg']=str(e)
                return self.maindata

            partition_metrics=["AtMinIsr","InSyncReplicasCount","LastStableOffsetLag","ReplicasCount","UnderReplicated","UnderMinIsr"]
            partition_data=[]
            i=0
            for i in range(partition_count):
                data={}
                for metric in partition_metrics:
                    jmxQuery = [jmx.JMXQuery(f"kafka.cluster:type=*,name={metric},topic=quickstart-events,partition={i}")]
                    value= jmxConnection.query(jmxQuery)[0].value
                    data[metric]=value
                
                data["name"]="Partition_No_"+str(i)
                data.update(lag_data[data["name"]])
                partition_data.append(data)
            self.maindata["Partition_Metrics"]=partition_data
            self.maindata["Topic Name"]=self.kafka_topic_name

            self.maindata['tabs']={
                "Kafka Partition Metrics":{
                    "order":1,
                    "tablist":[
                        "Partition_Metrics"
                    ]}
                }

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
    kafka_topic_name="quickstart-events"
    kafka_home="/app/kafka_2.13-3.7.0"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_host', help='host name to access the kafka server metrics',default=kafka_host)
    parser.add_argument('--kafka_jmx_port', help='jmx port to access the kafka server metrics',default=kafka_jmx_port)
    parser.add_argument('--kafka_topic_name', help='kafka topic name',default=kafka_topic_name)
    parser.add_argument('--kafka_home', help='kafka home path', default=kafka_home)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
