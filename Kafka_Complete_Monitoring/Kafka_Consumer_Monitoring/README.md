# **Kafka Consumer Monitoring**

## About Apache Kafka
Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.
Kafka Consumer
A Kafka consumer is a client application that pulls event data from one or more Kafka topics. 

**Install the Kafka Consumer plugin and monitor key consumer metrics.**

## Prerequisites
- To enable Kafka Consumer JMX port

Find the following similar code block in the kafka-console-consumer.sh script.

```
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx512M"
fi
```
And paste the following lines below the above code block.

```
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=9997"
export JMX_PORT=9997
```
**Restart the kafka consumer after the above changes.**
- Install the jmxquery module for Python3.

    ```
    pip install jmxquery
    ```
- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend to run the plugin.


## Plugin Installation

Create a directory named "kafka_consumer_monitoring" under the Site24x7 Linux Agent plugin directory:
```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_consumer_monitoring
  ```
Download all the files in the "kafka_consumer_monitoring" folder and place them under the "kafka_consumer_monitoring" directory.

**Execute the below command with appropriate arguments to check for the valid json output:**

```
python3 kafka_consumer_monitoring.py --kafka_consumer_host=<KAFKA_CONSUMER_HOST_NAME> kafka_consumer_jmx_port=<KAFKA_CONSUMER_PORT_NO> --kafka_consumer_partition=<KAFKA_CONSUMER_PARTITION_NO> --kafka_topic_name=<KAFKA_TOPIC_NAME> --kafka_consumer_client_id=<KAFKA_CONSUMER_CLIENT_ID> --logs_enabled=False --log_type_name=None --log_file_path=None
```

Since it's a Python plugin, to run the plugin on a Windows server, please follow the steps in the below link. The remaining configuration steps are the same. https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

### Configuration
Provide your Kafka Consumer configurations in kafka_consumer_monitoring.cfg file

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
The following metrics are captured by the Kafka Consumer monitoring plugin :

- **Records Lag Max(All Partitions)**

    The maximum number of messages consumer is behind producer across all partitions
- **Bytes Consumed Rate(All Topics)**

    The average number of bytes consumed per second across all topics.
- **Bytes Consumed Rate(Topic Specific)**

    The average number of bytes consumed per second for a specific topic

- **Records Consumed Rate(All Topics)**

    The average number of records consumed per second across all topics
- **Records Consumed Rate(Topic Specific)**

    The average number of records consumed per second for a specific topic
- **Fetch Rate**

    The number of fetch requests per second from the consumer
- **Records Lag**

    The number of messages consumer is behind producer on this partition

- **Records Lag Max**

    The maximum number of messages consumer is behind producer for a specific partition

- **Records Per Request Avg**

    The average number of records in each request
- **Fetch Throttle Time Avg**

    The average throttle time in milliseconds
- **Fetch Throttle Time Max**

    The maximum throttle time in milliseconds
- **Topic Name**

    The name of the Topic Specified to collect the metrics
- **Partition No.**

    The partition number specified to collect the metrics
- **Client ID**
 
    The client ID of the Consumer to collect the metrics

