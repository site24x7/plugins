#!/usr/bin/python3

import json
from kafka import KafkaConsumer



PLUGIN_VERSION=1
HEARTBEAT=True

class Kafka:

    def __init__(self,args):

        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT


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

                self.maindata['records-lag-max']=float(consumer_metrics['records-lag-max'])         
                self.maindata['bytes-consumed-rate']=float(consumer_metrics['bytes-consumed-rate'])   
                self.maindata['records-consumed-rate']=float(consumer_metrics['records-consumed-rate'])   
                self.maindata['fetch-rate']=float(consumer_metrics['fetch-rate'])
             
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
