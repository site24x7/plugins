#!/usr/bin/python3
import json
import os
import sys

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

plugin_rs = {}
metric_units = {'ping': 'ms', 'download': 'Mbps', 'upload': 'Mbps'}
plugin_rs['plugin_version'] = PLUGIN_VERSION
plugin_rs['heartbeat_required'] = HEARTBEAT

try:
    # Specify the path to the .pyz file
    speedtest_pyz_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "speedtest-cli.pyz")
    sys.path.insert(0, speedtest_pyz_path)

    # Import the speedtest module
    import speedtest

    threads = None
    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    results_dict = s.results.dict()

    plugin_rs["upload"] = round((results_dict["upload"] / 1024) / 1024, 2)
    plugin_rs["download"] = round((results_dict["download"] / 1024) / 1024, 2)
    plugin_rs["ping"] = results_dict["ping"]
    plugin_rs['units'] = metric_units

except Exception as e:
    plugin_rs['status'] = 0
    plugin_rs['msg'] = str(e)

print(json.dumps(plugin_rs))
