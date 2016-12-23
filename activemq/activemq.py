#!/usr/bin/python
"""

Site24x7 ActiveMQ Plugin

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
ACTIVEMQ_HOST = "localhost"

ACTIVEMQ_PORT = "8161"

ACTIVEMQ_USERNAME = "admin"

ACTIVEMQ_PASSWORD = "admin"

# Mention the units of your metrics . If any new metrics are added, make
# an entry here for its unit if needed.
METRICS_UNITS = {'total_message_count': 'units', 'total_connections_count': 'units',
                 'total_consumer_count': 'units', 'total_producer_count': 'units'}


class ActiveMQ(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '8161'))
        self.username = self.configurations.get('user', 'root')
        self.password = self.configurations.get('password', '')

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
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required'] = HEARTBEAT

        bool_result, data = self.checkPreRequisites(data)

        if bool_result == False:
            return data
        else:
            try:
                import requests
                from requests import ConnectionError
            except Exception:
                data['status'] = 0
                data['msg'] = 'requests module not installed'
                return data

            url = 'http://%s:%s/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost' % (
                self.host, self.port)

            try:
                r = requests.get(url, auth=(self.username, self.password))
                json_data = r.json()

                total_message_count = json_data['value']['TotalMessageCount']
                total_connections_count = json_data[
                    'value']['TotalConnectionsCount']
                total_consumer_count = json_data['value']['TotalConsumerCount']
                total_producer_count = json_data['value']['TotalProducerCount']

                data['total_message_count'] = total_message_count
                data['total_connections_count'] = total_connections_count
                data['total_consumer_count'] = total_consumer_count
                data['total_producer_count'] = total_producer_count
            except ConnectionError as e:
                data['status'] = 0
                data['msg'] = str("Connection error.")

            data['units'] = METRICS_UNITS

        return data


if __name__ == "__main__":
    configurations = {'host': ACTIVEMQ_HOST, 'port': ACTIVEMQ_PORT,
                      'user': ACTIVEMQ_USERNAME, 'password': ACTIVEMQ_PASSWORD}

    activemq_plugins = ActiveMQ(configurations)

    result = activemq_plugins.metricCollector()

    print(json.dumps(result, indent=4, sort_keys=True))
