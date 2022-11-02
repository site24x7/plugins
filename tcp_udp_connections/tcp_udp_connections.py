#!/usr/bin/python

import subprocess,json

METRIC_UNITS={'Number_of_TCP_connections':'count','Number_of_UDP_connections':'count'}
PLUGIN_VERSION="1"
HEARTBEAT="true"

class datacollector:
    def __init__(self):
        self.data={}
        self.data['plugin_version']=PLUGIN_VERSION
        self.data['heartbeat_required']=HEARTBEAT
    def metricCollector(self):
        try:
            self.tcp_count=int(subprocess.check_output("netstat -lt | wc -l",shell=True).decode())
            self.udp_count=int(subprocess.check_output("netstat -lu | wc -l",shell=True).decode())
            self.data["Number_of_TCP_connections"]=self.tcp_count
            self.data["Number_of_UDP_connections"]=self.udp_count
        except Exception as e:
            self.data["status"]=0
            self.data["msg"]=str(e)
        self.data['units']=METRIC_UNITS
        
        return self.data

if __name__=="__main__":
    update=datacollector()
    result=update.metricCollector()
    print(json.dumps(result,indent=4,sort_keys=True))

