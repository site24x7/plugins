#!/usr/bin/python

import sys
import json
import subprocess

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
            import distro 
elif PYTHON_MAJOR_VERSION == 2:
            import platform 
            
os_info = distro.name()
PLUGIN_VERSION = "1"
HEARTBEAT="true"

data={}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required']=HEARTBEAT
data['packages_to_be_updated']=0
data['security_updates']=0

command="yum check-update --security | grep -i 'needed for security'"

def get_command_output(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

if 'CentOS' in os_info or 'Red Hat' in os_info:
        out = get_command_output(command)
        if out:
            out=out.decode()
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
                
elif 'Ubuntu' in os_info  :
    file_path='/var/lib/update-notifier/updates-available'
    lines = [line.strip('\n') for line in open(file_path)]
    for line in lines:
        if line:
            if ( 'packages can be updated' in line ) or ('can be installed immediately' in line ) or ('can be applied immediately' in line):
                data['packages_to_be_updated'] = line.split()[0]
            if ('updates are security updates' in line) or ('updates are standard security updates' in line):
                data['security_updates'] = line.split()[0]
else:
    data['msg']=f"{os_info} not supported"
    data['status']=0
print(json.dumps(data))
