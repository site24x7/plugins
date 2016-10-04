#!/usr/bin/python

import json

### This plugin in python monitors the performance metrics of couchdb servers
### CouchDB, is an open source database that completely embraces the web. 
### It is a NoSQL database that uses JSON to store data, uses JavaScript as its query language using MapReduce, and uses HTTP for an API.
### This plugin monitors the performance of a CouchDB server. 

### Author: Sriram, Zoho Corp
### Language : Python
### Tested in Ubuntu

#if any changes to this plugin increase the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
COUCHDB_HOST='127.0.0.1'

COUCHDB_PORT="5984"

COUCHDB_STATS_URI="/_stats/"

COUCHDB_USERNAME=None

COUCHDB_PASSWORD=None

METRICS_UNITS={'request_time':'ms','auth_cache_hits':'number','auth_cache_misses':'number','database_reads':'number','database_writes':'number','open_databases':'number','open_os_files':'number','no_of_http_post_requests':'number',
			  'no_of_http_copy_requests':'number','no_of_http_get_requests':'number','no_of_http_head_requests':'number','no_of_http_move_requests':'number','no_of_http_put_requests':'number','no_of_http_200_responses':'number','no_of_http_201_responses':'number',
			  'no_of_http_202_responses':'number','no_of_http_301_responses':'number','no_of_http_304_responses':'number','no_of_http_400_responses':'number','no_of_http_401_responses':'number','no_of_http_403_responses':'number',
			  'no_of_http_404_responses':'number','no_of_http_405_responses':'number','no_of_http_409_responses':'number','no_of_http_412_responses':'number','no_of_http_500_responses':'number',
			  'bulk_requests':'number','view_reads':'number','clients_requesting_changes':'number','temporary_view_reads':'number'}

METRICS_KEY_VS_NAME ={'COPY':'no_of_http_copy_requests','GET':'no_of_http_get_requests','HEAD':'no_of_http_head_requests','MOVE':'no_of_http_move_requests','PUT':'no_of_http_put_requests','POST':'no_of_http_post_requests',
					 '200':'no_of_http_200_responses','201':'no_of_http_201_responses','202':'no_of_http_202_responses','301':'no_of_http_301_responses','304':'no_of_http_304_responses','400':'no_of_http_400_responses',
					 '401':'no_of_http_401_responses','403':'no_of_http_403_responses','404':'no_of_http_404_responses','405':'no_of_http_405_responses','409':'no_of_http_409_responses','412':'no_of_http_412_responses','500':'no_of_http_500_responses'}

def metricCollector():
	data = {}
	#defaults

	data['plugin_version'] = PLUGIN_VERSION

	data['heartbeat_required']=HEARTBEAT

	data['units']=METRICS_UNITS

	import requests
	
	from requests.exceptions import ConnectionError

	from urlparse import urljoin
	
	server = "http://"+COUCHDB_HOST+":"+COUCHDB_PORT+"/"
	
	url = urljoin(server, COUCHDB_STATS_URI)
	
	credentials = None

	if COUCHDB_USERNAME and COUCHDB_PASSWORD:
		credentials = (COUCHDB_USERNAME,COUCHDB_PASSWORD)

	req_headers={}

	req_headers['Accept'] = 'text/json'

	try:
		response = requests.get(url, auth=credentials, headers=req_headers,timeout=int(30))
		
		if response.status_code == 404:
			data['status']=0
			data['msg']='received status code 404'
			return data

		if response.status_code == 400:
			data['status']=0
			data['msg']='received status code 400'
			return data

		couch_dict = response.json()

		for attribute, attribute_value in couch_dict.items():
			for metric, val in attribute_value.items():
				if 'current' in val and val['current'] is not None:
					if metric in METRICS_KEY_VS_NAME:
						metric = METRICS_KEY_VS_NAME[metric]
					data[metric]=val['current']
	except ConnectionError as e:
			data['status']=0
			data['msg']='Connection Error'  
	
	return data

if __name__ == "__main__":
	
	print(json.dumps(metricCollector(), indent=4, sort_keys=True))