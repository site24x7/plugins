#!/usr/bin/python3

import json
import sys  

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section


RABBITMQ_API_URI="/api/overview"

RABBITMQ_NODES_URI="/api/nodes"



METRICS_UNITS={'mem_used':'MB','disk_free_limit':'MB'}

BYTES_TO_MB_LIST=['mem_used','disk_free_limit']

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

    getOverview(data)

    getNodes(data)

    return data



def convertBytesToMB(v):
    try:
        byte_s=int(v)
        kilobytes=byte_s/1000;
        megabytes=kilobytes/1000;
        v=megabytes
    except Exception as e:
        pass
    return v  

def getOverview(data):
    try:
        URL = RABBITMQ_SERVER+RABBITMQ_API_URI
        if RABBITMQ_USERNAME and RABBITMQ_PASSWORD:
            password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
            
            password_mgr.add_password(REALM, URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
            auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
            opener = connector.build_opener(auth_handler)
            connector.install_opener(opener)

        response = connector.urlopen(URL,timeout=40)
        
    
        byte_responseData = response.read()
        str_responseData = byte_responseData.decode('UTF-8')
        
        rabbit_dict = json.loads(str_responseData)
        if rabbit_dict:
            if 'consumers' in rabbit_dict['object_totals']:
                data['consumers']=rabbit_dict['object_totals']['consumers']

            if 'queues' in rabbit_dict['object_totals']:
                data['queues']=rabbit_dict['object_totals']['queues']

            if 'exchanges' in rabbit_dict['object_totals']:
                data['exchanges']=rabbit_dict['object_totals']['exchanges']

            if 'channels' in rabbit_dict['object_totals']:
                data['channels']=rabbit_dict['object_totals']['channels']           

            if 'messages_ready' in rabbit_dict['queue_totals']:
                data['messages_ready']=rabbit_dict['queue_totals']['messages_ready']

            if 'messages_unacknowledged' in rabbit_dict['queue_totals']:
                data['messages_unack']=rabbit_dict['queue_totals']['messages_unacknowledged']

            if 'messages' in rabbit_dict['queue_totals']:
                data['messages']=rabbit_dict['queue_totals']['messages']

            if  'messages_details' in rabbit_dict['queue_totals']:
                data['messages_rate']=rabbit_dict['queue_totals']['messages_details']['rate']

            if  'messages_ready_details' in rabbit_dict['queue_totals']:
                data['messages_ready_rate']=rabbit_dict['queue_totals']['messages_ready_details']['rate']

            if  'messages_unacknowledged_details' in rabbit_dict['queue_totals']:
                data['messages_unack_rate']=rabbit_dict['queue_totals']['messages_unacknowledged_details']['rate']

            if 'deliver_details' in rabbit_dict['message_stats']:
                data['deliverrate']=rabbit_dict['message_stats']['deliver_details']['rate']
            if 'ack_details' in rabbit_dict['message_stats']:
                data['ackrate']=rabbit_dict['message_stats']['ack_details']['rate']
            if 'publish_details' in rabbit_dict['message_stats']:
                data['publishrate']=rabbit_dict['message_stats']['publish_details']['rate']

    except Exception as e:
           data['status']=0
           data['msg']="Plugin Error : "+str(e)
    
def getNodes(data):
    try:
       
        NODES_URL=RABBITMQ_SERVER+RABBITMQ_NODES_URI 
        if RABBITMQ_USERNAME and RABBITMQ_PASSWORD:
            password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(REALM, NODES_URL, RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
            auth_handler = connector.HTTPBasicAuthHandler(password_mgr)
            opener = connector.build_opener(auth_handler)
            connector.install_opener(opener)

        response = connector.urlopen(NODES_URL, timeout=40)

        byte_responseData = response.read()
        str_responseData = byte_responseData.decode('UTF-8')

        rabbit_nodes_dict = json.loads(str_responseData)
        nodes_dict=rabbit_nodes_dict[0]
        if nodes_dict:
            if 'mem_used' in nodes_dict:
                value = convertBytesToMB(nodes_dict['mem_used'])
                data['mem_used']=value
            if 'fd_used' in nodes_dict:
                data['fd_used']=nodes_dict['fd_used']
            if 'run_queue' in nodes_dict:
                data['run_queue']=nodes_dict['run_queue']
            if 'sockets_used' in nodes_dict:
                data['sockets_used']=nodes_dict['sockets_used']
            if 'proc_used' in nodes_dict:
                data['proc_used']=nodes_dict['proc_used']
            if 'processors' in nodes_dict:
                data['processors']=nodes_dict['processors']
            if 'fd_total' in nodes_dict:
                data['fd_total']=nodes_dict['fd_total']
            if 'sockets_total' in nodes_dict:
                data['sockets_total']=nodes_dict['sockets_total']
            if 'disk_free_limit' in nodes_dict:
                value=convertBytesToMB(nodes_dict['disk_free_limit'])
                data['disk_free_limit']=value

            if 'partitions' in nodes_dict:
                partitions=nodes_dict['partitions']
                data['partitions']=len(partitions)
    except  Exception as e:
        data['status']=0
        data['msg']=str(e)

if __name__ == "__main__":
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?',default='localhost')
    parser.add_argument('--port',help="Port",nargs='?',default="15672")
    parser.add_argument('--username',help="Username",default="guest")
    parser.add_argument('--password',help="Password",default="guest")
    parser.add_argument('--realm',help="Realm",default=None)

    args=parser.parse_args()
    
    RABBITMQ_HOST=args.host
    RABBITMQ_PORT=args.port
    RABBITMQ_USERNAME=args.username
    RABBITMQ_PASSWORD=args.password
    REALM=args.realm

    RABBITMQ_SERVER = "http://"+RABBITMQ_HOST+":"+RABBITMQ_PORT

    print(json.dumps(metricCollector(), indent=4, sort_keys=True))