#!/bin/bash

export JAVA_HOME="/usr/bin/java"

export PLUGIN_VERSION="1"

export HEARTBEAT="true"

if [ ! -f ./EhcachePlugin.class ]; then
 $JAVA_HOME/javac EhcachePlugin.java
fi

data=$($JAVA_HOME/java -cp . EhcachePlugin)

echo "$data|plugin_version:$PLUGIN_VERSION|heartbeat:$HEARTBEAT"