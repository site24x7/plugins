
# **Complete Kafka Monitoring**

## **Apache Kafka**

Apache Kafka is an open-source distributed stream-processing platform developed by the Apache Software Foundation. It is written in Java and Scala, and is used to collect, process, and store real-time data streams. Its core capabilities include high throughput, scalability, and low latency, and it is often used to build stream data pipelines and applications.




## Starting Kafka with JMX

### **To enable Kafka Broker JMX port**

Find the following code block in the kafka-server-start.sh script.

```
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
fi
```

Paste the following lines below the above code block.

```
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=<JMX_PORT>"
export JMX_PORT=<JMX_PORT>
```
Replace the <JMX_PORT> with a desirable port.


### **To enable Kafka Producer JMX port**

Find the following similar code block in the kafka-console-producer.sh script.

```
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx512M"
fi
```
And paste the following lines below the above code block.

```
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=<JMX_PORT>"
export JMX_PORT=<JMX_PORT>
```
Replace the <JMX_PORT> with a desirable port.




 

### **To enable Kafka Consumer JMX port**

Find the following similar code block in the kafka-console-consumer.sh script.

```
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx512M"
fi
```
And paste the following lines below the above code block.

```
export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=<JMX_PORT>"
export JMX_PORT=<JMX_PORT>
```
Replace the <JMX_PORT> with a desirable port.

