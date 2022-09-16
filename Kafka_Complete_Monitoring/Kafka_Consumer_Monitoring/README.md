# **Kafka Consumer Monitoring**

## Apache Kafka

Apache Kafka is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real time data feeds.

## Kafka Consumer

A client that consumes records from a Kafka cluster. This client transparently handles the failure of Kafka brokers, and transparently adapts as topic partitions it fetches migrate within the cluster

**Therefore it is pivotal to monitor the Kafka Consumer**

## Prerequisites
 - Installation of jmxquery module for Python3
```
pip3 install jmxquery
```

 - Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation

- Create a directory named "kafka_consumer_monitoring" under the Site24x7 Linux Agent plugin directory

```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_consumer_monitoring
```

 - Download all the files in the "kafka_consumer_monitoring" folder and place it under the "kafka_consumer_monitoring" directory. 

```


```

- Execute the below command with appropriate arguments to check for the valid json output:

```
python3 kafka_consumer_monitoring.py --kafka_consumer_host=<KAFKA_CONSUMER_HOST_NAME> kafka_consumer_jmx_port=<KAFKA_CONSUMER_PORT_NO> --kafka_consumer_partition=<KAFKA_CONSUMER_PARTITION_NO> --kafka_topic_name=<KAFKA_TOPIC_NAME> --kafka_consumer_client_id=<KAFKA_CONSUMER_CLIENT_ID> --logs_enabled=False --log_type_name=None --log_file_path=None
```
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


## Configuration

- Provide your Kafka Consumer configurations in kafka_consumer_monitoring.cfg file

```
[kafka_consumer_1]
kafka_consumer_host=<KAFKA_CONSUMER_HOST_NAME>
kafka_consumer_jmx_port=<KAFKA_CONSUMER_PORT_NO>
kafka_consumer_partition=<KAFKA_CONSUMER_PARTITION_NO>
kafka_topic_name=<KAFKA_TOPIC_NAME>
kafka_consumer_client_id=<KAFKA_CONSUMER_CLIENT_ID>
logs_enabled=False
log_type_name=None
log_file_path=None

```

## Supported Metrics
The following metrics are captured by the Kafka Consumer Monitoring Plugin :

- **Records Lag Max(All Partitions)**
    
    Maximum number of messages consumer is behind producer across all partitions

- **Bytes Consumed Rate(All Topics)**
    
    Average number of bytes consumed per second across all topics.

- **Bytes Consumed Rate(Topic Specific)**

    Average number of bytes consumed per second for a specific topic

- **Records Consumed Rate(All Topics)**

    Average number of records consumed per second across all topics

- **Records Consumed Rate(Topic Specific)**

    Average number of records consumed per second for a specific topic

- **Fetch Rate**

    Number of fetch requests per second from the consumer

- **Records Lag**

    Number of messages consumer is behind producer on this partition

- **Records Lag Max**

    Maximum number of messages consumer is behind producer, for a specific partition

- **Records Per Request Avg**

    Average number of records in each request

- **Fetch Throttle Time Avg**

    Average throttle time milliseconds

- **Fetch Throttle Time Max**

    Maximum throttle time in milliseconds
- **Topic Name**

    Name of the Topic Specified to collect the metrics

- **Partition No.**

    Partition no specified to collect the metrics

- **Client ID**
    
    Client ID of the Consumer to collect the metrics

