# **Apache Kafka Monitoring**

## About Apache Kafka

Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.



## Quick installation

If you're using Linux servers, use the Oracle plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/kafka/installer/Site24x7KafkaPluginInstaller.sh && sudo bash Site24x7KafkaPluginInstaller.sh
```

## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.


### Prerequisites

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

### Plugin Installation
- Create a directory named "kafka" 
  
- Download all the files in the "kafka" folder.
  ```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/kafka/kafka.py && sed -i "1s|^.*|#! $(which python3)|" kafka.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/kafka/kafka.cfg
  ```

- Execute the below command with appropriate arguments to check for the valid json output:
    
        python3 kafka.py --kafka_host "KAFKA_BROKER_HOST_IP" --kafka_jmx_port "KAFKA_BROKER_PORT_NO"
    
- After above command with parameters gives expected output, please configure the relevant parameters in the kafka.cfg file.

      [kafka_instance]
      kafka_host="localhost"
      kafka_jmx_port=9999


#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the kafka.py script.

- Place the "kafka" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/kafka
  
#### Windows
        
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "kafka" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\kafka

## Supported Metrics
The following metrics are captured by the Kafka monitoring plugin:

### Traffic Metrics

| Metric Name                                      | Description                                                                                           |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Bytes In Per Sec                                 | Rate of bytes received by the broker per second.                                                      |
| Bytes Out Per Sec                                | Rate of bytes sent by the broker per second.                                                          |
| Total Fetch Requests Per Sec                     | Total rate of fetch requests per second.                                                              |
| Total Produce Requests Per Sec                   | Total rate of produce requests per second.                                                            |
| Failed Fetch Requests Per Sec                    | Rate of fetch requests that failed per second.                                                        |
| Failed Produce Requests Per Sec                  | Rate of produce requests that failed per second.                                                      |

### Replication Metrics

| Metric Name                                      | Description                                                                                           |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Replication Bytes In Per Sec                     | Rate of bytes replicated to the broker per second.                                                    |
| Replication Bytes Out Per Sec                    | Rate of bytes replicated from the broker per second.                                                  |
| Reassignment Bytes In Per Sec                    | Rate of bytes reassigned to the broker per second.                                                    |
| Reassignment Bytes Out Per Sec                   | Rate of bytes reassigned from the broker per second.                                                  |
| Under Replicated Partitions                      | Number of under-replicated partitions.                                                                |
| Under Min Isr Partition Count                    | Number of partitions with replicas under the minimum in-sync replicas.                                |
| Replicas Ineligible To Delete Count              | Number of replicas not eligible for deletion.                                                         |
| Replicas To Delete Count                         | Number of replicas pending deletion.                                                                  |

### ISR (In-Sync Replica) Metrics

| Metric Name                                      | Description                                                                                           |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| At Min Isr Partition Count                       | Number of partitions with replicas currently at or below the minimum in-sync replicas.                |
| Isr Expands Per Sec                              | Rate of in-sync replica expansion per second.                                                         |
| Isr Shrinks Per Sec                              | Rate of in-sync replica shrinkage per second.                                                         |
| Partitions With Late Transactions Count          | Number of partitions with late transactions.                                                          |
| Leader Count                                     | Number of leaders managed by the replication manager.                                                 |
| Producer Id Count                                | Number of active producer IDs.                                                                        |

### Controller Metrics

| Metric Name                                      | Description                                                                                           |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Active Controller Count                          | Number of active controllers in the Kafka cluster.                                                    |
| Offline Partitions Count                         | Number of partitions that are offline.                                                                |
| Global Partition Count                           | Total number of partitions across all brokers.                                                        |
| Leader Election Rate                             | Rate of leader elections in the cluster.                                                              |
| Total Topics Count                               | Total number of topics in the Kafka cluster.                                                          |
| Topics Ineligible To Delete Count                | Number of topics not eligible for deletion.                                                           |
| Topics To Delete Count                           | Number of topics pending deletion.                                                                    |

### Purgatory Metrics

| Metric Name                                      | Description                                                                                           |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Purgatory Size Produce                           | Number of produce requests in purgatory.                                                              |
| Purgatory Size Fetch                             | Number of fetch requests in purgatory.                                                                |
| ZooKeeper Disconnects Per Sec                    | Rate of ZooKeeper disconnections per second.                                                          |


| Metric Name                                      | Description                                                                                           |
|--------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Bytes Rejected Per Sec                           | Rate of bytes rejected by the broker per second.                                                      |
| Fetch Message Conversions Per Sec                | Rate of fetch message conversions per second.                                                         |
| Invalid Magic Number Records Per Sec             | Rate of records with invalid magic numbers per second.                                                |
| Invalid Message Crc Records Per Sec              | Rate of records with invalid message CRC per second.                                                  |
| Invalid Offset Or Sequence Records Per Sec       | Rate of records with invalid offsets or sequences per second.                                         |
| No Key Compacted Topic Records Per Sec           | Rate of records in compacted topics with no key per second.                                           |
| Produce Message Conversions Per Sec              | Rate of produce message conversions per second.                                                       |
| Reassigning Partitions                           | Number of partitions currently being reassigned.                                                      |
| Current Control ID                               | Current control ID of the Kafka controller.                                                           |
| Request Handler Avg Idle Percent                 | Average idle percentage of request handlers.                                                          |
