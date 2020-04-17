#!/usr/bin/python

import json
import platform
import subprocess
import traceback
import os

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

NFS_MOUNT=["/mnt/nfs/var/nfs","/mnt/nfs/home"]

ERROR_MSG=[]

def metricCollector():
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required']=HEARTBEAT

    try:

        PLUGIN_STATUS=1
        for mounts in NFS_MOUNT:
            NFS_COMMAND = ["/opt/site24x7/monagent/plugins/nfs_check.sh",mounts] 
            proc = subprocess.Popen(NFS_COMMAND,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
            top_output = proc.communicate()[0]
            top_output=top_output.strip()
            if '%%' in top_output:
                s=top_output.split('%%')
                data[mounts+'_status']=1
            elif top_output=="-1":
                data[mounts+'_status']=2
                PLUGIN_STATUS=-1
                ERROR_MSG.append(mounts+' is unmounted')
            elif top_output=='-2':
                data[mounts+'_status']=3
                if ERROR_MSG:
                    ERROR_MSG.append('and '+mounts+' - NFS Server Host is not reachable')
                else:
                    ERROR_MSG.append(mounts+'- NFS Server Host is not reachable')
		PLUGIN_STATUS=-1
        if PLUGIN_STATUS==-1:
	     data['status']=0
	if ERROR_MSG:
            data['msg']= " ".join(str(x) for x in ERROR_MSG)
    except Exception as exception:
        traceback.print_exc()
        data['status']=0
        data['msg']=str(exception)
    
    return data


if __name__ == '__main__':
    
    print json.dumps(metricCollector(), indent=4, sort_keys=True)

