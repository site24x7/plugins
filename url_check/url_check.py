#!/usr/bin/python

import sys,json,time

#sample ['http://localhost:80','http://testserver:9090/index.html','https://plus.site24x7.com']
URLS_TO_BE_MONITORED=[]

#kindly choose the display name for your url. it will be easier to identify in site24x7 client
#sample :: {'http://localhost:1000':'apache_localhost','https://plus.site24x7.com':'plus_server'}
URLS_VS_DISPLAY_NAME={}

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
    from http.client import InvalidURL
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError
    from httplib import InvalidURL

def metric_collector(url_data):
    for each_url in URLS_TO_BE_MONITORED:
        try:
            start_time = time.time() * 1000
            response = urlconnection.urlopen(each_url, timeout=5)
            latency = round(((time.time() * 1000) - start_time))
            url_data[URLS_VS_DISPLAY_NAME[each_url]+'_response_time']=latency
            url_data[URLS_VS_DISPLAY_NAME[each_url]+'_status']=1
            http_status_code = response.getcode()
            if  http_status_code >= 400:
                url_data[URLS_VS_DISPLAY_NAME[each_url]+'_'+'status'] = 0
            url_data[URLS_VS_DISPLAY_NAME[each_url]+'_status_code'] = http_status_code
        except Exception as e:
            url_data[URLS_VS_DISPLAY_NAME[each_url]+'_status']=0
            url_data[URLS_VS_DISPLAY_NAME[each_url]+'_status_code']=-1

url_data = {}
url_data['plugin_version'] = PLUGIN_VERSION
url_data['heartbeat_required'] = HEARTBEAT
metric_collector(url_data)
print((json.dumps(url_data)))
