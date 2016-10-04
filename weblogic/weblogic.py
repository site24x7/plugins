#!/usr/bin/python
"""

Site24x7 Oracle Weblogic 12 Plugin

"""

import json
import os

# if any impacting changes to this plugin kindly increment the plugin
# version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
WEBLOGIC_HOST = "localhost"

WEBLOGIC_PORT = "7001"

WEBLOGIC_USERNAME = "admin"

WEBLOGIC_PASSWORD = "admin@123"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'heap_size_current': 'MB'}


class Weblogic(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '7001'))
        self.username = self.configurations.get('user', 'admin')
        self.password = self.configurations.get('password', 'admin')

    def checkPreRequisites(self, data):
        bool_result = True
        try:
            import requests
        except Exception:
            data['status'] = 0
            data['msg'] = 'requests module not installed'
            bool_result = False
            requests_returnVal = os.system(
                'pip install requests >/dev/null 2>&1')
            if requests_returnVal == 0:
                bool_result = True
                data.pop('status')
                data.pop('msg')
        return bool_result, data

    def metricCollector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}

        bool_result, data = self.checkPreRequisites(data)

        if bool_result is False:
            return data
        else:
            try:
                import requests
                from requests import ConnectionError
            except Exception:
                data['status'] = 0
                data['msg'] = 'requests module not installed'
                return data

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
            except ConnectionError as e:
                data['status'] = 0
                data['msg'] = str("Connection error.")

            data['units'] = METRICS_UNITS

        return data


if __name__ == "__main__":
    configurations = {'host': WEBLOGIC_HOST, 'port': WEBLOGIC_PORT,
                      'user': WEBLOGIC_USERNAME, 'password': WEBLOGIC_PASSWORD}

    weblogic_plugin = Weblogic(configurations)

    result = weblogic_plugin.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
