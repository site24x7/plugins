#!/usr/bin/python
"""

Site24x7 Oracle Weblogic 12 Plugin

"""

import json
import os

import warnings
warnings.filterwarnings("ignore")

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'heap_size_current': 'MB'}


class Weblogic(object):
    def __init__(self, config):
        self.configurations = config
        self.host = self.configurations.get('host')
        self.port = int(self.configurations.get('port'))
        self.username = self.configurations.get('user')
        self.password = self.configurations.get('password')

    def checkPreRequisites(self, data):
        bool_result = True
        try:
            import requests
        except Exception as e:
            import sys
            requests_returnVal = os.system(sys.executable +' -m ' +'pip install requests >/dev/null 2>&1')
            if requests_returnVal != 0:
                bool_result = False
                data['status'] = 0
                data['msg'] = 'requests module not installed'
        return bool_result, data

    def metricCollector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}
        bool_result, data = self.checkPreRequisites(data)
        if bool_result is False:
            return data
        import requests
        url = 'http://%s:%s/management/tenant-monitoring/servers/AdminServer' % (
            self.host, self.port)
        try:
            r = requests.get(url, auth=(self.username, self.password), headers={'Accept': 'application/json'})
            json_data = r.json()

            heap_size = json_data["body"]["item"]["heapSizeCurrent"]
            heap_size /= 1024 * 1024  # Convert to MB
            data["heap_size_current"] = heap_size

            # Get health of all servers

            url = 'http://%s:%s/management/tenant-monitoring/servers' % (
                self.host, self.port)

            r = requests.get(url, auth=(self.username, self.password), headers={'Accept': 'application/json'})
            json_data = r.json()
            items = json_data['body']['items']

            for item in items:
                if item["health"] == "HEALTH_OK":
                    health_status = 1
                else:
                    health_status = 0

                data[item["name"]] = health_status
        except Exception as e:
            data['status'] = 0
            data['msg'] = str(e)

        data['units'] = METRICS_UNITS

        return data

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='weblogic server host',default='localhost')
    parser.add_argument('--port', help='weblogic server port',default='7001')
    parser.add_argument('--username', help='weblogic server name',default=None)
    parser.add_argument('--password',help='weblogic server password',default=None)
    args = parser.parse_args()
    configurations = {'host': args.host, 'port': args.port,
                      'user': args.username, 'password': args.password}
    weblogic_plugin = Weblogic(configurations)
    result = weblogic_plugin.metricCollector()
    print(json.dumps(result, indent=4, sort_keys=True))
