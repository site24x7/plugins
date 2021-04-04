#!/usr/bin/python3

import json
import platform
import subprocess
import traceback
import os
import argparse

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

METRIC_UNITS = {
    "client_ip_address" : "ip",
    "mount_point" : "path",
    "disk_usage" : "%",
    "nfs_version" : "version",
    "shared_directory" : "path",
    "server_ip_address" : "ip"
}

ERROR_MSG=[]

MOUNT = ""

result = {}

def nfs_details (output):
    data = {}
    try:
        output = ' '.join(output.split())
        output = output.split(" ")
        output[5] = output[5].replace('%%1', '')
        output[5] = output[5].replace('%%0', '')
        server = output[0].split(":")
        data['server_ip_address'] = str(server[0])
        data['shared_directory'] = str(server[1])
        data['mount_point'] = str(output[5])
        data['disk_usage'] = int(output[4].replace('%', ''))
            
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)
        
    return data
    
    
def mount_metrics (output):
    data = {}
    try:
        output = ' '.join(output.split())
        output = output.split(" ")
        for out in output:
            if "vers" in out and "clientaddr" in out:
                out = out.split(",")
                for each in out:
                    if "vers" in each:
                        each = each.split("=")    
                        data['nfs_version'] = str(each[1])
                    if "clientaddr" in each:
                        each = each.split("=")
                        data['client_ip_address'] = str(each[1])
                    if each=="rw":
                        data['mount_permission'] = "read/write"
                    if each=="ro":
                        data['mount_permission'] = "read only"
    
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)
    
    return data


def metricCollector():
    data = {}

    try:

        os.chmod("/opt/site24x7/monagent/plugins/nfs/nfs_check.sh", 0o775)
        proc = subprocess.Popen(['/opt/site24x7/monagent/plugins/nfs/nfs_check.sh ' + MOUNT], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        top_output = proc.communicate()[0]
        top_output=top_output.strip()
        top_output=top_output.decode("utf-8")
        if "@@@@@@" in top_output:
            output = top_output.split("@@@@@@")
            top_output = output[1]
            output = output[0]
        if '%%' in top_output:
            data.update(nfs_details(top_output))
            data.update(mount_metrics(output))
        elif '-1' in top_output:
            data['status']=0
            data['msg']= MOUNT+" is unmounted"
        elif '-2' in top_output:
            data['status']=0
            data['msg']= MOUNT+" - NFS Server Host is not reachable"
    except Exception as e:
        data['status']=0
        data['msg']=str(e)
    
    return data


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--mount_folder', help="nfs mount point", type=str)
    
    args = parser.parse_args()
    if args.mount_folder:
        MOUNT = args.mount_folder
    
    result = metricCollector()
    
    result['plugin_version'] = PLUGIN_VERSION
    result['heartbeat_required']=HEARTBEAT
    result['units'] = METRIC_UNITS
    
    print(json.dumps(result, indent=4, sort_keys=True))
