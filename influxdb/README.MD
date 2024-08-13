
# **InfluxDB Monitoring**

## About Influxdb
InfluxDB is an open-source time series database developed by InfluxData. It's designed to handle high write and query loads, making it ideal 
for storing, querying, and managing time-stamped data.

### Plugin Installation
- Create a directory named "influxdb" 
  
- Download all the files in the "influxdb" folder.
  ```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/influxdb/influxdb.py && sed -i "1s|^.*|#! $(which python3)|" influxdb.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/influxdb/influxdb.cfg
  ```

- Execute the below command with appropriate arguments to check for the valid json output:
    
        python3 influxdb.py --host_name "hosname or ipaddress" --port "port no" 

- After above command with parameters gives expected output, please configure the relevant parameters in the influxdb.cfg file.

      [influxdb_instance]
      host_name = "localhost"
      port = "8086"

#### Linux

- Place the "influxdb" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/influxdb

#### Windows
        
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "kafka" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\influxdb

## Performance Metrics
Name		            	| 	Description
---         		   	|   	---
influxdb_buckets_total		|	The total number of buckets created in InfluxDB. A bucket is a named location where time series data is stored.
influxdb_dashboards_total		|	The total number of dashboards created. Dashboards are used for visualizing and analyzing time series data in InfluxDB.
influxdb_organizations_total		|	The total number of organizations configured. An organization in InfluxDB represents a group or a collection of users.
influxdb_remotes_total		|	The total number of remote connections or endpoints configured for data replication or querying across InfluxDB instances.
influxdb_replications_total		|	The total number of active data replications. Replications allow data to be copied to another InfluxDB instance or bucket.
influxdb_scrapers_total		|	The total number of scrapers configured. Scrapers are used to pull data from external sources, such as Prometheus endpoints, into InfluxDB.
influxdb_telegrafs_total		|	The total number of Telegraf configurations in InfluxDB. Telegraf is the data collection agent that can be configured to send data to InfluxDB.
influxdb_users_total		|	The total number of users created in the InfluxDB instance.
go_gc_duration_seconds_count		|	The total number of garbage collection (GC) cycles completed by the Go runtime.
go_goroutines		|	The current number of goroutines (lightweight threads) in use by the Go runtime.
go_memstats_alloc_bytes		|	The number of bytes of memory currently allocated by the Go runtime.
go_memstats_buck_hash_sys_bytes		|	The amount of memory used by the Go runtime for hash buckets.
go_memstats_frees_total		|	The total number of memory free operations performed by the Go runtime.
go_memstats_gc_sys_bytes		|	The amount of memory used by the Go runtime for garbage collection metadata.
go_memstats_heap_alloc_bytes		|	The number of bytes allocated on the heap.
go_memstats_heap_idle_bytes		|	The number of bytes in the heap that are not in use.
go_memstats_heap_inuse_bytes		|	The total number of buckets created in InfluxDB. A bucket is a named location where time series data is stored.
go_memstats_heap_released_bytes		|	The number of bytes of heap memory released back to the operating system.
go_memstats_heap_sys_bytes		|	The total amount of memory obtained from the system for the heap.
go_memstats_last_gc_time_seconds		|	The Unix timestamp of when the last garbage collection cycle finished.
go_memstats_lookups_total		|	The total number of pointer lookups performed by the Go runtime.
go_memstats_mallocs_total		|	The total number of memory allocation operations performed by the Go runtime.
go_memstats_mcache_inuse_bytes		|	The number of bytes in use by the memory cache in the Go runtime.
go_memstats_mcache_sys_bytes		|	The total memory obtained from the system for memory cache in the Go runtime.
go_memstats_mspan_inuse_bytes		|	The number of bytes of memory spans in use by the Go runtime.
go_memstats_mspan_sys_bytes		|	The total memory obtained from the system for memory spans in the Go runtime.
go_memstats_next_gc_bytes		|	The target heap size for the next garbage collection cycle.
go_memstats_other_sys_bytes		|	The number of bytes used by other system memory in the Go runtime.
go_memstats_stack_inuse_bytes		|	The number of bytes in use by the Go runtime's stack.
go_memstats_stack_sys_bytes		|	The total memory obtained from the system for the Go runtime's stack.
go_memstats_sys_bytes		|	The total amount of memory obtained from the system by the Go runtime.
go_threads		|	The number of OS threads created by the Go runtime.
task_executor_promise_queue_usage		|	The current usage of the promise queue in the task executor. This metric indicates how many promises are in the queue, which are essentially placeholders for future results.
task_executor_total_runs_active		|	The total number of currently active task executions. This metric shows how many tasks are being executed at the moment.
task_executor_workers_busy		|	The number of worker threads currently busy executing tasks.
task_scheduler_current_execution		|	The current number of tasks being executed by the scheduler.
task_scheduler_execute_delta_count		|	The number of times tasks have been executed, calculated as a delta over a period.
task_scheduler_total_execute_failure		|	The total number of task execution failures.
task_scheduler_total_execution_calls		|	The total number of calls made to execute tasks.
task_scheduler_total_release_calls		|	The total number of calls made to release resources after task execution.
task_scheduler_total_schedule_calls		|	The total number of calls made to schedule tasks.
task_scheduler_total_schedule_fails		|	The total number of failures encountered while scheduling tasks.
task_scheduler_schedule_delay_count		|	The count of delays encountered when scheduling tasks.
storage_retention_check_duration_count		|	The total count of retention check operations performed. Retention checks are used to enforce data retention policies in InfluxDB, ensuring old data is removed according to defined rules.

