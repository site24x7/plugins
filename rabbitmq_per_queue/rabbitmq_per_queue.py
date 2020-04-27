#!/usr/bin/python

import json

import sys

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
RABBITMQ_HOST='localhost'

RABBITMQ_PORT="15672"

RABBITMQ_USERNAME='guest'

RABBITMQ_PASSWORD='guest'

VHOST_NAME="/" #Default vhost: /. All / will be encoded

QUEUE_NAME="Test Queue"
    
REALM=None

RABBITMQ_SERVER = "http://"+RABBITMQ_HOST+":"+RABBITMQ_PORT

METRICS = {'consumers', 'messages', 'messages_persistent', 'messages_ready', 'messages_unacknowledged'}

METRICS_UNITS={'mem_used':'MB','disk_free_limit':'MB'}

BYTES_TO_MB_LIST=['mem_used','disk_free_limit']

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as connector
    VHOST_NAME=urllib.parse.quote('/', safe='')
    RABBITMQ_API_URI="/api/queues/"+VHOST_NAME+"/"+connector.quote(QUEUE_NAME)
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as connector
    VHOST_NAME=VHOST_NAME.replace("/", "%2F")
    RABBITMQ_API_URI="/api/queues/"+VHOST_NAME+"/"+connector.quote(QUEUE_NAME)

def metricCollector():
    data = {}
    #defaults
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required']=HEARTBEAT
    data['units']=METRICS_UNITS
    getQueueDetails(data)
    return data

def getQueueDetails(data):
    try:
        URL = RABBITMQ_SERVER+RABBITMQ_API_URI
        if RABBITMQ_USERNAME and RABBITMQ_PASSWORD:
            password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(REALM, URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
            auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
            opener = connector.build_opener(auth_handler)
            connector.install_opener(opener)

        response = connector.urlopen(URL, timeout=10)
    
        byte_responseData = response.read()
        str_responseData = byte_responseData.decode('UTF-8')

        rabbit_dict = json.loads(str_responseData)
        
        if rabbit_dict:
            if 'consumers' in rabbit_dict: data['consumers']=rabbit_dict['consumers']
            if 'messages' in rabbit_dict: data['messages']=rabbit_dict['messages']
            if 'messages_ready' in rabbit_dict: data['messages.ready']=rabbit_dict['messages_ready']
            if 'messages_persistent' in rabbit_dict: data['messages.persistent']=rabbit_dict['messages_persistent']
            if 'messages_unacknowledged' in rabbit_dict: data['messages.unack']=rabbit_dict['messages_unacknowledged']
            
            if 'rate' in rabbit_dict['messages_details']: data['messages.rate']=rabbit_dict['messages_details']['rate']
            if 'rate' in rabbit_dict['messages_ready_details']: data['messages.ready.rate']=rabbit_dict['messages_ready_details']['rate']
            if 'rate' in rabbit_dict['messages_unacknowledged_details']: data['messages.unack.rate']=rabbit_dict['messages_unacknowledged_details']['rate']

            if 'message_stats' in rabbit_dict:
                message_stats = rabbit_dict['message_stats']
                if 'deliver_details' in message_stats : data['deliver.rate']= message_stats['deliver_details']['rate']
                if 'ack_details' in message_stats: data['ack.rate']= message_stats['ack_details']['rate']
                if 'publish_details' in message_stats: data['publish.rate']= message_stats['publish_details']['rate']

    except Exception as e:
        data['status']=0
        data['msg']=str(e)
    
if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
