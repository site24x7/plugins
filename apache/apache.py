#!/usr/bin/python3

import json
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from http.client import InvalidURL
from collections import OrderedDict

#Change the Apache stats URL accordingly here. Retain the "?auto" suffix.
url = "http://localhost:80/server-status?auto"
username = None
password = None

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

dict_reqdMet = {'Total Accesses':'total_accesses',
                'Total kBytes':'total_kbytes',
                'CPULoad':'cpu_load',
                'Uptime':'uptime',
                'ReqPerSec':'req_per_sec',
                'BytesPerSec':'bytes_per_sec',
                'BytesPerReq':'bytes_per_req',
                'BusyWorkers':'busy_workers',
                'IdleWorkers':'idle_workers'
                }

METRICS_UNITS = {'total_kbytes':'Bytes',
                 'uptime':'Seconds',
                 'bytes_per_sec':'Bytes',
                 'bytes_per_req':'Bytes'
                 }

class apache():
    def __init__(self):
        self._userName = username
        self._userPass = password
        self._url = url
    def main(self):
        self.metricCollector()
    def metricCollector(self):
        try:
            if (self._userName and self._userPass):
                    password_mgr = urlconnection.HTTPPasswordMgr()
                    password_mgr.add_password(self._realm, self._url, self._userName, self._userPass)
                    auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                    opener = urlconnection.build_opener(auth_handler)
                    urlconnection.install_opener(opener)
            response = urlconnection.urlopen(self._url, timeout=10)
            if response.status == 200:
                byte_responseData = response.read()
                str_responseData = byte_responseData.decode('UTF-8')
                self._parseStats(str_responseData)
            else:
                print(str(json.dumps({'Error_code':str(response.status)})))
        except HTTPError as e:
            print(str(json.dumps({'Error_code':'HTTP Error '+str(e.code)})))
        except URLError as e:
            print(str(json.dumps({'Error_code':'URL Error '+str(e.reason)})))
        except InvalidURL as e:
            print(str(json.dumps({'Error_code':'Invalid URL'})))
    def _parseStats(self,str_responseData):
        try:
            dictApacheData = {}
            listStatsData = str_responseData.split('\n')
            for eachStat in listStatsData:
                stats = eachStat.split(':')
                if str(stats[0]) in dict_reqdMet:
                    dictApacheData.setdefault(dict_reqdMet[str(stats[0])],str(stats[1]))
            dictApacheData['plugin_version'] = PLUGIN_VERSION
            dictApacheData['heartbeat_required'] = HEARTBEAT
            dictApacheData['units'] = METRICS_UNITS
            print(str(json.dumps(dictApacheData)))
        except TypeError as e:
            print(str(json.dumps({'Error_code': 'Type error in _parseStats'})))
        except Exception as e:
            print(str(json.dumps({'Error_code':str(e)})))
    
if __name__ == '__main__':
    ap = apache()
    ap.main()