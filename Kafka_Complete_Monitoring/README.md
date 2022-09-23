
# **Complete Kafka Monitoring**

## **Apache Kafka**

Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.




## Starting Kafka with JMX

**Starting Kafka Broker at JMX port 9999**
```
JMX_PORT=9999 bin/kafka-server-start.sh config/server.properties
```
*In case port 9999 is occupied, choose an open port.*

 
**Starting Kafka Producer at JMX port 9982**

```
JMX_PORT=9982 bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
```
*In case port 9982 is occupied, choose an open port.*

 
**Starting Kafka Consumer at JMX port 9983**

```
JMX_PORT=9983 bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
```
*In case port 9983 is occupied, choose an open port.*

