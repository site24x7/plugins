#!/usr/bin/python

import subprocess,sys,json

METRIC_UNITS={'Available_Updates':'count','Security_Updates':'count'}
PLUGIN_VERSION="1"
HEARTBEAT="true"

class datacollector:
    def __init__(self):
        self.data={}
        self.data['plugin_version']=PLUGIN_VERSION
        self.data['heartbeat_required']=HEARTBEAT
    def metricCollector(self):
        try:
            self.updates=subprocess.check_output("yum check-update | wc -l",shell=True)
            self.security=subprocess.check_output("yum list-security |wc -l",shell=True)
            self.data["Available_Updates"]=int(self.updates)
            self.data["Security_Updates"]=int(self.security)
        except Exception as e:
            self.data["status"]=0
            self.data["msg"]=str(e)
        self.data['units']=METRIC_UNITS
        
        return self.data

if __name__=="__main__":
    update=datacollector()
    result=update.metricCollector()
    print(json.dumps(result,indent=4,sort_keys=True))
