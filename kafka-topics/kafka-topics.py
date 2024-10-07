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
        self.kafka_server_port=args.kafka_server_port
        self.kafka_topic_name=args.kafka_topic_name
        self.kafka_group_name=args.kafka_group_name


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
        
        out=self.execute_command(f"""bash {self.kafka_home}/bin/kafka-consumer-groups.sh --bootstrap-server {self.kafka_host}:{self.kafka_server_port}  --describe --group {self.kafka_group_name}""", True).decode()
        if not out:
            return {}
        cmd_metrics=out.split("\n")[2:-1]
        cols=out.split("\n")[1].split()
        for index,col in enumerate(cols):
            if col=="TOPIC":
                topic_index=index
            elif col=="CURRENT-OFFSET":
                current_offset_index=index
            elif col=="PARTITION":
                partition_index=index
            elif col=="LOG-END-OFFSET":
                log_end_offset_index=index
            elif col=="LAG":
                lag_index=index

        data={}
        for cmd_metric in cmd_metrics:
            
            cmd_metric=cmd_metric.split()
            if cmd_metric[topic_index]== self.kafka_topic_name:
                partition_no=cmd_metric[partition_index]
                current_offset=cmd_metric[current_offset_index]
                if current_offset=="-":current_offset=0
                log_end_offset=cmd_metric[log_end_offset_index]
                if log_end_offset=="-":log_end_offset=0
                consumer_lag=cmd_metric[lag_index]
                if consumer_lag=="-":consumer_lag=0

                data[f"Partition_No_{partition_no}"]={"CurrentOffset":current_offset, "LogEndOffset":log_end_offset, "ConsumerLag": consumer_lag}
            
        return data


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


            try:
                lag_data=self.cmd_lag_metric()
            except Exception as e:
                self.maindata["status"]=0
                self.maindata['msg']=str(e)
                return self.maindata
            

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
                if data["name"] in lag_data:
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
            self.maindata['tags']=f"Kafka_Broker_Host:Kafka_Topics_Monitoring"

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata



if __name__=="__main__":

    kafka_host="localhost"
    kafka_jmx_port=9999
    kafka_server_port=9092
    kafka_topic_name="mani-topic-1"
    kafka_home="/home/s247-lin-plugin/Documents/kafka/kafka_2.13-3.8.0"
    kafka_group_name="mani-group-1"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_host', help='host name to access the kafka server metrics',default=kafka_host)
    parser.add_argument('--kafka_jmx_port', help='jmx port to access the kafka server metrics',default=kafka_jmx_port)
    parser.add_argument('--kafka_server_port', help='server port to access the kafka server metrics',default=kafka_server_port)
    parser.add_argument('--kafka_topic_name', help='kafka topic name',default=kafka_topic_name)
    parser.add_argument('--kafka_home', help='kafka home path', default=kafka_home)
    parser.add_argument('--kafka_group_name', help='kafka group name', default=kafka_group_name)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
