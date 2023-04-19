# **Kafka Producer Monitoring**

## About Apache Kafka
Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.

## Kafka Producer
Producers are client applications that send data into Kafka broker topics. 
Install the Apache Kafka Producer plugin to monitor key Kafka producer metrics and ensure a steady flow of data.


### Prerequisites
- To enable Kafka Producer JMX port

Find the following similar code block in the kafka-console-producer.sh script.

```
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx512M"
fi
```
And paste the following lines below the above code block.

```
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=9998"
export JMX_PORT=9998
```

- Install the jmxquery module for Python3.
```
pip install jmxquery
```

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you intend  to run the plugin.



### Plugin Installation

Create a directory named "kafka_producer_monitoring" under the Site24x7 Linux Agent plugin directory:

```
  Linux    ->   /opt/site24x7/monagent/plugins/kafka_producer_monitoring
```
Download all the files in the "kafka_producer_monitoring" folder and place them under the "kafka_producer_monitoring" directory.

Execute the below command with appropriate arguments to check for the valid json output:

```
python3 kafka_producer_monitoring.py --kafka_producer_host=<KAFKA_PRODUCER_HOST_NAME> kafka_producer_jmx_port=<KAFKA_PRODUCER_PORT_NO> --kafka_producer_client_id=<KAFKA_PRODUCER_CLIENT_ID> --logs_enabled=False --log_type_name=None --log_file_path=None
```

Since this is a Python plugin, to run the plugin in a Windows server, please follow the steps in the below link. The remaining configuration steps are the same. 
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

### **Configuration**
##### Provide your Kafka Producer configurations in kafka_producer_monitoring.cfg file:

```
[kafka_producer_1]
kafka_producer_host=localhost
kafka_producer_jmx_port=9998
kafka_producer_client_id=<KAFKA_PRODUCER_CLIENT_ID>
logs_enabled=False
log_type_name=None
log_file_path=None
```
#### Supported Metrics
The following metrics are captured by the Kafka Producer monitoring plugin :

- **Compression Rate Avg**

    The average compression rate of batches sent

- **Response Rate**

    The average number of bytes consumed per second across all topics.
- **Request Rate**

    The average number of requests sent per second

- **Request Latency Avg**

    The average request latency
- **Outgoing Byte Rate**

    The average number of outgoing/incoming bytes per second
- **IO Wait Time NS Avg**

    The average length of time the I/O thread spent waiting for a socket
- **Batch Size Avg**

    The average number of bytes sent per partition per request
- **Client ID**

    Client ID Name
