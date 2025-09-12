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
    plugin_script_path = os.path.dirname(os.path.realpath(__file__))
    
    try:
        import zipimport
        importer = zipimport.zipimporter(plugin_script_path + "/speedtest-cli.pyz")
        speedtest = importer.load_module("speedtest")
    except:
        plugin_rs['status'] = 0
        plugin_rs['msg'] = 'speedtest module not installed'
        print(json.dumps(plugin_rs))
        sys.exit(1)

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
