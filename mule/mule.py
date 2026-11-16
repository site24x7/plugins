#!/usr/bin/python3

import json
import argparse
from jmxquery import JMXConnection, JMXQuery

PLUGIN_VERSION = 1
HEARTBEAT = True


class MuleMonitoring:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.hostname = args.hostname
        self.port = args.port

    def metric_collector(self):
        try:
            jmx = JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.hostname}:{self.port}/jmxrmi")

            queries = [
                JMXQuery('java.lang:type=Runtime/Pid'),
                JMXQuery('java.lang:type=Memory/HeapMemoryUsage'),
                JMXQuery('java.lang:type=Memory/NonHeapMemoryUsage'),
                JMXQuery('java.lang:type=Memory/ObjectPendingFinalizationCount'),
                JMXQuery('java.lang:name=G1 Eden Space,type=MemoryPool/Usage'),
                JMXQuery('java.lang:name=G1 Eden Space,type=MemoryPool/PeakUsage'),
                JMXQuery('java.lang:name=G1 Old Gen,type=MemoryPool/Usage'),
                JMXQuery('java.lang:name=G1 Old Gen,type=MemoryPool/PeakUsage'),
                JMXQuery('java.lang:name=G1 Survivor Space,type=MemoryPool/Usage'),
                JMXQuery('java.lang:name=G1 Survivor Space,type=MemoryPool/PeakUsage'),
                JMXQuery('java.lang:name=Metaspace,type=MemoryPool/Usage'),
                JMXQuery('java.lang:name=Metaspace,type=MemoryPool/PeakUsage'),
                JMXQuery('java.lang:name=Compressed Class Space,type=MemoryPool/Usage'),
                JMXQuery('java.lang:name=G1 Young Generation,type=GarbageCollector/CollectionCount'),
                JMXQuery('java.lang:name=G1 Young Generation,type=GarbageCollector/CollectionTime'),
                JMXQuery('java.lang:name=G1 Young Generation,type=GarbageCollector/LastGcInfo'),
                JMXQuery('java.lang:name=G1 Old Generation,type=GarbageCollector/CollectionCount'),
                JMXQuery('java.lang:name=G1 Old Generation,type=GarbageCollector/CollectionTime'),
                JMXQuery('java.lang:name=G1 Concurrent GC,type=GarbageCollector/CollectionCount'),
                JMXQuery('java.lang:name=G1 Concurrent GC,type=GarbageCollector/CollectionTime'),
                JMXQuery('java.lang:type=Threading/ThreadCount'),
                JMXQuery('java.lang:type=Threading/DaemonThreadCount'),
                JMXQuery('java.lang:type=Threading/PeakThreadCount'),
                JMXQuery('java.lang:type=Threading/TotalStartedThreadCount'),
                JMXQuery('java.lang:type=Threading/TotalThreadAllocatedBytes'),
                JMXQuery('java.lang:type=Threading/CurrentThreadCpuTime'),
                JMXQuery('java.lang:type=OperatingSystem/ProcessCpuLoad'),
                JMXQuery('java.lang:type=OperatingSystem/AvailableProcessors'),
                JMXQuery('java.lang:type=OperatingSystem/ProcessCpuTime'),
                JMXQuery('java.lang:type=OperatingSystem/CommittedVirtualMemorySize'),
                JMXQuery('java.lang:type=OperatingSystem/OpenFileDescriptorCount'),
                JMXQuery('java.lang:type=OperatingSystem/MaxFileDescriptorCount'),
                JMXQuery('java.lang:type=ClassLoading/LoadedClassCount'),
                JMXQuery('java.lang:type=ClassLoading/TotalLoadedClassCount'),
                JMXQuery('java.lang:type=ClassLoading/UnloadedClassCount'),
                JMXQuery('java.lang:type=Compilation/TotalCompilationTime'),
                JMXQuery('java.nio:name=direct,type=BufferPool/Count'),
                JMXQuery('java.nio:name=direct,type=BufferPool/MemoryUsed'),
                JMXQuery('java.nio:name=mapped,type=BufferPool/Count'),
                JMXQuery('java.nio:name=mapped,type=BufferPool/MemoryUsed'),
            ]

            results = jmx.query(queries)

            raw = {}
            for r in results:
                if r.value is not None:
                    raw[r.to_query_string()] = r.value

            pid_value = self._get(raw, 'java.lang:type=Runtime/Pid', 0)
            self.maindata['PID'] = "Process " + str(int(pid_value))

            heap_memory_used = self._get(raw, 'java.lang:type=Memory/HeapMemoryUsage/used', 0)
            heap_memory_max = self._get(raw, 'java.lang:type=Memory/HeapMemoryUsage/max', 0)
            self.maindata['Heap Used Percent'] = round(heap_memory_used / heap_memory_max * 100, 2) if heap_memory_max > 0 else 0
            self.maindata['Heap Free Memory'] = heap_memory_max - heap_memory_used if heap_memory_max > 0 else 0

            open_file_count = self._get(raw, 'java.lang:type=OperatingSystem/OpenFileDescriptorCount', 0)
            max_file_count = self._get(raw, 'java.lang:type=OperatingSystem/MaxFileDescriptorCount', 0)
            self.maindata['File Descriptor Usage Percent'] = round(open_file_count / max_file_count * 100, 2) if max_file_count > 0 else 0

            total_thread_count = self._get(raw, 'java.lang:type=Threading/ThreadCount', 0)
            self.maindata['Thread Count'] = total_thread_count

            process_cpu_value = self._get(raw, 'java.lang:type=OperatingSystem/ProcessCpuLoad', 0)
            self.maindata['CPU Process Load'] = round(max(process_cpu_value, 0) * 100, 2)

            young_gen_gc_count = self._get(raw, 'java.lang:name=G1 Young Generation,type=GarbageCollector/CollectionCount', 0)
            old_gen_gc_count = self._get(raw, 'java.lang:name=G1 Old Generation,type=GarbageCollector/CollectionCount', 0)
            concurrent_gc_count = self._get(raw, 'java.lang:name=G1 Concurrent GC,type=GarbageCollector/CollectionCount', 0)
            self.maindata['GC Collections Total'] = young_gen_gc_count + old_gen_gc_count + concurrent_gc_count

            young_gen_gc_time = self._get(raw, 'java.lang:name=G1 Young Generation,type=GarbageCollector/CollectionTime', 0)
            old_gen_gc_time = self._get(raw, 'java.lang:name=G1 Old Generation,type=GarbageCollector/CollectionTime', 0)
            concurrent_gc_time = self._get(raw, 'java.lang:name=G1 Concurrent GC,type=GarbageCollector/CollectionTime', 0)
            self.maindata['GC Time Total'] = young_gen_gc_time + old_gen_gc_time + concurrent_gc_time

            self.maindata['Open Files'] = self._get(raw, 'java.lang:type=OperatingSystem/OpenFileDescriptorCount')
            self.maindata['Classes Loaded'] = self._get(raw, 'java.lang:type=ClassLoading/LoadedClassCount')

            self.maindata['Heap Memory Used'] = heap_memory_used
            self.maindata['Heap Memory Committed'] = self._get(raw, 'java.lang:type=Memory/HeapMemoryUsage/committed')
            self.maindata['Heap Memory Max'] = self._format_bytes(heap_memory_max)
            self.maindata['Heap Memory Init'] = self._format_bytes(self._get(raw, 'java.lang:type=Memory/HeapMemoryUsage/init', 0))
            self.maindata['Heap Memory Used Percentage'] = self.maindata['Heap Used Percent']
            self.maindata['Non Heap Memory Used'] = self._get(raw, 'java.lang:type=Memory/NonHeapMemoryUsage/used')
            self.maindata['Non Heap Memory Committed'] = self._get(raw, 'java.lang:type=Memory/NonHeapMemoryUsage/committed')
            self.maindata['Non Heap Memory Max'] = self._format_bytes(self._get(raw, 'java.lang:type=Memory/NonHeapMemoryUsage/max', 0))
            self.maindata['Non Heap Memory Init'] = self._format_bytes(self._get(raw, 'java.lang:type=Memory/NonHeapMemoryUsage/init', 0))
            self.maindata['Pending Object Finalization Count'] = self._get(raw, 'java.lang:type=Memory/ObjectPendingFinalizationCount')

            self.maindata['Eden Space Used'] = self._get(raw, 'java.lang:name=G1 Eden Space,type=MemoryPool/Usage/used')
            self.maindata['Eden Space Committed'] = self._get(raw, 'java.lang:name=G1 Eden Space,type=MemoryPool/Usage/committed')
            self.maindata['Eden Space Peak Used'] = self._get(raw, 'java.lang:name=G1 Eden Space,type=MemoryPool/PeakUsage/used')
            self.maindata['Old Gen Used'] = self._get(raw, 'java.lang:name=G1 Old Gen,type=MemoryPool/Usage/used')
            self.maindata['Old Gen Committed'] = self._get(raw, 'java.lang:name=G1 Old Gen,type=MemoryPool/Usage/committed')
            self.maindata['Old Gen Max'] = self._format_bytes(self._get(raw, 'java.lang:name=G1 Old Gen,type=MemoryPool/Usage/max', 0))
            self.maindata['Old Gen Peak Used'] = self._get(raw, 'java.lang:name=G1 Old Gen,type=MemoryPool/PeakUsage/used')
            self.maindata['Survivor Space Used'] = self._get(raw, 'java.lang:name=G1 Survivor Space,type=MemoryPool/Usage/used')
            self.maindata['Survivor Space Committed'] = self._get(raw, 'java.lang:name=G1 Survivor Space,type=MemoryPool/Usage/committed')
            self.maindata['Survivor Space Peak Used'] = self._get(raw, 'java.lang:name=G1 Survivor Space,type=MemoryPool/PeakUsage/used')
            self.maindata['Metaspace Used'] = self._get(raw, 'java.lang:name=Metaspace,type=MemoryPool/Usage/used')
            self.maindata['Metaspace Committed'] = self._get(raw, 'java.lang:name=Metaspace,type=MemoryPool/Usage/committed')
            self.maindata['Metaspace Max'] = self._format_bytes(self._get(raw, 'java.lang:name=Metaspace,type=MemoryPool/Usage/max', 0))
            self.maindata['Metaspace Peak Used'] = self._get(raw, 'java.lang:name=Metaspace,type=MemoryPool/PeakUsage/used')
            self.maindata['Compressed Class Space Used'] = self._get(raw, 'java.lang:name=Compressed Class Space,type=MemoryPool/Usage/used')

            self.maindata['Young Gen GC Count'] = young_gen_gc_count
            self.maindata['Young Gen GC Time'] = young_gen_gc_time
            self.maindata['Old Gen GC Count'] = old_gen_gc_count
            self.maindata['Old Gen GC Time'] = old_gen_gc_time
            self.maindata['Concurrent GC Count'] = concurrent_gc_count
            self.maindata['Concurrent GC Time'] = concurrent_gc_time
            self.maindata['Last GC Duration'] = self._get(raw, 'java.lang:name=G1 Young Generation,type=GarbageCollector/LastGcInfo/duration')
            self.maindata['Last GC Thread Count'] = self._get(raw, 'java.lang:name=G1 Young Generation,type=GarbageCollector/LastGcInfo/GcThreadCount')

            daemon_thread_count = self._get(raw, 'java.lang:type=Threading/DaemonThreadCount', 0)
            self.maindata['Live Thread Count'] = total_thread_count
            self.maindata['Daemon Thread Count'] = daemon_thread_count
            self.maindata['Peak Thread Count'] = self._get(raw, 'java.lang:type=Threading/PeakThreadCount')
            self.maindata['Total Started Thread Count'] = self._get(raw, 'java.lang:type=Threading/TotalStartedThreadCount')
            self.maindata['Non Daemon Thread Count'] = total_thread_count - daemon_thread_count
            self.maindata['Total Threads Allocated Bytes'] = self._get(raw, 'java.lang:type=Threading/TotalThreadAllocatedBytes')
            current_thread_cpu_ns = self._get(raw, 'java.lang:type=Threading/CurrentThreadCpuTime', 0)
            self.maindata['Current Thread CPU Time'] = round(current_thread_cpu_ns / 60000000000, 4)

            self.maindata['Process CPU Load'] = round(max(process_cpu_value, 0) * 100, 2)
            self.maindata['Available Processors'] = str(int(self._get(raw, 'java.lang:type=OperatingSystem/AvailableProcessors', 0))) + " Cores"
            process_cpu_ns = self._get(raw, 'java.lang:type=OperatingSystem/ProcessCpuTime', 0)
            self.maindata['Process CPU Time'] = round(process_cpu_ns / 60000000000, 4)
            self.maindata['Committed Virtual Memory'] = self._get(raw, 'java.lang:type=OperatingSystem/CommittedVirtualMemorySize')
            self.maindata['Open File Descriptor Count'] = self._get(raw, 'java.lang:type=OperatingSystem/OpenFileDescriptorCount')
            self.maindata['Max File Descriptor Count'] = str(int(max_file_count)) + " Descriptors"

            self.maindata['Loaded Class Count'] = self._get(raw, 'java.lang:type=ClassLoading/LoadedClassCount')
            self.maindata['Total Loaded Class Count'] = self._get(raw, 'java.lang:type=ClassLoading/TotalLoadedClassCount')
            self.maindata['Unloaded Class Count'] = self._get(raw, 'java.lang:type=ClassLoading/UnloadedClassCount')
            self.maindata['Total Compilation Time'] = self._get(raw, 'java.lang:type=Compilation/TotalCompilationTime')
            self.maindata['Direct Buffer Count'] = self._get(raw, 'java.nio:name=direct,type=BufferPool/Count')
            self.maindata['Direct Buffer Memory Used'] = self._get(raw, 'java.nio:name=direct,type=BufferPool/MemoryUsed')
            self.maindata['Mapped Buffer Count'] = self._get(raw, 'java.nio:name=mapped,type=BufferPool/Count')
            self.maindata['Mapped Buffer Memory Used'] = self._get(raw, 'java.nio:name=mapped,type=BufferPool/MemoryUsed')

            bytes_metrics = [
                'Heap Free Memory', 'Heap Memory Used', 'Heap Memory Committed',
                'Non Heap Memory Used', 'Non Heap Memory Committed',
                'Eden Space Used', 'Eden Space Committed', 'Eden Space Peak Used',
                'Old Gen Used', 'Old Gen Committed', 'Old Gen Peak Used',
                'Survivor Space Used', 'Survivor Space Committed', 'Survivor Space Peak Used',
                'Metaspace Used', 'Metaspace Committed', 'Metaspace Peak Used',
                'Compressed Class Space Used', 'Total Threads Allocated Bytes',
                'Committed Virtual Memory', 'Direct Buffer Memory Used', 'Mapped Buffer Memory Used',
            ]
            for key in bytes_metrics:
                val = self.maindata.get(key)
                if val is not None and isinstance(val, (int, float)):
                    self.maindata[key] = round(val / 1048576, 2)

            ms_metrics = [
                'GC Time Total', 'Young Gen GC Time', 'Old Gen GC Time',
                'Concurrent GC Time', 'Last GC Duration', 'Total Compilation Time',
            ]
            for key in ms_metrics:
                val = self.maindata.get(key)
                if val is not None and isinstance(val, (int, float)):
                    self.maindata[key] = round(val / 60000, 4)

        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)

        self.maindata['units'] = {
            'Heap Used Percent': '%',
            'Heap Free Memory': 'MB',
            'File Descriptor Usage Percent': '%',
            'CPU Process Load': '%',
            'GC Time Total': 'min',
            'Heap Memory Used': 'MB',
            'Heap Memory Committed': 'MB',
            'Heap Memory Used Percentage': '%',
            'Non Heap Memory Used': 'MB',
            'Non Heap Memory Committed': 'MB',
            'Eden Space Used': 'MB',
            'Eden Space Committed': 'MB',
            'Eden Space Peak Used': 'MB',
            'Old Gen Used': 'MB',
            'Old Gen Committed': 'MB',
            'Old Gen Peak Used': 'MB',
            'Survivor Space Used': 'MB',
            'Survivor Space Committed': 'MB',
            'Survivor Space Peak Used': 'MB',
            'Metaspace Used': 'MB',
            'Metaspace Committed': 'MB',
            'Metaspace Peak Used': 'MB',
            'Compressed Class Space Used': 'MB',
            'Young Gen GC Time': 'min',
            'Old Gen GC Time': 'min',
            'Concurrent GC Time': 'min',
            'Last GC Duration': 'min',
            'Total Threads Allocated Bytes': 'MB',
            'Current Thread CPU Time': 'min',
            'Process CPU Load': '%',
            'Process CPU Time': 'min',
            'Committed Virtual Memory': 'MB',
            'Total Compilation Time': 'min',
            'Direct Buffer Memory Used': 'MB',
            'Mapped Buffer Memory Used': 'MB',
        }

        self.maindata['tabs'] = {
            'Heap Memory': {
                'order': 1,
                'tablist': [
                    'Heap Memory Used', 'Heap Memory Committed', 'Heap Memory Max',
                    'Heap Memory Init', 'Heap Memory Used Percentage',
                    'Non Heap Memory Used', 'Non Heap Memory Committed',
                    'Non Heap Memory Max', 'Non Heap Memory Init',
                    'Pending Object Finalization Count'
                ]
            },
            'Memory Pools': {
                'order': 2,
                'tablist': [
                    'Eden Space Used', 'Eden Space Committed', 'Eden Space Peak Used',
                    'Old Gen Used', 'Old Gen Committed', 'Old Gen Max', 'Old Gen Peak Used',
                    'Survivor Space Used', 'Survivor Space Committed', 'Survivor Space Peak Used',
                    'Metaspace Used', 'Metaspace Committed', 'Metaspace Max', 'Metaspace Peak Used',
                    'Compressed Class Space Used'
                ]
            },
            'Garbage Collection': {
                'order': 3,
                'tablist': [
                    'Young Gen GC Count', 'Young Gen GC Time',
                    'Old Gen GC Count', 'Old Gen GC Time',
                    'Concurrent GC Count', 'Concurrent GC Time',
                    'Last GC Duration', 'Last GC Thread Count'
                ]
            },
            'Threads': {
                'order': 4,
                'tablist': [
                    'Live Thread Count', 'Daemon Thread Count', 'Peak Thread Count',
                    'Total Started Thread Count', 'Non Daemon Thread Count',
                    'Total Threads Allocated Bytes', 'Current Thread CPU Time'
                ]
            },
            'CPU & System': {
                'order': 5,
                'tablist': [
                    'Process CPU Load',
                    'Process CPU Time',
                    'Committed Virtual Memory',
                    'Open File Descriptor Count', 'Max File Descriptor Count'
                ]
            }
        }

        return self.maindata

    def _get(self, raw_dict, key, default=None):
        val = raw_dict.get(key)
        if val is None:
            return default
        if isinstance(val, (int, float)):
            return val
        return default

    def _format_bytes(self, value):
        if value is None or value <= 0:
            return "Unlimited"
        mb = value / 1048576
        return str(round(mb, 2)) + " MB"


if __name__ == '__main__':
    hostname = "localhost"
    port = "9999"

    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='Mule JMX hostname', default=hostname)
    parser.add_argument('--port', help='Mule JMX port', default=port)
    args = parser.parse_args()

    obj = MuleMonitoring(args)
    result = obj.metric_collector()
    print(json.dumps(result, indent=4))
