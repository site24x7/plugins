#!/usr/bin/python3
import json,time
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from http.client import InvalidURL
from collections import OrderedDict

url = "http://localhost:80/haproxy?stats;csv"       #Please retain the ";csv" prefix after adding your URL here.
username = None                            #Enter the user name provided by you in haproxy config file here
password = None                            #Enter the password provided by you in haproxy config file here
realm = None                               #Enter 'None' if no realm specified in haproxy config file


#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"


dict_reqdMet = {'stot':'sessions-total' ,
                'ereq':'request-errors' ,
                'bin':'bytes-in',
                'bout':'bytes-out' ,
                'scur':'sessions-active-current' ,
                'qcur':'requests-queue-current' ,
                'act':'servers-active' ,
                'rate':'sessions-rate-current' ,
                'status':'status' 
                }

METRICS_UNITS = {'appname_BACKEND_bytes-out':'KB'}

class haproxy():
    def __init__(self):
        self._url = url
        self._userName = username
        self._userPass = password
        self._realm = realm
        self.dictCounterValues = {}
    def main(self):
        self.metricCollector()
    def metricCollector(self):
        self._openURL()
    def _openURL(self):
        try:
            if (self._userName and self._userPass):
                password_mgr = urlconnection.HTTPPasswordMgr()
                password_mgr.add_password(self._realm, self._url, self._userName, self._userPass)
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                opener = urlconnection.build_opener(auth_handler)
                urlconnection.install_opener(opener)
                #requestObj = urlconnection.Request(self._url)
            response = urlconnection.urlopen(self._url, timeout=10)
            time.sleep(5)
            response1 = urlconnection.urlopen(self._url, timeout=10)
            if (response.status == 200 and response1.status == 200):
                byte_responseData = response.read()
                str_responseData = byte_responseData.decode('UTF-8')
                self._parseStats(str_responseData)
                byte_responseData1 = response1.read()
                str_responseData1 = byte_responseData1.decode('UTF-8')
                self._parseStats(str_responseData1,counter=True)
            else:
                print(str(json.dumps({'Error_code':str(response.status)})))
        except HTTPError as e:
            print(str(json.dumps({'Error_code':'HTTP Error '+str(e.code)})))
        except URLError as e:
            print(str(json.dumps({'Error_code':'URL Error '+str(e.reason)})))
        except InvalidURL as e:
            print(str(json.dumps({'Error_code':'Invalid URL'})))
    def _parseStats(self,str_statsData,counter=False):
        listHeaderData = []
        listInterfaces = []
        dictInterfaceData = OrderedDict()
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
                        dictInterfaceData.setdefault(str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]]),listValues[eachValue])
                        if (counter == True and (listHeaderData[eachValue] == 'bin' or listHeaderData[eachValue] == 'bout')):
                            finalValue = ((int(listValues[eachValue]) - int(self.dictCounterValues[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])]))/5)
                            dictInterfaceData[str_dictKey+ "_" + str(dict_reqdMet[listHeaderData[eachValue]])] = str(finalValue)
                        else:
                            pass
        if counter==False:
            self.dictCounterValues = dictInterfaceData
        else:
            dictInterfaceData['plugin_version'] = PLUGIN_VERSION
            dictInterfaceData['heartbeat_required']=HEARTBEAT
            print(str(json.dumps(dictInterfaceData)))

if __name__ == '__main__':
    hap = haproxy()
    hap.main()