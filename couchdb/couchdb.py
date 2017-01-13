#!/usr/bin/python

import json

import sys

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
COUCHDB_HOST='127.0.0.1'

COUCHDB_PORT="5984"

COUCHDB_STATS_URI="/_stats/"

COUCHDB_USERNAME=None

COUCHDB_PASSWORD=None

REALM=None

METRICS_UNITS={'request_time':'ms','auth_cache_hits':'number','auth_cache_misses':'number','database_reads':'number','database_writes':'number','open_databases':'number','open_os_files':'number','no_of_http_post_requests':'number',
			  'no_of_http_copy_requests':'number','no_of_http_get_requests':'number','no_of_http_head_requests':'number','no_of_http_move_requests':'number','no_of_http_put_requests':'number','no_of_http_200_responses':'number','no_of_http_201_responses':'number',
			  'no_of_http_202_responses':'number','no_of_http_301_responses':'number','no_of_http_304_responses':'number','no_of_http_400_responses':'number','no_of_http_401_responses':'number','no_of_http_403_responses':'number',
			  'no_of_http_404_responses':'number','no_of_http_405_responses':'number','no_of_http_409_responses':'number','no_of_http_412_responses':'number','no_of_http_500_responses':'number',
			  'bulk_requests':'number','view_reads':'number','clients_requesting_changes':'number','temporary_view_reads':'number'}

METRICS_KEY_VS_NAME ={'COPY':'no_of_http_copy_requests','GET':'no_of_http_get_requests','HEAD':'no_of_http_head_requests','MOVE':'no_of_http_move_requests','PUT':'no_of_http_put_requests','POST':'no_of_http_post_requests',
					 '200':'no_of_http_200_responses','201':'no_of_http_201_responses','202':'no_of_http_202_responses','301':'no_of_http_301_responses','304':'no_of_http_304_responses','400':'no_of_http_400_responses',
					 '401':'no_of_http_401_responses','403':'no_of_http_403_responses','404':'no_of_http_404_responses','405':'no_of_http_405_responses','409':'no_of_http_409_responses','412':'no_of_http_412_responses','500':'no_of_http_500_responses'}

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector

def metricCollector():
	data = {}
	
	#defaults
	data['plugin_version'] = PLUGIN_VERSION

	data['heartbeat_required']=HEARTBEAT

	data['units']=METRICS_UNITS

	URL = "http://"+COUCHDB_HOST+":"+COUCHDB_PORT+COUCHDB_STATS_URI
	
	try:
		if COUCHDB_USERNAME and COUCHDB_PASSWORD:
			password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
			password_mgr.add_password(REALM, URL, COUCHDB_USERNAME, COUCHDB_PASSWORD)
			auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
			opener = connector.build_opener(auth_handler)
			connector.install_opener(opener)
		response = connector.urlopen(URL, timeout=10)
		byte_responseData = response.read()
		str_responseData = byte_responseData.decode('UTF-8')
		couch_dict = json.loads(str_responseData)
		for attribute, attribute_value in couch_dict.items():
			for metric, val in attribute_value.items():
				if 'current' in val and val['current'] is not None:
					if metric in METRICS_KEY_VS_NAME:
						metric = METRICS_KEY_VS_NAME[metric]
					data[metric]=val['current']
	except Exception as e:
			data['status']=0
			data['msg']=str(e)  
	
	return data

if __name__ == "__main__":
	
	print(json.dumps(metricCollector(), indent=4, sort_keys=True))
