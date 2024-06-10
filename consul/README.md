


# Consul Monitoring


## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.6 or higher version should be installed.

### Installation  

- Create a directory named "consul".
- Install the **requests** python module.
	```
	pip3 install requests
	```

	
- Download the below files in the "consul" folder and place it under the "consul" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/consul/consul.py && sed -i "1s|^.*|#! $(which python3)|" consul.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/consul/consul.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```bash
       python3 --host "hostname" --port "port no" 
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the consul.cfg file.
	```
    [emqx]
    host="localhost"
    port="8500"

	```	
#### Linux
- Place the "consul" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/consul
#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further, move the folder "consul" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\consul


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics:

- `Consul Autopilot Failure_Tolerance`: This metric indicates the current failure tolerance setting for Consul Autopilot, which determines how many Consul servers are required to be healthy for leader election in a highly available cluster.
- `Consul Raft Applied_Index`: This metric represents the highest index that has been successfully applied to the Consul Raft consensus log, reflecting the current state of the Consul cluster.
- `Consul Raft Commitnumlogs`: This metric indicates the number of entries (logs) committed to the Raft consensus log in the last update.
- `Consul Raft Last_Index`: This metric shows the index of the last entry in the Raft consensus log.
- `Consul Raft Leader Dispatchnumlogs`: This metric reflects the number of log entries dispatched by the current leader for replication to other servers.
- `Consul Raft Apply`: This metric represents the number of times Consul attempted to apply an entry from the Raft log to the Consul state store.
- `Consul Raft Committime`: This metric indicates the time spent on the last Raft log commit operation.
- `Consul Raft Fsm Enqueue`: This metric reflects the number of times Consul queued an entry for processing by the Raft finite state machine.
- `Consul Runtime Alloc_Bytes`: This metric shows the total number of bytes currently allocated by Consul's memory allocator.
- `Consul Runtime Free_Count`: This metric represents the number of free objects currently available in Consul's memory pool.
- `Consul Runtime Heap_Objects`: This metric indicates the current number of objects in use on Consul's heap memory.
- `Consul Runtime Malloc_Count`: This metric reflects the total number of memory allocation requests made by Consul.
- `Consul Runtime Total_Gc_Pause_Ns`: This metric represents the total time spent by Consul's garbage collector during all garbage collection cycles.
- `Consul Runtime Total_Gc_Runs`: This metric indicates the total number of garbage collection cycles performed by Consul.
- `Consul Session_Ttl Active`: This metric shows the number of currently active sessions with a Time-To-Live (TTL) value.
- `Consul Client Rpc`: This metric reflects the number of RPC (Remote Procedure Call) requests made by Consul clients.
- `Consul Rpc Request`: This metric represents the total number of RPC requests received by the Consul server.
- `Consul Acl Resolvetoken`: This metric indicates the number of times Consul processed requests to resolve ACL (Access Control List) tokens.
- `Consul Http Get V1 Agent Metrics`: This metric reflects the number of HTTP GET requests received by the Consul agent at the `/v1/agent/metrics` endpoint.
- `Consul Memberlist Gossip`: This metric represents the number of gossip messages exchanged between Consul servers for memberlist maintenance.

