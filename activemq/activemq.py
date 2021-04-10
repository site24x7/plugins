#!/usr/bin/python3

import json
import argparse

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 3

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the Solr JMX
HOST_NAME = ""

# Enter the port configures for the Solr JMX
PORT = ""

# Enter the Broker name to be monitored from your Apache Solr
BROKER_NAME = ""

# Enter the Destination name to be monitored from your Apache Solr
DESTINATION_NAME = ""

URL = ""
QUERY = ""

result_json = {}

METRIC_UNITS = {
    "broker_memory_percent": "percent",
    "queue_memory_percent": "percent",
    "store_percent_usage": "percent",
    "temp_percent_usage": "percent",
    "average_enqueue_time": "milliseconds",
    "consumer_count": "",
    "dequeue_count": "messages",
    "dispatch_count": "messages",
    "enqueue_count": "messages",
    "expired_count":  "messages",
    "in_flight_count": "messages",
    "max_enqueue_time": "milliseconds",
    "min_enqueue_time": "milliseconds",
    "producer_count": "",
    "queue_size": "messages"
}

metric_map = {
    "broker_metrics": {
        "StorePercentUsage": "store_percent_usage",
        "TempPercentUsage": "temp_percent_usage",
        "MemoryPercentUsage": "broker_memory_percent_usage"
    },
    "queue_metrics": {
        "AverageEnqueueTime": "average_enqueue_time",
        "ConsumerCount": "consumer_count",
        "DequeueCount": "dequeue_count",
        "DispatchCount": "dispatch_count",
        "EnqueueCount": "enqueue_count",
        "ExpiredCount": "expired_count",
        "InFlightCount": "in_flight_count",
        "MemoryPercentUsage": "queue_memory_percent_usage",
        "MaxEnqueueTime": "max_enqueue_time",
        "MinEnqueueTime": "min_enqueue_time",
        "ProducerCount": "producer_count",
        "QueueSize": "queue_size"
    }
}


# JMX Query is executed and getting the Performance metric data after filtering the output
def mbean_attributes(jmxconnection, QUERY, javax, metric_arg):
    result = {}
    try:
        for metric in metric_arg:
            output = jmxconnection.getAttribute(javax.management.ObjectName(QUERY), metric)
            result[metric_arg[metric]] = output

    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)

    return result


# JMX url is defined and JMX connection is established, Query and metric keys are passed to process
def get_output():
    URL = "service:jmx:rmi:///jndi/rmi://" + HOST_NAME + ":" + PORT + "/jmxrmi"
    try:
        import jpype
        from jpype import java
        from jpype import javax

        jpype.startJVM(convertStrings=False)
        jhash = java.util.HashMap()
        jmxurl = javax.management.remote.JMXServiceURL(URL)
        jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
        jmxconnection = jmxsoc.getMBeanServerConnection()

        QUERY = "org.apache.activemq:type=Broker,brokerName=" + BROKER_NAME
        result_json = mbean_attributes(jmxconnection, QUERY, javax, metric_map["broker_metrics"])

        QUERY = "org.apache.activemq:type=Broker,brokerName=" + BROKER_NAME + ",destinationType=Queue,destinationName=" + DESTINATION_NAME
        result_json.update(mbean_attributes(jmxconnection, QUERY, javax, metric_map["queue_metrics"]))

        result_json["broker_name"] = BROKER_NAME
        result_json["queue_name"] = DESTINATION_NAME

    except Exception as e:
        result_json["status"] = 0
        result_json["msg"] = str(e)

    return result_json


# arguments are parsed from activemq.cfg file and assigned with the variables
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="activemq host_name", type=str)
    parser.add_argument('--port', help="activemq port", type=str)
    parser.add_argument('--broker_name', help="activemq broker_name", type=str)
    parser.add_argument('--destination_name', help="activemq destination_name", type=str)
    args = parser.parse_args()
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
    if args.broker_name:
        BROKER_NAME = args.broker_name
    if args.destination_name:
        DESTINATION_NAME = args.destination_name

    result_json = get_output()

    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS

    print(json.dumps(result_json, indent=4, sort_keys=True))
