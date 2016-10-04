#!/bin/bash

#This Plugin executes the MulePlugin JAVA class to get the mule server details to monitor
#######################################@FILE AND DIRECTORY COUNT@######################################
# INPUT :
# PLUGIN_VERSION = Version of this Plugins - If there is any change in this Script. Need to increase the Plugin Version as 2,3,4 etc to 
# make the changes to take effect.
# HEARTBEAT = true/false. If it true,Site24x7 will alert if the Plugins will not send the data for 5 mins
# METRICS_UNITS = If you need Units for the attributes, then add Unit the given format 
##########################################################################################################
# Attributes Monitored:
# memory_usage
# min_processing_time
# max_processing_time
# avg_processing_time
# processed_events
# sync_events_received
# async_events_received
# execution_errors
# fatal_errors
##########################################################################################################


##########INPUTS#########################
export PLUGIN_VERSION="1"

export HEARTBEAT="true"


data=$(java -cp /opt/site24x7/monagent/plugins/mule MulePlugin)

echo "$data|plugin_version:$PLUGIN_VERSION|heartbeat:$HEARTBEAT"
