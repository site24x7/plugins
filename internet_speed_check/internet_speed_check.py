#!/usr/bin/python
import os
import json
import sys

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

try:
    import speedtest
except Exception as e:
    python_command = "python" 
    if sys.version_info[0] == 3:
        python_command = "python3" if platform.system() != "Windows" else "python"

    if platform.system() != "Windows":
        returnVal = os.system(f'{python_command} -m pip install --upgrade pip speedtest-cli >/dev/null 2>&1')
    else:
        returnVal = os.system(f'{python_command} -m pip install --upgrade pip speedtest-cli >NUL 2>&1')
    
    import speedtest

plugin_rs = {}
metric_units = {'ping':'ms','download':'Mbps','upload':'Mbps'}
plugin_rs['plugin_version'] = PLUGIN_VERSION
plugin_rs['heartbeat_required'] = HEARTBEAT

try:
    threads = None
    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    results_dict = s.results.dict()
    plugin_rs["upload"] = round((results_dict["upload"]/1024)/1024)
    plugin_rs["download"] = round((results_dict["download"]/1024)/1024)
    plugin_rs["ping"] = results_dict["ping"]
    plugin_rs['units'] = metric_units
except Exception as e:
    plugin_rs['status'] = 0
    plugin_rs['msg'] = str(e)

print(json.dumps(plugin_rs))
