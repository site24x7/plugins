#!/usr/bin/python3
import json
import math

PLUGIN_VERSION=1
HEARTBEAT=True

METRICS_UNITS={
    "Response Rate":"/sec",
    "Request Rate":"/sec",
    "Request Latency Avg":"/sec",
    "Outgoing Byte Rate":"Bytes",
    "IO Wait Time NS Avg":"ns",
    "Batch Size Avg":"Bytes"}


class appname:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.kafka_producer_host=args.kafka_producer_host
        self.kafka_producer_jmx_port=args.kafka_producer_jmx_port

        self.kafka_producer_client_id=args.kafka_producer_client_id

        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path

    
    def metriccollector(self):
        
        try:
            global jmx
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.kafka_producer_host}:{self.kafka_producer_jmx_port}/jmxrmi")
            
            metric_queries={
                "Compression Rate Avg":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/compression-rate-avg",
                "Response Rate":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/response-rate",
                "Request Rate":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/request-rate",
                "Request Latency Avg":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/request-latency-avg",
                "Outgoing Byte Rate":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/outgoing-byte-rate",
                "IO Wait Time NS Avg":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/io-wait-time-ns-avg",
                "Batch Size Avg":f"kafka.producer:type=producer-metrics,client-id={self.kafka_producer_client_id}/batch-size-avg"
        }

            
            for metric in metric_queries:
                    
                jmxQuery = [jmx.JMXQuery(metric_queries[metric])]
                metric_result = jmxConnection.query(jmxQuery)
                data=metric_result[0].value
                if math.isnan(data):
                    self.maindata[metric]=-1
                else:
                    self.maindata[metric]=data

            self.maindata["Client ID"]=self.kafka_producer_client_id


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

    kafka_producer_host="localhost"
    kafka_producer_jmx_port=9982
    kafka_producer_client_id="console-producer"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--kafka_producer_host', help='host name to access the kafka consumer metrics',default=kafka_producer_host)
    parser.add_argument('--kafka_producer_jmx_port', help='jmx port to access the kafka consumer metrics',default=kafka_producer_jmx_port)
    parser.add_argument('--kafka_producer_client_id', help='kafka consumer client id',default=kafka_producer_client_id)

    

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=appname(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
