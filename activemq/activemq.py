#!/usr/bin/python

import json
import argparse
import socket
import ipaddress

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the Activemq JMX host
HOST_NAME = ""

# Enter the port configures for the Activemq JMX port
PORT = ""

# Enter the Broker name to be monitored from your Activemq broker
BROKER_NAME = ""

# Enter the Destination name to be monitored from your Activemq Queue name
DESTINATION_NAME = ""

ACTIVEMQ_LOGS_LOG_TYPE_NAME = "ActiveMQ Logs"
ACTIVEMQ_LOGS_ENABLED = "False"
ACTIVEMQ_LOGS_FILE_PATH = "/var/log/apache-activemq*/data/activemq*.log"

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
    result = {}
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
        result = mbean_attributes(jmxconnection, QUERY, javax, metric_map["broker_metrics"])

        QUERY = "org.apache.activemq:type=Broker,brokerName=" + BROKER_NAME + ",destinationType=Queue,destinationName=" + DESTINATION_NAME
        result.update(mbean_attributes(jmxconnection, QUERY, javax, metric_map["queue_metrics"]))

        result["broker_name"] = BROKER_NAME
        result["queue_name"] = DESTINATION_NAME

    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)

    return result


def resolve_ip_address(host):
    if not host:
        return host
    if host == "localhost":
        return "localhost"
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    try:
        return socket.gethostbyname(host)
    except Exception:
        return host


# arguments are parsed from activemq.cfg file and assigned with the variables
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="activemq host_name", type=str)
    parser.add_argument('--port', help="activemq port", type=str)
    parser.add_argument('--broker_name', help="activemq broker_name", type=str)
    parser.add_argument('--destination_name', help="activemq destination_name", type=str)
    parser.add_argument('--activemq_logs_enabled', help='enable log collection for ActiveMQ logs', default=ACTIVEMQ_LOGS_ENABLED)
    parser.add_argument('--activemq_logs_file_path', help='list of comma separated log file paths', nargs='?', default=ACTIVEMQ_LOGS_FILE_PATH)
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

    applog = {}
    if args.activemq_logs_enabled in ['True', 'true', '1']:
        applog["logs_enabled"] = True
        applog["log_type_name"] = ACTIVEMQ_LOGS_LOG_TYPE_NAME
        applog["log_file_path"] = args.activemq_logs_file_path
    else:
        applog["logs_enabled"] = False
    result_json['applog'] = applog

    result_json['s247config'] = {
        "ip_address": resolve_ip_address(HOST_NAME)
    }

    print(json.dumps(result_json, indent=4, sort_keys=True))
