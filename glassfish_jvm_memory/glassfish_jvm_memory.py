#!/usr/bin/python

import json
import urllib2

###
### Plugin to monitor JVM memory details in a Glasfish Server
### 
### It uses the inbuilt Glassfish monitoring options to get the monitoring data.
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server


### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu

### 
### Steps to configure Glassfish Server to enable monitoring for Site24x7
### To enable monitoring follow the below steps
### 
### Goto <Glassfish-Installation-dir>/bin
### execute the asadmin  
### ./asadmin
### set server.monitoring-service.module-monitoring-levels.jvm=LOW

# Change the Glassfish server details
HOST = "localhost"
ADMINPORT = "1012"
USERNAME = None
PASSWORD = None

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

### Attribute Names
KEYS = {'usednonheapsize-count': 'usednonheapsize', # Amount of used non-heap memory in bytes
        'maxheapsize-count':'maxheapsize',# Maximum amount of heap memory in bytes that can be used for memory management
        'initheapsize-count':'initheapsize', # Amount of heap memory in bytes that the JVM initially requests from OS for memory management
        'initnonheapsize-count':'initnonheapsize', # Amount of non-heap memory in bytes that the JVM initially requests from OS for memory management
        'usedheapsize-count':'usedheapsize', # Amount of used heap memory in bytes
        'committednonheapsize-count':'committednonheapsize', # Amount of non-heap memory in bytes that is committed for the JVM to use
        'objectpendingfinalizationcount-count':'objectpendingfinalizationcount', # Approximate number of objects for which finalization is pending
        'maxnonheapsize-count':'maxnonheapsize', # Maximum amount of non-heap memory in bytes that can be used for memory management
        'committedheapsize-count':'committedheapsize', # Amount of heap memory in bytes that is committed for the JVM to use     
}

### Attribute Units
UNITS = {'usednonheapsize':'MB',
         'maxheapsize':'MB',
         'initheapsize':'MB',
         'initnonheapsize':'MB',
         'usedheapsize':'MB',
         'committednonheapsize':'MB',
         'maxnonheapsize':'MB',
         'committedheapsize':'MB',
}

class Glassfish():
    def __init__(self):
        self.data = {}
        self.data['plugin_version'] = PLUGIN_VERSION
        self.data['heartbeat_required'] = HEARTBEAT
        self.url = "http://"+HOST+":"+ADMINPORT+"/monitoring/domain/server/jvm/memory.json"
        
    def getData(self):
        try:
            ### Create Authentication Handler for the HTTP Request
            pwdmgr = urllib2.HTTPPasswordMgr()
            pwdmgr.add_password(None, self.url, USERNAME, PASSWORD)
            auth = urllib2.HTTPBasicAuthHandler(pwdmgr)
            
            ### Create Proxy Handler for the HTTP Request
            proxy = urllib2.ProxyHandler({}) # Uses NO Proxy
            
            ### Create a HTTP Request with the authentication and proxy handlers
            opener = urllib2.build_opener(proxy, auth)
            urllib2.install_opener(opener)
            
            ### Get HTTP Response
            response = urllib2.urlopen(self.url, timeout=10)
            
            ### Parse the response data
            if response.getcode() == 200:
                bytedata = response.read()
                output = bytedata.decode('UTF-8')
                self.data = self.parseData(output)
                self.data['units'] = UNITS
            else:
                self.data['msg'] = str(response.getcode())
        
        except Exception as e:
            self.data['msg'] = str(e)
        
        return self.data
    
    ### Parse Glassfish Server Memory Data
    def parseData(self, output):
        try:
            line = json.loads(output)
            
            if line['exit_code'] == 'SUCCESS' : 
                elements = line['extraProperties']
                elements = elements['entity']
                
                if elements : 
                    for key,value in elements.iteritems():
                        if key in KEYS.keys(): 
                            
                            if 'count' in value : 
                                ### Convert bytes to MB
                                if value['unit'] == 'bytes' :
                                    value['count'] = int(value['count']) / float(1024*1024)
                                self.data[KEYS[key]] = round(value['count'],2)
                else : self.data['msg'] = "Enable Monitoring"
            else : 
                self.data['msg'] = 'Execution Failure' 
                    
        except Exception as e:
            self.data['msg'] = str(e) 
        
        return self.data
    
if __name__ == '__main__':
    glassfish = Glassfish()
    result = glassfish.getData()
    print(json.dumps(result, indent=4, sort_keys=True))