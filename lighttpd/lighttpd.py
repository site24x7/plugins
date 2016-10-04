#!/usr/bin/python

import json
import urllib2

### This plugin in python monitors the performance metrics of Lighttpd servers

### It uses the inbuilt Lighttpd monitoring options to get the monitoring data.
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu

### Configure Lighttpd Server to enable monitoring for Site24x7
### Open Lighttpd confi file.  File location: /etc/lighttpd/lighttpd.conf
### Add "mod_status" to server.modules
### Add status urls if not present  ::: status.status-url="/server-status"
### Restart Lighttpd Server

# Change the Lighttpd stats URL accordingly here. Retain the "?auto" suffix.
URL = "http://localhost:80/server-status?auto"
USERNAME = None
PASSWORD = None

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

### Attribute Names
KEYS = {'Total Accesses':'accesses', # number of requests handled 
        'Total kBytes':'traffic',# overall outgoing traffic
        'Uptime':'uptime', # server uptime
        'BusyServers':'busy_servers', # number of currently active connections
        'IdleServers':'idle_servers' # number of currently inactive connections
}

### Attribute Units
UNITS = {'traffic':'KB',
         'uptime':'seconds'
}

class Lighttp():
    def __init__(self):
        self.data = {}
        self.data['plugin_version'] = PLUGIN_VERSION
        self.data['heartbeat_required'] = HEARTBEAT
        
    def getData(self):
        try:
            ### Create Authentication Handler for the HTTP Request
            pwdmgr = urllib2.HTTPPasswordMgr()
            pwdmgr.add_password(None, URL, USERNAME, PASSWORD)
            auth = urllib2.HTTPBasicAuthHandler(pwdmgr)
            
            ### Create Proxy Handler for the HTTP Request
            proxy = urllib2.ProxyHandler({}) # Uses NO Proxy
            
            ### Create a HTTP Request with the authentication and proxy handlers
            opener = urllib2.build_opener(proxy, auth)
            urllib2.install_opener(opener)
            
            ### Get HTTP Response
            response = urllib2.urlopen(URL, timeout=10)
            
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
        try:
            line = output.split('\n')
            for _ in line:
                value = _.split(':')
                if str(value[0]) in KEYS.keys(): self.data[KEYS[value[0]]] = value[1]
        except Exception as e:
            self.data['msg'] = str(e) 
        
        return self.data
    
if __name__ == '__main__':
    lighttp = Lighttp()
    result = lighttp.getData()
    print(json.dumps(result, indent=4, sort_keys=True))
