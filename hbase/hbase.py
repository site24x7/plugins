#!/usr/bin/python3

import json
import requests

PLUGIN_VERSION = 1
HEARTBEAT = True

METRICS_UNITS = {
    "Rit Oldest Age": "ms",
    "Rit Duration Min": "ms",
    "Rit Duration Max": "ms",
    "Rit Duration Mean": "ms",
    "Rit Duration Median": "ms",
    "Rit Count": "count",
    "Rit Count Over Threshold": "count",
    "IPC Queue Size": "bytes",
    "IPC Calls In General Queue": "count",
    "IPC Calls In Replication Queue": "count",
    "IPC Calls In Priority Queue": "count",
    "IPC Open Connections": "count",
    "IPC Active Handlers": "count",
    "IPC Total Call Time Max": "ms",
    "IPC Total Call Time Mean": "ms",
    "IPC Total Call Time Median": "ms",
    "IPC Total Call Time 99th Percentile": "ms",
    "Regions Servers": "count",
    "Dead Region Servers": "count",
    "Mem Non Heap Used": "MB",
    "Mem Non Heap Committed": "MB",
    "Mem Non Heap Max": "MB",
    "Mem Heap Used": "MB",
    "Mem Heap Committed": "MB",
    "Mem Heap Max": "MB",
    "Mem Max": "MB",
    "GC Count ParNew": "count",
    "GC Time ParNew": "ms",
    "GC Count CMS": "count",
    "GC Time CMS": "ms",
    "GC Count": "count",
    "GC Time": "ms",
    "Threads New": "count",
    "Threads Runnable": "count",
    "Threads Blocked": "count",
    "Threads Waiting": "count",
    "Threads Timed Waiting": "count",
    "Threads Terminated": "count",
    "Free Physical Memory Size": "MB",
    "Free Swap Space Size": "MB",
    "Total Physical Memory Size": "MB",
    "Total Swap Space Size": "MB",
    "Committed Virtual Memory Size": "MB",
    "Sent Data": "bytes",
    "Received Data": "bytes",
    "Out Of Order Scanner Exception": "count",
    "Unknown Scanner Exception": "count",
    "Region Too Busy Exception": "count",
    "HLog Split Time Mean": "ms",
    "HLog Split Time Min": "ms",
    "HLog Split Time Max": "ms",
    "HLog Split Time Num Operations": "count",
    "HLog Split Size Mean": "bytes",
    "HLog Split Size Min": "bytes",
    "HLog Split Size Max": "bytes",
    "HLog Split Size Num Operations": "count"
}

