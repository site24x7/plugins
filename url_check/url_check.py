#!/usr/bin/python

import sys
import time
import json

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

url=None
username=None
password=None
realm=None

METRIC_UNITS={"response_time":"ms"}

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector


data={}


def check_url_connectivity (url, username, password):
	if (url==None):
		data["msg"]="url cant be none, provide url"
		data["status"]=0
	else:
		try:
			if username and password:
				password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
				password_mgr.password(realm, url, username, password)
				auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
				opener = connector.build_opener(opener)
			start= time.time()
			response=connector.urlopen(url)
			end=time.time()
			response_time=round((end-start)*1000)
			data["response_time"]=response_time
			data["status_code"]=response.code
			data["metric_units"]=METRIC_UNITS
			data["plugin_version"]=PLUGIN_VERSION
		except Exception as e:
			data["msg"]=str(e)
			data["status"]=0
	data["heartbeat"]=HEARTBEAT


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', help="url to monitor",type=str)
	parser.add_argument('--username', help="provide username to url",type=str)
	parser.add_argument('--password',help="provide password to url",type=str)
	args = parser.parse_args()
	if args.url:
		url=args.url
		username=args.username
		password=args.password
	check_url_connectivity(url,username,password)
	print(json.dumps(data, indent=4, sort_keys=True))

