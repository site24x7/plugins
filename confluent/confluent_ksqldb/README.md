#Confluent Platform - KSQLDB Plugin
---

## Plugin Setup

### Prerequisites
* Monitoring data is fetched using JMX Configuration

* How to enable JMX configuration
    ---
    
    Locate file ksql-run-class.sh and add the line "export JMX_PORT=9994". If port 9994 is occupied please choose a different one.


## Plugin installation

### Linux
* Create a directory "confluent_ksqldb".

* Go to the created directory and run the following commands

		wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent/confluent_ksqldb/confluent_ksqldb.sh
		wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent/confluent_ksqldb/ConfluentPlatform.java
		
* Open confluent_ksqldb.sh and Set the values for **HOSTNAME**, **PORT** , **JAVA_HOME**

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field. Make sure to paste the path to bin directory and not the path to java

* Move the directory "confluent_ksqldb" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluent_ksqldb

* The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Metrics captured
---

List of metrics can be found in help doc - https://docs.ksqldb.io/en/latest/operate-and-deploy/installation/server-config/#jmx-metrics
