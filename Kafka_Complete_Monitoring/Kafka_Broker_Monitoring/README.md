# **Kafka Broker Monitoring**

## About Apache Kafka

Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.

## Kafka Broker
A Kafka broker is a single Kafka server that runs on a Kafka cluster. On deployment, each broker independently runs the Kafka broker process. Each broker hosts some set of partitions and handles events to write to the partition or read from them.

**Install the Kafka Broker plugin to monitor crucial Kafka broker processes.**


## Prerequisites

- Install the jmxquery module for Python3.
  ```
  pip install jmxquery
  ```

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation
Create a directory named "kafka_broker_monitoring" under the Site24x7 Linux Agent plugin directory:
```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_broker_monitoring
  ```
Download all the files in the "kafka_broker_monitoring" folder and place them under the "kafka_broker_monitoring" directory.

Execute the below command with appropriate arguments to check for the valid json output:
```
python3 kafka_broker_monitoring.py --kafka_host=<KAFKA_BROKER_HOST_NAME> --kafka_jmx_port=<KAFKA_BROKER_PORT_NO> --kafka_consumer_partition=<KAFKA_CONSUMER_PARTITION_NO> --kafka_topic_name=<KAFKA_TOPIC_NAME> --logs_enabled=False --log_type_name=None --log_file_path=None
```

Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

## Configuration
Provide your Kafka Broker configurations in kafka_broker_monitoring.cfg file

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
The following metrics are captured by the Kafka Broker monitoring plugin :

- **Under Replicated Partitions**

    The number of unreplicated partitions
- **ISR Shrinks Per Sec**

    The rate at which the pool of in-sync replicas (ISRs) shrinks

- **ISR Expands Per Sec**

    The rate at which the pool of in-sync replicas (ISRs) expands
- **Active Controller Count**

    The number of active controllers in cluster

- **Offline Partitions Count**

    The number of offline partitions

- **Leader Election Rate And Time Ms**

    The leader election rate and latency

- **Unclean Leader Elections Per Sec**

    The number of “unclean” elections per second
- **Total Time Ms**

    The total time to serve the specified request

- **Purgatory Size**

    The number of requests waiting in producer purgatory
- **Bytes In Per Sec**

    The aggregate incoming byte rate
- **Network Request Rate**

    The average number of bytes sent per partition per request
- **Network Error Rate**

    The Error Rate of the network
- **Total Broker Partitions**

    The number of partitions on this broker. This should be mostly even across all brokers
- **Young Generation GC Count**

    The total count of young garbage collection processes executed by the JVM
- **Young Generation GC Time**

    The total amount of time (in milliseconds) the JVM has spent executing young garbage collection processes
- **Old Generation GC Count**

    The total count of old garbage collection processes executed by the JVM
- **Old Generation GC Time**

    The total amount of time (in milliseconds) the JVM has spent executing old garbage collection processes
- **Log End Offset**

    The log end offset is the offset of the last message written to a log.
