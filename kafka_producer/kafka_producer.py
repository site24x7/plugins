#!/usr/bin/python

import re
import json
import os
import sys
import traceback
from kafka import KafkaConsumer
from kafka import KafkaProducer

### Monitors the performance metrics of kafka producers.

### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Shobana, Zoho Corp
### Language : Python
### Tested in Ubuntu

### Configure kafka Server to enable monitoring for Site24x7

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Change the broker name and port accordingly here:
BROKER_NAME = "localhost"

PORT="9092"

### Attribute Units
UNITS = { 'connection_count':'Nos',
'network_io_rate':'Bytes/sec',
'incoming_byte_rate':'Bytes/sec',
'outgoing_byte_rate':'Bytes/sec',
'avg_request_latency':'ms',
'request_rate':'Requests/sec',
'response_rate':'Responses/sec',
'io-time-ns-avg':'ns'
}

class Kafka(object):
    
    def __init__(self,broker,port):
        self.connection = None
        self.broker = broker  #Broker name of kafka
        self.port = port    #port of kafka

    def getConnection(self):
        self.connection=KafkaConsumer(bootstrap_servers=[self.broker+":"+self.port])   # Kafka consumer connection 

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        ### Parse the response data
        try:
            self.getConnection()
            if self.connection :
                result=self.connection.metrics()
                for  k,v in result.items():
                    if k =='consumer-metrics':
                        consumer_metrics=v

                ### Attribute Names
                data['connection_count']=int(consumer_metrics['connection-count'])         #The current number of active connections.
                data['network_io_rate']=float(consumer_metrics['network-io-rate'])         #The average number of network operations (reads or writes) on all connections per second.
                data['incoming_byte_rate']=float(consumer_metrics['incoming-byte-rate'])   #The average number of incoming bytes received per second
                data['outgoing_byte_rate']=float(consumer_metrics['outgoing-byte-rate'])   #The average number of outgoing bytes sent per second to all servers
                data['avg_request_latency']=float(consumer_metrics['request-latency-avg']) # The average request latency is a measure of the amount of time between when KafkaProducer send was called until the producer receives a response from the broker. 
                data['request_rate']=float(consumer_metrics['request-rate'])               #the rate at which producers send data to brokers
                data['response_rate']=float(consumer_metrics['response-rate'])             #the rate of responses received from brokers
                data['io-time-ns-avg']=float(consumer_metrics['io-time-ns-avg'])           #Average length of time the I/O thread spent waiting for a socket (in ns)
               
                data['units']=UNITS
        
        except Exception as e:
            data['status']=0
            data['msg']='Connection Error'
        
        
        return data

if __name__ == "__main__":

    consumer = Kafka(BROKER_NAME,PORT)

    result = consumer.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
    
