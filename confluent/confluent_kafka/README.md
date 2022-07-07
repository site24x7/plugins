#Confluent Platform Plugin
---

## Plugin Setup

### Prerequisites
* Monitoring data is fetched using JMX Configuration

* How to enable JMX configuration
    ---
    
    To Enable JMX Configuration: append line -Dcom.sun.management.jmxremote.rmi.port=9992 in variable KAFKA_JMX_OPTS under section #JMX settings in kafka-run-class.sh and add line export JMX_PORT=9992 before line exec $base_dir/kafka-run-class.sh $EXTRA_ARGS kafka.Kafka $@ in kafka-server-start.sh. If port 9992 is occupied please choose a different one.


## Plugin installation

### Linuxii
* Create a directory "confluent_kafka" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluent_kafka

* Go to the created directory and run the following commands
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent_kafka/confluent_kafka.sh`
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent_kafka/ConfluentPlatform.java`


### Plugin configuration
---
* Open confluent_kafka.sh and Set the values for **HOSTNAME**, **PORT** , **JAVA_HOME**

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field. Make sure to paste the path to bin directory and not the path to java

### Metrics captured
---

Metrics explanation can be found here : https://docs.confluent.io/current/kafka/monitoring.html#broker-metrics

####Kafka Server Metrics
* ReplicaManager.UnderReplicatedPartitions
* KafkaController.OfflinePartitionsCount
* KafkaController.ActiveControllerCount

####Kafka Broker Metrics
* BrokerTopicMetrics.MessagesInPerSec
* BrokerTopicMetrics.BytesInPerSec
* BrokerTopicMetrics.BytesOutPerSec
* RequestMetrics.RequestsPerSec
* LogFlushStats.LogFlushRateAndTimeMs
* ControllerStats.LeaderElectionRateAndTimeMs
* ControllerStats.UncleanLeaderElectionsPerSec
* ReplicaManager.PartitionCount
* ReplicaManager.LeaderCount
* ReplicaManager.IsrShrinksPerSec
* ReplicaFetcherManager.MaxLag
* FetcherLagMetrics.ConsumerLag
* RequestMetrics.TotalTimeMs
* ProducerRequestPurgatory.PurgatorySize
* FetchRequestPurgatory.PurgatorySize
