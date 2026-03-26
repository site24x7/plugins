#!/usr/bin/python3
"""
Site24x7 Tomcat Plugin
"""
import argparse
import sys
import socket
import ssl
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
TOMCAT_PROTOCOL = 'http'
TOMCAT_USERNAME = 'user'
TOMCAT_PASSWORD = 'user'
TOMCAT_VERIFY_SSL = 'true'
TOMCAT_URL = '/manager'
LOGS_ENABLED = 'true'
LOG_TYPE_NAME = 'Tomcat Access Logs'
LOG_FILE_PATH = '/opt/*tomcat*/logs/*access*.txt'

METRICS_UNITS = {
    'Connectors': {
        'Bytes Received': 'MB',
        'Bytes Sent': 'MB',
        'Processing Time': 'ms',
        'Max Time': 'ms'
        },
    'Available Memory': 'MB',
    'Free Memory': 'MB',
    'Percent Used Memory': '%',
    'Total Memory': 'MB',
    'Used Memory': 'MB',
    'Committed G1_Eden_Space': 'MB',
    'Used G1_Eden_Space': 'MB',
    'Committed G1_Old_Gen': 'MB',
    'Used G1_Old_Gen': 'MB',
    'Committed G1_Survivor_Space': 'MB',
    'Used G1_Survivor_Space': 'MB',
    "Committed CodeHeap_'non-nmethods'": 'MB',
    "Used CodeHeap_'non-nmethods'": 'MB',
    "Committed CodeHeap_'non-profiled_nmethods'": 'MB',
    "Used CodeHeap_'non-profiled_nmethods'": 'MB',
    "Committed CodeHeap_'profiled_nmethods'": 'MB',
    "Used CodeHeap_'profiled_nmethods'": 'MB',
    'Committed Compressed_Class_Space': 'MB',
    'Used Compressed_Class_Space': 'MB',
    'Committed Metaspace': 'MB',
    'Used Metaspace': 'MB'
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
        self.protocol = self.configurations.get('protocol', TOMCAT_PROTOCOL)
        self.username = self.configurations.get('username', TOMCAT_USERNAME)
        self.password = self.configurations.get('password', TOMCAT_PASSWORD)
        self.verify_ssl = self.configurations.get('verify_ssl', TOMCAT_VERIFY_SSL).lower() == 'true'
        self.plugin_version = self.configurations.get('plugin_version', PLUGIN_VERSION)
        self.url = self.configurations.get('url', TOMCAT_URL)
        self.logs_enabled = self.configurations.get('logs_enabled', LOGS_ENABLED)
        self.log_type_name = self.configurations.get('log_type_name', LOG_TYPE_NAME)
        self.log_file_path = self.configurations.get('log_file_path', LOG_FILE_PATH)

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
        tomcatUrl = self.protocol + "://" + host + ":" + str(port) + url
        try:
            pwdManager = urlconnection.HTTPPasswordMgrWithDefaultRealm()
            pwdManager.add_password(None, tomcatUrl, user, password)
            authHandler = urlconnection.HTTPBasicAuthHandler(pwdManager)
            
            # Handle SSL verification
            if self.protocol == 'https' and not self.verify_ssl:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                https_handler = urlconnection.HTTPSHandler(context=ssl_context)
                opener = urlconnection.build_opener(authHandler, https_handler)
            else:
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

        serverinfoUrl = self.url + "/serverinfo"
        serverinfoData, serverinfoError = self.readUrl(self.host, self.port, serverinfoUrl, self.username, self.password)
        if serverinfoError:
            serverinfoUrl = self.url + "/text/serverinfo"
            serverinfoData, serverinfoError = self.readUrl(self.host, self.port, serverinfoUrl, self.username, self.password)
        if not serverinfoError:
            serverinfo = serverinfoData.decode("utf-8").splitlines()
            tomcatStatusStr = serverinfo[0]
            
            tomcatVersionStr = (serverinfo[1].split(":"))[1].strip()
            data['Tomcat Version'] = tomcatVersionStr.strip("[]").strip()
            
            if len(serverinfo) > 5:
                jvmVersionStr = (serverinfo[5].split(":"))[1].strip()
                data['JVM Version'] = jvmVersionStr.strip("[]").strip()
            
            if len(serverinfo) > 6:
                jvmVendorStr = (serverinfo[6].split(":"))[1].strip()
                data['JVM Vendor'] = jvmVendorStr.strip("[]").strip()
            
            data['Server Info'] = tomcatStatusStr.split(' ')[0]
            
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

                    connectors = []
                    for connector in xmlTreeData.findall('./connector'):
                        name = str(connector.get('name'))
                        name = name.replace("\"", "")
                        thread = connector.find('./threadInfo')
                        request = connector.find('./requestInfo')
                        connector_data = {
                            'name': name,
                            'Current Thread Count': int(thread.get('currentThreadCount')),
                            'Busy Thread Count': int(thread.get('currentThreadsBusy')),
                            'Max Thread Count': str(int(thread.get('maxThreads'))) + ' threads',
                            'Bytes Received': convertBytesToMB(float(request.get('bytesReceived'))),
                            'Bytes Sent': convertBytesToMB(float(request.get('bytesSent'))),
                            'Error Count': float(request.get('errorCount')),
                            'Processing Time': float(request.get('processingTime')),
                            'Request Count': float(request.get('requestCount')),
                            'Max Time': float(request.get('maxTime'))
                        }
                        connectors.append(connector_data)
                    
                    if connectors:
                        data['Connectors'] = connectors

                    memorypool_data = {}
                    for mempool in xmlTreeData.findall('.//memorypool'):
                        name = str(mempool.get('name')).replace(" ", "_")
                        
                        usageInit = convertBytesToMB(float(mempool.get('usageInit')))
                        usageCommitted = convertBytesToMB(float(mempool.get('usageCommitted')))
                        usageUsed = convertBytesToMB(float(mempool.get('usageUsed')))
                        
                        usageMaxRaw = float(mempool.get('usageMax'))
                        if usageMaxRaw == -1:
                            usageMax = 'Unlimited'
                        else:
                            usageMax = str(convertBytesToMB(usageMaxRaw)) + ' MB'
                        
                        memorypool_data[f'Init {name}'] = str(usageInit) + ' MB'
                        memorypool_data[f'Committed {name}'] = usageCommitted
                        memorypool_data[f'Max {name}'] = usageMax
                        memorypool_data[f'Used {name}'] = usageUsed

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
                        'Connectors':{
                            'order':1,
                            'tablist':[
                                'Connectors'
                            ]
                        },
                        'JVM CodeHeap Usage': {
                            'order': 2,
                            'tablist': [
                                "Committed CodeHeap_'non-nmethods'",
                                "Used CodeHeap_'non-nmethods'",
                                "Committed CodeHeap_'non-profiled_nmethods'",
                                "Used CodeHeap_'non-profiled_nmethods'",
                                "Committed CodeHeap_'profiled_nmethods'",
                                "Used CodeHeap_'profiled_nmethods'"
                            ]
                        },
                        'JVM Memory Pool Usage': {
                            'order': 3,
                            'tablist': [
                                "Committed Compressed_Class_Space",
                                "Used Compressed_Class_Space",
                                "Committed G1_Eden_Space",
                                "Used G1_Eden_Space",
                                "Committed G1_Old_Gen",
                                "Used G1_Old_Gen",
                                "Committed G1_Survivor_Space",
                                "Used G1_Survivor_Space",
                                "Committed Metaspace",
                                "Used Metaspace"
                            ]
                        }
                    }
                else:
                    data['msg'] = 'Unable to collect data for the server'
        else:
            data['msg'] = serverinfoData
            data['status'] = 0

        applog = {}
        if self.logs_enabled in ['True', 'true', '1']:
            applog["logs_enabled"] = True
            applog["log_type_name"] = self.log_type_name
            applog["log_file_path"] = self.log_file_path
        else:
            applog["logs_enabled"] = False
        data['applog'] = applog

        data['units'] = METRICS_UNITS
        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help="Host Name", nargs='?', default=TOMCAT_HOST)
    parser.add_argument('--port', help="Port", nargs='?', default=TOMCAT_PORT)
    parser.add_argument('--protocol', help="Protocol (http or https)", default=TOMCAT_PROTOCOL)
    parser.add_argument('--username', help="Username", default=TOMCAT_USERNAME)
    parser.add_argument('--password', help="Password", default=TOMCAT_PASSWORD)
    parser.add_argument('--verify_ssl', help="Verify SSL Certificate (true or false)", default=TOMCAT_VERIFY_SSL)
    parser.add_argument('--plugin_version', help="plugin_version", default=PLUGIN_VERSION)
    parser.add_argument('--url', help="URL", default=TOMCAT_URL)
    parser.add_argument('--logs_enabled', help="logs_enabled", default=LOGS_ENABLED)
    parser.add_argument('--log_type_name', help="log_type_name", default=LOG_TYPE_NAME)
    parser.add_argument('--log_file_path', help="log_file_path", default=LOG_FILE_PATH)

    args = parser.parse_args()

    configurations = {
        'host': args.host,
        'port': args.port,
        'protocol': args.protocol,
        'username': args.username,
        'password': args.password,
        'verify_ssl': args.verify_ssl,
        'url': args.url,
        'plugin_version': args.plugin_version,
        'logs_enabled': args.logs_enabled,
        'log_type_name': args.log_type_name,
        'log_file_path': args.log_file_path
    }

    tomcat_plugins = Tomcat(configurations)
    result = tomcat_plugins.metricCollector()
    print(json.dumps(result, indent=4, sort_keys=True))
