# **Kafka Broker Monitoring**

## Apache Kafka

Apache Kafka is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real time data feeds.

## Kafka Broker

Apache Kafka is composed of a network of machines called brokers. In a contemporary deployment, these may not be separate physical servers but containers running on pods running on virtualized servers running on actual processors in a physical datacenter somewhere. However they are deployed, they are independent machines each running the Kafka broker process. Each broker hosts some set of partitions and handles incoming requests to write new events to those partitions or read events from them. Brokers also handle replication of partitions between each other.



**Therefore it is pivotal to monitor the Kafka Broker**

## Prerequisites
 - Installation of jmxquery module for Python3
```
pip install jmxquery
```

 - Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation

- Create a directory named "kafka_broker_monitoring" under the Site24x7 Linux Agent plugin directory

```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_broker_monitoring
```

 - Download all the files in the "kafka_broker_monitoring" folder and place it under the "kafka_broker_monitoring" directory. 

```


```

- Execute the below command with appropriate arguments to check for the valid json output:

```
python3 kafka_broker_monitoring.py --kafka_host=<KAFKA_BROKER_HOST_NAME> --kafka_jmx_port=<KAFKA_BROKER_PORT_NO> --kafka_consumer_partition=<KAFKA_CONSUMER_PARTITION_NO> --kafka_topic_name=<KAFKA_TOPIC_NAME> --logs_enabled=False --log_type_name=None --log_file_path=None
```
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


## Configuration

- Provide your Kafka Producer configurations in kafka_producer_monitoring.cfg file

```
[kafka_broker_1]
kafka_host=<KAFKA_BROKER_HOST_NAME>
kafka_jmx_port=<KAFKA_BROKER_PORT_NO>
kafka_consumer_partition=<KAFKA_CONSUMER_PARTITION_NO>
kafka_topic_name=<KAFKA_TOPIC_NAME>
logs_enabled=False
log_type_name=None
log_file_path=None





```

## Supported Metrics
The following metrics are captured by the Kafka Producer Monitoring Plugin :

- **Under Replicated Partitions**
    
    Number of unreplicated partitions

- **ISR Shrinks Per Sec**
    
    Rate at which the pool of in-sync replicas (ISRs) shrinks

- **ISR Expands Per Sec**

    Rate at which the pool of in-sync replicas (ISRs) expands

- **Active Controller Count**

    Number of active controllers in cluster

- **Offline Partitions Count**

    Number of offline partitions

- **Leader Election Rate And Time Ms**

    Leader election rate and latency

- **Unclean Leader Elections Per Sec**

    Number of “unclean” elections per second

- **Total Time Ms**

    Total time to serve the specified request



- **Purgatory Size**

    Number of requests waiting in producer purgatory

- **Bytes In Per Sec**

    Aggregate incoming byte rate

- **Network Request Rate**

    The average number of bytes sent per partition per request

- **Network Error Rate**

    The Error Rate of the network


- **Total Broker Partitions**

    Number of partitions on this broker. This should be mostly even across all brokers

- **Young Generation GC Count**

    The total count of young garbage collection processes executed by the JVM

- **Young Generation GC Time**

    The total amount of time (in milliseconds) the JVM has spent executing young garbage collection processes

- **Old Generation GC Count**

    The total count of old garbage collection processes executed by the JVM

- **Old Generation GC Time**

    The total amount of time (in milliseconds) the JVM has spent executing old garbage collection processes

- **Log End Offset**

    The log end offset is the offset of the last message written to a log


