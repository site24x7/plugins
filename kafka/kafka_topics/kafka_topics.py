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
        

    def metriccollector(self):

        try:
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.kafka_host}:{self.kafka_jmx_port}/jmxrmi")
            metric_queries={

            "topic_metrics":{
                f"Bytes In Per Sec":f"kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec,topic={self.kafka_topic_name}",
                f"Bytes Out Per Sec":f"kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec,topic={self.kafka_topic_name}",
                f"Messages In Per Sec":f"kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic={self.kafka_topic_name}",
            },
            }

            jmxQuery = [jmx.JMXQuery(f"kafka.cluster:type=*,name=ReplicasCount,topic={self.kafka_topic_name},partition=*")]
            partition_count= len(jmxConnection.query(jmxQuery))
            if partition_count>25:partition_count=25
            self.maindata[f'Partition Count']=partition_count
            

            for metric_type in metric_queries:
                 for metrics in metric_queries[metric_type]:
                      query=metric_queries[metric_type][metrics]
                      jmxQuery = [jmx.JMXQuery(query)]
                      metric_result = jmxConnection.query(jmxQuery)
                      if metric_result:
                        self.maindata[metrics]=metric_result[0].value
            
            partition_metrics=["InSyncReplicasCount","LastStableOffsetLag","ReplicasCount","UnderReplicated","UnderMinIsr"]
            partition_data=[]

            i=0
            for i in range(partition_count):
                data={}
                for metric in partition_metrics:
                    jmxQuery = [jmx.JMXQuery(f"kafka.cluster:type=*,name={metric},topic={self.kafka_topic_name},partition={i}")]
                    value= jmxConnection.query(jmxQuery)
                    if value[0].value:
                        data[metric]=value[0].value
                    else:
                        data[metric]=0

                data["name"]="Partition_No_"+str(i)

                partition_data.append(data)


            self.maindata["Partitions"]=partition_data
            self.maindata["Topic Name"]=self.kafka_topic_name

            self.maindata['tabs']={
                "Kafka Partitions":{
                    "order":1,
                    "tablist":[
                        "Partitions"
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
            self.maindata['tags']=f"Kafka_Broker_Host:Kafka_Topics_Monitoring"

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata

if __name__=="__main__":

    kafka_host="localhost"
    kafka_jmx_port=9999
    kafka_topic_name="my-topic"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_host', help='host name to access the kafka server metrics',default=kafka_host)
    parser.add_argument('--kafka_jmx_port', help='jmx port to access the kafka server metrics',default=kafka_jmx_port)
    parser.add_argument('--kafka_topic_name', help='kafka topic name',default=kafka_topic_name)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
