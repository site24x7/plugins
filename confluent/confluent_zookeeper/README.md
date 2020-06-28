#Confluent Platform - Zookeeper Plugin
---

## Plugin Setup

### Prerequisites
* Monitoring data is fetched using JMX Configuration

* How to enable JMX configuration
    ---
    Locate the file kafka-run-class.sh and add the line "export JMX_PORT=9994".
    If already configured for confluent_kafka plugin this step can be ignored.


## Plugin installation

### Linux
* Create a directory "confluent_zookeeper" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluent_zookeeper

* Go to the created directory and run the following commands
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent_zookeeper/confluent_zookeeper.sh`
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent_zookeeper/ConfluentPlatform.java`


### Plugin configuration
---
* Open confluent_zookeeper.sh and Set the values for **HOSTNAME**, **PORT** , **JAVA_HOME**

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field. Make sure to paste the path to bin directory and not the path to java

### Metrics captured
---

List of metrics can be found in the help doc: https://docs.confluent.io/current/kafka/monitoring.html#zk-metrics

* SessionExpireListener.ZooKeeperDisconnectsPerSec
* SessionExpireListener.ZooKeeperExpiresPerSec
* SessionExpireListener.ZooKeeperSyncConnectsPerSec
* SessionExpireListener.ZooKeeperAuthFailuresPerSec
* SessionExpireListener.ZooKeeperReadOnlyConnectsPerSec
* SessionExpireListener.ZooKeeperSaslAuthenticationsPerSec