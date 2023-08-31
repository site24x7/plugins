#!/usr/bin/python3
import json
import math

PLUGIN_VERSION=1
HEARTBEAT=True

METRICS_UNITS={
    "Fetch Throttle Time Avg":"ms",
    "Fetch Throttle Time Max":"ms"
}


class kafka:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.kafka_consumer_host=args.kafka_consumer_host
        self.kafka_consumer_jmx_port=args.kafka_consumer_jmx_port
        self.kafka_consumer_partition=args.kafka_consumer_partition
        self.kafka_topic_name=args.kafka_topic_name
        self.kafka_consumer_client_id=args.kafka_consumer_client_id

        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path

    
    def metriccollector(self):
        
        try:
            global jmx
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.kafka_consumer_host}:{self.kafka_consumer_jmx_port}/jmxrmi")
            
            metric_queries={
                "Records Lag Max(All Partitions)":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id}/records-lag-max",
                f"Bytes Consumed Rate(All Topics)":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id}/bytes-consumed-rate",
                f"Bytes Consumed Rate({self.kafka_topic_name})":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id},topic={self.kafka_topic_name}/bytes-consumed-rate",
                "Records Consumed Rate(All Topics)":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id}/records-consumed-rate",
                f"Records Consumed Rate({self.kafka_topic_name})":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id},topic={self.kafka_topic_name}/records-consumed-rate",
                "Fetch Rate":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id}/fetch-rate",
                f"Records Lag ( Partition No. : {self.kafka_consumer_partition} )":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id},topic={self.kafka_topic_name},partition={self.kafka_consumer_partition}/records-lag",
                f"Records Lag Max ( Partition No. : {self.kafka_consumer_partition} )":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id},topic={self.kafka_topic_name},partition={self.kafka_consumer_partition}/records-lag-max",
                "Records Per Request Avg":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id},topic={self.kafka_topic_name}/records-per-request-avg",
                "Fetch Throttle Time Avg":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id}/fetch-throttle-time-avg",
                "Fetch Throttle Time Max":f"kafka.consumer:type=consumer-fetch-manager-metrics,client-id={self.kafka_consumer_client_id}/fetch-throttle-time-max"
                
            }
            
            for metric in metric_queries:
                    
                jmxQuery = [jmx.JMXQuery(metric_queries[metric])]
                metric_result = jmxConnection.query(jmxQuery)
                if metric_result:
                    data=metric_result[0].value
                    if math.isnan(data):
                        self.maindata[metric]=-1
                    else:
                        self.maindata[metric]=data

            
            self.maindata["Topic Name"]=self.kafka_topic_name
            self.maindata["Partition No."]=f"Partition No : {self.kafka_consumer_partition}"
            self.maindata["Client ID"]=self.kafka_consumer_client_id




            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                    applog["logs_enabled"]=True
                    applog["log_type_name"]=self.logtypename
                    applog["log_file_path"]=self.logfilepath
            else:
                    applog["logs_enabled"]=False
            self.maindata['applog'] = applog
            self.maindata['tags']=f"Client_ID:{self.kafka_consumer_client_id},Kafka_Host:{self.kafka_consumer_host},Kafka_Topic:{self.kafka_topic_name}"



        except Exception as e: 
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata




if __name__=="__main__":

    kafka_consumer_host="localhost"
    kafka_consumer_jmx_port=9997
    kafka_consumer_partition=0
    kafka_topic_name="quickstart-events"
    kafka_client_id="console-consumer"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_consumer_host', help='host name to access the kafka consumer metrics',default=kafka_consumer_host)
    parser.add_argument('--kafka_consumer_jmx_port', help='jmx port to access the kafka consumer metrics',default=kafka_consumer_jmx_port)
    parser.add_argument('--kafka_consumer_partition', help='partition to monitor the metrics',default=kafka_consumer_partition)
    parser.add_argument('--kafka_topic_name', help='kafka topic name',default=kafka_topic_name)
    parser.add_argument('--kafka_consumer_client_id', help='kafka consumer client id',default=kafka_client_id)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    
    args=parser.parse_args()

    obj=kafka(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
    
