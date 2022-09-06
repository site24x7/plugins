#!/usr/bin/python3

import json
import subprocess


PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={'download':'mbps','upload':'mbps','bytes sent':'Bytes','bytes received':'Bytes'}


class Speedtestcli:


    def __init__(self):
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS



    def metricCollector(self):
        
        result=subprocess.run(["speedtest-cli",'--json'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        if result.returncode==0:
            result=result.stdout.decode()
            result=json.loads(result)
            self.maindata['download']=(result['download']*0.000000125)
            self.maindata['upload']=(result['upload']*0.000000125)
            self.maindata['ping']=result['ping']
            self.maindata['timestamp']=result['timestamp']
            self.maindata['bytes sent']=result['bytes_sent']
            self.maindata['bytes received']=result['bytes_received']
            self.maindata['share']=result['share']

            for s in result['server']:
                self.maindata["server."+s]=result['server'][s]

            for c in result['client']:
                self.maindata["client."+c]=result['client'][c]
        else:
            self.maindata['msg']=result.stdout.decode()
            self.maindata['status']=0

        return self.maindata
        
                
        
obj=Speedtestcli()
result=obj.metricCollector()
print(json.dumps(result,indent=True))
