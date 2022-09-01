# **Kafka Consumer Monitoring**

## Apache Kafka

Apache Kafka is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real time data feeds.

## Kafka Consumer

A client that consumes records from a Kafka cluster. This client transparently handles the failure of Kafka brokers, and transparently adapts as topic partitions it fetches migrate within the cluster

**Therefore it is pivotal to monitor the Kafka Consumer**

## Prerequisites
 - Installation of kafka python module for Python3
```
pip install kafka-python
```

 - Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation

- Create a directory named "kafka_consumer_monitoring" under the Site24x7 Linux Agent plugin directory

```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_consumer_monitoring
```

 - Download all the files in the "kafka_consumer_monitoring" folder and place it under the "kafka_consumer_monitoring" directory. 

```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/kafka_consumer_monitoring/kafka_consumer_monitoring.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/kafka_consumer_monitoring/kafka_consumer_monitoring.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```
python3 kafka_consumer_monitoring.py --broker=<broker name> --port=<port no>
```
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


## Configuration

- Provide your Kafka Consumer configurations in kafka_consumer_monitoring.cfg file

```
[kafka_consumer_1]
broker=<Broker Name>
port=<Broker Port>

```

## Supported Metrics
The following metrics are captured by the Kafka Consumer Monitoring plugin :

- **Maximum Records Lag**

	Increasing value means that the consumer is not keeping up with the producers.

- **Bytes Consumer Rate**

  Average bytes consumed per second for each consumer for a specific topic or   	  across all  topics.

- **Records Consumed Rate**

   Average bytes consumed per second for each consumer for a specific topic or    across all topics

- **Fetch Rate**

	The number of fetch requests per second from the consumer
- **Avg Fetch Size**

	Average number of bytes fetched per request

	

- **Max Fetch Size**

	Maximum number of bytes fetched per request

- **Avg Records Per Request**

	Average number of records in each request

- **Avg Fetch Latency**

	Average time taken for a fetch request

- **Max Fetch Latency**

	Maximum time taken for a fetch request

- **Avg Fetch Throttle Time**

	Average throttle time in milliseconds
	

- **Maximum Fetch Throttle time**

	Maximum throttle time in milliseconds
	

