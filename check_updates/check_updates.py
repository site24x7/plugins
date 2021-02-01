#!/usr/bin/python

import json
import platform
import subprocess

PLUGIN_VERSION = "1"
HEARTBEAT="true"

data={}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required']=HEARTBEAT

commands = {'packages_to_be_updated':'yum updateinfo list available | wc -l','security_updates':'yum updateinfo list security all | wc -l'}

os_info = platform.linux_distribution()[0].lower()

def get_command_output(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

if 'centos' in os_info or 'red hat' in os_info:
    for each_cmd,each_val in commands.items():
        out = get_command_output(each_val)
        if out:
            out = out.rstrip()
            out = int(out) - 7
            data[each_cmd] = out
else:
    FILE_PATH='/var/lib/update-notifier/updates-available'
    lines = [line.strip('\n') for line in open(FILE_PATH)]
    for line in lines:
        if 'packages can be updated' in line:
            data['packages_to_be_updated'] = line.split()[0]
        if 'updates are security updates' in line:
            data['security_updates'] = line.split()[0]
print(json.dumps(data))
