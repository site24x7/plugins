# **Kafka Producer Monitoring**

## Apache Kafka

Apache Kafka is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real time data feeds.

## Kafka Producer

The Kafka producer is conceptually much simpler than the consumer since it has no need for group coordination. A producer partitioner maps each message to a topic partition, and the producer sends a produce request to the leader of that partition.

**Therefore it is pivotal to monitor the Kafka Producer**

## Prerequisites
 - Installation of jmxquery module for Python3
```
pip install jmxquery
```

 - Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation

- Create a directory named "kafka_producer_monitoring" under the Site24x7 Linux Agent plugin directory

```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_producer_monitoring
```

 - Download all the files in the "kafka_producer_monitoring" folder and place it under the "kafka_producer_monitoring" directory. 

```
wget https://raw.githubusercontent.com/site24x7/plugins/master/Kafka_Complete_Monitoring/Kafka_Producer_Monitoring/kafka_producer_monitoring.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/Kafka_Complete_Monitoring/Kafka_Producer_Monitoring/kafka_producer_monitoring.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```
python3 kafka_producer_monitoring.py --kafka_producer_host=<KAFKA_PRODUCER_HOST_NAME> kafka_producer_jmx_port=<KAFKA_PRODUCER_PORT_NO> --kafka_producer_client_id=<KAFKA_PRODUCER_CLIENT_ID> --logs_enabled=False --log_type_name=None --log_file_path=None
```
Since it's a python plugin, to run in windows server please follow the steps in below link, remaining configuration steps are exactly the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers


## Configuration

- Provide your Kafka Producer configurations in kafka_producer_monitoring.cfg file

```
[kafka_producer_1]
kafka_producer_host=<KAFKA_PRODUCER_HOST_NAME>
kafka_producer_jmx_port=<KAFKA_PRODUCER_PORT_NO>
kafka_producer_client_id=<KAFKA_PRODUCER_CLIENT_ID>
logs_enabled=False
log_type_name=None
log_file_path=None


```

## Supported Metrics
The following metrics are captured by the Kafka Producer Monitoring Plugin :

- **Compression Rate Avg**
    
    Average compression rate of batches sent

- **Response Rate**
    
    Average number of bytes consumed per second across all topics.

- **Request Rate**

    Average number of requests sent per second

- **Request Latency Avg**

    Average request latency
- **Outgoing Byte Rate**

    Average number of outgoing/incoming bytes per second

- **IO Wait Time NS Avg**

    Average length of time the I/O thread spent waiting for a socket

- **Batch Size Avg**

    The average number of bytes sent per partition per request

- **Client ID**

    Client ID Name









