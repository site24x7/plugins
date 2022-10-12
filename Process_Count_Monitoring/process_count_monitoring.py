#!/usr/bin/python3
import json
import subprocess


PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class appname:

    def __init__(self,user):
        
        self.maindata={}
        self.user=user
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS


    
    def metriccollector(self):

        try:
            ps=subprocess.run(['ps', 'h', '-Lu',self.user],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            query=subprocess.run(["wc",'-l'],input=ps.stdout,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            self.maindata[f"Process Count( User : {self.user}) "]=int(query.stdout.decode().replace("\n",""))


          
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0  
        
        return self.maindata




if __name__=="__main__":

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--user_name",help="Name of the user",default="root")
    args=parser.parse_args()

    user=args.user_name
    obj=appname(user)


    result=obj.metriccollector()
    print(json.dumps(result,indent=True))