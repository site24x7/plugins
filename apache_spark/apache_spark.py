#!/usr/bin/python3
import json
import requests
import argparse

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {
    "Executormetrics Majorgccount": "count",
    "Executormetrics Majorgctime": "s",
    "Executormetrics Minorgccount": "count",
    "Executormetrics Minorgctime": "s",
    "Executormetrics Totalgctime": "s",
    "Jvmcpu Jvmcputime": "s",
    "Executor Cputime": "s",
    "Executor Deserializecputime": "s",
    "Executor Deserializetime": "s",
    "Executor Resultserializationtime": "s",
    "Executor Shufflefetchwaittime": "s",
    "Executor Shufflemergedremotereqsduration": "s",
    "Executor Shufflerecordswritten": "s",
    "Executor Shuffleremotereqsduration": "s",
    "Executor Shufflewritetime": "s",
    "Blockmanager Disk Diskspaceused_Mb": "MB",
    "Blockmanager Memory Maxmem_Mb": "MB",
    "Blockmanager Memory Maxoffheapmem_Mb": "MB",
    "Blockmanager Memory Maxonheapmem_Mb": "MB",
    "Blockmanager Memory Memused_Mb": "MB",
    "Blockmanager Memory Offheapmemused_Mb": "MB",
    "Blockmanager Memory Onheapmemused_Mb": "MB",
    "Blockmanager Memory Remainingmem_Mb": "MB",
    "Blockmanager Memory Remainingoffheapmem_Mb": "MB",
    "Blockmanager Memory Remainingonheapmem_Mb": "MB",
    "Executormetrics Directpoolmemory": "bytes",
    "Executormetrics Jvmheapmemory": "bytes",
    "Executormetrics Jvmoffheapmemory": "bytes",
    "Executormetrics Mappedpoolmemory": "bytes",
    "Executormetrics Offheapexecutionmemory": "bytes",
    "Executormetrics Offheapstoragememory": "bytes",
    "Executormetrics Offheapunifiedmemory": "bytes",
    "Executormetrics Onheapexecutionmemory": "bytes",
    "Executormetrics Onheapstoragememory": "bytes",
    "Executormetrics Onheapunifiedmemory": "bytes",
    "Executor Filesystem File Read_Bytes": "bytes",
    "Executor Filesystem File Write_Bytes": "bytes",
    "Executor Filesystem Hdfs Read_Bytes": "bytes",
    "Executor Filesystem Hdfs Write_Bytes": "bytes",
    "Executor Bytesread": "bytes",
    "Executor Byteswritten": "bytes",
    "Executor Diskbytesspilled": "bytes",
    "Executor Memorybytesspilled": "bytes",
    "Executor Shufflebyteswritten": "bytes",
    "Executor Shufflelocalbytesread": "bytes",
    "Executor Shufflemergedlocalbytesread": "bytes",
    "Executor Shufflemergedremotebytesread": "bytes",
    "Executor Shuffletotalbytesread": "bytes",
    "Executor Shuffleremotebytesread": "bytes"
}

