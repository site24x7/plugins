#!/usr/bin/python

import json
import argparse
import requests
from requests.auth import HTTPBasicAuth

METRICS = {'consumers', 'messages', 'messages_persistent', 'messages_ready', 'messages_unacknowledged'}

def metricCollector():
    data = {}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='hostname to be monitored', type=str, nargs='?', default="localhost")
    parser.add_argument('--port', help='port to be monitored', type=int, nargs='?', default=15672)
    parser.add_argument('--username', help='username', type=str, nargs='?', default="guest")
    parser.add_argument('--password', help='password', type=str, nargs='?', default="guest")
    parser.add_argument('--vhost', help='virtual host name', type=str, nargs='?', default="/")
    parser.add_argument('--queue_name', help='queue_name to be monitored', type=str, nargs='?', default="Test Queue")
    parser.add_argument('--plugin_version', help='plugin template version', type=int, nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args = parser.parse_args()

    input_data = {
        'hostname': args.hostname,
        'port': args.port,
        'username': args.username,
        'password': args.password,
        'vhost': args.vhost,
        'queue_name': args.queue_name,
    }
    
    input_data['vhost'] = requests.utils.quote(input_data['vhost'], safe='')
    input_data['queue_name'] = requests.utils.quote(input_data['queue_name'])
    
    URL = f"http://{input_data['hostname']}:{input_data['port']}/api/queues/{input_data['vhost']}/{input_data['queue_name']}"
    
    data['plugin_version'] = args.plugin_version
    data['heartbeat_required'] = args.heartbeat

    try:
        response = requests.get(URL, auth=HTTPBasicAuth(input_data['username'], input_data['password']), timeout=10)
        response.raise_for_status()
        rabbit_dict = response.json()
        if rabbit_dict:
            if 'consumers' in rabbit_dict: data['consumers'] = rabbit_dict['consumers']
            if 'messages' in rabbit_dict: data['messages'] = rabbit_dict['messages']
            if 'messages_ready' in rabbit_dict: data['messages.ready'] = rabbit_dict['messages_ready']
            if 'messages_persistent' in rabbit_dict: data['messages.persistent'] = rabbit_dict['messages_persistent']
            if 'messages_unacknowledged' in rabbit_dict: data['messages.unack'] = rabbit_dict['messages_unacknowledged']
            
            if 'rate' in rabbit_dict.get('messages_details', {}): data['messages.rate'] = rabbit_dict['messages_details']['rate']
            if 'rate' in rabbit_dict.get('messages_ready_details', {}): data['messages.ready.rate'] = rabbit_dict['messages_ready_details']['rate']
            if 'rate' in rabbit_dict.get('messages_unacknowledged_details', {}): data['messages.unack.rate'] = rabbit_dict['messages_unacknowledged_details']['rate']

            if 'message_stats' in rabbit_dict:
                message_stats = rabbit_dict['message_stats']
                if 'deliver_details' in message_stats: data['deliver.rate'] = message_stats['deliver_details']['rate']
                if 'ack_details' in message_stats: data['ack.rate'] = message_stats['ack_details']['rate']
                if 'publish_details' in message_stats: data['publish.rate'] = message_stats['publish_details']['rate']

    except requests.HTTPError as e:
        data['status'] = 0
        data['msg'] = str(e)
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)

    return data
        
if __name__ == "__main__":    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
