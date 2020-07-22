#!/usr/bin/python

import subprocess
import json

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

if __name__ == '__main__':
    cmd = 'mailq | grep -c "^[A-F0-9]"'
    data = {}
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    
    data['mailq_count'] = int(output) 
    data['heartbeat_required'] = HEARTBEAT
    data['plugin_version'] = PLUGIN_VERSION
    print(json.dumps(data, indent=2, sort_keys=False))
    
