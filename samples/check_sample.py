#!/usr/bin/python

import json

from random import randint

#if any changes are made to this plugin, kindly update the plugin version here.
PLUGIN_VERSION = "1" 

#Setting this to true will alert you when there is a communication problem while posting plugin data to server 
HEARTBEAT="true"

#Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS={'metric_1':'MB', 'metric_2':'ms'}

def metricCollector():
	  data = {}
	  data['plugin_version'] = PLUGIN_VERSION
	  data['heartbeat_required'] = HEARTBEAT
	  data['metric_1']=randint(0,1000)
	  data['metric_2']=randint(0,500)
	  data['metric_3']=randint(0,100)
	  data['units']=METRICS_UNITS
	  return data

if __name__ == "__main__":

     result = metricCollector() 

     print(json.dumps(result, indent=4, sort_keys=True))
