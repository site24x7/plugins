#!/bin/bash

JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/bin
PLUGIN_FOLDER="jvm"
PLUGIN_PATH="/opt/site24x7/monagent/plugins/jvm/"
host="127.0.0.1"   
port=7199
plugin_version="5" 
heartbeat_required="true"  
$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH/JVMMonitoring.java
data=$($JAVA_HOME/java -cp $PLUGIN_PATH JVMMonitoring "$host" "$port" "$plugin_version" "$heartbeat_required")
echo "$data"
