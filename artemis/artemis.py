#!/usr/bin/python


import json
import argparse


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the ActiveMQ Artemis JMX
HOST_NAME = ""

# Enter the port configures for the Solr JMX
PORT = ""

# Enter the Broker name to be monitored from your Apache ActiveMQ Artemis
BROKER_NAME = ""

# Enter the Address name to be monitored from your Apache ActiveMQ Artemis
ADDRESS_NAME = ""

# Enter the Queue name to be monitored from your Apache ActiveMQ Artemis
QUEUE_NAME = ""

# Enter the User name of the artemis broker
USER = ""

#Enter the password if the artemis broker
PASSWORD = ""

URL = ""
QUERY = ""

result_json = {}


METRIC_UNITS = {
    "address_memory_usage" : "percent",
    "address_memory_usage_percent" : "percent",
    "max_disk_usage" : "percent",
    "connection_count" : "milliseconds",
    "total_connection_count" : "",
    "total_message_count" : "messages",
    "total_messages_added" : "messages",
    "total_messages_acknowledged" : "messages",
    "total_consumer_count":  "messages",
    "address_size" : "messages",
    "number_of_page" : "milliseconds",
    "number_of_messages" : "milliseconds",
    "number_of_bytes_per_page" : "",
    "routed_message_count" : "messages",
    "unrouted_message_count" : "messages",
    "message_count" : "messages",
    "consumer_count" : "messages",
    "max_consumers" : "messages",
    "messages_added" : "messages",
    "messages_expired" : "messages",
    "messages_acknowledged" : "messages",
    "messages_killed" : "messages"
}


artemis_metrics = {
    "broker_metrics" : {
        "AddressMemoryUsage" : "address_memory_usage",
        "AddressMemoryUsagePercentage" : "address_memory_usage_percent",
        "MaxDiskUsage" : "max_disk_usage",
        "ConnectionCount" : "connection_count",
        "TotalConnectionCount" : "total_connection_count",
        "TotalMessageCount" : "total_message_count",
        "TotalMessagesAdded" : "total_messages_added",
        "TotalMessagesAcknowledged" : "total_messages_acknowledged",
        "TotalConsumerCount":  "total_consumer_count"
    },
    "address_metrics" : {
        "AddressSize" : "address_size",
        "NumberOfPages" : "number_of_page",
        "NumberOfMessages" : "number_of_messages",
        "NumberOfBytesPerPage" : "number_of_bytes_per_page",
        "RoutedMessageCount" : "routed_message_count",
        "UnRoutedMessageCount" : "unrouted_message_count",
        "MessageCount" : "message_count"
    },
    "queue_metrics" : {
        "ConsumerCount" : "consumer_count",
        "MaxConsumers" : "max_consumers",
        "MessagesAdded" : "messages_added",
        "MessagesExpired" : "messages_expired",
        "MessagesAcknowledged" : "messages_acknowledged",
        "MessagesKilled" : "messages_killed"
    }
}


# JMX Query is executed and getting the Performance metric data after filtering the output
def fetch_metrics_via_jmx(jmxconnection, QUERY, javax, jmx_map):
    
    result = {}
    try:
        for metric in jmx_map:
            output = jmxconnection.getAttribute(javax.management.ObjectName(QUERY),metric)
            result[jmx_map[metric]] = output

    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)

    return result


# JMX url is defined and JMX connection is established, Query and metric keys are passed to process
def get_output():

    result = {}

    try:
        import jpype
        from jpype import java
        from jpype import javax
        
        URL = "service:jmx:rmi:///jndi/rmi://" + HOST_NAME + ":" + PORT + "/jmxrmi"
        jpype.startJVM(convertStrings=False)
        jhash=java.util.HashMap()
        jarray=jpype.JArray(java.lang.String)([USER,PASSWORD])
        jhash.put(javax.management.remote.JMXConnector.CREDENTIALS,jarray);
        jmxurl=javax.management.remote.JMXServiceURL(URL)
        jmxsoc=javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
        jmxconnection=jmxsoc.getMBeanServerConnection();

        QUERY = "org.apache.activemq.artemis:broker=\"" + BROKER_NAME + "\""
        result = fetch_metrics_via_jmx(jmxconnection, QUERY, javax, artemis_metrics["broker_metrics"])

        QUERY = "org.apache.activemq.artemis:broker=\"" + BROKER_NAME + "\",component=addresses,address=\"" + ADDRESS_NAME + "\""
        result.update(fetch_metrics_via_jmx(jmxconnection, QUERY, javax, artemis_metrics["address_metrics"]))
        
        QUERY = "org.apache.activemq.artemis:broker=\"" + BROKER_NAME + "\",component=addresses,address=\"" + ADDRESS_NAME + "\",subcomponent=queues,routing-type=\"anycast\",queue=\"" + QUEUE_NAME + "\""
        result.update(fetch_metrics_via_jmx(jmxconnection, QUERY, javax, artemis_metrics["queue_metrics"]))

        result["broker_name"] = BROKER_NAME
        
        
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)
    
    return result


# arguments are parsed from activemq.cfg file and assigned with the variables
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="artemis host_name", type=str)
    parser.add_argument('--port', help="artemis port", type=str)
    parser.add_argument('--broker_name', help="artemis broker_name", type=str)
    parser.add_argument('--address_name', help="artemis address_name", type=str)
    parser.add_argument('--queue_name', help="artemis queue_name", type=str)
    parser.add_argument('--user', help="artemis user", type=str)
    parser.add_argument('--password', help="artemis password", type=str)
    
    args = parser.parse_args()
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
    if args.broker_name:
        BROKER_NAME = args.broker_name
    if args.address_name:
        ADDRESS_NAME = args.address_name
    if args.queue_name:
        QUEUE_NAME = args.queue_name
    if args.user:
        USER = args.user
    if args.password:
        PASSWORD = args.password

    result_json = get_output()

    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS

    print(json.dumps(result_json, indent=4, sort_keys=True))
