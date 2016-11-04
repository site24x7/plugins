#!/usr/bin/python

"""

__author__ = Vijay, Zoho Corp
Language = Python

Tested in Ubuntu, Windows 8

"""

import json
import sys

PYTHON_MAJOR_VERSION = sys.version_info[0]
REQUESTS_INSTALLED = None
if PYTHON_MAJOR_VERSION == 3:
    import urllib.request as urlconnection
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection

###################################### CONFIG SECTION START ###########################################

url = "http://localhost:2379"

###################################### CONFIG SECTION START ###########################################

DEFAULT_URL = "http://localhost:2379"

proxy = urlconnection.ProxyHandler({})
opener = urlconnection.build_opener(proxy)
urlconnection.install_opener(opener)

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

SELF_METRICS = {
        "recvAppendRequestCnt": "self_recv_appendreq_cnt",
        "recvPkgRate": "self_recv_pkg_rate",
        "recvBandwidthRate": "self_recv_bandwidth_rate",
        "sendAppendRequestCnt": "self_appendreq_cnt",
        "sendPkgRate": "self_send_pkg_rate",
        "sendBandwidthRate": "self_send_bandwidth_rate"
}

class EtcdMon():
    metrics = {}
    config = {}
    base_url = ""

    def __init__(self, config):
        self.config = config
        self.base_url = self.get_data("url", DEFAULT_URL, "", None)

    def _get_metrics(self):
        self.metrics['plugin_version'] = PLUGIN_VERSION
        self.metrics['heartbeat_required'] = HEARTBEAT
        
        self_metrics = self._get_self_metrics()
        for key, val in SELF_METRICS.items():
            if key in self_metrics:
                self.metrics[val] = self_metrics[key]
            else:
                self.metrics[val] = 0

        return self.metrics

    def _get_self_metrics(self):
        return self.__get_url_data(self.base_url+"/v2/stats/self")

    def __get_url_data(self, url):
        str_responseData = None
        try:
            response = urlconnection.urlopen(url)
            byte_responseData = response.read()
            str_responseData = byte_responseData.decode('UTF-8')
        except Exception as e:
            pass

        if str_responseData:
            return json.loads(str_responseData)

    def get_data(self, key, default_value, *invalid_values):
        if key in self.config:
            val = self.config.get(key)
            if val in invalid_values:
                return default_value
            else:
                return val
        return  default_value

if __name__ == '__main__':
    config = {}
    mon = EtcdMon(config)
    metrics = mon._get_metrics()
    print(json.dumps(metrics))
