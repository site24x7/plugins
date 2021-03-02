#!/bin/bash

HOST="127.0.0.1"
PORT=7199
METRIC_FILE="metrics.txt"

JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/bin
PLUGIN_FOLDER="jmx"

PLUGIN_VERSION=1
HEARTBEAT="false"


#PLUGIN_PATH=$(pwd)
PLUGIN_PATH="/opt/site24x7/monagent/plugins/"$PLUGIN_FOLDER"/"

$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH/JMXMonitoring.java

data=$($JAVA_HOME/java -cp $PLUGIN_PATH JMXMonitoring $HOST $PORT $METRIC_FILE)

default_attributes="plugin_version:$PLUGIN_VERSION|heartbeat_required:$HEARTBEAT"

echo "$default_attributes|$data"
