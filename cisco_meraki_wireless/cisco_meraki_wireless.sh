#!/bin/bash
set echo off

APIKEY=$1
NETWORKID=$2
BASEURL=$3
JAVA_HOME=$4

POLL_INTERVAL="5"
PLUGIN_VERSION="1"
HEARTBEAT_REQUIRED="true"

PLUGIN_FOLDER_NAME="cisco_meraki_wireless"

PLUGIN_PATH="/opt/site24x7/monagent/plugins/"$PLUGIN_FOLDER_NAME
export CLASS_PATH=$PLUGIN_PATH/json.jar:$PLUGIN_PATH/httpcore-4.4.10.jar:$PLUGIN_PATH/httpclient-4.5.6.jar:$PLUGIN_PATH/commons-logging-1.2.jar:$PLUGIN_PATH/commons-codec-1.10.jar

$JAVA_HOME/javac -cp $CLASS_PATH -d $PLUGIN_PATH $PLUGIN_PATH"/MerakiDataCollector.java"
data=$($JAVA_HOME/java -cp $CLASS_PATH:$PLUGIN_PATH "MerakiDataCollector" $APIKEY $NETWORKID $BASEURL $POLL_INTERVAL $PLUGIN_VERSION $HEARTBEAT_REQUIRED)

echo "$data"