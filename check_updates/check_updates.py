#!/usr/bin/python

import json
import platform
import subprocess

PLUGIN_VERSION = "1"
HEARTBEAT="true"

data={}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required']=HEARTBEAT

command="yum check-update --security | grep -i 'needed for security'"

os_info = platform.linux_distribution()[0].lower()

def get_command_output(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

if 'centos' in os_info or 'red hat' in os_info:
        out = get_command_output(command)
        if out:
            out = out.rstrip()
            count = out.split("needed for security")
            security_count = count[0].split()[0]
            if security_count == 'No':
            	data['security_updates'] = 0
            else:
               data['security_updates'] = security_count
            packages_count = count[1].split()
            for each in packages_count:
                 if each.isdigit():
                     data['packages_to_be_updated']=each
                
else:	
    FILE_PATH='/var/lib/update-notifier/updates-available'
    lines = [line.strip('\n') for line in open(FILE_PATH)]
    for line in lines:
        if 'packages can be updated' in line:
            data['packages_to_be_updated'] = line.split()[0]
        if 'updates are security updates' in line:
            data['security_updates'] = line.split()[0]
print(json.dumps(data))
