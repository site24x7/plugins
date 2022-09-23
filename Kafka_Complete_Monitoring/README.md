# **Kafka Complete Monitoring**

## Apache Kafka

Apache Kafka is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real time data feeds.



## Starting Kafka with JMX

- #### Starting Kafka Broker at JMX port 9999
  ```
  JMX_PORT=9999 bin/kafka-server-start.sh config/server.properties
  ```
    *Incase if port 9999 is occupied choose a open port*

&nbsp;


- #### Starting Kafka Producer at JMX port 9982
  ```
  JMX_PORT=9982 bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
  ```
  *Incase if port 9982 is occupied choose a open port*

&nbsp;


- #### Starting Kafka Consumer at JMX port 9983
  ```
  JMX_PORT=9983 bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
  ```
  *Incase if port 9983 is occupied choose a open port*

