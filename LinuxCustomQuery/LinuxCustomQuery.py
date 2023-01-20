#!/usr/bin/python3
import json
import subprocess
import re

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}

class lcq:

    def __init__(self,args):

        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.cmd=args.cmd
        self.regex=args.regex
        self.displayname=args.displayname

    def metriccollector(self):
        
        ps = subprocess.Popen(self.cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ps.communicate()[0].decode('utf-8').strip()
        if self.regex!=None:
            data=re.findall(self.regex,output)[0]
        else:
            data=output

        self.maindata[self.displayname]=data

        return self.maindata
                                             

if __name__=="__main__":

    cmd="grep -c ^processor /proc/cpuinfo"
    displayname="cpu_cores"
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--cmd', help='enter command for metrics',default=cmd)
    parser.add_argument('--regex',help='enter regex to get filter the output', default=None)
    parser.add_argument('--displayname',help='metric names comma separated',default=displayname)
    args=parser.parse_args()
    
    obj=lcq(args)
    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
