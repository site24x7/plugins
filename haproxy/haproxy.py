#!/usr/bin/python

import os
import sys
import json,time
from collections import OrderedDict
from _socket import timeout

url = "http://localhost:80/haproxy?stats;csv"       #Please retain the ";csv" prefix after adding your URL here.
username = None                            #Enter the user name provided by you in haproxy config file here
password = None                            #Enter the password provided by you in haproxy config file here
realm = None                 #Enter 'None' if no realm specified in haproxy config file. Do not include any escape characters while adding this value


#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"


dict_reqdMet = {'ereq':'request-errors' ,
                'bin':'bytes-in',
                'bout':'bytes-out' ,
                'qcur':'requests-queue-current' ,
                'rate':'sessions-rate-current' 
                }

METRICS_UNITS = {'appname_BACKEND_bytes-out':'KB'}

counterFilePath = '/opt/site24x7/monagent/plugins/haproxy/counter.json'


PYTHON_MAJOR_VERSION = sys.version_info[0]
#REQUESTS_INSTALLED = None
if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
    from http.client import InvalidURL
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError,URLError
    from httplib import InvalidURL


class haproxy():
    def __init__(self):
        self._url = url
        self._userName = username
        self._userPass = password
        self._realm = realm
        self.dictCounterValues = {}
        self.dictInterfaceData = {}
        self.loadCounterValues()
    def loadCounterValues(self):
        file_obj = None
        if not os.path.exists(counterFilePath):
            file_obj = open(counterFilePath,'w')
            file_obj.close()
        else:
            file_obj = open(counterFilePath,'r')
            str_counterValues = file_obj.read()
            if str_counterValues:
                self.dictCounterValues = json.loads(str_counterValues)
            file_obj.close()
    def updateCounterValues(self,dict_valuesToUpdate):
        if os.path.exists(counterFilePath):
            file_obj = open(counterFilePath,'w')
            file_obj.write(json.dumps(dict_valuesToUpdate))
            file_obj.close()
    def main(self):
        if PYTHON_MAJOR_VERSION == 3:
            self.metricCollector3()
        elif PYTHON_MAJOR_VERSION == 2:
            self.metricCollector2()
        else:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Python version is 2 and requests not installed'
        print(json.dumps(self.dictInterfaceData))
    def metricCollector3(self):
        self._openURL3()
        self.dictInterfaceData['plugin_version'] = PLUGIN_VERSION
        self.dictInterfaceData['heartbeat_required']= HEARTBEAT
    def metricCollector2(self):
        self._openURL2()
        self.dictInterfaceData['plugin_version'] = PLUGIN_VERSION
        self.dictInterfaceData['heartbeat_required']= HEARTBEAT
    def _openURL2(self):
        try:
            if (self._userName and self._userPass):
                password_mgr = urlconnection.HTTPPasswordMgr()
                password_mgr.add_password(self._realm, self._url, self._userName, self._userPass)
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                opener = urlconnection.build_opener(auth_handler)
                urlconnection.install_opener(opener)
            response = urlconnection.urlopen(self._url, timeout=10)
            if (response.getcode() == 200):
                byte_responseData = response.read()
                str_responseData = byte_responseData.decode('UTF-8')
                self._parseStats(str_responseData)
            else:
                self.dictInterfaceData['status'] = 0
                self.dictInterfaceData['msg'] = 'Response status code from haproxy url is :'  + str(response.getcode())
        except HTTPError as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] ='Haproxy stats url has HTTP Error '+str(e.code)
        except URLError as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Haproxy stats url has URL Error '+str(e.reason)
        except InvalidURL as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Haproxy stats url is invalid URL'
        except Exception as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Haproxy stats URL error : ' + str(e)
    def _openURL3(self):
        try:
            if (self._userName and self._userPass):
                password_mgr = urlconnection.HTTPPasswordMgr()
                password_mgr.add_password(self._realm, self._url, self._userName, self._userPass)
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                opener = urlconnection.build_opener(auth_handler)
                urlconnection.install_opener(opener)
            response = urlconnection.urlopen(self._url, timeout=10)
            if (response.status == 200):
                byte_responseData = response.read()
                str_responseData = byte_responseData.decode('UTF-8')
                self._parseStats(str_responseData)
            else:
                self.dictInterfaceData['status'] = 0
                self.dictInterfaceData['msg'] = 'Response status code from haproxy url is :'  + str(response.status)
        except HTTPError as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] ='Haproxy stats url has HTTP Error '+str(e.code)
        except URLError as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Haproxy stats url has URL Error '+str(e.reason)
        except InvalidURL as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Haproxy stats url is invalid URL'
        except Exception as e:
            self.dictInterfaceData['status'] = 0
            self.dictInterfaceData['msg'] = 'Haproxy stats URL error : ' + str(e)
    def _parseStats(self,str_statsData):
        listHeaderData = []
        listInterfaces = []
        #dictInterfaceData = OrderedDict()
        dcTime = time.time()
        listStatsData = str_statsData.split("#")[1].lstrip().rstrip().split("\n")
        for interfaceIndex in range(len(listStatsData)):
            str_interfaceData = ""
            listValues = listStatsData[interfaceIndex].split(",")
            if interfaceIndex == 0:
                for eachValue in range(len(listValues)-1):
                    listHeaderData.append(listValues[eachValue])
                #print("\n HeaderData \n" + str(listHeaderData))
            else:
                str_dictKey = str(listValues[0])+'_'+str(listValues[1])
                if str_dictKey in listInterfaces:
                    continue
                else:
                    listInterfaces.append(str_dictKey)
                for eachValue in range(len(listValues)-1):
                    if listHeaderData[eachValue] in dict_reqdMet.keys():
                        if listValues[eachValue] == '':
                            listValues[eachValue] = '0'
                        self.dictInterfaceData.setdefault(str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]]),listValues[eachValue])
                        try:
                            if (listHeaderData[eachValue] == 'bin' or listHeaderData[eachValue] == 'bout'):
                                if ((str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])) in self.dictCounterValues):
                                    finalValue = int(listValues[eachValue]) - int(self.dictCounterValues[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])])
                                    if finalValue > 0:
                                        self.dictInterfaceData[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])] = str(finalValue)
                                    else:
                                        self.dictInterfaceData[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])] = '0'
                                else:
                                    self.dictInterfaceData[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])] = '0'
                                self.dictCounterValues[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])] = int(listValues[eachValue])
                        except Exception as e:
                            pass
        #self.dictCounterValues = self.dictInterfaceData
        #self.dictCounterValues['ct'] = dcTime
        self.updateCounterValues(self.dictCounterValues)

if __name__ == '__main__':
    hap = haproxy()
    hap.main()