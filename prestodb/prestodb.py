#!/usr/bin/python3

import json
import jpype
from jpype import java
from jpype import javax

# if any impacting changes to this plugin kindly increment the plugin version here
plugin_version = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
heartbeat_required = "true"


host=None
port=None


prestodb_metrics={
	"AbandonedQueries.TotalCount" : "execution_abandoned_queries_total_count",
	"CanceledQueries.TotalCount" : "execution_canceled_queries_total_count",
	"CompletedQueries.TotalCount" : "execution_completed_queries_total_count",
	"ConsumedCpuTimeSecs.TotalCount" : "execution_consumed_cpu_time_secs_total_count",
	"StartedQueries.TotalCount" : "execution_started_queries_total_count",
	"Executor.ActiveCount" : "executor_active_count",
	"Executor.CompletedTaskCount" : "executor_completed_task_count",
	"Executor.CorePoolSize" : "executor_core_pool_size",
	"Executor.LargestPoolSize" : "executor_largest_pool_size",
	"Executor.MaximumPoolSize" : "executor_maximum_pool_size",
	"Executor.QueuedTaskCount" : "executor_queued_task_count",
	"Executor.TaskCount" : "executor_task_count",
	"ActiveCount" : "failure_detector_active_count",
	"ClusterMemoryBytes" : "cluster_memory_bytes",
	"AssignedQueries" : "memory_assigned_queries",
	"BlockedNodes" : "memory_blocked_nodes",
	"FreeDistributedBytes" : "memory_free_distributed_bytes",
	"Nodes" : "memory_nodes",
	"ReservedDistributedBytes" : "memory_reserved_distributed_bytes",
	"ReservedRevocableDistributedBytes" : "memory_reserved_revocable_distributed_bytes",
	"TotalDistributedBytes" : "memory_total_distributed_bytes",
	"FreeBytes" : "memory_free_bytes",
	"MaxBytes" : "memory_max_bytes",
	"ReservedBytes" : "memory_reserved_bytes",
	"ReservedRevocableBytes" : "memory_reserved_revocable_bytes"
}



metric_units={
	"execution_consumed_cpu_time_secs_total_count" : "second",
	"cluster_memory_bytes" : "byte",
	"memory_assigned_queries" : "byte",
	"memory_blocked_nodes" : "byte",
	"memory_free_distributed_bytes" : "byte",
	"memory_nodes" : "byte",
	"memory_reserved_distributed_bytes" : "byte",
	"memory_reserved_revocable_distributed_bytes" : "byte",
	"memory_total_distributed_bytes" : "byte",
	"memory_free_bytes" : "byte",
	"memory_max_bytes" : "byte",
	"memory_reserved_bytes" : "byte",
	"memory_reserved_revocable_bytes" : "byte"
}

user=""
passw=""
result={}


def metric_collector(url):
	try:
		jpype.startJVM()
		jhash=java.util.HashMap()
		jarray=jpype.JArray(java.lang.String)([user,passw])
		jhash.put(javax.management.remote.JMXConnector.CREDENTIALS,jarray);
		jmxurl=javax.management.remote.JMXServiceURL(url)
		jmxsoc=javax.management.remote.JMXConnectorFactory.connect(jmxurl,jhash)
		connection=jmxsoc.getMBeanServerConnection();
		queries={
			"com.facebook.presto.execution:name=QueryManager" : ["AbandonedQueries.TotalCount","CanceledQueries.TotalCount","CompletedQueries.TotalCount","ConsumedCpuTimeSecs.TotalCount","StartedQueries.TotalCount"],
			"com.facebook.presto.execution:name=RemoteTaskFactory" : ["Executor.ActiveCount","Executor.CompletedTaskCount","Executor.CorePoolSize","Executor.LargestPoolSize","Executor.MaximumPoolSize","Executor.QueuedTaskCount","Executor.TaskCount"],
			"com.facebook.presto.failureDetector:name=HeartbeatFailureDetector" : ["ActiveCount"],
			"com.facebook.presto.memory:name=ClusterMemoryManager" : ["ClusterMemoryBytes"],
			"com.facebook.presto.memory:type=ClusterMemoryPool,name=general" : ["AssignedQueries","BlockedNodes","FreeDistributedBytes","Nodes","ReservedDistributedBytes","ReservedRevocableDistributedBytes","TotalDistributedBytes"],
			"com.facebook.presto.memory:type=MemoryPool,name=general" : ["FreeBytes","MaxBytes","ReservedBytes","ReservedRevocableBytes"]
		}

		for query in queries:
			for metric in queries[query]:
				metric_value=round(connection.getAttribute(javax.management.ObjectName(query),metric))
				result[prestodb_metrics[metric]]=metric_value

		result["plugin_version"]=plugin_version
		result["units"]=metric_units

	except Exception as e:
		result["msg"]=str(e)
		result["status"]=0

	result["heartbeat_required"]=heartbeat_required


	

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--host', help="provide host adress",type=str)
	parser.add_argument('--port', help="provide port number",type=str)
	args = parser.parse_args()
	if args.host:
		host=args.host
	if args.port:
		port=args.port
	url="service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" %(host,port)
	metric_collector(url)
	print(json.dumps(result, indent=4, sort_keys=True))

	
