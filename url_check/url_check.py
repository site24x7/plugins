#!/usr/bin/python

import sys
import time
import json
PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector
    

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION="1"

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

URL=None

USERNAME=None

PASSWORD=None

realm=None

CONTENT_CHECK=None

METRIC_UNITS={"response_time":"ms"}

output_json={}


def check_response_content (response, CONTENT_CHECK):
	result = {}
	
	try:
		content=response.read()
		content=content.decode('utf-8')
		if CONTENT_CHECK not in content:
			result["msg"]=("{} : Not found in given endpoint".format(CONTENT_CHECK))
			result["status"]=0
	except Exception as e:
		result["msg"]=str(e)
		result["status"]=0
		
	return result


def check_url_connectivity (URL, USERNAME, PASSWORD, CONTENT_CHECK):
	result = {}
	
	if (URL==None):
		result["msg"]="url cant be none, provide url"
		result["status"]=0
	else:
		try:
			if USERNAME and PASSWORD:
				password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
				password_mgr.password(realm, URL, USERNAME, PASSWORD)
				auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
				opener = connector.build_opener(opener)
			start= time.time()
			response=connector.urlopen(URL)
			end=time.time()
			response_time=round((end-start)*1000)
			if CONTENT_CHECK and CONTENT_CHECK != 'None':
				result = check_response_content(response, CONTENT_CHECK)
				result["content_check_string"] = str(CONTENT_CHECK)
			if "status" not in result.keys():
				result["response_time"] = response_time
				result["status_code"] = response.code
				result["metric_units"] = METRIC_UNITS
		except Exception as e:
			result["msg"]=str(e)
			result["status"]=0
			
	result["plugin_version"] = PLUGIN_VERSION
	result["heartbeat_required"]=HEARTBEAT
	
	return result


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', help="url to monitor",type=str)
	parser.add_argument('--username', help="provide username to url",type=str)
	parser.add_argument('--password',help="provide password to url",type=str)
	parser.add_argument('--content_check',help="provide content to check in url response",type=str)
	args = parser.parse_args()
	
	if args.url:
		URL = args.url
		USERNAME = args.username
		PASSWORD = args.password
	if args.content_check:
		CONTENT_CHECK = args.content_check
	
	if CONTENT_CHECK:
		output_json = check_url_connectivity(URL,USERNAME,PASSWORD,CONTENT_CHECK)
	else:
		output_json = check_url_connectivity(URL,USERNAME,PASSWORD,None)
	print(json.dumps(output_json, indent=4, sort_keys=True))
