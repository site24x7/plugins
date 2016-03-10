#!/usr/bin/python

import httplib
import json
import urllib2

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
NGINX_STATUS_URL = "http://localhost/status"

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
            
            req = urllib2.Request(self.nginx_status_url)
            request = urllib2.urlopen(req)
            response = request.read()

        except urllib2.HTTPError, e:
            data['status']=0
            data['msg']='HTTP error'
            
        except urllib2.URLError, e:
            data['status']=0
            data['msg']='URL error'

        except httplib.HTTPException, e:
            data['status']=0
            data['msg']='HTTP Exception'

        except Exception:
            data['status']=0
            data['msg']='Exception Occured'

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
   
