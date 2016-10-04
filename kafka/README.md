# Monitoring Apache Kafka Servers

### This plugin in python monitors the Producer metrics of Apache kafka servers
It uses the inbuilt Apache kafka monitoring options to get the monitoring data.Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Shobana, Zoho Corp
### Language : Python
### Tested in Ubuntu

# Update Apache kafka Server configuration details
BROKER_NAME = "localhost"  
PORT="9092"

# Monitored Attributes

# PRODUCER METRICS
	connection_count - The current number of active connections with the kafka cluster.
	network_io_rate - The average number of network operations (read or writes) on all connections per second.
	incoming_byte_rate - The average number of incoming bytes received per second.
	outgoing_byte_rate - The average number of outgoing bytes sent per second to all servers.
	avg_request_latency - The average request latency ia a measure of the amount of time between when kafka producer send was called until the producer receives a response from the broker.
	request_rate - The rate at which producers send data to brokers.
	response_rate - The rate of responses received from brokers.
	io_time_ns_avg - Average length of time the I/O thread spent waiting for a socket (in ns)

### Changes in the plugin will be reflected in Site24x7 only when there is a change in plugin_version.
HEARTBEAT - false : Site24x7 will alert as down only when plugin status is down
HEARTBEAT - true : Site24x7 will alert as down 1. When plugin status is down 2. When there is no data from plugin
Learn more about the plugin installation steps and the various performance metrics that you can monitor in https://www.site24x7.com/plugins.html