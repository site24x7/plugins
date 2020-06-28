#!/bin/bash

HOST="127.0.0.1"
PORT=9991

PLUGIN_VERSION=1
HEARTBEAT="true"

JAVA_HOME="/usr/bin"

PLUGIN_FOLDER_NAME="confluent"

PLUGIN_PATH="/opt/site24x7/monagent/plugins/"$PLUGIN_FOLDER_NAME

$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH"/ConfluentPlatform.java"

data=$($JAVA_HOME/java -cp $PLUGIN_PATH "ConfluentPlatform" $HOST $PORT)

echo "$data"