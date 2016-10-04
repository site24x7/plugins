#!/usr/bin/python
"""

Site24x7 VoltDB Plugin

"""
import argparse
import sys
import urllib2
import socket
import xml.etree.ElementTree as ET
from math import log
import json
import os
import traceback
from voltdbclient import *

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
VOLTDB_HOST = 'localhost'

VOLTDB_PORT = '21212'

METRICS_UNITS = {'java_used':'MB',
                 'java_unused':'MB',
                 'tuple_used_mem':'MB',
                 'pooled_mem':'MB',
                 'indexed_mem':'MB',
                 'max_heap_java':'MB',
                 'tuple_alloc_mem':'MB'
                 }

def convertBytesToMB(v):
    try:
        byte_s=float(v)        
        kilobytes=byte_s/1024;        
        megabytes=kilobytes/1024;        
        v=round(megabytes,2)    
    except Exception as e:        
        pass    
    return v


class VoltDB(object):
    
    def __init__(self,config):
        self.configurations = config
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '21212'))        

        
    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT

        try:
            client = FastSerializer(self.host, self.port)
            stats = VoltProcedure( client, "@Statistics", 
                [ FastSerializer.VOLTTYPE_STRING, 
                 FastSerializer.VOLTTYPE_INTEGER ] )

            response = stats.call([ "memory", 0 ])
            if response == None:
                data['status']=0
            else:
                data['status']=1
                for t in response.tables:
                    for row in t.tuples:
                        data['RSS'] = float(row[3])
                        data['java_used'] = convertBytesToMB(float(row[4]))
                        data['java_unused'] = convertBytesToMB(float(row[5]))
                        data['tuple_used_mem'] = convertBytesToMB(float(row[6]))
                        data['tuple_alloc_mem'] = convertBytesToMB(float(row[7]))
                        data['tuple_count'] = float(row[10])
                        data['pooled_mem'] = convertBytesToMB(float(row[11]))
                        data['max_heap_java'] = convertBytesToMB(float(row[13]))
                        data['indexed_mem'] = convertBytesToMB(float(row[8]))
            client.close()
        except Exception as e:
            data['msg']=str(e)
            data[status]=0
        data['units'] = METRICS_UNITS
        return data


if __name__ == "__main__":

    configurations = {'host': VOLTDB_HOST,'port': VOLTDB_PORT}

    voltdb_plugins = VoltDB(configurations)
    
    result = voltdb_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
