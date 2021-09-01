#!/usr/bin/python
"""

Site24x7 Oracle Weblogic 12 Plugin

"""

import json
import os

import urllib
import urllib.request as urlconnection

from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler

from socket import timeout

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
METRICS_UNITS = {}


class Weblogic(object):
    def __init__(self, config):
        self.configurations = config
        self.host = self.configurations.get('host')
        self.port = int(self.configurations.get('port'))
        self.username = self.configurations.get('user')
        self.password = self.configurations.get('password')
        

    def metricCollector(self):
        data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}
        timeout_api_hits=[]
        try:
            # Get health and heap_size of all servers

            url = 'http://%s:%s/management/tenant-monitoring/servers' % (
                self.host, self.port)

            password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()

            password_mgr.add_password(None, url, self.username, self.password)

            handler = urlconnection.HTTPBasicAuthHandler(password_mgr)

            opener = urlconnection.build_opener(handler)

            urlconnection.install_opener(opener)

            hdr = {'Accept':'application/json'}

            req = urlconnection.Request(url, headers=hdr)
            response = urlconnection.urlopen(req)

            json_data = json.loads(response.read().decode('UTF-8'))

            items = json_data['body']['items']
            for item in items:
                if "health" in item:
                    if item["health"]=="HEALTH_OK":
                        health_status=1
                    else:
                        health_status=0
                else:
                    health_status=0
                
                data[item["name"]+"_health"] = health_status
                if item["state"]=="RUNNING":
                    url="http://"+self.host+":"+str(self.port)+"/management/tenant-monitoring/servers/"+item["name"]
                    try:
                        password_mgr.add_password(None, url, self.username, self.password)
                        handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                        opener = urlconnection.build_opener(handler)
                        urlconnection.install_opener(opener)

                        req = urlconnection.Request(url, headers=hdr)
                        response = urlconnection.urlopen(req,timeout=5)
                        json_data = json.loads(response.read().decode('UTF-8'))

                        heap_size=json_data["body"]["item"]["heapSizeCurrent"]
                        heap_size/=1024*1024
                    except timeout as e:
                        heap_size="-"
                        timeout_api_hits.append(item["name"])
                        
                else:
                    heap_size=0
                data[item["name"]+"_heap_size_current"]=heap_size
                METRICS_UNITS[item["name"]+"_heap_size_current"]="MB"
            if len(timeout_api_hits)>0:
                msg="Heapsize url timeout : "
                temp_msg=",".join(timeout_api_hits)
                msg=msg+temp_msg
                data["msg"]=msg
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
