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
    "mount_point" : "path",
    "nfs_version" : "version",
    "shared_directory" : "path",
    "server_ip_address" : "ip",
    "domain" : "",
    "mount_permission" : ""
}

ERROR_MSG=[]

MOUNT = ""

result = {}

def get_nfs_mount_data (output, ipaddr,count,mpath):
    data = {}

    try:

        output = ' '.join(output.split())
        output = output.split(" ")
        server = output[0].split(ipaddr)
        data['Folder '+count+' Shared Directory'] = server[1]
        data[mpath+' Disk Usage'] = int(output[4].replace('%', ''))
        try:
           data[mpath+' Status'] =1
        except:
           pass
        METRIC_UNITS[mpath + ' Disk Usage'] = "%"

    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)
        #print(e)
        
    return data
    
    
def get_nfs_mount_info (output,count):
    data = {}
    try:
        output = ' '.join(output.split())
        output = output.split(" ")

        for out in output:
            if "vers" in out or "domain" in out:
                out = out.split(",")
                for each in out:

                    if "vers" in each:
                        each = each.split("=")    
                        data['nfs Version'] = str(each[1])

                    if each=="rw":
                        data['Folder '+count+' Mount Permission'] = "read/write"

                    if each=="ro":
                        data['Folder '+count+' Mount Permission'] = "read only"

                    if "addr" in each:
                        each = each.split("=")
                        data['Folder ' +count+' Server IP Address'] = str(each[1])

                    if "domain" in each:
                        each = each.split("=")
                        data['Folder '+count+' Domain'] = str(each[1])
        
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)
        #print(e)
    
    return data


def metricCollector(MOUNT,folder):
    data = {}

    try:

        os.chmod("/opt/site24x7/monagent/plugins/nfs/nfs_check.sh", 0o775)
        proc = subprocess.Popen(['/opt/site24x7/monagent/plugins/nfs/nfs_check.sh ' + MOUNT], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        top_output = proc.communicate()[0]
        top_output=top_output.strip()
        top_output=top_output.decode("utf-8")
        data['Folder '+folder+' Mount Point'] = MOUNT
        
        if "@@@@@@" in top_output:
            output = top_output.split("@@@@@@")
            top_output = output[1]
            output = output[0]
            

        if '%%' in top_output:
            data.update(get_nfs_mount_info(output,folder))
            data.update(get_nfs_mount_data(top_output, data["Folder "+folder+' Server IP Address'],folder,MOUNT))
            data["Folder "+folder+" Status"]= "Mounted"
            data["Folder "+folder+" Status"]= "Mounted"
            
            
        elif '-1' in top_output:
            data["Folder "+folder+" Status"]= "Unmounted"
            data[MOUNT+' Status'] =0

        elif '-2' in top_output:
            data["Folder "+folder+" Status"]= "Server not reachable"
            data[MOUNT+' Status'] =0

    except Exception as e:
        data['status']=0
        data['msg']=str(e)
        #print('1\n',e)
    
    return data


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--mount_folder', help="nfs mount point", type=str)
    
    args = parser.parse_args()
    if args.mount_folder:
        folders = args.mount_folder
        folders=folders.split(",")
    n=1

    for i in folders:
        result_collector = metricCollector(i,str(n))
        n+=1
        result.update(result_collector )
    
    result['plugin_version'] = PLUGIN_VERSION
    result['heartbeat_required']=HEARTBEAT
    result['units'] = METRIC_UNITS
    
    print(json.dumps(result, indent=4, sort_keys=True))
