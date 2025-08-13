#!/bin/bash
set echo off

PLUGIN_VERSION="1"
HEARTBEAT_REQUIRED="true"


HOST=""
PORT=""
USERNAME=""
PASSWORD=""
JAVA_HOME="/usr/bin"

PLUGIN_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CLASS_PATH=$PLUGIN_PATH/json-20140107.jar:$PLUGIN_PATH/jconn4.jar

$JAVA_HOME/javac -Xlint:deprecation -cp $CLASS_PATH -d $PLUGIN_PATH $PLUGIN_PATH"/sybaseDB.java"
data=$($JAVA_HOME/java -cp $CLASS_PATH:$PLUGIN_PATH "sybaseDB" $PLUGIN_VERSION $HEARTBEAT_REQUIRED $HOST $PORT $USERNAME $PASSWORD)

echo "$data"
