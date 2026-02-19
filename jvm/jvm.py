#!/usr/bin/python3

import jmxquery as jmx
import json
import argparse

PLUGIN_VERSION = 1
HEARTBEAT = True

class JVMMonitor:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.jvm_host = args.jvm_host
        self.jvm_jmx_port = args.jvm_jmx_port

    def metriccollector(self):
        try:
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.jvm_host}:{self.jvm_jmx_port}/jmxrmi")
            
            metric_queries = {
                "operating_system": {
                    "Runtime Free Memory": "java.lang:type=OperatingSystem/FreePhysicalMemorySize",
                    "Runtime Total Memory": "java.lang:type=OperatingSystem/TotalPhysicalMemorySize"
                },
                "threading": {
                    "Daemon threads": "java.lang:type=Threading/DaemonThreadCount",
                    "Live threads": "java.lang:type=Threading/ThreadCount",
                    "Peak threads": "java.lang:type=Threading/PeakThreadCount",
                    "Total Started Threads": "java.lang:type=Threading/TotalStartedThreadCount",
                    "User Time": "java.lang:type=Threading/CurrentThreadUserTime",
                    "CPU Time": "java.lang:type=Threading/CurrentThreadCpuTime"
                },
                "compilation": {
                    "Compilation Time": "java.lang:type=Compilation/TotalCompilationTime"
                },
                "class_loading": {
                    "Classes Loaded": "java.lang:type=ClassLoading/TotalLoadedClassCount",
                    "Classes Unloaded": "java.lang:type=ClassLoading/UnloadedClassCount"
                },
                "runtime": {
                    "Uptime": "java.lang:type=Runtime/Uptime",
                    "VmName": "java.lang:type=Runtime/VmName"
                }
            }

            for metric_type in metric_queries:
                for metric_name in metric_queries[metric_type]:
                    query = metric_queries[metric_type][metric_name]
                    jmxQuery = [jmx.JMXQuery(query)]
                    metric_result = jmxConnection.query(jmxQuery)
                    if metric_result:
                        value = metric_result[0].value
                        if metric_name == "Runtime Free Memory" or metric_name == "Runtime Total Memory":
                            self.maindata[metric_name] = value
                        else:
                            self.maindata[metric_name] = value

            jmxQuery = [jmx.JMXQuery("java.lang:type=OperatingSystem/ProcessCpuLoad")]
            metric_result = jmxConnection.query(jmxQuery)
            if metric_result and metric_result[0].value is not None:
                self.maindata['CPU Usage'] = round(metric_result[0].value * 100, 2)

            heap_metrics = {
                'Heap Committed': 'java.lang:type=Memory/HeapMemoryUsage/committed',
                'Heap Max': 'java.lang:type=Memory/HeapMemoryUsage/max',
                'Heap Used': 'java.lang:type=Memory/HeapMemoryUsage/used'
            }
            for metric_name, query_str in heap_metrics.items():
                try:
                    jmxQuery = [jmx.JMXQuery(query_str)]
                    metric_result = jmxConnection.query(jmxQuery)
                    if metric_result:
                        self.maindata[metric_name] = metric_result[0].value
                except Exception as e:
                    if 'msg' not in self.maindata:
                        self.maindata['msg'] = str(e)
                    else:
                        self.maindata['msg'] += f"; {str(e)}"
                    self.maindata['status'] = 0

            nonheap_metrics = {
                'Non Heap Committed': 'java.lang:type=Memory/NonHeapMemoryUsage/committed',
                'Non Heap Max': 'java.lang:type=Memory/NonHeapMemoryUsage/max',
                'Non Heap Used': 'java.lang:type=Memory/NonHeapMemoryUsage/used'
            }
            for metric_name, query_str in nonheap_metrics.items():
                try:
                    jmxQuery = [jmx.JMXQuery(query_str)]
                    metric_result = jmxConnection.query(jmxQuery)
                    if metric_result:
                        self.maindata[metric_name] = metric_result[0].value
                except Exception as e:
                    if 'msg' not in self.maindata:
                        self.maindata['msg'] = str(e)
                    else:
                        self.maindata['msg'] += f"; {str(e)}"
                    self.maindata['status'] = 0

            memory_pools = [
                'Metaspace',
                'Compressed Class Space',
                'CodeHeap \'non-nmethods\'',
                'CodeHeap \'profiled nmethods\'',
                'CodeHeap \'non-profiled nmethods\'',
                'G1 Eden Space',
                'G1 Old Gen',
                'G1 Survivor Space',
                'PS Eden Space',
                'PS Old Gen',
                'PS Survivor Space',
                'Par Eden Space',
                'Par Survivor Space',
                'CMS Old Gen'
            ]
            
            for pool_name in memory_pools:
                for metric_type in ['Committed', 'Max', 'Used']:
                    try:
                        query_str = f"java.lang:name={pool_name},type=MemoryPool/Usage/{metric_type.lower()}"
                        jmxQuery = [jmx.JMXQuery(query_str)]
                        metric_result = jmxConnection.query(jmxQuery)
                        if metric_result:
                            self.maindata[f'{pool_name},type=MemoryPool {metric_type}'] = metric_result[0].value
                    except Exception as e:
                        if 'msg' not in self.maindata:
                            self.maindata['msg'] = str(e)
                        else:
                            self.maindata['msg'] += f"; {str(e)}"
                        self.maindata['status'] = 0

            gc_collectors = [
                'Copy',
                'MarkSweepCompact',
                'ParNew',
                'ConcurrentMarkSweep',
                'PSScavenge',
                'PSMarkSweep',
                'G1 Young Generation',
                'G1 Old Generation'
            ]
            
            for gc_name in gc_collectors:
                try:
                    jmxQuery = [jmx.JMXQuery(f"java.lang:name={gc_name},type=GarbageCollector/CollectionCount")]
                    metric_result = jmxConnection.query(jmxQuery)
                    if metric_result:
                        self.maindata[f'{gc_name} Collections Count'] = metric_result[0].value
                    
                    jmxQuery = [jmx.JMXQuery(f"java.lang:name={gc_name},type=GarbageCollector/CollectionTime")]
                    metric_result = jmxConnection.query(jmxQuery)
                    if metric_result:
                        self.maindata[f'{gc_name} Time Spent'] = metric_result[0].value
                except Exception as e:
                    if 'msg' not in self.maindata:
                        self.maindata['msg'] = str(e)
                    else:
                        self.maindata['msg'] += f"; {str(e)}"
                    self.maindata['status'] = 0

        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)

        self.maindata['units'] = {
            "Classes Unloaded": "class",
            "Classes Loaded": "class",
            "Uptime": "ms",
            "Runtime Free Memory": "bytes",
            "Runtime Total Memory": "bytes",
            "CPU Usage": "%",
            "CPU Time": "ns",
            "User Time": "ns",
            "Compilation Time": "ms",
            "Heap Committed": "bytes",
            "Heap Max": "bytes",
            "Heap Used": "bytes",
            "Non Heap Committed": "bytes",
            "Non Heap Max": "bytes",
            "Non Heap Used": "bytes",
            "Compressed Class Space,type=MemoryPool Committed": "bytes",
            "Compressed Class Space,type=MemoryPool Max": "bytes",
            "Compressed Class Space,type=MemoryPool Used": "bytes",
            "Metaspace,type=MemoryPool Committed": "bytes",
            "Metaspace,type=MemoryPool Max": "bytes",
            "Metaspace,type=MemoryPool Used": "bytes",
            "CodeHeap 'non-nmethods',type=MemoryPool Committed": "bytes",
            "CodeHeap 'non-nmethods',type=MemoryPool Max": "bytes",
            "CodeHeap 'non-nmethods',type=MemoryPool Used": "bytes",
            "CodeHeap 'profiled nmethods',type=MemoryPool Committed": "bytes",
            "CodeHeap 'profiled nmethods',type=MemoryPool Max": "bytes",
            "CodeHeap 'profiled nmethods',type=MemoryPool Used": "bytes",
            "CodeHeap 'non-profiled nmethods',type=MemoryPool Committed": "bytes",
            "CodeHeap 'non-profiled nmethods',type=MemoryPool Max": "bytes",
            "CodeHeap 'non-profiled nmethods',type=MemoryPool Used": "bytes",
            "G1 Eden Space,type=MemoryPool Committed": "bytes",
            "G1 Eden Space,type=MemoryPool Max": "bytes",
            "G1 Eden Space,type=MemoryPool Used": "bytes",
            "G1 Old Gen,type=MemoryPool Committed": "bytes",
            "G1 Old Gen,type=MemoryPool Max": "bytes",
            "G1 Old Gen,type=MemoryPool Used": "bytes",
            "G1 Survivor Space,type=MemoryPool Committed": "bytes",
            "G1 Survivor Space,type=MemoryPool Max": "bytes",
            "G1 Survivor Space,type=MemoryPool Used": "bytes",
            "PS Eden Space,type=MemoryPool Committed": "bytes",
            "PS Eden Space,type=MemoryPool Max": "bytes",
            "PS Eden Space,type=MemoryPool Used": "bytes",
            "PS Old Gen,type=MemoryPool Committed": "bytes",
            "PS Old Gen,type=MemoryPool Max": "bytes",
            "PS Old Gen,type=MemoryPool Used": "bytes",
            "PS Survivor Space,type=MemoryPool Committed": "bytes",
            "PS Survivor Space,type=MemoryPool Max": "bytes",
            "PS Survivor Space,type=MemoryPool Used": "bytes",
            "Par Eden Space,type=MemoryPool Committed": "bytes",
            "Par Eden Space,type=MemoryPool Max": "bytes",
            "Par Eden Space,type=MemoryPool Used": "bytes",
            "Par Survivor Space,type=MemoryPool Committed": "bytes",
            "Par Survivor Space,type=MemoryPool Max": "bytes",
            "Par Survivor Space,type=MemoryPool Used": "bytes",
            "CMS Old Gen,type=MemoryPool Committed": "bytes",
            "CMS Old Gen,type=MemoryPool Max": "bytes",
            "CMS Old Gen,type=MemoryPool Used": "bytes",
            "Copy Time Spent": "ms",
            "MarkSweepCompact Time Spent": "ms",
            "ParNew Time Spent": "ms",
            "ConcurrentMarkSweep Time Spent": "ms",
            "PSScavenge Time Spent": "ms",
            "PSMarkSweep Time Spent": "ms",
            "G1 Young Generation Time Spent": "ms",
            "G1 Old Generation Time Spent": "ms"
        }

        self.maindata['tabs'] = {
            "Threading": {
                "order": 1,
                "tablist": [
                    "Daemon threads",
                    "Live threads",
                    "Peak threads",
                    "Total Started Threads",
                    "User Time",
                    "CPU Time"
                ]
            },
            "Memory": {
                "order": 2,
                "tablist": [
                    "Heap Committed",
                    "Heap Max",
                    "Heap Used",
                    "Non Heap Committed",
                    "Non Heap Max",
                    "Non Heap Used",
                    "Metaspace,type=MemoryPool Committed",
                    "Metaspace,type=MemoryPool Max",
                    "Metaspace,type=MemoryPool Used",
                    "Compressed Class Space,type=MemoryPool Committed",
                    "Compressed Class Space,type=MemoryPool Max",
                    "Compressed Class Space,type=MemoryPool Used",
                    "CodeHeap 'non-nmethods',type=MemoryPool Committed",
                    "CodeHeap 'non-nmethods',type=MemoryPool Max",
                    "CodeHeap 'non-nmethods',type=MemoryPool Used",
                    "CodeHeap 'profiled nmethods',type=MemoryPool Committed",
                    "CodeHeap 'profiled nmethods',type=MemoryPool Max",
                    "CodeHeap 'profiled nmethods',type=MemoryPool Used",
                    "CodeHeap 'non-profiled nmethods',type=MemoryPool Committed",
                    "CodeHeap 'non-profiled nmethods',type=MemoryPool Max",
                    "CodeHeap 'non-profiled nmethods',type=MemoryPool Used",
                    "G1 Eden Space,type=MemoryPool Committed",
                    "G1 Eden Space,type=MemoryPool Max",
                    "G1 Eden Space,type=MemoryPool Used",
                    "G1 Old Gen,type=MemoryPool Committed",
                    "G1 Old Gen,type=MemoryPool Max",
                    "G1 Old Gen,type=MemoryPool Used",
                    "G1 Survivor Space,type=MemoryPool Committed",
                    "G1 Survivor Space,type=MemoryPool Max",
                    "G1 Survivor Space,type=MemoryPool Used",
                    "PS Eden Space,type=MemoryPool Committed",
                    "PS Eden Space,type=MemoryPool Max",
                    "PS Eden Space,type=MemoryPool Used",
                    "PS Old Gen,type=MemoryPool Committed",
                    "PS Old Gen,type=MemoryPool Max",
                    "PS Old Gen,type=MemoryPool Used",
                    "PS Survivor Space,type=MemoryPool Committed",
                    "PS Survivor Space,type=MemoryPool Max",
                    "PS Survivor Space,type=MemoryPool Used",
                    "Par Eden Space,type=MemoryPool Committed",
                    "Par Eden Space,type=MemoryPool Max",
                    "Par Eden Space,type=MemoryPool Used",
                    "Par Survivor Space,type=MemoryPool Committed",
                    "Par Survivor Space,type=MemoryPool Max",
                    "Par Survivor Space,type=MemoryPool Used",
                    "CMS Old Gen,type=MemoryPool Committed",
                    "CMS Old Gen,type=MemoryPool Max",
                    "CMS Old Gen,type=MemoryPool Used"
                ]
            },
            "Garbage Collection": {
                "order": 3,
                "tablist": [
                    "Copy Collections Count",
                    "Copy Time Spent",
                    "MarkSweepCompact Collections Count",
                    "MarkSweepCompact Time Spent",
                    "ParNew Collections Count",
                    "ParNew Time Spent",
                    "ConcurrentMarkSweep Collections Count",
                    "ConcurrentMarkSweep Time Spent",
                    "PSScavenge Collections Count",
                    "PSScavenge Time Spent",
                    "PSMarkSweep Collections Count",
                    "PSMarkSweep Time Spent",
                    "G1 Young Generation Collections Count",
                    "G1 Young Generation Time Spent",
                    "G1 Old Generation Collections Count",
                    "G1 Old Generation Time Spent"
                ]
            }
        }

        return self.maindata


if __name__ == "__main__":
    jvm_host = "localhost"
    jvm_jmx_port = "7199"
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jvm_host', help='host name to access the JVM metrics', default=jvm_host)
    parser.add_argument('--jvm_jmx_port', help='jmx port to access the JVM metrics', default=jvm_jmx_port)
    args = parser.parse_args()

    obj = JVMMonitor(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=4))
