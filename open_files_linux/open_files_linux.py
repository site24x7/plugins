
### Language : Python
### Tested in Ubuntu

import sys,json
import argparse
#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"


PROC_FILE = "/proc/sys/fs/file-nr"

METRIC_UNITS = {'open_files': 'units', 'total_files': 'units'}

def metricCollector():
    data = {}
    try:
        open_nr, free_nr, max = open(PROC_FILE).readline().split("\t")
        open_files = int(open_nr) - int(free_nr)
        data["open_files"] = int(open_files)
        data["total_files"] = int(max)
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required'] = HEARTBEAT
    except Exception as e:
        data["status"] = 0
        data["msg"] = str(e)
    data["units"] = METRIC_UNITS
    return data
    
def run(param=None):

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", help="host", type=str, default="localhost"
    )
    result = metricCollector()
    return result

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", help="host", type=str, default="localhost"
    )

    result = metricCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
