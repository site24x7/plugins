# Redis Monitoring

## Quick installation

If you're using Linux servers, use the redis plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/installer/Site24x7RedisPluginInstaller.sh && sudo bash Site24x7RedisPluginInstaller.sh
```
## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Execute the following command in your server to install Redis: 

		pip install redis

## Plugin Installation  
- Create a directory named `redis`.
  
	```bash
	mkdir redis
 	cd redis/
  	```
 
- Download all the files under the `redis` directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/redis.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/redis/redis.cfg
	```

- Execute the below command with appropriate arguments to check for the valid JSON output:

	```bash
	python redis.py --host "localhost" --port "6379" --password "" 
	```

- Provide your redis configurations in redis.cfg file.

	```bash
	[redis]
	host = "localhost"
	port = "6379"
	password = ""
	```
 
  #### Linux
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the redis.py script.

- Move the `redis` directory to the Site24x7 Linux Agent plugin directory: 

	```bash
	mv redis /opt/site24x7/monagent/plugins/
	```
 
  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.


- Move the folder `redis` under Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured

Name		        	| 	Description
---         			|   	---
Active Defrag Hits		|	Number of value reallocations performed by active the defragmentation process.
Active Defrag Key Hits  	|	Number of keys that were actively defragmented.
Active Defrag Misses		|	Number of aborted value reallocations started by the active defragmentation process.
Active Defrag Key Misses	|	Number of keys that were skipped by the active defragmentation process.
Active Defrag Running		|	When activedefrag is enabled, this indicates whether defragmentation is currently active.
AOF Last Bgrewrite Status	|	Status of the last AOF rewrite operation.
AOF Last Rewrite Time		|	Duration of the last AOF rewrite operation in seconds.
Blocked Clients			|	Number of clients waiting on a blocking call.
CPU Sys				|	System CPU consumed by the Redis server, which is the sum of system CPU consumed by all threads of the server process.
CPU Sys Children		|	System CPU consumed by the background processes.
CPU User			|	User CPU consumed by the Redis server, which is the sum of user CPU consumed by all threads of the server process.
CPU User Children		|	User CPU consumed by the background processes.
CPU Sys Main Thread		|	System CPU consumed by the Redis server main thread.	
Cluster Enabled			|	Indicate Redis cluster is enabled.
Connected Clients		|	Number of client connections (excluding replicas).
Connected Slaves		|	Number of connected replicas.
Evicted Keys			|	The total number of keys evicted due to the maxmemory limit.
Expired Keys			|	Total number of key expiration events.
Fragmentation Ratio		|	Ratio between Memory RSS and Used Memory.
Hit Ratio			|	Measure of the efficiency of key retrieval from the cache. It's calculated as the ratio of successful key lookups (hits) to the total number of key operations (both hits and misses).
IO Threaded Reads Processed	|	Number of read events processed by the main and I/O threads.
IO Threaded Writes Processed	|	Number of write events processed by the main and I/O threads.
IO Threads Active		|	Indicating if I/O threads are active.
Incoming Traffic		|	The network's read rate per second in KB/sec.
Outgoing Traffic		|	The network's write rate per second in KB/sec.
Keyspace Hits			|	Number of successful lookup of keys in the main dictionary.
Keyspace Misses			|	Number of failed lookup of keys in the main dictionary.
Latest Fork Usec		|	Duration of the latest fork operation in microseconds.
Master Repl Offset		|	The server's current replication offset.
Second Repl Offset		|	The offset up to which replication IDs are accepted.
Max Clients			|	The maximum number of connected clients.
Max Memory			|	The value of the maxmemory configuration directive.
Memory Lua			|	NumbeSync Fullr of bytes used by the Lua engine for EVAL scripts.
Memory Overhead			|	The sum in bytes of all overheads that the server allocated for managing its internal data structures.
Memory Peak			|	Peak memory consumed by Redis.
Memory RSS			|	Number of bytes that Redis allocated as seen by the operating system (a.k.a resident set size). 
Memory Startup			|	Initial amount of memory consumed by Redis at startup.
Ops/Sec				|	Number of commands processed per second.
Pubsub Channels			|	The number of active pubsub channels.
Pubsub Patterns			|	The number of active pubsub patterns.
RDB Bgsave in Progress		|	Indicating a RDB save is on-going.
RDB Changes Since Last Save	|	Number of changes since the last dump.
RDB Last Save Time		|	Epoch-based timestamp of last successful RDB save.
Redis Mode			|	The server's mode ( standalone, sentinel or cluster).
Redis Version			|	Version of the Redis server.
Rejected Connections		|	Number of connections rejected because of maxclients limit.
Repl Backlog Histlen		| 	Size of the data in the replication backlog buffer.
Role				|	Role of the server ( master or slave ).
Sync Full			|	The number of full resyncs with replicas.
Sync Partial Err		|	The number of denied partial resync requests.
Sync Partial Ok			|	The number of accepted partial resync requests.
Total Commands Processed	|	Total number of commands processed by the server.
Total Connections Received	|	Total number of connections accepted by the server.
Total Expires			|	The total number of keys with an expiration.
Total Keys			|	The total number of keys.
Total Persists			|	The total number of keys persisted (keys - expires).
Uptime				|	Number of seconds since the Redis server start.
Uptime in Days			|	Number of days since the Redis server start.
Used Memory			|	Total number of bytes allocated by Redis using its allocator.
expires				|	The number of keys with an expiration in a db.
expires_percent			|	Percentage of total keys with an expiration in a db.
keys				|	The total number of keys in a db.
persist				|	The number of keys persisted in a db (db.keys - db.expires).
persist_percent			|	Percentage of total keys that are persisted in a db.