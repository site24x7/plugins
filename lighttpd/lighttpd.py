#!/usr/bin/python

import json,sys

### This plugin in python monitors the performance metrics of Lighttpd servers

### It uses the inbuilt Lighttpd monitoring options to get the monitoring data.
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server

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
UNITS = {'traffic':'KB','uptime':'seconds'}


PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
    from http.client import InvalidURL
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError
    from httplib import InvalidURL

class Lighttp():
    def __init__(self):
        self.data = {}
        self._userName = USERNAME
        self._userPass = PASSWORD
        self.data['plugin_version'] = PLUGIN_VERSION
        self.data['heartbeat_required'] = HEARTBEAT
        
    def getData(self):
        try:
            if self._userName and self._userPass:
                password_mgr = urlconnection.HTTPPasswordMgrWithDefaultRealm()
                password_mgr.add_password(None, URL, self._userName, self._userPass)
                auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
                opener = urlconnection.build_opener(auth_handler)
                urlconnection.install_opener(opener)
            response = urlconnection.urlopen(URL, timeout=10)
            if response.getcode() == 200:
                byte_responseData = response.read()
                str_responseData = byte_responseData.decode('UTF-8')
                self.data = self.parseData(str_responseData)
                self.data['units'] = UNITS
            else:
                self.data['status'] = 0
                self.data['msg'] = 'Error_code' + str(response.getcode())
        except HTTPError as e:
            self.data['status'] = 0
            self.data['msg'] = 'Error_code : HTTP Error ' + str(e.code)
        except URLError as e:
            self.data['status'] = 0
            self.data['msg'] = 'Error_code : URL Error ' + str(e.reason)
        except InvalidURL as e:
            self.data['status'] = 0
            self.data['msg'] = 'Error_code : Invalid URL'
        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = 'Exception occured in collecting data : ' + str(e)
        
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
