#!/usr/bin/python3

import json
import requests
import argparse

PLUGIN_VERSION = 1
HEARTBEAT = True

METRICS_UNITS = {
    "Total Capacity": "bytes",
    "Used Capacity": "bytes",
    "Remaining Capacity": "bytes",
    "Estimated Capacity Lost Total": "bytes",
    "Heap Memory Committed": "bytes",
    "Heap Memory Used": "bytes",
    "Non-Heap Memory Committed": "bytes",
    "Non-Heap Memory Used": "bytes",
    "Total CPU": "%",
    "Total Memory": "bytes",
    "Free Memory": "bytes"
}

class HDFSMonitor:
    def __init__(self,host,port):
        self.maindata = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
            'units': METRICS_UNITS
        }
        self.host = host
        self.port = port

    def metric_collector(self):
        try:
            url = f"http://{self.host}:{self.port}/jmx"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            beans = data.get("beans", [])

            for bean in beans:
                name = bean.get("name")
                if name == "Hadoop:service=NameNode,name=FSNamesystemState":
                    self.maindata["Total Blocks"] = bean.get("BlocksTotal", 0)
                    self.maindata["Total Capacity"] = bean.get("CapacityTotal", 0)
                    self.maindata["Used Capacity"] = bean.get("CapacityUsed", 0)
                    self.maindata["Remaining Capacity"] = bean.get("CapacityRemaining", 0)
                    self.maindata["Estimated Capacity Lost Total"] = bean.get("EstimatedCapacityLostTotal", 0)
                    self.maindata["Total Files"] = bean.get("FilesTotal", 0)
                    self.maindata["Fs Lock Queue Length"] = bean.get("FsLockQueueLength", 0)
                    self.maindata["Maximum Objects"] = bean.get("MaxObjects", 0)
                    self.maindata["Dead Data Nodes"] = bean.get("NumDeadDataNodes", 0)
                    self.maindata["Decommissioning Dead Data Nodes"] = bean.get("NumDecomDeadDataNodes", 0)
                    self.maindata["Decommissioning Live Data Nodes"] = bean.get("NumDecomLiveDataNodes", 0)
                    self.maindata["Total Decommissioning Data Nodes"] = bean.get("NumDecommissioningDataNodes", 0)
                    self.maindata["Total Live Data Nodes"] = bean.get("NumLiveDataNodes", 0)
                    self.maindata["Total Stale Data Nodes"] = bean.get("NumStaleDataNodes", 0)
                    self.maindata["Pending Deletion Blocks"] = bean.get("PendingDeletionBlocks", 0)
                    self.maindata["Pending Replication Blocks"] = bean.get("Pending Replication Blocks", 0)
                    self.maindata["Scheduled Replication Blocks"] = bean.get("ScheduledReplicationBlocks", 0)
                    self.maindata["Under Replicated Blocks"] = bean.get("UnderReplicatedBlocks", 0)
                    self.maindata["Total Load"] = bean.get("TotalLoad", 0)
                    self.maindata["Total Volume Failures"] = bean.get("VolumeFailuresTotal", 0)

                elif name == "Hadoop:service=NameNode,name=FSNamesystem":
                    self.maindata["Corrupted Blocks"] = bean.get("CorruptBlocks", 1)
                    self.maindata["Missing Blocks"] = bean.get("MissingBlocks", 1)

                elif name == "java.lang:type=Memory":
                    heap = bean.get("HeapMemoryUsage", {})
                    non_heap = bean.get("NonHeapMemoryUsage", {})
                    self.maindata["Heap Memory Committed"] = heap.get("committed", 0)
                    self.maindata["Heap Memory Used"] = heap.get("used", 0)
                    self.maindata["Non-Heap Memory Committed"] = non_heap.get("committed", 0)
                    self.maindata["Non-Heap Memory Used"] = non_heap.get("used", 0)

                elif name == "Hadoop:service=NameNode,name=JvmMetrics":
                    self.maindata["Fatal Logs"] = bean.get("LogFatal", 0)
                    self.maindata["Error Logs"] = bean.get("LogError", 0)
                    self.maindata["Warning Logs"] = bean.get("LogWarn", 0)
                    self.maindata["Total Logs Info"] = bean.get("LogInfo", 0)
                    self.maindata["New Threads"] = bean.get("ThreadsNew", 0)
                    self.maindata["Runnable Threads"] = bean.get("ThreadsRunnable", 0)
                    self.maindata["Blocked Threads"] = bean.get("ThreadsBlocked", 0)
                    self.maindata["Waiting Threads"] = bean.get("ThreadsWaiting", 0)
                    self.maindata["Terminated Threads"] = bean.get("ThreadsTerminated", 0)

                elif name == "java.lang:type=OperatingSystem":
                    self.maindata["Total CPU"] = bean.get("SystemCpuLoad", 0) * 100
                    self.maindata["Total Memory"] = bean.get("TotalPhysicalMemorySize", 0)
                    self.maindata["Free Memory"] = bean.get("FreePhysicalMemorySize", 0)

            self.maindata["tabs"] = {
                "Threads": {
                    "order": 1,
                    "tablist": [
                        "New Threads", "Runnable Threads", "Blocked Threads",
                        "Waiting Threads", "Terminated Threads"
                    ]
                },
                "Storage": {
                    "order": 2,
                    "tablist": [
                        "Total Capacity", "Used Capacity", "Remaining Capacity",
                        "Estimated Capacity Lost Total", "Total Volume Failures"
                    ]
                },
                "Blocks": {
                    "order": 3,
                    "tablist": [
                        "Total Blocks", "Total Files", "Corrupted Blocks",
                        "Missing Blocks", "Pending Deletion Blocks",
                        "Pending Replication Blocks", "Scheduled Replication Blocks",
                        "Under Replicated Blocks", "Total Load",
                        "Fs Lock Queue Length", "Maximum Objects"
                    ]
                },
                "DataNode": {
                    "order": 4,
                    "tablist": [
                        "Dead Data Nodes", "Decommissioning Dead Data Nodes",
                        "Decommissioning Live Data Nodes", "Total Decommissioning Data Nodes",
                        "Total Live Data Nodes", "Total Stale Data Nodes"
                    ]
                }
            }

            return self.maindata

        except Exception as e:
            return {
                "plugin_version": PLUGIN_VERSION,
                "heartbeat_required": HEARTBEAT,
                "status": 0,
                "msg": f"Error fetching HDFS metrics: {e}"
            }

def run(param):
    host = param.get("host")
    port = param.get("port")
    obj = HDFSMonitor(host, port)
    return obj.metric_collector()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, help='HDFS host', default="localhost")
    parser.add_argument('--port', required=True, help='HDFS JMX port', default="9870")
    args = parser.parse_args()

    param = {"host": args.host, "port": args.port}
    print(json.dumps(run(param)))
