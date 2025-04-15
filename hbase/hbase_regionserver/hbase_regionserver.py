#!/usr/bin/python3

import json
import requests

PLUGIN_VERSION = 1
HEARTBEAT = True

METRICS_UNITS = {
    "IPC Queue Size": "bytes",
    "IPC Total Call Time Max": "ms",
    "IPC Total Call Time Mean": "ms",
    "IPC Total Call Time Median": "ms",
    "IPC Total Call Time 99th Percentile": "ms",
    "Mem Non Heap Used": "MB",
    "Mem Non Heap Committed": "MB",
    "Mem Non Heap Max": "MB",
    "Mem Heap Used": "MB",
    "Mem Heap Committed": "MB",
    "Mem Heap Max": "MB",
    "Mem Max": "MB",
    "GC Time ParNew": "ms",
    "GC Time CMS": "ms",
    "GC Time": "ms",
    "Free Physical Memory Size": "MB",
    "Free Swap Space Size": "MB",
    "Total Physical Memory Size": "MB",
    "Total Swap Space Size": "MB",
    "Committed Virtual Memory Size": "MB",
    "Sent Data": "bytes",
    "Received Data": "bytes",
    "HLog File Size": "bytes",
    "Num Bytes Compacted Count": "bytes",
    "Total Table Size":"bytes",
    "Memstore Size": "bytes",
    "Store File Size": "bytes"
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
                if name == "Hadoop:service=HBase,name=RegionServer,sub=Regions":
                    hostname = bean.get("tag.Hostname")
                    if hostname:
                        self.maindata["Hostname"] = hostname

                    compactions_completed = 0
                    bytes_compacted = 0
                    files_compacted = 0

                    for key, value in bean.items():
                        if "compactionsCompletedCount" in key:
                            compactions_completed += value
                        elif "numBytesCompactedCount" in key:
                            bytes_compacted += value
                        elif "numFilesCompactedCount" in key:
                            files_compacted += value

                    self.maindata["Compactions Completed Count"] = compactions_completed
                    self.maindata["Num Bytes Compacted Count"] = bytes_compacted
                    self.maindata["Num Files Compacted Count"] = files_compacted


                elif name == "Hadoop:service=HBase,name=RegionServer,sub=IPC":
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


                elif name == "Hadoop:service=HBase,name=RegionServer,sub=Server":
                    self.maindata["Store File Count"] = bean.get("storeFileCount", 0)
                    self.maindata["Store File Size"] = bean.get("storeFileSize", 0)
                    self.maindata["Memstore Size"] = bean.get("memStoreSize", 0)
                    
                    put_count = bean.get("Put_num_ops", 0)
                    delete_count = bean.get("Delete_num_ops", 0)
                    increment_count = bean.get("Increment_num_ops", 0)
                    append_count = bean.get("Append_num_ops", 0)

                    self.maindata["Put Count"] = put_count
                    self.maindata["Delete Count"] = delete_count
                    self.maindata["Increment Count"] = increment_count
                    self.maindata["Append Count"] = append_count

                    self.maindata["HLog File Count"] = bean.get("hlogFileCount", 0)
                    self.maindata["HLog File Size"] = bean.get("hlogFileSize", 0)

                    self.maindata["Scan Operations"] = bean.get("ScanTime_num_ops", 0)
                    self.maindata["Scan Next Min"] = bean.get("ScanTime_min", 0)
                    self.maindata["Scan Next Max"] = bean.get("ScanTime_max", 0)
                    self.maindata["Scan Next Mean"] = bean.get("ScanTime_mean", 0)
                    self.maindata["Scan Next Median"] = bean.get("ScanTime_median", 0)



                elif name == "Hadoop:service=HBase,name=RegionServer,sub=TableLatencies":
                    get_ops_total = 0
                    get_min_list = []
                    get_max_list = []
                    get_mean_list = []
                    get_median_list = []

                    for key, value in bean.items():
                        if "getTime" in key:
                            if key.endswith("_num_ops"):
                                get_ops_total += value
                            elif key.endswith("_min"):
                                get_min_list.append(value)
                            elif key.endswith("_max"):
                                get_max_list.append(value)
                            elif key.endswith("_mean"):
                                get_mean_list.append(value)
                            elif key.endswith("_median"):
                                get_median_list.append(value)

                    self.maindata["Get Operations"] = get_ops_total
                    self.maindata["Get Min"] = min(get_min_list) if get_min_list else 0
                    self.maindata["Get Max"] = max(get_max_list) if get_max_list else 0
                    self.maindata["Get Mean"] = sum(get_mean_list) / len(get_mean_list) if get_mean_list else 0
                    self.maindata["Get Median"] = sum(get_median_list) / len(get_median_list) if get_median_list else 0
                    
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

                elif name == "java.lang:type=Runtime":
                    self.maindata["VM Name"] = bean.get("VmName", "")
                    self.maindata["Boot Class Path"] = bean.get("BootClassPath", "")
                    self.maindata["VM Vendor"] = bean.get("VmVendor", "")
                    self.maindata["VM Version"] = bean.get("VmVersion", "")
                    self.maindata["Library Path"] = bean.get("LibraryPath", "")
                    self.maindata["Spec Name"] = bean.get("SpecName", "")
                    self.maindata["Spec Vendor"] = bean.get("SpecVendor", "")
                    self.maindata["Spec Version"] = bean.get("SpecVersion", "")

                elif name == "Hadoop:service=HBase,name=RegionServer,sub=Tables":
                    self.maindata["Total Tables"] = bean.get("numTables", 0)

                    total_table_size = 0
                    total_read_requests = 0
                    total_write_requests = 0
                    total_total_requests = 0

                    for key, value in bean.items():
                        if key.endswith("_metric_tableSize"):
                            total_table_size += value
                        elif key.endswith("_metric_readRequestCount"):
                            total_read_requests += value
                        elif key.endswith("_metric_writeRequestCount"):
                            total_write_requests += value
                        elif key.endswith("_metric_totalRequestCount"):
                            total_total_requests += value

                    self.maindata["Total Table Size"] = total_table_size
                    self.maindata["Total Read Request Count"] = total_read_requests
                    self.maindata["Total Write Request Count"] = total_write_requests
                    self.maindata["Total Request Count"] = total_total_requests

                                    


            self.maindata["tabs"] = {
                "Inter-Process Communication": {
                    "order": 1,
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
                    "order": 2,
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
                    "order": 3,
                    "tablist": [
                        "Threads New",
                        "Threads Runnable",
                        "Threads Blocked",
                        "Threads Waiting",
                        "Threads Timed Waiting",
                        "Threads Terminated"
                    ]
                },
                "Table Opeartions": {
                    "order": 4,
                    "tablist": [
                        "Total Tables",
                        "Total Table Size",
                        "Total Read Request Count",
                        "Total Write Request Count",
                        "Total Request Count"
                    ]
                },
                "Operations Latency": {
                    "order": 5,
                    "tablist": [
                        "Get Operations",
                        "Get Min",
                        "Get Max",
                        "Get Mean",
                        "Get Median",
                        "Scan Operations",
                        "Scan Next Min",
                        "Scan Next Max",
                        "Scan Next Mean",
                        "Scan Next Median"
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
    parser.add_argument('--port', help='HBase JMX port', default='16030')
    parser.add_argument('--log_file_path', help='HBase log file path', default=default_log_path)
    args = parser.parse_args()

    obj = HBaseMonitor(args)
    result = obj.metric_collector()
    print(json.dumps(result))
