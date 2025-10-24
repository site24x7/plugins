#!/usr/bin/python3
import json
import os
import sys
import time

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

plugin_rs = {}
metric_units = {
    'ping': 'ms',
    'download': 'Mbps',
    'upload': 'Mbps',
    'latency': 'ms',
    'packet_loss': '%',
    'bytes_sent': 'MB',
    'bytes_received': 'MB'
}
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
    best = s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    results_dict = s.results.dict()

    plugin_rs["upload"] = round((results_dict["upload"] / 1024) / 1024, 2)
    plugin_rs["download"] = round((results_dict["download"] / 1024) / 1024, 2)
    plugin_rs["ping"] = results_dict["ping"]

    plugin_rs["server_name"] = best.get("name", "-")
    plugin_rs["server_country"] = best.get("country", "-")
    plugin_rs["latency"] = round(best.get("latency", 0), 2)
    plugin_rs["packet_loss"] = results_dict.get("packetLoss", 0)
    plugin_rs["isp"] = results_dict.get("client", {}).get("isp", "-")
    plugin_rs["client_ip"] = results_dict.get("client", {}).get("ip", "-")
    
    speedtest_timestamp = results_dict.get("timestamp", "")
    if speedtest_timestamp:
        try:
            from datetime import datetime
            parsed_time = datetime.fromisoformat(speedtest_timestamp.replace('Z', '+00:00'))
            plugin_rs["timestamp"] = parsed_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            plugin_rs["timestamp"] = "-"
            plugin_rs['msg'] = str(e)

    else:
        plugin_rs["timestamp"] = "-"
    
    plugin_rs["bytes_sent"] = round(results_dict.get("bytes_sent", 0) / (1024 * 1024), 2)
    plugin_rs["bytes_received"] = round(results_dict.get("bytes_received", 0) / (1024 * 1024), 2)

    plugin_rs['units'] = metric_units

except Exception as e:
    error_msg = str(e)
    if "403" in error_msg or "Forbidden" in error_msg:
        plugin_rs["upload"] = 0
        plugin_rs["download"] = 0
        plugin_rs["ping"] = 0
        plugin_rs["server_name"] = "-"
        plugin_rs["server_country"] = "-"
        plugin_rs["latency"] = 0
        plugin_rs["packet_loss"] = 0
        plugin_rs["isp"] = "-"
        plugin_rs["client_ip"] = "-"
        plugin_rs["timestamp"] = "-"
        plugin_rs["bytes_sent"] = 0
        plugin_rs["bytes_received"] = 0
        plugin_rs['units'] = metric_units
        plugin_rs['msg'] = error_msg
    else:
        plugin_rs['status'] = 0
        plugin_rs['msg'] = error_msg

print(json.dumps(plugin_rs))
