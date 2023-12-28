# **Kafka Broker Monitoring**

## About Apache Kafka

Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.

## Kafka Broker
A Kafka broker is a single Kafka server that runs on a Kafka cluster. On deployment, each broker independently runs the Kafka broker process. Each broker hosts some set of partitions and handles events to write to the partition or read from them.

**Install the Kafka Broker plugin to monitor crucial Kafka broker processes.**


## Prerequisites

- To enable Kafka Broker JMX port

    Find the following code block in the kafka-server-start.sh script.


        if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
            export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
        fi


    Paste the following lines below the above code block.

        
        export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=9999"
        export JMX_PORT=9999
        
- Restart the kafka broker after the above changes.


- Install the jmxquery module for Python3.
  ```
  pip install jmxquery
  ```

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation
- Create a directory named "kafka_broker_monitoring" 
  
- Download all the files in the "kafka_broker_monitoring" folder.
  ```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/Kafka_Complete_Monitoring/Kafka_Broker_Monitoring/kafka_broker_monitoring.py && sed -i "1s|^.*|#! $(which python3)|" kafka_broker_monitoring.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/Kafka_Complete_Monitoring/Kafka_Broker_Monitoring/kafka_broker_monitoring.cfg
  ```

- Execute the below command with appropriate arguments to check for the valid json output:
    
        python3 kafka_broker_monitoring.py --kafka_host "KAFKA_BROKER_HOST_IP" --kafka_jmx_port "KAFKA_BROKER_PORT_NO" --kafka_consumer_partition "KAFKA_CONSUMER_PARTITION_NO" --kafka_topic_name "KAFKA_TOPIC_NAME" --logs_enabled "False" --log_type_name "None" --log_file_path "None"
    
- After above command with parameters gives expected output, please configure the relevant parameters in the kafka_broker_monitoring.cfg file.

        [kafka_broker_1]
        kafka_host="localhost"
        kafka_jmx_port="9999"
        kafka_consumer_partition="KAFKA_CONSUMER_PARTITION_NO"
        kafka_topic_name="KAFKA_TOPIC_NAME"
        logs_enabled="False"
        log_type_name="None"
        log_file_path="None"

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the kafka_broker_monitoring.py script.

- Place the "kafka_broker_monitoring" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/kafka_broker_monitoring
  
#### Windows
        
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "kafka_broker_monitoring" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\kafka_broker_monitoring

  
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
