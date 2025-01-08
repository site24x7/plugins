#!/usr/bin/python

import json
import urllib2

###
### Plugin to monitor JVM Threads in a Glasfish Server
###
### It uses the inbuilt Glassfish monitoring options to get the monitoring data.
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Language : Python
### Tested in Ubuntu

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
KEYS = {'deadlockedthreads': 'deadlockedthreads', # No of threads in deadlock waiting to acquire object monitors or ownable synchronizers
        'totalstartedthreadcount':'totalstartedthreadcount',# No of threads created and also started since the Java virtual machine started
        'daemonthreadcount':'daemonthreadcount', # No of live daemon threads
        'monitordeadlockedthreads':'monitordeadlockedthreads', # number of threads in deadlock waiting to acquire object monitors
        'currentthreadusertime':'currentthreadusertime', # CPU time for a thread executed in user mode
        'peakthreadcount':'peakthreadcount', # the peak live thread count since the Java virtual machine started or peak was reset
        'threadcount':'threadcount', # number of live threads including both daemon and non-daemon threads
        'currentthreadcputime':'currentthreadcputime', # total CPU time for the current thread in nanoseconds       
}

### Attribute Units
UNITS = {'currentthreadusertime':'nanosecond',
         'currentthreadcputime':'nanosecond'
}

class Glassfish():
    def __init__(self):
        self.data = {}
        self.data['plugin_version'] = PLUGIN_VERSION
        self.data['heartbeat_required'] = HEARTBEAT
        self.url = "http://"+HOST+":"+ADMINPORT+"/monitoring/domain/server/jvm/thread-system.json"
        
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
    
    ### Parse Lighttp Server Stats Data
    def parseData(self, output):
        #print output
        try:
            line = json.loads(output)
            
            if line['exit_code'] == 'SUCCESS' : 
                elements = line['extraProperties']
                elements = elements['entity']
                
                if elements : 
                    for key,value in elements.iteritems():
                        if key in KEYS.keys()and 'count' in value :  self.data[KEYS[key]] = value['count']
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