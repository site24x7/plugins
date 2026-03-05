# Memcached Monitoring

Memcached is a free and open-source, general purpose distributed memory caching system. Analyze the performance of your Memcached server and take informed troubleshooting descisions by keeping track of critical metrics.

Get to know how to configure the Memcached plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Memcached servers.
  
Learn more https://www.site24x7.com/plugins/memcached-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Execute the following command in your server to install the required Python module:

```bash
pip install python-binary-memcached
```

### Plugin Installation  

- Create a directory named `memcached`.
  
```bash
mkdir memcached
cd memcached/
```
      
- Download below files and place it under the "memcached" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/memcached/memcached.py && sed -i "1s|^.*|#! $(which python3)|" memcached.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/memcached/memcached.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 memcached.py --host 127.0.0.1 --port 11211
```

- For SASL-enabled Memcached servers, pass the credentials:

```bash
python3 memcached.py --host 127.0.0.1 --port 11211 --username "username" --password "password"
```

- Provide your memcached configurations in memcached.cfg file.

```bash
[Memcached]
host = "127.0.0.1"
port = "11211"
username = ""
password = ""
```

> **Note:** Leave `username` and `password` empty if your Memcached server does not have SASL authentication enabled.

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "memcached" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv memcached /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "memcached" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Memcached Server Monitoring Plugin Metrics


| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Memcached Version           | The version of Memcached currently running on the server.              |
| PID                         | Process ID of the Memcached server.                                    |
| Architecture Bits            | Architecture of the server in bits (32 or 64).                         |
| Worker Threads               | Number of worker threads requested.                                    |
| Libevent Version             | Version of the libevent library being used.                            |
| Network Read                 | Total data read from the network (in MB).                              |
| Network Written              | Total data sent over the network (in MB).                              |
| User CPU Time                | Accumulated user CPU time for the process (in minutes).                |
| System CPU Time              | Accumulated system CPU time for the process (in minutes).              |
| Cache Hit Rate              | Percentage of GET requests that resulted in a cache hit.               |
| Memory Usage Percent        | Percentage of allocated memory currently in use.                       |
| Avg Item Size               | Average size of stored items (bytes used / current items), in MB.      |
| Current Items                | Number of items currently stored in the cache.                         |
| Current Connections          | Number of open connections to the server.                              |
| Evictions                    | Number of items evicted from the cache to free memory.                 |
| Cache Memory Used            | Current memory used to store items (in MB).                            |
| Max Memory Limit             | Maximum amount of memory allocated to the server (in MB).              |
| Uptime                      | Time since the server started (in minutes).                            |

### Memory & Storage

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Active Slab Classes         | Total number of active slab classes.                                   |
| Slab Memory Allocated       | Total memory allocated to slab pages (in MB).                          |
| Slabs Total Pages           | Total number of pages allocated across all slab classes.               |
| Slabs Total Chunks          | Total number of chunks across all slab classes.                        |
| Slabs Used Chunks           | Total number of chunks in use across all slab classes.                 |
| Slabs Free Chunks           | Total number of free chunks across all slab classes.                   |
| Slabs Free Chunks End       | Total free chunks at the end of the last allocated page.               |
| Slab Memory Requested       | Total memory requested from slab allocator (in MB).                    |
| Hash Table Memory            | Memory currently used by the hash table (in MB).                       |
| Hash Power Level             | Current size multiplier for the hash table.                            |
| Hash Is Expanding            | Indicates if the hash table is currently expanding.                    |
| Memory Allocation Failures   | Number of memory allocation failures.                                  |
| Store No Memory              | Number of store commands failed due to no available memory.            |
| Store Too Large              | Number of store commands failed because the item was too large.        |
| Slabs Chunk Size             | Total chunk size across all slab classes (in MB).                      |
| Slabs Chunks Per Page        | Total chunks per page across all slab classes.                         |

### Operations

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| GET Commands                 | Total number of GET commands received.                                 |
| SET Commands                 | Total number of SET commands received.                                 |
| FLUSH Commands               | Total number of FLUSH commands received.                               |
| TOUCH Commands               | Total number of TOUCH commands received.                               |
| GET Hits                     | Number of GET requests that resulted in a cache hit.                   |
| GET Misses                   | Number of GET requests that resulted in a cache miss.                  |
| DELETE Hits                  | Number of successful DELETE operations.                                |
| DELETE Misses                | Number of DELETE requests for keys not found.                          |
| INCREMENT Hits               | Number of successful INCREMENT operations.                             |
| INCREMENT Misses             | Number of failed INCREMENT operations (key not found).                 |
| DECREMENT Hits               | Number of successful DECREMENT operations.                             |
| DECREMENT Misses             | Number of failed DECREMENT operations (key not found).                 |
| CAS Hits                     | Number of successful CAS (Check-And-Set) operations.                   |
| CAS Misses                   | Number of CAS operations where the key was not found.                  |
| CAS Value Mismatches          | Number of CAS operations where the value did not match.                |
| TOUCH Hits                   | Number of successful TOUCH operations.                                 |
| TOUCH Misses                 | Number of TOUCH requests for keys not found.                           |
| Total Items                  | Total number of items stored since the server started.                 |
| AUTH Commands                | Number of authentication commands processed.                           |
| AUTH Errors                  | Number of failed authentication attempts.                              |

### Eviction

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Evicted Active               | Number of active items evicted before expiration.                      |
| Evicted Unfetched            | Number of items evicted that were never retrieved.                     |
| Expired Unfetched            | Number of items that expired without being fetched.                    |
| Expired Items Reclaimed      | Number of times an expired entry's memory was reclaimed for a new item.|
| Evicted With Expiry          | Number of evicted items that had an expiration time set.               |
| Last Evicted Item Age        | Time since the last evicted item was stored (in minutes).              |
| Out Of Memory Errors         | Number of times items could not be stored due to memory limit.         |

### LRU

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Moves To Cold                | Number of items moved from hot/warm to cold LRU.                       |
| Moves To Warm                | Number of items moved from cold to warm LRU.                           |
| Moves Within LRU             | Number of items reshuffled within the same LRU.                        |
| Hot LRU Items                | Number of items in the hot LRU across all slabs.                       |
| Warm LRU Items               | Number of items in the warm LRU across all slabs.                      |
| Cold LRU Items               | Number of items in the cold LRU across all slabs.                      |
| Non-Expiring Items           | Number of items that never expire across all slabs.                    |
| Oldest Item Age              | Age of the oldest item in the cache (in minutes).                      |
| LRU Tail Repairs             | Number of times the LRU tail pointer was repaired.                     |
| LRU Crawler Starts           | Number of times the LRU crawler was started.                           |
| LRU Tail Relocked            | Number of times the LRU tail was relocked due to contention.           |
| LRU Crawler Reclaimed        | Number of items reclaimed by the LRU crawler.                          |
| Crawler Items Checked        | Total items inspected by the LRU crawler.                              |
| Direct Reclaims              | Number of direct memory reclaims performed.                            |

### Connections

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Total Connections            | Total number of connections opened since the server started.           |
| Max Connections              | Maximum number of concurrent connections allowed.                      |
| Rejected Connections         | Number of connections rejected due to max connection limit.            |
| Connection Structures        | Number of connection structures allocated by the server.               |
| Connection Yields            | Number of times a connection yielded to another due to limit.          |
| Accepting Connections        | Whether the server is currently accepting new connections.             |
| Reserved File Descriptors    | Number of file descriptors reserved for internal use.                  |
| Listener Disabled Count      | Number of times the listener was disabled due to connection limit.     |

## Sample Image

<img width="3292" height="1746" alt="image" src="https://github.com/user-attachments/assets/27c0cdf3-9907-43d5-a72c-fdbcda40938e" />
