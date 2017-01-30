#!/usr/bin/python
"""
Site24x7 Varnish Plugin

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
VARNISH_HOST = "localhost"
VARNISH_PORT = "6082"

# Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS_V3 = {'cache_hit': 'units', 'cache_miss': 'units', 'n_wrk_create': 'units', 'n_wrk_lqueue': 'units',
                 'sess_pipe_overflow': 'units'}

METRICS_UNITS_V4 = {'cache_hit': 'units', 'cache_miss': 'units', 'threads_created': 'units', 'thread_queue_len': 'units',
                 'sess_pipe_overflow': 'units'}

class VarnishCache(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '6082'))

    def metric_collector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}
        output = subprocess.check_output(['varnishstat', '-1', '-j'])
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
            data['cache_hit'] = j['MAIN.cache_hit']['value']
            data['cache_miss'] = j['MAIN.cache_miss']['value']
            data['threads_created'] = j['MAIN.threads_created']['value']
            data['thread_queue_len'] = j['MAIN.thread_queue_len']['value']
            data['sess_pipe_overflow'] = j['MAIN.sess_pipe_overflow']['value']
            data['units'] = METRICS_UNITS_V4
        return data
    def get_major_version(self):
        output = subprocess.check_output(['varnishd', '-V'], stderr=subprocess.STDOUT).decode('utf-8')
        version = re.search('varnish-(.*) ', output)
        return version.group(1)[0]

if __name__ == "__main__":
    configurations = {'host': VARNISH_HOST, 'port': VARNISH_PORT}
    varnish_plugins = VarnishCache(configurations)
    result = varnish_plugins.metric_collector()
    print(json.dumps(result, indent=4, sort_keys=True))
