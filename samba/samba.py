#!/usr/bin/python

import json
import subprocess

### Author: Bhuvaneshwari S, Zoho Corp
### Language : Python
### Tested in Ubuntu

#if any changes are made to this plugin, kindly update the plugin version here
PLUGIN_VERSION ="1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Mention the units of your metrics. If any new metrics are added, make an entry here for its unit if needed.
METRIC_UNITS={'users':'count', 'folders_accessed':'count','samba_version':'text'}

def metricCollector():
	data={}
	data['plugin_version'] = PLUGIN_VERSION
	data['heartbeat_required']=HEARTBEAT
	
##smbstatus gets report of current samba server connections
	p = subprocess.Popen('smbstatus', stdout=subprocess.PIPE)
	output, err = p.communicate()
	oparr = output.decode().split('\n')
	version_op = oparr[1].replace("Samba version ","")
	samba_version =  version_op.split("-")[0]
	index=[0,0]
	marker = 0
	for i, item in enumerate(oparr[:]):
		if str(item).startswith('----------------'):
			index[marker]=i
			marker=marker+1
			if marker==2:
				break
			
##Gets the users count from list of users connected to samba server
	users_connected = index[1]-index[0]-3
	
	service_dict=dict()
	if users_connected>0:
		for i in range(index[1]+1,index[1]+users_connected+1):
			service = oparr[i].split(" ")[0]
			if service in service_dict:
				service_dict[service]+=1
			else:
				service_dict[service]=1
##Gets the unique number of shared folders being accessed by users
	unique_share_services = len(service_dict.keys())
	
	data['users']=users_connected
	data['folders_accessed']=unique_share_services
	data['samba_version']=samba_version
	data['units']=METRIC_UNITS
	return data

if __name__=="__main__":
	result = metricCollector()
	print(json.dumps(result, indent=4, sort_keys=True))
