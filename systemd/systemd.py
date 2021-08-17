#!/usr/bin/python


import json
import sys
import argparse
import subprocess


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# to store the final result value and upload to client
result_json = {}


METRIC_UNITS = {
    "total_unit" : "Unit",
    "loaded_unit" : "Unit",
    "active_unit" : "Unit",
    "failed_unit" : "Unit",
    "inactive_unit" : "Unit",
    "deactivating_unit" : "Unit",
    "activating_unit" : "Unit",
    "monitored_unit" : "Unit",
    "systemd_version" : "",
    "systemd_uptime" : "",
}


# Dictionary to store the command to get the value of the metrics
cmd_dictionary = {
    "total_unit" : "systemctl --all | grep -i 'loaded units listed'",
    "loaded_unit" : "systemctl --state loaded list-units | grep -i 'loaded units listed'",
    "active_unit" : "systemctl --state active | grep -i 'loaded units listed'",
    "failed_unit" : "systemctl --state failed | grep -i 'loaded units listed'",
    "inactive_unit" : "systemctl --state inactive | grep -i 'loaded units listed'",
    "deactivating_unit" : "systemctl --state deactivating | grep -i 'loaded units listed'",
    "activating_unit" : "systemctl --state activating | grep -i 'loaded units listed'",
    "monitored_unit" : "systemctl --state monitored | grep -i 'loaded units listed'",
    "systemd_version" : "systemctl --version | grep -i 'systemd'",
    "systemd_uptime" : "systemctl status colord | grep -Po '.*; \K(.*)(?: ago)'",
    #"system_health" : "systemctl --version | grep -i 'systemd'",
}

  
# Execute the linux command and retrive the value for the metrics  
def get_output(command):
    try:
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        output = proc.communicate()[0]
        output = output.strip()
        output = output.decode("utf-8")
    except Exception as e:
        output = str(e)
        return output  
        
    if " loaded units listed." in output:
        output = output.strip(" loaded units listed.")
    elif "systemd " in output:
        output = output[13:29]
        
    return output                       
                   
            
if __name__ == '__main__':
    
    for each in cmd_dictionary:
    	result_json[each] = get_output(cmd_dictionary[each])
    
    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS
    
    print(json.dumps(result_json, indent=4, sort_keys=True))