tabs={
  "Blockmanager Memory": {
    "order": 1,
    "tablist": [
      "Blockmanager Disk Diskspaceused_Mb",
      "Blockmanager Memory Maxmem_Mb",
      "Blockmanager Memory Maxoffheapmem_Mb",
      "Blockmanager Memory Maxonheapmem_Mb",
      "Blockmanager Memory Memused_Mb",
      "Blockmanager Memory Offheapmemused_Mb",
      "Blockmanager Memory Onheapmemused_Mb",
      "Blockmanager Memory Remainingmem_Mb",
      "Blockmanager Memory Remainingoffheapmem_Mb",
      "Blockmanager Memory Remainingonheapmem_Mb"
    ]
  },
  "Dagscheduler and Live listener bus": {
    "order": 2,
    "tablist": [
      "Dagscheduler Job Activejobs",
      "Dagscheduler Job Alljobs",
      "Dagscheduler Stage Failedstages",
      "Dagscheduler Stage Runningstages",
      "Dagscheduler Stage Waitingstages",
      "Livelistenerbus Numeventsposted",
      "Livelistenerbus Queue Appstatus Numdroppedevents",
      "Livelistenerbus Queue Executormanagement Numdroppedevents",
      "Livelistenerbus Queue Shared Numdroppedevents",
      "Livelistenerbus Queue Appstatus Size",
      "Livelistenerbus Queue Executormanagement Size",
      "Livelistenerbus Queue Shared Size"
    ]
  },
  "Executor Metrics": {
    "order": 3,
    "tablist": [
      "Executormetrics Directpoolmemory",
      "Executormetrics Jvmheapmemory",
      "Executormetrics Jvmoffheapmemory",
      "Executormetrics Majorgccount",
      "Executormetrics Majorgctime",
      "Executormetrics Mappedpoolmemory",
      "Executormetrics Minorgccount",
      "Executormetrics Minorgctime",
      "Executormetrics Offheapexecutionmemory",
      "Executormetrics Offheapstoragememory",
      "Executormetrics Offheapunifiedmemory",
      "Executormetrics Onheapexecutionmemory",
      "Executormetrics Onheapstoragememory",
      "Executormetrics Onheapunifiedmemory",
      "Executormetrics Processtreejvmrssmemory",
      "Executormetrics Processtreejvmvmemory",
      "Executormetrics Processtreeotherrssmemory",
      "Executormetrics Processtreeothervmemory",
      "Executormetrics Processtreepythonrssmemory",
      "Executormetrics Processtreepythonvmemory",
      "Executormetrics Totalgctime"
    ]
  },
  "Executor Filesystem and Threadpool Status": {
    "order": 4,
    "tablist": [
      "Executor Filesystem File Largeread_Ops",
      "Executor Filesystem File Read_Bytes",
      "Executor Filesystem File Read_Ops",
      "Executor Filesystem File Write_Bytes",
      "Executor Filesystem File Write_Ops",
      "Executor Filesystem Hdfs Largeread_Ops",
      "Executor Filesystem Hdfs Read_Bytes",
      "Executor Filesystem Hdfs Read_Ops",
      "Executor Filesystem Hdfs Write_Bytes",
      "Executor Filesystem Hdfs Write_Ops",
      "Executor Threadpool Activetasks",
      "Executor Threadpool Completetasks",
      "Executor Threadpool Currentpool_Size",
      "Executor Threadpool Maxpool_Size",
      "Executor Threadpool Startedtasks"
    ]
  },
  "Executor Shuffle and Hive external catalog": {
    "order": 5,
    "tablist": [
    "Hiveexternalcatalog Filecachehits",
    "Hiveexternalcatalog Filesdiscovered",
    "Hiveexternalcatalog Hiveclientcalls",
    "Hiveexternalcatalog Parallellistingjobcount",
    "Hiveexternalcatalog Partitionsfetched",
    "Executor Shufflebyteswritten",
    "Executor Shufflecorruptmergedblockchunks",
    "Executor Shufflefetchwaittime",
    "Executor Shufflelocalblocksfetched",
    "Executor Shufflelocalbytesread",
    "Executor Shufflemergedfetchfallbackcount",
    "Executor Shufflemergedlocalblocksfetched",
    "Executor Shufflemergedlocalbytesread",
    "Executor Shufflemergedlocalchunksfetched",
    "Executor Shufflemergedremoteblocksfetched",
    "Executor Shufflemergedremotebytesread",
    "Executor Shufflemergedremotechunksfetched",
    "Executor Shufflemergedremotereqsduration",
    "Executor Shufflerecordsread",
    "Executor Shufflerecordswritten",
    "Executor Shuffleremoteblocksfetched",
    "Executor Shuffleremotebytesread",
    "Executor Shuffleremotebytesreadtodisk",
    "Executor Shuffleremotereqsduration",
    "Executor Shuffletotalbytesread",
    "Executor Shufflewritetime"
    ]
  }
}

class SparkServerMetrics:
    
    def __init__(self, hostname, port):
        self.maindata = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
            'tabs':tabs,
            'units': METRICS_UNITS
        }
        self.units = METRICS_UNITS
        self.url = f"http://{hostname}:{port}/metrics/json"
        self.fetch_metrics()

    
    def fetch_metrics(self):
        try:
            response = requests.get(self.url)
            metrics_json = response.json()
            self.parse_metrics(metrics_json)
        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0

    def parse_metrics(self, metrics_json):
        for key, value in metrics_json.get("gauges", {}).items():
            formatted_key = self.format_key(key).replace("."," ").title()
            if "time" in formatted_key:
                self.maindata[formatted_key] = self.ms_to_s(value['value'])
            else:
                self.maindata[formatted_key] = value['value']
        
        for key, value in metrics_json.get("counters", {}).items():
            formatted_key = self.format_key(key).replace("."," ").title()
            if "time" in formatted_key:
                self.maindata[formatted_key] = self.ms_to_s(value['count'])
            else:
                self.maindata[formatted_key] = value['count']

    def format_key(self, key):
        parts = key.split('.')
        if len(parts) > 1:
            return '.'.join(parts[2:]) 
        return key
    
    def ms_to_s(self, value):
        return round(value/1000,2)

    def get_metrics(self):
        return self.maindata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Spark Server Metrics")
    parser.add_argument('--hostname', type=str, default="localhost", help="Hostname of the Spark server")
    parser.add_argument('--port', type=int, default=4040, help="Port number of the Spark server")
    
    args = parser.parse_args()

    metrics = SparkServerMetrics(args.hostname, args.port)
    
    
    print(json.dumps(metrics.get_metrics()))
