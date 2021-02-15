#!/usr/bin/python

import json
import sys

METRICS = {'consumers', 'messages', 'messages_persistent', 'messages_ready', 'messages_unacknowledged'}
METRICS_UNITS={'mem_used':'MB','disk_free_limit':'MB'}
BYTES_TO_MB_LIST=['mem_used','disk_free_limit']
PYTHON_MAJOR_VERSION = sys.version_info[0]


def metricCollector():
    data = {}
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='hostname to be monitored', type=str, nargs='?', default="localhost")
    parser.add_argument('--port', help='port to be monitored', type=int, nargs='?', default=15672)
    parser.add_argument('--username', help='username', type=str, nargs='?', default="guest")
    parser.add_argument('--password', help='password', type=str, nargs='?', default="guest")
    parser.add_argument('--vhost', help='virtual host name', type=str, nargs='?', default="/")
    parser.add_argument('--queue_name', help='queue_name to be monitored', type=str, nargs='?', default="Test Queue")
    parser.add_argument('--realm', help='realm', nargs='?', default=None)
    
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args = parser.parse_args()
    
    input_data = {}    
    
    input_data['hostname'] = args.hostname
    input_data['port'] = args.port
    input_data['username'] = args.username
    input_data['password'] = args.password
    input_data['vhost'] = args.vhost
    input_data['queue_name'] = args.queue_name
    input_data['realm'] = args.realm
    
    #defaults
    data['plugin_version'] = args.plugin_version
    data['heartbeat_required']=args.heartbeat
    data['units']=METRICS_UNITS
    
    input_data['server'] = "http://"+input_data['hostname']+":"+str(input_data['port'])
    
    if PYTHON_MAJOR_VERSION == 3:
        import urllib
        import urllib.request as connector
        input_data['vhost']=urllib.parse.quote('/', safe='')
        input_data['uri']="/api/queues/"+input_data['vhost']+"/"+connector.quote(input_data['queue_name'])
    elif PYTHON_MAJOR_VERSION == 2:
        import urllib2 as connector
        input_data['vhost']=input_data['vhost'].replace("/", "%2F")
        input_data['uri']="/api/queues/"+input_data['vhost']+"/"+connector.quote(input_data['queue_name'])
    

    try:
        URL = input_data['server']+input_data['uri']
        if input_data['username'] and input_data['password']:
            password_mgr = connector.HTTPPasswordMgrWithDefaultRealm()            
            password_mgr.add_password(input_data['realm'], URL, input_data['username'], input_data['password'])
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

    return data
        
if __name__ == "__main__":    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
