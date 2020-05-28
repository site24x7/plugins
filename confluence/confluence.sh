#!/bin/bash

HOST="127.0.0.1"
PORT=8099
RMI_UNAME=""
RMI_PASSWORD=""
PLUGIN_VERSION=2
HEARTBEAT_REQUIRED="true"

export RMI_UNAME
export RMI_PASSWORD

#JAVA_HOME="/lib/jdk8/jdk/bin" 

PLUGIN_FOLDER_NAME="confluence"

PLUGIN_PATH="/opt/site24x7/monagent/plugins/"$PLUGIN_FOLDER_NAME

$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH"/Confluence.java"

data=$($JAVA_HOME/java -cp $PLUGIN_PATH "Confluence" $HOST $PORT $PLUGIN_VERSION $HEARTBEAT_REQUIRED)

echo "$data"
