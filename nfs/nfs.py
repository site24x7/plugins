#!/usr/bin/python3
import json
import subprocess
import re

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={
    "Disk Usage":"%",
    "Total Size":"mb",
    "Used Size":"mb",
    "Avail Size":"mb",
}

class nfs:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.mount_path=args.mount_path

        
    def execute_cmd(self, command):
        result=subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result
    
    def gb_to_mb(self, val):
        return float(val)*1000
    
    def basic_metrics(self, result):

        subdata={}
        if result.returncode == 0 :
            output=result.stdout.decode()
            data=output.split("\n")[1].split()
            ipaddress=None
            shared_path=None
            
            if ":" in data[0]:
                ipaddress, shared_path = data[0].split(":")
            Total_Size, Used_Size, Avail_Size =data[1:4]
            percent_used=data[4].strip("%")

            if Total_Size[-1]=="G":Total_Size=self.gb_to_mb(Total_Size[:-1])
            if Used_Size[-1]=="G":Used_Size=self.gb_to_mb(Used_Size[:-1])
            if Avail_Size[-1]=="G":Avail_Size=self.gb_to_mb(Avail_Size[:-1])


            subdata['Server IP Address']=ipaddress
            subdata['Shared Directory']=shared_path
            subdata['Disk Usage']=percent_used
            subdata['Total Size']=Total_Size
            subdata['Used Size']=Used_Size
            subdata['Avail Size']=Avail_Size

        else:
            subdata['msg']=result.stderr
            subdata['status']=0
        return subdata
    

    def advance_metrics(self,result, ipaddress):

        subdata={}
        if result.returncode==0:

            pattern = re.compile(rf".*{ipaddress}.*", re.MULTILINE)
            ip_matches = pattern.findall(result.stdout.decode())            
            for match in ip_matches:
                pattern = re.compile(rf".*{self.mount_path}.*", re.MULTILINE)
                ip_match = pattern.findall(match)   
                if ip_match:
                    break 

            ip_match=ip_match[0]
            pattern = re.compile(rf"\(.*addr={ipaddress}\)", re.MULTILINE)
            mount_match=pattern.findall(ip_match)
            if mount_match:
                mount_match=mount_match[0].strip("(,)")
            
            mount_data=mount_match.split(",")
            subdata['Mount Permission']=mount_data[0]
            subdata['NFS Version']=mount_data[2].split("=")[1]

        else:
            subdata['msg']=result.stderr
            subdata['status']=0
        return subdata
    

    def metriccollector(self):

        try:
            self.maindata['Mount Point']=self.mount_path
            nfs_cmd_1=["df", "-hP", self.mount_path]
            result=self.execute_cmd(nfs_cmd_1)
            basic_data=self.basic_metrics(result)
            self.maindata.update(basic_data)
            if "status" in self.maindata:
                if self.maindata['status']==0:
                    return self.maindata

            nfs_cmd_2=["mount"]
            result=self.execute_cmd(nfs_cmd_2)
            advance_data=self.advance_metrics(result, self.maindata['Server IP Address'])
            self.maindata.update(advance_data)
            if "status" in self.maindata:
                if self.maindata['status']==0:
                    return self.maindata
                
        except Exception as e:
            self.maindata['status']=0
            self.maindata['msg']=str(e)
                    
        return self.maindata


if __name__=="__main__":
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--mount_path', help='mount_path', nargs='?', default="/mnt/backups")
    args=parser.parse_args()

    obj=nfs(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