class HBaseMonitor:

    def __init__(self, args):
        self.maindata = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
            'units': METRICS_UNITS
        }
        self.host = args.host
        self.port = args.port
        self.log_file_path = args.log_file_path

    def metric_collector(self):
        try:
            def to_mb(value):
                return round(value / (1024 * 1024), 2)
            url = f"http://{self.host}:{self.port}/jmx"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            beans = data.get("beans", [])

            for bean in beans:
                name = bean.get("name")
                if name == "Hadoop:service=HBase,name=Master,sub=Balancer":
                    hostname = bean.get("tag.Hostname")
                    if hostname:
                        self.maindata["Hostname"] = hostname
                    
                elif name == "Hadoop:service=HBase,name=Master,sub=AssignmentManager":
                    self.maindata["Rit Oldest Age"] = bean.get("ritOldestAge", 0)
                    self.maindata["Rit Count"] = bean.get("ritCount", 0)
                    self.maindata["Rit Count Over Threshold"] = bean.get("ritCountOverThreshold", 0)
                    self.maindata["Rit Duration Min"] = bean.get("RitDuration_min", 0)
                    self.maindata["Rit Duration Max"] = bean.get("RitDuration_max", 0)
                    self.maindata["Rit Duration Mean"] = bean.get("RitDuration_mean", 0)
                    self.maindata["Rit Duration Median"] = bean.get("RitDuration_median", 0)

                elif name == "Hadoop:service=HBase,name=Master,sub=IPC":
                    self.maindata["IPC Queue Size"] = bean.get("queueSize", 0)
                    self.maindata["IPC Calls In General Queue"] = bean.get("numCallsInGeneralQueue", 0)
                    self.maindata["IPC Calls In Replication Queue"] = bean.get("numCallsInReplicationQueue", 0)
                    self.maindata["IPC Calls In Priority Queue"] = bean.get("numCallsInPriorityQueue", 0)
                    self.maindata["IPC Open Connections"] = bean.get("numOpenConnections", 0)
                    self.maindata["IPC Active Handlers"] = bean.get("numActiveHandler", 0)
                    self.maindata["IPC Total Call Time Max"] = bean.get("TotalCallTime_max", 0)
                    self.maindata["IPC Total Call Time Mean"] = bean.get("TotalCallTime_mean", 0)
                    self.maindata["IPC Total Call Time Median"] = bean.get("TotalCallTime_median", 0)
                    self.maindata["IPC Total Call Time 99th Percentile"] = bean.get("TotalCallTime_99th_percentile", 0)
                    self.maindata["Sent Data"] = bean.get("sentBytes", 0)
                    self.maindata["Received Data"] = bean.get("receivedBytes", 0)
                    self.maindata["Out Of Order Scanner Exception"] = bean.get("exceptions.OutOfOrderScannerNextException", 0)
                    self.maindata["Unknown Scanner Exception"] = bean.get("exceptions.UnknownScannerException", 0)
                    self.maindata["Region Too Busy Exception"] = bean.get("exceptions.RegionTooBusyException", 0)


                elif name == "Hadoop:service=HBase,name=Master,sub=Server":
                    self.maindata["Regions Servers"] = bean.get("numRegionServers", 0)
                    self.maindata["Dead Region Servers"] = bean.get("numDeadRegionServers", 0)
                    self.maindata["Cluster Requests"] = bean.get("clusterRequests", 0)
                    self.maindata["Merge Plan Count"] = bean.get("mergePlanCount", 0)
                    self.maindata["Split Plan Count"] = bean.get("splitPlanCount", 0)
                    self.maindata["Average Load"] = bean.get("averageLoad", 0)

                elif name == "Hadoop:service=HBase,name=JvmMetrics":
                    self.maindata["Mem Non Heap Used"] = bean.get("MemNonHeapUsedM", 0)
                    self.maindata["Mem Non Heap Committed"] = bean.get("MemNonHeapCommittedM", 0)
                    self.maindata["Mem Non Heap Max"] = bean.get("MemNonHeapMaxM", 0)
                    self.maindata["Mem Heap Used"] = bean.get("MemHeapUsedM", 0)
                    self.maindata["Mem Heap Committed"] = bean.get("MemHeapCommittedM", 0)
                    self.maindata["Mem Heap Max"] = bean.get("MemHeapMaxM", 0)
                    self.maindata["Mem Max"] = bean.get("MemMaxM", 0)
                    self.maindata["GC Count ParNew"] = bean.get("GcCountParNew", 0)
                    self.maindata["GC Time ParNew"] = bean.get("GcTimeMillisParNew", 0)
                    self.maindata["GC Count CMS"] = bean.get("GcCountConcurrentMarkSweep", 0)
                    self.maindata["GC Time CMS"] = bean.get("GcTimeMillisConcurrentMarkSweep", 0)
                    self.maindata["GC Count"] = bean.get("GcCount", 0)
                    self.maindata["GC Time"] = bean.get("GcTimeMillis", 0)
                    self.maindata["Threads New"] = bean.get("ThreadsNew", 0)
                    self.maindata["Threads Runnable"] = bean.get("ThreadsRunnable", 0)
                    self.maindata["Threads Blocked"] = bean.get("ThreadsBlocked", 0)
                    self.maindata["Threads Waiting"] = bean.get("ThreadsWaiting", 0)
                    self.maindata["Threads Timed Waiting"] = bean.get("ThreadsTimedWaiting", 0)
                    self.maindata["Threads Terminated"] = bean.get("ThreadsTerminated", 0)

                elif name == "java.lang:type=OperatingSystem":
                    self.maindata["Free Physical Memory Size"] = to_mb(bean.get("FreePhysicalMemorySize", 0))
                    self.maindata["Free Swap Space Size"] = to_mb(bean.get("FreeSwapSpaceSize", 0))
                    self.maindata["Total Physical Memory Size"] = to_mb(bean.get("TotalPhysicalMemorySize", 0))
                    self.maindata["Total Swap Space Size"] = to_mb(bean.get("TotalSwapSpaceSize", 0))
                    self.maindata["Committed Virtual Memory Size"] = to_mb(bean.get("CommittedVirtualMemorySize", 0))

                elif name == "Hadoop:service=HBase,name=Master,sub=FileSystem":
                    self.maindata["HLog Split Time Mean"] = bean.get("HlogSplitTime_mean", 0)
                    self.maindata["HLog Split Time Min"] = bean.get("HlogSplitTime_min", 0)
                    self.maindata["HLog Split Time Max"] = bean.get("HlogSplitTime_max", 0)
                    self.maindata["HLog Split Time Num Operations"] = bean.get("HlogSplitTime_num_ops", 0)

                    self.maindata["HLog Split Size Mean"] = bean.get("HlogSplitSize_mean", 0)
                    self.maindata["HLog Split Size Min"] = bean.get("HlogSplitSize_min", 0)
                    self.maindata["HLog Split Size Max"] = bean.get("HlogSplitSize_max", 0)
                    self.maindata["HLog Split Size Num Operations"] = bean.get("HlogSplitSize_num_ops", 0)

                elif name == "java.lang:type=Runtime":
                    self.maindata["VM Name"] = bean.get("VmName", "")
                    self.maindata["Boot Class Path"] = bean.get("BootClassPath", "")
                    self.maindata["VM Vendor"] = bean.get("VmVendor", "")
                    self.maindata["VM Version"] = bean.get("VmVersion", "")
                    self.maindata["Library Path"] = bean.get("LibraryPath", "")
                    self.maindata["Spec Name"] = bean.get("SpecName", "")
                    self.maindata["Spec Vendor"] = bean.get("SpecVendor", "")
                    self.maindata["Spec Version"] = bean.get("SpecVersion", "")


            self.maindata["tabs"] = {
                "Assignment Manager": {
                    "order": 1,
                    "tablist": [
                        "Rit Oldest Age",
                        "Rit Count",
                        "Rit Count Over Threshold",
                        "Rit Duration Min",
                        "Rit Duration Max",
                        "Rit Duration Mean",
                        "Rit Duration Median"
                    ]
                },
                "Inter-Process Communication": {
                    "order": 2,
                    "tablist": [
                        "IPC Queue Size",
                        "IPC Calls In General Queue",
                        "IPC Calls In Replication Queue",
                        "IPC Calls In Priority Queue",
                        "IPC Open Connections",
                        "IPC Active Handlers",
                        "IPC Total Call Time Max",
                        "IPC Total Call Time Mean",
                        "IPC Total Call Time Median",
                        "IPC Total Call Time 99th Percentile",
                        "Sent Data",
                        "Received Data",
                        "Out Of Order Scanner Exception",
                        "Unknown Scanner Exception",
                        "Region Too Busy Exception"
                    ]
                },
                "JVM": {
                    "order": 3,
                    "tablist": [
                        "Mem Non Heap Used",
                        "Mem Non Heap Committed",
                        "Mem Non Heap Max",
                        "Mem Heap Used",
                        "Mem Heap Committed",
                        "Mem Heap Max",
                        "Mem Max",
                        "GC Count ParNew",
                        "GC Time ParNew",
                        "GC Count CMS",
                        "GC Time CMS",
                        "GC Count",
                        "GC Time"
                    ]
                },
                "Thread": {
                    "order": 4,
                    "tablist": [
                        "Threads New",
                        "Threads Runnable",
                        "Threads Blocked",
                        "Threads Waiting",
                        "Threads Timed Waiting",
                        "Threads Terminated"
                    ]
                },
                "HLog": {
                    "order": 5,
                    "tablist": [
                        "HLog Split Time Mean",
                        "HLog Split Time Min",
                        "HLog Split Time Max",
                        "HLog Split Time Num Operations",
                        "HLog Split Size Mean",
                        "HLog Split Size Min",
                        "HLog Split Size Max",
                        "HLog Split Size Num Operations"
                    ]
                }
            }

            self.maindata["applog"] = {
                "logs_enabled": True,
                "log_type_name":"HBase Logs",
                "log_file_path": self.log_file_path
            }

            return self.maindata

        except requests.exceptions.RequestException as e:
            return {
                "plugin_version": PLUGIN_VERSION,
                "heartbeat_required": HEARTBEAT,
                "status": 0,
                "msg": f"Error fetching HBase JMX metrics: {e}"
            }

if __name__ == "__main__":
    import argparse

    default_log_path = (
        "/var/log/*hbase*/*.log , "
        "/opt/*hbase*/logs/*.log*, "
        "/*hbase*/*log*/*.log, "
        "C:\\*hbase*\\logs\\*.log*, "
        "C:\\Program Files\\*hbase*\\logs\\*.log*"
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='HBase host', default='localhost')
    parser.add_argument('--port', help='HBase JMX port', default='16010')
    parser.add_argument('--log_file_path', help='HBase log file path', default=default_log_path)
    args = parser.parse_args()

    obj = HBaseMonitor(args)
    result = obj.metric_collector()
    print(json.dumps(result))
    
