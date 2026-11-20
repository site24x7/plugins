#!/bin/bash

HOST="localhost"
PORT="7199"
JMX_USER="site24x7"
JMX_PASSWORD="plugin123"
KEYSTORE="/home/murali/cassandra/cassandra4.0.13/conf/NewCerts/cassandra4.keystore.jks"
KEYSTORE_PASSWORD="cassandra"
TRUSTSTORE="/home/murali/cassandra/cassandra4.0.13/conf/NewCerts/cassandra4.truststore.jks"
TRUSTSTORE_PASSWORD="cassandra"



JAVA_HOME="/home/plugin-team/java/jdk-11.0.22/bin"

PLUGIN_FOLDER_NAME="Cassandra"

PLUGIN_PATH="/opt/site24x7/monagent/plugins/"$PLUGIN_FOLDER_NAME

export CLASSPATH=$CLASSPATH:$PLUGIN_PATH"/json-simple-2.1.2.jar":$PLUGIN_PATH

#$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH"/CassandraSSL.java"
#$JAVA_HOME/javac -cp ".:json-simple-2.1.2.jar" $PLUGIN_PATH"/CassandraSSL.java"
$JAVA_HOME/javac $PLUGIN_PATH"/CassandraSSL.java"


#data=$($JAVA_HOME/java -cp $PLUGIN_PATH "Cassandra" $HOST $PORT $JMX_USER $JMX_PASSWORD $KEYSTORE $KEYSTORE_PASSWORD $TRUSTSTORE $TRUSTSTORE_PASSWORD)

#data=$($JAVA_HOME/java -cp ".:json-simple-2.1.2.jar" "CassandraSSL" $HOST $PORT $JMX_USER $JMX_PASSWORD $KEYSTORE $KEYSTORE_PASSWORD $TRUSTSTORE $TRUSTSTORE_PASSWORD)
data=$($JAVA_HOME/java "CassandraSSL" $HOST $PORT $JMX_USER $JMX_PASSWORD $KEYSTORE $KEYSTORE_PASSWORD $TRUSTSTORE $TRUSTSTORE_PASSWORD)

echo "$data"
