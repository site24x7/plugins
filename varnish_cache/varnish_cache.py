#!/usr/bin/python

"""
Site24x7 Varnish Plugin

author: selvakumar.cs
Edited to support all types of data from varnish cache

"""
import importlib
import json
import os
import subprocess
import re

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
VARNISH_INSTANCE = ""

# Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS_V3 = {'cache_hit': 'units', 'cache_miss': 'units', 'n_wrk_create': 'units', 'n_wrk_lqueue': 'units',
                 'sess_pipe_overflow': 'units'}

METRICS_UNITS_V4 = {'cache_hit': 'units', 'cache_miss': 'units', 'threads_created': 'units', 'thread_queue_len': 'units',
                 'sess_pipe_overflow': 'units'}

class VarnishCache(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None

    def metric_collector(self):
        data = {
            'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT
        }
        
        varnish_command = ['varnishstat', '-1', '-j']

        if VARNISH_INSTANCE != "":
            varnish_command.append('-n')
            varnish_command.append(VARNISH_INSTANCE)    

        output = subprocess.check_output(varnish_command)
        j = json.loads(output.decode())
        varnish_version = self.get_major_version()
        if int(varnish_version) < 4:
            data['cache_hit'] = j['cache_hit']['value']
            data['cache_miss'] = j['cache_miss']['value']
            data['n_wrk_create'] = j['n_wrk_create']['value']
            data['n_wrk_lqueue'] = j['n_wrk_lqueue']['value']
            data['sess_pipe_overflow'] = j['sess_pipe_overflow']['value']
            data['units'] = METRICS_UNITS_V3
        else:
            for key,value in j.items():            
                if '.' in key:
                    key_name=key.split('.');
                    if key_name[1] in METRICS_UNITS_V4:
                        data[key_name[1]]=value['value']
            data['units'] = METRICS_UNITS_V4
        return data
    def get_major_version(self):
        output = subprocess.check_output(['varnishd', '-V'], stderr=subprocess.STDOUT).decode('utf-8')
        version = re.search('varnish-(.*) ', output)
        return version.group(1)[0]

if __name__ == "__main__":
    configurations = {}
    varnish_plugins = VarnishCache(configurations)
    result = varnish_plugins.metric_collector()
    print(json.dumps(result, indent=4, sort_keys=True))

