#!/usr/bin/python

import sys
import json

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
NGINX_STATUS_URL = "http://localhost/status"

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 3:
            import urllib
            import urllib.request as urlconnection
            from urllib.error import URLError, HTTPError
            from http.client import InvalidURL
elif PYTHON_MAJOR_VERSION == 2:
            import urllib2 as urlconnection
            from urllib2 import HTTPError, URLError
            from httplib import InvalidURL

class NginxPlus (object):
    def __init__(self,config):
        self.configurations=config
        self.nginx_status_url=self.configurations.get('nginx_url', 'http://localhost/status')

    def metricCollector(self):
            data = {}
            #defaults
            data['plugin_version'] = PLUGIN_VERSION
            data['heartbeat_required']=HEARTBEAT
            status = self.getStatus(data)
            if status:
                # Connections
                if 'connections' in status:
                    data['connections_accepted'] = status['connections'].get('accepted', None)
                    data['connections_dropped'] = status['connections'].get('dropped', None)
                    data['connections_active'] = status['connections'].get('active', None)
                    data['connections_idle'] = status['connections'].get('idle', None)

                # Requests
                data['requests_total'] = status['requests']['total']
                data['requests_current'] = status['requests']['current']

                #SSL
                if 'ssl' in status:
                    data['handshakes'] = status['ssl']['handshakes']
                    data['handshakes_failed'] = status['ssl']['handshakes_failed']
                    data['session_reuses'] = status['ssl']['session_reuses']
                
                # Server zones
                if 'server_zones' in status:
                    for zone, items in status['server_zones'].iteritems():
                        # Requests
                        name = 'zone_%s_requests' % zone
                        data[name] = items.get('requests', None)

                        name = 'zone_%s_received' % zone
                        data[name] = items.get('received', None)

                        name = 'zone_%s_discarded' % zone
                        data[name] = items.get('discarded', None)

                        name = 'zone_%s_sent' % zone
                        data[name] = items.get('sent', None)

                        name = 'zone_%s_processing' % zone
                        data[name] = items.get('processing', None)

                        if 'responses' in items:
                            # Responses
                            name = 'zone_%s_responses' % zone
                            data[name] = items['responses'].get('total', None)

                            # Responses: 1xx
                            name = 'zone_%s_responses_1xx' % zone
                            data[name] = items['responses'].get('1xx', None)

                            # Responses: 2xx
                            name = 'zone_%s_responses_2xx' % zone
                            data[name] = items['responses'].get('2xx', None)

                            # Responses: 3xx
                            name = 'zone_%s_responses_3xx' % zone
                            data[name] = items['responses'].get('3xx', None)

                            # Responses: 4xx
                            name = 'zone_%s_responses_4xx' % zone
                            data[name] = items['responses'].get('4xx', None)

                            # Responses: 5xx
                            name = 'zone_%s_responses_5xx' % zone
                            data[name] = items['responses'].get('5xx', None)

                # Upstreams
                if 'upstreams' in status:
                    for group, servers in status['upstreams'].iteritems():

                        for server in servers:

                            if 'server' in server:
                                # State
                                name = 'upstream_%s_%s_state' % (group, server['server'])
                                data[name] = server.get('state', 'unknown')

                                # Requests
                                name = 'upstream_%s_%s_requests' % (group, server['server'])
                                data[name] = server.get('requests', None)

                                # Responses
                                if 'responses' in server:
                                    name = 'upstream_%s_%s_responses_total' % (group, server['server'])
                                    data[name] = server['responses'].get('total', None)

                                    # Requests: 1xx
                                    name = 'upstream_%s_%s_responses_1xx' % (group, server['server'])
                                    data[name] = server['responses'].get('1xx', None)

                                    # Responses: 2xx
                                    name = 'upstream_%s_%s_responses_2xx' % (group, server['server'])
                                    data[name] = server['responses'].get('2xx', None)

                                    # Responses: 3xx
                                    name = 'upstream_%s_%s_responses_3xx' % (group, server['server'])
                                    data[name] = server['responses'].get('3xx', None)

                                    # Responses: 4xx
                                    name = 'upstream_%s_%s_responses_4xx' % (group, server['server'])
                                    data[name] = server['responses'].get('4xx', None)

                                    # Responses: 5xx
                                    name = 'upstream_%s_%s_responses_5xx' % (group, server['server'])
                                    data[name] = server['responses'].get('5xx', None)

                                # Fails
                                name = 'upstream_%s_%s_fails' % (group, server['server'])
                                data[name] = server.get('fails', None)

                                # Unavail
                                name = 'upstream_%s_%s_unavail' % (group, server['server'])
                                data[name] = server.get('unavail', None)

            return data

    def getStatus(self,data):
        try:
            request = urlconnection.urlopen(self.nginx_status_url)
            response = request.read()
        except HTTPError as e:
            data['status'] = 0
            data['msg'] = 'Error_code : HTTP Error ' + str(e.code)
        except URLError as e:
            data['status'] = 0
            data['msg'] = 'Error_code : URL Error ' + str(e.reason)
        except InvalidURL as e:
            data['status'] = 0
            data['msg'] = 'Error_code : Invalid URL'
        except Exception as e:  
            data['status']=0
            data['msg']=str(traceback.format_exc())

        try:
            status = json.loads(response)
        except Exception:
            import traceback
            traceback.format_exc()
            return False

        return status

if __name__ == "__main__":
    
    configurations = {'nginx_url':NGINX_STATUS_URL}

    nginx_plus = NginxPlus(configurations)
   
    result = nginx_plus.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
   

