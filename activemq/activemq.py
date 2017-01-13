#!/usr/bin/python
"""

Site24x7 ActiveMQ Plugin

"""

import json

import os

import sys

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
ACTIVEMQ_HOST = "localhost"

ACTIVEMQ_PORT = "8161"

ACTIVEMQ_USERNAME = "admin"

ACTIVEMQ_PASSWORD = "admin"

REALM = None

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'total_message_count': 'units', 'total_connections_count': 'units',
                 'total_consumer_count': 'units', 'total_producer_count': 'units'}

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector

def metricCollector():
    
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    data['units'] = METRICS_UNITS

    URL = 'http://%s:%s/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost' % (ACTIVEMQ_HOST, ACTIVEMQ_PORT)
    try:
        if ACTIVEMQ_USERNAME and ACTIVEMQ_PASSWORD:
            password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(REALM, URL, ACTIVEMQ_USERNAME, ACTIVEMQ_PASSWORD)
            auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
            opener = connector.build_opener(auth_handler)
            connector.install_opener(opener)

        response = connector.urlopen(URL, timeout=10)
        byte_responseData = response.read()
        str_responseData = byte_responseData.decode('UTF-8')
        json_data = json.loads(str_responseData)

        total_message_count = json_data['value']['TotalMessageCount']
        total_connections_count = json_data['value']['TotalConnectionsCount']
        total_consumer_count = json_data['value']['TotalConsumerCount']
        total_producer_count = json_data['value']['TotalProducerCount']

        data['total_message_count'] = total_message_count
        data['total_connections_count'] = total_connections_count
        data['total_consumer_count'] = total_consumer_count
        data['total_producer_count'] = total_producer_count
        
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)

    return data
    
if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
