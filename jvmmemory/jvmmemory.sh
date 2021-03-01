#!/bin/bash

JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/bin
PLUGIN_FOLDER="jvx"
PLUGIN_PATH="/opt/site24x7/monagent/plugins/jvmmemory/"
$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH/JVMMemoryMonitoring.java
data=$($JAVA_HOME/java -cp $PLUGIN_PATH JVMMemoryMonitoring)
echo "$data"
