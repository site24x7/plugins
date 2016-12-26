#!/usr/bin/python
"""

Site24x7 Tomcat Plugin

"""
import argparse
import sys
import urllib2
import socket
import xml.etree.ElementTree as ET
from math import log
import json
import os
import traceback

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
TOMCAT_HOST = 'localhost'

TOMCAT_PORT = '8080'

TOMCAT_USERNAME = 'admin'

TOMCAT_PASSWORD = 'admin'

TOMCAT_URL = '/manager'

TOMCAT_CONNECTOR = 'http-nio-8080'

TOMCAT_TIMEOUT = '5'

METRICS_UNITS = {'bytes_received':'MB',
                 'bytes_sent':'MB',
                 'processing_time':'ms'
                 }

def convertBytesToMB(v):
    try:
        byte_s=float(v)        
        kilobytes=byte_s/1024;        
        megabytes=kilobytes/1024;        
        v=round(megabytes,2)    
    except Exception as e:        
        pass    
    return v

class Tomcat(object):
    
    def __init__(self,config):
        self.configurations = config
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '8080'))
        self.username = self.configurations.get('user')
        self.password = self.configurations.get('password')
        self.connector = self.configurations.get('connector')
        self.url = self.configurations.get('url','/manager')
        self.timeout = int(self.configurations.get('timeout'))
        
    def readXmlFromUrl(self,host,port,url,user,password):
        xmlUrl = url+"/status?XML=true"
        xmlData,xmlError = self.readUrl(host,port,xmlUrl,user,password)
        if(xmlError):
            return xmlData,xmlError
        else:
            try:
                root = ET.fromstring(xmlData)
            except ET.ParseError as e:
                root="ERROR: Unable to read the XML page. Error: %s" %(e)
                xmlError=True
            return root,xmlError
        
    def readUrl(self,host,port,url,user,password):
        error=False
        tomcatUrl = "http://"+host+":"+str(port)+url
        try:
            pwdManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pwdManager.add_password(None,tomcatUrl,user,password)
            authHandler = urllib2.HTTPBasicAuthHandler(pwdManager)
            opener=urllib2.build_opener(authHandler)
            urllib2.install_opener(opener)
            req = urllib2.Request(tomcatUrl)
            handle = urllib2.urlopen(req, None)
            data = handle.read()
        except urllib2.HTTPError as e:
            if(e.code==401):
                data="ERROR: Unauthorized user. Does not have permissions. %s" %(e)
            elif(e.code==403):
                data="ERROR: Forbidden, yours credentials are not correct. %s" %(e)
            else:
                data="ERROR: The server couldn\'t fulfill the request. %s" %(e)
            error=True
        except urllib2.URLError as e:
            data = 'ERROR: We failed to reach a server. Reason: %s' %(e.reason)
            error = True
        except socket.timeout as e:
            data = 'ERROR: Timeout error'
            error = True
        except socket.error as e:
            data = "ERROR: Unable to connect with host "+self.host+":"+self.port
            error = True
        except:
            data = "ERROR: Unexpected error: %s"%(sys.exc_info()[0])
            error = True

        return data,error

        
    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        
        socket.setdefaulttimeout(float(self.timeout))
        serverinfoUrl = self.url+"/serverinfo"
        serverinfoData,serverinfoError = self.readUrl(self.host,self.port,serverinfoUrl,self.username,self.password)
        if serverinfoError:
            serverinfoUrl = self.url+"/text/serverinfo"
            serverinfoData,serverinfoError = self.readUrl(self.host,self.port,serverinfoUrl,self.username,self.password)
        if(serverinfoError==False):
            serverinfo = serverinfoData.splitlines()
            tomcatVersionStr = (serverinfo[1].split(":"))[1]
            tomcatStatusStr = serverinfo[0]
            tomcatVersion = (tomcatVersionStr.split("/"))[1].split(".")[0]
            if (tomcatVersion.isdigit()):
                data['tomcat_version']=tomcatVersion
            if(tomcatStatusStr.split(' ')[0]=='OK'):
                data['tomcat_server_status']=1
            else:
                data['tomcat_server_status']=0
            xmlTreeData,xmlError = self.readXmlFromUrl(self.host,self.port,self.url,self.username,self.password)
            if (xmlError!=True):
                if (xmlTreeData!=None):
                    if data['tomcat_server_status']==0:
                        if xmlTreeData.tag=='status':   
                            data['tomcat_server_status']=1
                    for connector in xmlTreeData.findall('./connector'):
                        name=str(connector.get('name'))
                        name=name.replace("\"", "")
                        if name==self.connector:
                            thread = connector.find('./threadInfo')
                            request = connector.find('./requestInfo')
                            data['name']=name
                            data['thread_count']=int(thread.get('currentThreadCount'))     
                            data['thread_busy']=int(thread.get('currentThreadsBusy'))       
                            data['thread_allowed']=float(thread.get('maxThreads'))       
                            data['bytes_received']=convertBytesToMB(float(request.get('bytesReceived')))       
                            data['bytes_sent']=convertBytesToMB(float(request.get('bytesSent')))       
                            data['error_count']=float(request.get('errorCount'))       
                            data['processing_time']=float(request.get('processingTime'))       
                            data['request_count']=float(request.get('requestCount'))       
                else:
                    data['msg']='Unable to collect data for the server'    
        else:
            data['msg']=serverinfoData 
            data['tomcat_server_status']=0    
        data['units'] = METRICS_UNITS   
        return data


if __name__ == "__main__":

    configurations = {'host': TOMCAT_HOST,'port': TOMCAT_PORT,'user': TOMCAT_USERNAME,'password': TOMCAT_PASSWORD, 'url': TOMCAT_URL, 'connector': TOMCAT_CONNECTOR, 'timeout': TOMCAT_TIMEOUT}

    tomcat_plugins = Tomcat(configurations)
    
    result = tomcat_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
