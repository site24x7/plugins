#!/bin/bash
set echo off


HOST=""
PORT=""
USERNAME=""
PASSWORD=""
JAVA_HOME="/usr/bin"

PLUGIN_FOLDER_NAME="sybase"

PLUGIN_PATH=""
export CLASS_PATH=$PLUGIN_PATH/json-20140107.jar:$PLUGIN_PATH/jconn4.jar

$JAVA_HOME/javac -cp $CLASS_PATH -d $PLUGIN_PATH $PLUGIN_PATH"/sybaseInstaller.java"
data=$($JAVA_HOME/java -cp $CLASS_PATH:$PLUGIN_PATH "sybaseInstaller" $HOST $PORT $USERNAME $PASSWORD)

echo "$data"

