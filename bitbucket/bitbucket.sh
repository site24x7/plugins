#!/bin/bash

HOST="127.0.0.1"
PORT=3333
PLUGIN_VERSION=1
HEARTBEAT_REQUIRED="true"
RMI_UNAME=""
RMI_PASSWORD=""

export RMI_UNAME
export RMI_PASSWORD

#JAVA_HOME="/lib/jdk8/jdk/bin" 

PLUGIN_FOLDER_NAME="bitbucket"

PLUGIN_PATH="/opt/site24x7/monagent/plugins/"$PLUGIN_FOLDER_NAME

$JAVA_HOME/javac -d $PLUGIN_PATH $PLUGIN_PATH"/Bitbucket.java"

data=$($JAVA_HOME/java -cp $PLUGIN_PATH "Bitbucket" $HOST $PORT $PLUGIN_VERSION $HEARTBEAT_REQUIRED)

echo "$data"
