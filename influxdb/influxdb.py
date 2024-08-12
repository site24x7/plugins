#!/usr/bin/python3

import requests
import json

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "6"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the Solr JMX
HOST_NAME = "localhost"

# Enter the port configures for the Solr JMX
PORT = "8086"

# InfluxDB Metrics Endpoint
INFLUXDB_METRICS_URL = "http://localhost:8086/metrics"

# List of metrics to monitor
METRICS_TO_MONITOR = {
    "influxdb_buckets_total":"influxdb_buckets_total",
    "influxdb_dashboards_total":"influxdb_dashboards_total",
    "influxdb_organizations_total":"influxdb_organizations_total",
    "influxdb_remotes_total":"influxdb_remotes_total",
    "influxdb_replications_total":"influxdb_replications_total",
    "influxdb_scrapers_total":"influxdb_scrapers_total",
    "influxdb_telegrafs_total":"influxdb_telegrafs_total",
    "influxdb_tokens_total":"influxdb_tokens_total",
    "influxdb_users_total":"influxdb_users_total",
    "go_gc_duration_seconds_count": "go_gc_duration_seconds_count",
    "go_goroutines": "go_goroutines",
    "go_memstats_alloc_bytes": "go_memstats_alloc_bytes",
    "go_memstats_buck_hash_sys_bytes": "go_memstats_buck_hash_sys_bytes",
    "go_memstats_frees_total": "go_memstats_frees_total",
    "go_memstats_gc_sys_bytes": "go_memstats_gc_sys_bytes",
    "go_memstats_heap_alloc_bytes": "go_memstats_heap_alloc_bytes",
    "go_memstats_heap_idle_bytes": "go_memstats_heap_idle_bytes",
    "go_memstats_heap_inuse_bytes": "go_memstats_heap_inuse_bytes",
    "go_memstats_heap_released_bytes": "go_memstats_heap_released_bytes",
    "go_memstats_heap_sys_bytes": "go_memstats_heap_sys_bytes",
    "go_memstats_last_gc_time_seconds": "go_memstats_last_gc_time_seconds",
    "go_memstats_lookups_total": "go_memstats_lookups_total",
    "go_memstats_mallocs_total": "go_memstats_mallocs_total",
    "go_memstats_mcache_inuse_bytes": "go_memstats_mcache_inuse_bytes",
    "go_memstats_mcache_sys_bytes": "go_memstats_mcache_sys_bytes",
    "go_memstats_mspan_inuse_bytes": "go_memstats_mspan_inuse_bytes",
    "go_memstats_mspan_sys_bytes": "go_memstats_mspan_sys_bytes",
    "go_memstats_next_gc_bytes": "go_memstats_next_gc_bytes",
    "go_memstats_other_sys_bytes": "go_memstats_other_sys_bytes",
    "go_memstats_stack_inuse_bytes": "go_memstats_stack_inuse_bytes",
    "go_memstats_stack_sys_bytes": "go_memstats_stack_sys_bytes",
    "go_memstats_sys_bytes": "go_memstats_sys_bytes",
    "go_threads": "go_threads",
    "task_executor_promise_queue_usage": "task_executor_promise_queue_usage",
    "task_executor_total_runs_active": "task_executor_total_runs_active",
    "task_executor_workers_busy": "task_executor_workers_busy",
    "task_scheduler_current_execution": "task_scheduler_current_execution",
    "task_scheduler_execute_delta_count": "task_scheduler_execute_delta_count",
    "task_scheduler_total_execute_failure": "task_scheduler_total_execute_failure",
    "task_scheduler_total_execution_calls": "task_scheduler_total_execution_calls",
    "task_scheduler_total_release_calls": "task_scheduler_total_release_calls",
    "task_scheduler_total_schedule_calls": "task_scheduler_total_schedule_calls",
    "task_scheduler_total_schedule_fails": "task_scheduler_total_schedule_fails",
    "task_scheduler_schedule_delay_count": "task_scheduler_schedule_delay_count",
    "storage_retention_check_duration_count": "storage_retention_check_duration_count"
}

METRICS_UNITS={
	"go_memstats_last_gc_time_seconds":"s",
	"go_gc_duration_seconds_count":"s"
	}
	
METRICS_TABS={
        "Tasks":{
                "order":1,
                "tablist":[
                    "task_executor_promise_queue_usage",
                    "task_executor_total_runs_active",
                    "task_executor_workers_busy",
                    "task_scheduler_current_execution",
                    "task_scheduler_execute_delta_count",  
                    "task_scheduler_total_execute_failure",   
                    "task_scheduler_total_execution_calls",  
                    "task_scheduler_total_release_calls",
                    "task_scheduler_total_schedule_calls",
                    "task_scheduler_schedule_delay_count",   
                    "task_scheduler_total_schedule_fails"
                   ]},
	"GO Metrics":{
                "order":2,
                "tablist":[
                    "go_gc_duration_seconds_count",
                    "go_goroutines",
                    "go_memstats_alloc_bytes",
                    "go_memstats_buck_hash_sys_bytes",
                    "go_memstats_frees_total",  
                    "go_memstats_gc_sys_bytes",   
                    "go_memstats_heap_alloc_bytes",  
                    "go_memstats_heap_idle_bytes",
                    "go_memstats_heap_inuse_bytes",
                    "go_memstats_heap_released_bytes",   
                    "go_memstats_heap_sys_bytes",   
                    "go_memstats_last_gc_time_seconds", 
                    "go_memstats_lookups_total", 
                    "go_memstats_mallocs_total",
                    "go_memstats_mcache_inuse_bytes",
                    "go_memstats_mspan_sys_bytes",
                    "go_memstats_next_gc_bytes",
                    "go_memstats_other_sys_bytes",
                    "go_memstats_stack_inuse_bytes",
                    "go_memstats_stack_sys_bytes",
                    "go_memstats_mcache_sys_bytes",
                    "go_memstats_mspan_inuse_bytes",
                    "go_memstats_sys_bytes"
                   ]}
}

def metricCollector():
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT

    try:
        response = requests.get("http://"+ HOST_NAME + ":" + PORT + "/metrics")
        #response = requests.get(INFLUXDB_METRICS_URL)
        response.raise_for_status()

        # Parse metrics
        metrics = parse_metrics(response.text)
        data.update(metrics)

    except Exception as e:
        data["status"] = 0
        data["msg"] = str(e)
    data['units']=METRICS_UNITS
    data['tabs']=METRICS_TABS
    return data

def parse_metrics(metrics_text):
    metrics = {}

    for line in metrics_text.splitlines():
        # Ignore comments and empty lines
        if line.startswith("#") or not line.strip():
            continue

        # Parse metric lines
        try:
            key, value = line.split()
            if key in METRICS_TO_MONITOR:
                metrics[METRICS_TO_MONITOR[key]] = float(value)
        except ValueError:
            continue  # skip lines that do not conform to expected format

    return metrics

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help='hostname of influxdb', nargs='?', default="localhost")
    parser.add_argument('--port',  help='port of influxdb', nargs='?', default= "8086")
    
    args = parser.parse_args()
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
    
    result = metricCollector()
    print(json.dumps(result))
