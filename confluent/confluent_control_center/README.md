# Confluent Platform Plugin
---

## Plugin Setup

### Prerequisites

* Monitoring data is fetched using JMX Configuration

* How to enable JMX configuration
    ---
    
    Locate the file control-center-run-class.sh and add the line "export JMX_PORT=9991". If port 9991 is occupied please choose a different one.


## Plugin installation

### Linux

* Create a directory "confluent_control_center".

* Go to the created directory and run the following commands

		wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent/confluent_control_center/confluent_control_center.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent/confluent_control_center/ConfluentPlatform.java
		
* Open confluent_control_center.sh and Set the values for **HOSTNAME**, **PORT** , **JAVA_HOME**

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field. Make sure to paste the path to bin directory and not the path to java

* Move the directory "confluent_control_center" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluent_control_center

* The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics captured
---

List of metrics can be found in the help doc

* Producer Metrics - https://docs.confluent.io/3.3.0/kafka/monitoring.html#kafka-monitoring-metrics-producer
* Consumer Metrics - https://docs.confluent.io/3.3.0/kafka/monitoring.html#kafka-monitoring-metrics-consumer
* Streams Metrics - https://docs.confluent.io/3.3.0/streams/monitoring.html#task-metrics
