#!/bin/bash

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION="1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server 
HEARTBEAT="true"

#Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS={attribute_1-'MB',attribute_2-'ms',attribute_3-'%'}

attribute_1=`awk -v min=1 -v max=1000 'BEGIN{srand(); print int(min+rand()*(max-min+1))}'`

attribute_2=`awk -v min=1 -v max=1000 'BEGIN{srand(); print int(min+rand()*(max-min+2))}'`

attribute_3=`awk -v min=1 -v max=1000 'BEGIN{srand(); print int(min+rand()*(max-min+5))}'`

attributes="attribute_1:$attribute_1|attribute_2:$attribute_2|attribute_3:$attribute_3"

default_attributes="plugin_version:$PLUGIN_VERSION|heartbeat_required:$HEARTBEAT|units:$METRICS_UNITS"

#After fetching your custom attributes kindly append the default attributes as follows:
echo "$attributes|$default_attributes"