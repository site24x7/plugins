#!/usr/bin/python

import json

import sys

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
COUCHBASE_SERVER_HOST='127.0.0.1'

COUCHBASE_SERVER_PORT="8091"

COUCHBASE_SERVER_STATS_URI="pools/default"

COUCHBASE_SERVER_USERNAME=None

COUCHBASE_SERVER_PASSWORD=None

REALM=None

DEFAULT_TIMEOUT=30

METRICS_UNITS = {'hdd.ram':'MB',"hdd.quotaTotal": "MB", "hdd.total": "MB","hdd.used": "MB","hdd.usedByData": "MB","ram.quotaTotalPerNode": "MB","ram.quotaUsed": "MB","ram.quotaUsedPerNode": "MB","ram.total":"MB","ram.used": "MB"}

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection

def metricCollector():
	data = {}
	
	#defaults
	data['plugin_version'] = PLUGIN_VERSION

	data['heartbeat_required']=HEARTBEAT

	data['units']=METRICS_UNITS

	URL = "http://"+COUCHBASE_SERVER_HOST+":"+COUCHBASE_SERVER_PORT+"/"+COUCHBASE_SERVER_STATS_URI
	
	try:
		
		if COUCHBASE_SERVER_USERNAME and COUCHBASE_SERVER_PASSWORD:
		   password_mgr = urlconnection.HTTPPasswordMgr()
		   password_mgr.add_password(REALM, URL, COUCHBASE_SERVER_USERNAME, COUCHBASE_SERVER_PASSWORD)
		   auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
		   opener = urlconnection.build_opener(auth_handler)
		   urlconnection.install_opener(opener)
		response = urlconnection.urlopen(URL, timeout=10)
		byte_responseData = response.read()
		str_responseData = byte_responseData.decode('UTF-8')

		couchserver_dict = json.loads(str_responseData)
		data['hdd.total']=couchserver_dict['storageTotals']['hdd']['total']
		data['hdd.quotaTotal']=couchserver_dict['storageTotals']['hdd']['quotaTotal']
		data['hdd.usedByData']=couchserver_dict['storageTotals']['hdd']['usedByData']
		data['hdd.used']=couchserver_dict['storageTotals']['hdd']['used']
		
		data['ram.used']=couchserver_dict['storageTotals']['ram']['used']
		data['ram.quotaUsed']=couchserver_dict['storageTotals']['ram']['quotaUsed']
		data['ram.quotaUsedPerNode']=couchserver_dict['storageTotals']['ram']['quotaUsedPerNode']
		data['ram.quotaTotalPerNode']=couchserver_dict['storageTotals']['ram']['quotaTotalPerNode']
		data['ram.total']=couchserver_dict['storageTotals']['ram']['total']
		for item in data:
			if '.' in item:
				data[item]=convertBytesToMB(data[item])	
		
	except Exception as e:
			data['status']=0
			data['msg']=str(e)
	
	return data

def convertBytesToMB(v):
    try:
        byte_s=float(v)
        kilobytes=byte_s/1024;
        megabytes=kilobytes/1024;
        v=round(megabytes,2)
    except Exception as e:
        pass
    return v 

if __name__ == "__main__":
	print(json.dumps(metricCollector(), indent=4, sort_keys=True))
