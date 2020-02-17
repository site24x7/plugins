#!/usr/bin/python

import json

PLUGIN_VERSION = "1"
HEARTBEAT="true"

FILE_PATH='/var/lib/update-notifier/updates-available'

lines = [line.strip('\n') for line in open(FILE_PATH)]

data={}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required']=HEARTBEAT

for line in lines:
     if 'packages can be updated' in line:
        data['packages_to_be_updated'] = line.split()[0]
     if 'updates are security updates' in line:
        data['security_updates'] = line.split()[0]


print(json.dumps(data,indent=4))
