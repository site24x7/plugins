#!/usr/bin/python

import json

import requests

import traceback
    
from requests.exceptions import ConnectionError

from requests.exceptions import Timeout

from urlparse import urljoin

#if any changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION=1

#Setting this to true will alert you when there is a network problem while posting plugin data to server
HEARTBEAT="true"

#Config Section
RABBITMQ_HOST='localhost'

RABBITMQ_PORT="15672"

RABBITMQ_API_URI="/api/overview"

RABBITMQ_NODES_URI="/api/nodes"

RABBITMQ_USERNAME='guest'

RABBITMQ_PASSWORD='guest'

RABBITMQ_SERVER = "http://"+RABBITMQ_HOST+":"+RABBITMQ_PORT+"/"

METRICS_UNITS={'mem_used':'MB','disk_free_limit':'MB'}

BYTES_TO_MB_LIST=['mem_used','disk_free_limit']

def metricCollector():
    data = {}
    #defaults

    data['plugin_version'] = PLUGIN_VERSION

    data['heartbeat_required']=HEARTBEAT

    data['units']=METRICS_UNITS

    credentials = None
    
    if RABBITMQ_USERNAME and RABBITMQ_PASSWORD:
        credentials = (RABBITMQ_USERNAME,RABBITMQ_PASSWORD)

    req_headers={}

    req_headers['Accept'] = 'application/json'

    api_working = isMgmtApiWorking(data,req_headers,credentials)

    if not api_working:
        return data

    getOverview(data,req_headers,credentials)

    getNodes(data,req_headers,credentials)

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

def isMgmtApiWorking(data,req_headers,credentials):
    try:
        url = urljoin(RABBITMQ_SERVER, RABBITMQ_API_URI)
        response = requests.get(url, auth=credentials, headers=req_headers,timeout=int(3))
        
        if response.status_code == 404:
            data['status']=0
            data['msg']='received status code 404'
            return False

        if response.status_code == 400:
            data['status']=0
            data['msg']='received status code 400'
            return False

        resp_dict = response.json()

        if resp_dict:
            if 'error' in resp_dict and resp_dict['error'] is not None:
                data['status']=0
                data['msg']='Login Failed - not authorized'
                return False

    except ConnectionError as e:
            data['status']=0
            data['msg']='Connection Error'
            return False

    except requests.exceptions.Timeout as e:
           data['status']=0
           data['msg']='Connection Time Out Error'
           return False

    return True

def getOverview(data,req_headers,credentials):
    try:
        url = urljoin(RABBITMQ_SERVER, RABBITMQ_API_URI)
        response = requests.get(url, auth=credentials, headers=req_headers,timeout=int(30))
        
        if response.status_code == 404:
            data['status']=0
            data['msg']='received status code 404'
            return data

        if response.status_code == 400:
            data['status']=0
            data['msg']='received status code 400'
            return data

        rabbit_dict = response.json()

        if rabbit_dict:
            if 'management_version' in rabbit_dict:
                data['mgmt_version']=rabbit_dict['management_version']

            if 'rabbitmq_version' in rabbit_dict:
                data['rabbitmq_version']=rabbit_dict['rabbitmq_version']

            if 'consumers' in rabbit_dict['object_totals']:
                data['consumers']=rabbit_dict['object_totals']['consumers']

            if 'queues' in rabbit_dict['object_totals']:
                data['queues']=rabbit_dict['object_totals']['queues']

            if 'exchanges' in rabbit_dict['object_totals']:
                data['exchanges']=rabbit_dict['object_totals']['exchanges']

            if 'channels' in rabbit_dict['object_totals']:
                data['channels']=rabbit_dict['object_totals']['channels']           

            data['messages_ready']=rabbit_dict['queue_totals']['messages_ready']
            data['messages_unack']=rabbit_dict['queue_totals']['messages_unacknowledged']
            data['messages']=rabbit_dict['queue_totals']['messages']

            data['messages_rate']=rabbit_dict['queue_totals']['messages_details']['rate']
            data['messages_ready_rate']=rabbit_dict['queue_totals']['messages_ready_details']['rate']
            data['messages_unack_rate']=rabbit_dict['queue_totals']['messages_unacknowledged_details']['rate']

            if 'deliver_details' in rabbit_dict['message_stats']:
                data['deliverrate']=rabbit_dict['message_stats']['deliver_details']['rate']
            if 'ack_details' in rabbit_dict['message_stats']:
                data['ackrate']=rabbit_dict['message_stats']['ack_details']['rate']
            if 'publish_details' in rabbit_dict['message_stats']:
                data['publishrate']=rabbit_dict['message_stats']['publish_details']['rate']

    except ConnectionError as e:
            data['status']=0
            data['msg']='Connection Error'

    except Exception as e:
           traceback.print_exc() 
    
    return data


def getNodes(data,req_headers,credentials):
    try:
        url = urljoin(RABBITMQ_SERVER, RABBITMQ_NODES_URI)
        response = requests.get(url, auth=credentials, headers=req_headers,timeout=int(30))
        
        rabbit_nodes_dict = response.json()

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
    except ConnectionError as e:
        return data

    return data


if __name__ == "__main__":
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))