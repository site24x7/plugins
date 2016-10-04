#!/usr/bin/python
"""

Site24x7 Hadoop Plugin

"""

import importlib
import os
import json

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
HADOOP_HOST = "localhost"

HADOOP_PORT = "50070"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'total_load': 'units', 'missing_blocks': 'units', 'corrupt_blocks': 'units'}


class Hadoop(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '50070'))

    def checkPreRequisites(self, data):
        bool_result = True
        try:
            requests = self.importModule('requests')
        except Exception as e:
            data['status'] = 0
            data['msg'] = str(e)
            bool_result = False
        return bool_result, data

    def importModule(self, importName, moduleName=None):
        bool_result = True

        if moduleName == None:
            moduleName = importName

        try:
            return importlib.import_module(importName, package=None)
        except Exception:
            # Try to install the package
            requests_returnVal = os.system(
                'pip install %s >/dev/null 2>&1' % moduleName)
            if requests_returnVal == 0:
                raise Exception('%s module not installed' % moduleName)

    def metricCollector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}

        bool_result, data = self.checkPreRequisites(data)

        if bool_result is False:
            return data
        else:
            import requests
            from requests.exceptions import ConnectionError

            url = 'http://%s:%s/jmx' % (
                self.host, self.port)

            try:
                r = requests.get(url)
                json_data = r.json()

                for bean in json_data['beans']:
                    if bean['name'] == "Hadoop:service=NameNode,name=FSNamesystem":
                        data['total_load'] = bean['TotalLoad']
                        data['missing_blocks'] = bean['MissingBlocks']
                        data['corrupt_blocks'] = bean['CorruptBlocks']
            except ConnectionError as e:
                data['status'] = 0
                data['msg'] = str("Connection error.")

            data['units'] = METRICS_UNITS

        return data


if __name__ == "__main__":
    configurations = {'host': HADOOP_HOST, 'port': HADOOP_PORT}

    hadoop_plugins = Hadoop(configurations)

    result = hadoop_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
