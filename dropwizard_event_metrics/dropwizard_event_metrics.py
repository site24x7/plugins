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
        an url call will be made to the server's '/metrics' which returns four types of attributes
        gauges, counters, histograms, meters, timers in which each of these attributes contains in depth metrics in which 
        we are going to take a few important statistics
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
                             'ch.qos.logback.core.Appender.all' : 'log_count',
                             'ch.qos.logback.core.Appender.debug' : 'debug_',
                             'ch.qos.logback.core.Appender.error': 'error_',
                             'ch.qos.logback.core.Appender.info': 'info_',
                             'ch.qos.logback.core.Appender.trace': 'trace_',
                             'ch.qos.logback.core.Appender.warn': 'warn_',
                             'io.dropwizard.jetty.MutableServletContextHandler.1xx-responses': '_1xx_',
                             'io.dropwizard.jetty.MutableServletContextHandler.2xx-responses': '_2xx_',
                             'io.dropwizard.jetty.MutableServletContextHandler.3xx-responses': '_3xx_',
                             'io.dropwizard.jetty.MutableServletContextHandler.4xx-responses': '_4xx_',
                             'io.dropwizard.jetty.MutableServletContextHandler.5xx-responses': '_5xx_'}
        
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
            for key in result["meters"]:
                if key in self.metricsTaken.keys():
                    dataKey = self.metricsTaken[key]
                    dataValue = result["meters"][key]['count']
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