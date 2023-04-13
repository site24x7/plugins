#!/usr/bin/python
"""

Site24x7 Tomcat Plugin

"""
import argparse
import sys
import socket
import xml.etree.ElementTree as ET
from math import log
import json
import os
import traceback

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError


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
    
    def __init__(self,args):
        self.args = args
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password
        self.connector = TOMCAT_CONNECTOR
        self.url = TOMCAT_URL
        self.timeout = TOMCAT_TIMEOUT
        
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
            pwdManager = urlconnection.HTTPPasswordMgrWithDefaultRealm()
            pwdManager.add_password(None,tomcatUrl,user,password)
            authHandler = urlconnection.HTTPBasicAuthHandler(pwdManager)
            opener=urlconnection.build_opener(authHandler)
            urlconnection.install_opener(opener)
            req = urlconnection.Request(tomcatUrl)
            handle = urlconnection.urlopen(req, None)
            data = handle.read()
        except HTTPError as e:
            if(e.code==401):
                data="ERROR: Unauthorized user. Does not have permissions. %s" %(e)
            elif(e.code==403):
                data="ERROR: Forbidden, yours credentials are not correct. %s" %(e)
            else:
                data="ERROR: The server couldn\'t fulfill the request. %s" %(e)
            error=True
        except URLError as e:
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
            serverinfo = serverinfoData.decode("utf-8").splitlines()
            tomcatVersionStr = (serverinfo[1].split(":"))[1]
            tomcatStatusStr = serverinfo[0]
            tomcatVersion = (tomcatVersionStr.split("/"))[1].split(".")[0]
            if (tomcatVersion.isdigit()):
                data['Tomcat Version']=tomcatVersion
            if(tomcatStatusStr.split(' ')[0]=='OK'):
                data['status']=1
            else:
                data['status']=0
            xmlTreeData,xmlError = self.readXmlFromUrl(self.host,self.port,self.url,self.username,self.password)
            if (xmlError!=True):
                if (xmlTreeData!=None):
                    if data['status']==0:
                        if xmlTreeData.tag=='status':   
                            data['status']=1
                    for connector in xmlTreeData.findall('./connector'):
                        name=str(connector.get('name'))
                        name=name.replace("\"", "")
                        if name==self.connector:
                            thread = connector.find('./threadInfo')
                            request = connector.find('./requestInfo')
                            data['Name']=name
                            data['Thread Count']=int(thread.get('currentThreadCount'))     
                            data['Thread Busy']=int(thread.get('currentThreadsBusy'))       
                            data['Thread Allowed']=float(thread.get('maxThreads'))       
                            data['Bytes Received']=convertBytesToMB(float(request.get('bytesReceived')))       
                            data['Bytes Sent']=convertBytesToMB(float(request.get('bytesSent')))       
                            data['Error Count']=float(request.get('errorCount'))       
                            data['Processing Time']=float(request.get('processingTime'))       
                            data['Request Count']=float(request.get('requestCount'))       
                else:
                    data['msg']='Unable to collect data for the server'    
        else:
            data['msg']=serverinfoData 
            data['status']=0    
        data['units'] = METRICS_UNITS   
        return data


if __name__ == "__main__":

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= TOMCAT_HOST)
    parser.add_argument('--port',help="Port",nargs='?', default= TOMCAT_PORT)
    parser.add_argument('--username',help="username", default= TOMCAT_USERNAME)
    parser.add_argument('--password',help="Password", default= TOMCAT_PASSWORD)
    args=parser.parse_args()

    tomcat_plugins = Tomcat(args)
    
    result = tomcat_plugins.metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
