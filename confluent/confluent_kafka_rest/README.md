#Confluent Platform - Kafka Rest Plugin
---

## Plugin Setup

### Prerequisites
* Monitoring data is fetched using JMX Configuration

* How to enable JMX configuration
    ---
    
    Look for the file ksql-run-class.sh and add the line "export JMX_PORT=9993". If port 9993 is occupied please choose a different one.


## Plugin installation

### Linux
* Create a directory "confluent_kafka_rest".

* Go to the created directory and run the following commands

		wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent/confluent_kafka_rest/confluent_kafka_rest.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent/confluent_kafka_rest/ConfluentPlatform.java
		
* Open confluent_kafka_rest.sh and Set the values for **HOSTNAME**, **PORT** , **JAVA_HOME**

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field. Make sure to paste the path to bin directory and not the path to java

* Move the directory "confluent_kafka_rest" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluent_kafka_rest

* The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics captured
---

List of metrics can be found in the help doc:

* jetty-metrics - https://docs.confluent.io/current/kafka-rest/monitoring.html#global-metrics
* jersey-metrics - https://docs.confluent.io/current/kafka-rest/monitoring.html#per-endpoint-metrics
