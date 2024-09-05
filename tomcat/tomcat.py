#!/usr/bin/python3
"""
Site24x7 Tomcat Plugin
"""
import argparse
import sys
import socket
import xml.etree.ElementTree as ET
import json
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError

# If any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
TOMCAT_HOST = 'localhost'
TOMCAT_PORT = '8080'
TOMCAT_USERNAME = 'user'
TOMCAT_PASSWORD = 'user'
TOMCAT_URL = '/manager'
TOMCAT_CONNECTOR = 'http-nio-8080'
TOMCAT_TIMEOUT = '5'
LOGS_ENABLED = 'true'
LOG_TYPE_NAME = 'Tomcat Access Logs'
LOG_FILE_PATH = '/opt/*tomcat*/logs/*access*.txt'

METRICS_UNITS = {
    'Bytes Received': 'MB',
    'Bytes Sent': 'MB',
    'Processing Time': 'ms',
    'Available Memory': 'GB',
    'Free Memory': 'GB',
    'Percent Used Memory': '%',
    'Total Memory': 'GB',
    'Used Memory': 'GB'
}

def convertBytesToMB(v):
    try:
        byte_s = float(v)
        kilobytes = byte_s / 1024
        megabytes = kilobytes / 1024
        return round(megabytes, 2)
    except Exception:
        return v

def convertMBToGB(v):
    try:
        megabytes = float(v)
        gigabytes = megabytes / 1024
        return round(gigabytes, 2)
    except Exception:
        return v

