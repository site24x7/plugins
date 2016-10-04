#!/usr/bin/python
"""

Site24x7 Varnish Plugin

"""

import importlib
import json
import os
import subprocess

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
VARNISH_HOST = "localhost"

VARNISH_PORT = "6082"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'cache_hit': 'units', 'cache_miss': 'units', 'n_wrk_create': 'units', 'n_wrk_queued': 'units',
                 'sess_pipe_overflow': 'units'}


class VarnishCache(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '6082'))

    def checkPreRequisites(self, data):
        bool_result = True
        try:
            self.importModule('lxml')
        except Exception as e:
            data['status'] = 0
            data['msg'] = str(e)
            bool_result = False
        return bool_result, data

    def importModule(self, importName, moduleName=None):
        bool_result = True

        if moduleName is None:
            moduleName = importName

        try:
            return importlib.import_module(importName, package=None)
        except Exception:
            # Try to install the package
            requests_returnVal = os.system(
                'pip install %s >/dev/null 2>&1' % moduleName)
            if requests_returnVal == 0:
                raise Exception('%s module not installed' % moduleName)

    def metric_collector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}

        bool_result, data = self.checkPreRequisites(data)

        if bool_result is False:
            return data
        else:
            output = subprocess.check_output(['varnishstat', '-1', '-j'])
            j = json.loads(output)

            data['cache_hit'] = j['cache_hit']['value']
            data['cache_miss'] = j['cache_miss']['value']
            data['n_wrk_create'] = j['n_wrk_create']['value']
            data['n_wrk_queued'] = j['n_wrk_queued']['value']
            data['sess_pipe_overflow'] = j['sess_pipe_overflow']['value']

            data['units'] = METRICS_UNITS

        return data


if __name__ == "__main__":
    configurations = {'host': VARNISH_HOST, 'port': VARNISH_PORT}

    varnish_plugins = VarnishCache(configurations)

    result = varnish_plugins.metric_collector()

    print(json.dumps(result, indent=4, sort_keys=True))
