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


STORE_METRICS = {
                  "getsSuccess": "gets_success",
                  "getsFail": "gets_fail",
                  "setsSuccess": "sets_success",
                  "setsFail": "sets_fail",
                  "deleteSuccess": "delete_success",
                  "deleteFail": "delete_fail",
                  "updateSuccess": "update_success",
                  "updateFail": "update_fail",
                  "createSuccess": "create_success",
                  "createFail": "create_fail",
                  "compareAndSwapSuccess": "compare_and_swap_success",
                  "compareAndSwapFail": "compare_and_swap_fail",
                  "compareAndDeleteSuccess": "compare_and_delete_success",
                  "compareAndDeleteFail": "compare_and_delete_fail",
                  "expireCount": "expire_count",
                  "watchers": "watchers"
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
        store_metrics = self._get_store_metrics()
        for key, val in STORE_METRICS.items():
            self.metrics[val] = store_metrics[key]

        return self.metrics

    def _get_store_metrics(self):
        return self.__get_url_data(self.base_url+"/v2/stats/store")

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
