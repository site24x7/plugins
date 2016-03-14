#!/usr/bin/python

import json

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
MEMCACHE_HOST='127.0.0.1'

MEMCACHE_PORT=11211

METRICS_UNITS={'uptime':'seconds','bytes_read':'bytes','bytes_written':'bytes','limit_maxbytes':'MB'}

BYTES_TO_MB_LIST=['bytes','limit_maxbytes']

METRICS_IGNORED=['time']

def metricCollector():
	data = {}
	#defaults

	data['plugin_version'] = PLUGIN_VERSION

	data['heartbeat_required']=HEARTBEAT

	data['units']=METRICS_UNITS
	
	try:
		import memcache
	except ImportError:
			data['status']=0
			data['msg']='memcache module not installed'
			return data

	try:
		mc = memcache.Client(["%s:%s"%(MEMCACHE_HOST, MEMCACHE_PORT)])
	except Exception as e:
			data['status']=0
			data['msg']=e
			return data

	stats = mc.get_stats()

	if stats:
		#get the dictionary from tuple
		dct = dict(stats)

		for k,v in dct.items():
			value_dict = v

		if value_dict:
			for k,v in value_dict.items():
				if k in METRICS_IGNORED:
					continue
				if k in BYTES_TO_MB_LIST:
					v=convertBytesToMB(v)
				data[k]=v

	if mc is not None:
        	mc.disconnect_all()
        	mc == None

	return data

def convertBytesToMB(v):
	try:
		byte_s=float(v)
		kilobytes=byte_s/1024;
		megabytes=kilobytes/1024;
		v=int(megabytes)
	except Exception as e:
		pass
	return v
	
if __name__ == "__main__":
	
	print(json.dumps(metricCollector(), indent=4, sort_keys=True))