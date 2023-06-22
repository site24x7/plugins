#!/usr/bin/python

import gpustat
import json
import subprocess

PLUGIN_VERSION = "1"

HEARTBEAT_REQUIRED = "true"


output = gpustat.new_query()
result_json = {}
for each_line in output:
    result_json["memory"] = str(int(each_line.memory_used))
    result_json["utilization"] = str(int(each_line.utilization))
    result_json["temperature"] = str(int(each_line.temperature))
    result_json["device_name"] = each_line.name.split(" ")

result_json["plugin_version"] = PLUGIN_VERSION

result_json["heartbeat_required"] = HEARTBEAT_REQUIRED


cmd = 'gpustat -cp'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
core_output = output.decode().split('\n')
for each in core_output:
    if each.startswith('['):
        core_out_line = each.split()    
        core_out="core_"+core_out_line[0].replace('[', '').replace(']', '')
        result_json[core_out] = core_out_line[5]

print(json.dumps(result_json))
