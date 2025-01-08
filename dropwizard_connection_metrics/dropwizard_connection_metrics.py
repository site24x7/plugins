#!/usr/bin/python3
### Language : Python
### Tested in Ubuntu

import urllib.request
import json

PLUGIN_VERSION = 1

HEARTBEAT = "true"

#inputs needed for this plugin,
'''
provide the protocol on which the server is running
http (or) https
'''
PROTOCOL = 'http'

'''
provide the hostname on which the server is running
'''
HOSTNAME = 'localhost'

'''
provide the admin port of the dropwizard server. Default value is 8081
'''
PORT = '8081'

class DropWizard:
    def __init__(self, protocol='http', host='localhost', port='8081'):
        ''' The params contains the hostname and port of the dropwizard server,
        an url call '/metrics' will be made to the server which returns four types of attributes
        gauges, counters, histograms, meters, timers. Each of these attributes inturn contains 
        in depth metrics, from which we will take a few important metrics
        '''
        self.url = '%s://%s:%s/metrics'%(protocol, host, port)
        
        self.req = urllib.request.Request(self.url)
        
        '''
            Site24x7 has its own standard on the naming conventions of the attributes, so the attributes
            returned should be changed to Site24x7 naming standard. For this, we have metricsTaken whose key contains
            the attribute returned from the server and the value represents an equivalent name in Site24x7 standard.
            For eg., attribute name should start with alphabet of '_'
        '''
        self.metricsTaken = {
                             'io.dropwizard.jetty.MutableServletContextHandler.requests' : 'total_requests_',
                             'io.dropwizard.jetty.MutableServletContextHandler.get-requests' : 'get_',
                             'io.dropwizard.jetty.MutableServletContextHandler.post-requests': 'post_',
                             'o.dropwizard.jetty.MutableServletContextHandler.put-requests': 'put_',
                             'io.dropwizard.jetty.MutableServletContextHandler.delete-requests': 'delete_',
                             'io.dropwizard.jetty.MutableServletContextHandler.move-requests': 'move_',
                             'io.dropwizard.jetty.MutableServletContextHandler.head-requests': 'head_',
                             'io.dropwizard.jetty.MutableServletContextHandler.connect-requests': 'connect_',
                             'io.dropwizard.jetty.MutableServletContextHandler.options-requests': 'options_',
                             'io.dropwizard.jetty.MutableServletContextHandler.other-requests': 'other_',
                             'org.eclipse.jetty.server.HttpConnectionFactory.8080.connections': '_8080_',
                             'org.eclipse.jetty.server.HttpConnectionFactory.8081.connections': '_8081_',
                             'org.eclipse.jetty.server.HttpConnectionFactory.8443.connections': '_8443_',
                             'org.eclipse.jetty.server.HttpConnectionFactory.8444.connections': '_8444_'}
        
        '''
            We have to supply the necessary units for each attributes that we are going to report to Site24x7.
            metricUnits is a dictionary contains the attributes that we are going to monitor as the key and 
            value as its units. The map will be included in the data map returned in the metricsCollector method
        '''
        self.metricUnits = {}
    
    def metricsCollector(self):
        data = {}
        try:
            with urllib.request.urlopen(self.req) as res:
                result = json.loads(res.read().decode())
            for key in result["timers"]:
                if key in self.metricsTaken.keys():
                    dataKey = self.metricsTaken[key]
                    dataValue = result["timers"][key]['count']
                    if dataKey in self.metricUnits and self.metricUnits[dataKey] is 'MB':
                        dataValue = self.convertToMB(dataValue)
                    data[dataKey] = dataValue
            data['units'] = self.metricUnits
        except Exception as e:
            data['error'] = str(e)
        return data
    
    def convertToMB(self, v):
        try:
            byte_s=float(v)        
            kilobytes=byte_s/1024;        
            megabytes=kilobytes/1024;        
            v=round(megabytes,2)    
        except Exception as e:        
            pass    
        return v
    
if __name__ == '__main__':
    
    dropWizard = DropWizard(protocol=PROTOCOL, host=HOSTNAME, port=PORT)
    
    result = dropWizard.metricsCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))