class Tomcat(object):
    def __init__(self, config):
        self.configurations = config
        self.host = self.configurations.get('host', TOMCAT_HOST)
        self.port = int(self.configurations.get('port', TOMCAT_PORT))
        self.username = self.configurations.get('username', TOMCAT_USERNAME)
        self.password = self.configurations.get('password', TOMCAT_PASSWORD)
        self.plugin_version = self.configurations.get('plugin_version', PLUGIN_VERSION)
        self.connector = self.configurations.get('connector', TOMCAT_CONNECTOR)
        self.url = self.configurations.get('url', TOMCAT_URL)
        self.timeout = int(self.configurations.get('timeout', TOMCAT_TIMEOUT))

    def readXmlFromUrl(self, host, port, url, user, password):
        xmlUrl = url + "/status?XML=true"
        xmlData, xmlError = self.readUrl(host, port, xmlUrl, user, password)
        if xmlError:
            return xmlData, xmlError
        else:
            try:
                root = ET.fromstring(xmlData)
            except ET.ParseError as e:
                root = "ERROR: Unable to read the XML page. Error: %s" % (e)
                xmlError = True
            return root, xmlError

    def readUrl(self, host, port, url, user, password):
        error = False
        tomcatUrl = "http://" + host + ":" + str(port) + url
        try:
            pwdManager = urlconnection.HTTPPasswordMgrWithDefaultRealm()
            pwdManager.add_password(None, tomcatUrl, user, password)
            authHandler = urlconnection.HTTPBasicAuthHandler(pwdManager)
            opener = urlconnection.build_opener(authHandler)
            urlconnection.install_opener(opener)
            req = urlconnection.Request(tomcatUrl)
            handle = urlconnection.urlopen(req, None)
            data = handle.read()
        except HTTPError as e:
            if e.code == 401:
                data = "ERROR: Unauthorized user. Does not have permissions. %s" % (e)
            elif e.code == 403:
                data = "ERROR: Forbidden, your credentials are not correct. %s" % (e)
            else:
                data = "ERROR: The server couldn't fulfill the request. %s" % (e)
            error = True
        except URLError as e:
            data = 'ERROR: We failed to reach a server. Reason: %s' % (e.reason)
            error = True
        except socket.timeout as e:
            data = 'ERROR: Timeout error'
            error = True
        except socket.error as e:
            data = "ERROR: Unable to connect with host " + self.host + ":" + str(self.port)
            error = True
        except:
            data = "ERROR: Unexpected error: %s" % (sys.exc_info()[0])
            error = True

        return data, error

    def formatKey(self, key):
        key = key.replace("_", " ")
        return key.capitalize()
    
    def metricCollector(self):
        data = {}
        data['plugin_version'] = self.plugin_version
        data['heartbeat_required'] = HEARTBEAT

        socket.setdefaulttimeout(float(self.timeout))
        serverinfoUrl = self.url + "/serverinfo"
        serverinfoData, serverinfoError = self.readUrl(self.host, self.port, serverinfoUrl, self.username, self.password)
        if serverinfoError:
            serverinfoUrl = self.url + "/text/serverinfo"
            serverinfoData, serverinfoError = self.readUrl(self.host, self.port, serverinfoUrl, self.username, self.password)
        if not serverinfoError:
            serverinfo = serverinfoData.decode("utf-8").splitlines()
            tomcatVersionStr = (serverinfo[1].split(":"))[1]
            tomcatStatusStr = serverinfo[0]
            tomcatVersion = (tomcatVersionStr.split("/"))[1].split(".")[0]
            if tomcatVersion.isdigit():
                data['Tomcat Version'] = f"v_{tomcatVersion}"
            if tomcatStatusStr.split(' ')[0] == 'OK':
                status = 1
            else:
                status = 0

            if status == 0:
                data['status'] = status

            xmlTreeData, xmlError = self.readXmlFromUrl(self.host, self.port, self.url, self.username, self.password)
            if not xmlError:
                if xmlTreeData is not None:
                    if data.get('status') == 0:
                        if xmlTreeData.tag == 'status':
                            data['status'] = 1

                    connector_data = {}
                    for connector in xmlTreeData.findall('./connector'):
                        name = str(connector.get('name'))
                        name = name.replace("\"", "")
                        if name == self.connector:
                            thread = connector.find('./threadInfo')
                            request = connector.find('./requestInfo')
                            connector_data = {
                                'Name': name,
                                'Thread Count': int(thread.get('currentThreadCount')),
                                'Thread Busy': int(thread.get('currentThreadsBusy')),
                                'Thread Allowed': float(thread.get('maxThreads')),
                                'Bytes Received': convertBytesToMB(float(request.get('bytesReceived'))),
                                'Bytes Sent': convertBytesToMB(float(request.get('bytesSent'))),
                                'Error Count': float(request.get('errorCount')),
                                'Processing Time': float(request.get('processingTime')),
                                'Request Count': float(request.get('requestCount'))
                            }

                    data.update(connector_data)

                    memorypool_data = {}
                    for mempool in xmlTreeData.findall('.//memorypool'):
                        name = str(mempool.get('name')).replace(" ", "_")
                        memorypool_data[f'Usage {name}'] = float(mempool.get('usageUsed'))

                    data.update(memorypool_data)

                    memoryObj = xmlTreeData.find('.//memory')
                    if memoryObj is not None:
                        freeMem = float(memoryObj.get('free'))
                        totalMem = float(memoryObj.get('total'))
                        maxMem = float(memoryObj.get('max'))
                        availableMem = freeMem + maxMem - totalMem
                        usedMem = maxMem - availableMem
                        percentUsedMem = float((usedMem * 100) / maxMem)
                        data.update({
                            'Available Memory': convertBytesToMB(float(availableMem)),
                            'Free Memory': convertBytesToMB(float(freeMem)),
                            'Max Memory': str(convertMBToGB(convertBytesToMB(float(maxMem)))) + ' GB',
                            'Total Memory': convertBytesToMB(float(totalMem)),
                            'Used Memory': convertBytesToMB(float(usedMem)),
                            'Percent Used Memory': percentUsedMem
                        })

                    data['tabs'] = {
                        'Memory Metrics': {
                            'order': 1,
                            'tablist': [
                                'Available Memory',
                                'Free Memory',
                                'Max Memory',
                                'Total Memory',
                                'Used Memory',
                                'Percent Used Memory'
                            ]
                        },
                        'JVM CodeHeap Usage': {
                            'order': 2,
                            'tablist': [
                                "Usage CodeHeap_'non-nmethods'",
                                "Usage CodeHeap_'non-profiled_nmethods'",
                                "Usage CodeHeap_'profiled_nmethods'"
                            ]
                        },
                        'JVM Memory Pool Usage': {
                            'order': 3,
                            'tablist': [
                                "Usage Compressed_Class_Space",
                                "Usage G1_Eden_Space",
                                "Usage G1_Old_Gen",
                                "Usage G1_Survivor_Space",
                                "Usage Metaspace"
                            ]
                        }
                    }
                else:
                    data['msg'] = 'Unable to collect data for the server'
        else:
            data['msg'] = serverinfoData
            data['status'] = 0

        data['units'] = METRICS_UNITS
        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help="Host Name", nargs='?', default=TOMCAT_HOST)
    parser.add_argument('--port', help="Port", nargs='?', default=TOMCAT_PORT)
    parser.add_argument('--username', help="Username", default=TOMCAT_USERNAME)
    parser.add_argument('--password', help="Password", default=TOMCAT_PASSWORD)
    parser.add_argument('--plugin_version', help="plugin_version", default=PLUGIN_VERSION)
    parser.add_argument('--connector', help="Connector Name", default=TOMCAT_CONNECTOR)
    parser.add_argument('--url', help="URL", default=TOMCAT_URL)
    parser.add_argument('--timeout', help="Timeout", default=TOMCAT_TIMEOUT)
    parser.add_argument('--logs_enabled', help="logs_enabled", default=LOGS_ENABLED)
    parser.add_argument('--log_type_name', help="log_type_name", default=LOG_TYPE_NAME)
    parser.add_argument('--log_file_path', help="log_file_path", default=LOG_FILE_PATH)

    args = parser.parse_args()

    configurations = {
        'host': args.host,
        'port': args.port,
        'username': args.username,
        'password': args.password,
        'connector': args.connector,
        'url': args.url,
        'timeout': args.timeout,
        'plugin_version' : args.plugin_version
    }

    tomcat_plugins = Tomcat(configurations)
    result = tomcat_plugins.metricCollector()
    print(json.dumps(result, indent=4, sort_keys=True))
