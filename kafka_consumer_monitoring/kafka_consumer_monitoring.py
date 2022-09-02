#!/usr/bin/python3

import json
from kafka import KafkaConsumer



PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={'Avg Fetch Throttle Time':'ms','Maximum Fetch Throttle time':'ms','Max Fetch Size':'Bytes','Max Fetch Latency':'ms','Bytes Consumed Rate':'Bytes','Avg Fetch Size':'Bytes','Avg Fetch Latency':'ms' }


class Kafka:

    def __init__(self,args):

        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS


        self.broker=args.broker
        self.port=args.port




    def metricCollector(self):
        try:
            self.getConnection()
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        self.consumerMetrics()
        return self.maindata




    def getConnection(self):
        self.Consumerconnection=KafkaConsumer(bootstrap_servers=[self.broker+":"+self.port])



    def consumerMetrics(self):
        try:
            if self.Consumerconnection :
                result=self.Consumerconnection.metrics()
                for  k,v in result.items():
                    if k =='consumer-fetch-manager-metrics':
                        consumer_metrics=v

                if consumer_metrics['records-lag-max']==float("-Infinity"):
                    self.maindata['Maximum Records Lag']=-1
                else:
                    self.maindata['Maximum Records Lag']=consumer_metrics['records-lag-max']


                self.maindata['Bytes Consumed Rate']=float(consumer_metrics['bytes-consumed-rate'])   
                self.maindata['Records Consumed Rate']=float(consumer_metrics['records-consumed-rate'])   
                self.maindata['Fetch Rate']=float(consumer_metrics['fetch-rate'])
                self.maindata['Avg Fetch Size']=float(consumer_metrics['fetch-size-avg'])

                if consumer_metrics['fetch-size-max']==float("-Infinity"):
                    self.maindata['Max Fetch Size']=-1
                else:
                    self.maindata['Max Fetch Size']=consumer_metrics['fetch-size-max']

                self.maindata['Avg Records Per Request']=float(consumer_metrics['records-per-request-avg'])
                self.maindata['Avg Fetch Latency']=float(consumer_metrics['fetch-latency-avg'])

                
                if consumer_metrics['fetch-latency-max']==float("-Infinity"):
                    self.maindata['Max Fetch Latency']=-1
                else:
                    self.maindata['Max Fetch Latency']=consumer_metrics['fetch-latency-max']


                self.maindata['Avg Fetch Throttle Time']=float(consumer_metrics['fetch-throttle-time-avg']) 

                if consumer_metrics['fetch-throttle-time-max']==float("-Infinity"):
                    self.maindata['Maximum Fetch Throttle time']=-1
                else:
                    self.maindata['Maximum Fetch Throttle time']=consumer_metrics['fetch-throttle-time-max']
            

             
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata




if __name__=="__main__":
    
    broker=None
    port=None

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--broker',help="Name of the broker",default="localhost")
    parser.add_argument('--port',help="Port no. of the broker",default="9092")
    args=parser.parse_args()

    kf=Kafka(args)


    result=kf.metricCollector()
    print(json.dumps(result,indent=True))
