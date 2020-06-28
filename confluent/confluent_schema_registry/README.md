#Confluent Platform - Schema Registry Plugin
---

## Plugin Setup

### Prerequisites
* Monitoring data is fetched using JMX Configuration

* How to enable JMX configuration
    ---
    
    Locate the file schema-registry-run-class.sh and add the line "export JMX_PORT=9995". If port 9995 is occupied please choose a different one.


## Plugin installation

### Linux
* Create a directory "confluent_schema_registry" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/confluent_schema_registry

* Go to the created directory and run the following commands
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent_schema_registry/confluent_schema_registry.sh`
    `wget https://raw.githubusercontent.com/site24x7/plugins/master/confluent_schema_registry/ConfluentPlatform.java`


### Plugin configuration
---
* Open confluent_schema_registry.sh and Set the values for **HOSTNAME**, **PORT** , **JAVA_HOME**

* If the java classpath is not set in your machine, run the commaand- `which java`. Copy the output you get and paste it in the *JAVA_HOME* field. Make sure to paste the path to bin directory and not the path to java

### Metrics captured
---

List of metrics can be found in the help doc

* jetty-metrics - https://docs.confluent.io/current/schema-registry/monitoring.html#mbean-kafka-schema-registry-type-jetty-metrics
* master-slave-role - https://docs.confluent.io/current/schema-registry/monitoring.html#mbean-kafka-schema-registry-type-master-slave-role
* jersey-metrics - https://docs.confluent.io/current/schema-registry/monitoring.html#per-endpoint-metrics
