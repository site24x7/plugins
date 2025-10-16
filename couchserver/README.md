Plugin for Couchbase Monitoring
===========

Couchbase is an open source database software which has a document-oriented NoSQL architecture. Install and use our Couchbase monitoring tool and get detailed insights into database activity and health.

Get to know how to configure the Couchbase plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of Couchbase servers.

Learn more https://www.site24x7.com/plugins/couchbase-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.

## Create a new user and grant read-only access permission

```bash
curl -u USERNAME:PASSWORD -X PUT \
http://localhost:8091/settings/rbac/users/local/your_username \
-d 'password=your_password&roles=cluster_admin,data_reader[*],query_select[*]'
```
## Verify the new user

Run the following command to check that the user was created successfully:

```bash
curl -u USERNAME:PASSWORD http://localhost:8091/settings/rbac/users/local/your_username
```

### Plugin Installation  

- Create a directory named "couchserver"

- Download the below files and place it under the "couchserver" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchserver/couchserver.py && sed -i "1s|^.*|#! $(which python3)|" couchserver.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchserver/couchserver.cfg

- Edit the couchserver.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python3 couchserver.py --host 127.0.0.1 --port 8091 --user your_username --password your_password
  
  #### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the couchserver.py script.
  
- Place the "couchserver" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins

  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

- Move the folder "couchserver" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins


## Metrics Captured

| Metric Name           | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Bucket Items          | Total number of documents/items in a bucket.                                 |
| Cmd Get               | Number of key-value GET operations performed per second.                     |
| Curr Items            | Current number of active items in memory for the node.                       |
| Ops Queued            | Number of operations currently queued and waiting to be processed.          |
| Quota Total HDD       | Total disk space quota allocated for Couchbase data.                         |
| Quota Total Ram Node  | Total RAM quota assigned per node.                                           |
| Quota Used Ram        | Amount of RAM currently used by all buckets.                                 |
| Quota Used Ram Node   | RAM used by buckets on a specific node.                                      |
| Total Bucket Items    | Total items across all buckets in the cluster.                               |
| Total HDD             | Total physical disk space available for Couchbase data.                      |
| Total Ram             | Total physical RAM available on the cluster nodes.                            |
| Used HDD              | Amount of disk space currently used by Couchbase data.                       |
| Used Ram              | Amount of RAM currently used across the cluster.                             |
| Used by Data HDD      | Percentage of disk space used specifically by bucket data (excluding indexes and metadata). |

## Bucket

| Metric Name        | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| Bucket Ops         | Number of operations (reads, writes, deletes) per second on the bucket.     |
| Get Hits           | Number of successful GET operations (cache hits) per second.                |
| Get Misses         | Number of GET operations that did not find the document in memory.          |
| Hit Ratio          | Percentage of GET operations served from memory cache.                       |
| Evictions          | Number of items removed from memory to free space for new data.             |
| Cache Miss Rate    | Percentage of GET operations that missed the cache.                          |
| Create Ops         | Number of document creation operations per second.                            |
| Update Ops         | Number of document update operations per second.                              |
| Bg Fetches         | Number of background fetches from disk to memory per second.                 |
| Data Disk Size     | Disk space used by the bucket's data (in MB).                                 |
| Actual Disk Size   | Total disk space used by the bucket, including metadata and overhead (in MB).|
| Doc Fragmentation  | Percentage of fragmentation in the bucket data files.                         |
| Write Queue        | Number of write operations waiting in the queue to be processed.             |
| Bucket Mem Used    | Amount of RAM used by this bucket (in MB).                                    |

## Memory

| Metric Name                           | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| Mem High Water                        | Maximum memory used by the node before triggering memory management actions.|
| Mem Low Water                         | Minimum memory threshold before the node can reclaim memory.                |
| Mem Overhead                           | Memory used internally by Couchbase for metadata and system operations (in MB). |
| Key Value Size                         | RAM used by key-value data on the node (in MB).                              |
| Node Cmd Get                           | Number of GET commands received by the node per second.                      |
| Node Get Hits                          | Number of successful GET operations (cache hits) at the node level.         |
| Node Items                             | Number of active items in the node's memory.                                 |
| Node Items Total                       | Total items including replicas on the node.                                   |
| Node Bg Fetches                        | Number of background fetches from disk to memory on the node per second.     |
| Node Mem Used                           | RAM used by the node for key-value storage (in MB).                          |
| Mem Actual Used                         | Actual RAM used by the node including overhead and active data (in MB).      |
| Mem Actual Free                         | Actual free RAM available on the node (in MB).                                |
| Page Faults                             | Number of memory page faults encountered by the node.                        |
| Virtual Bucket Active Resident Items Ratio | Percentage of active items currently in memory (resident in RAM).           |

## Query

| Metric Name           | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Query Elapsed Time    | Total time taken to process the query, including network and planning (in ms). |
| Query Execution Time  | Time taken by the query engine to actually execute the query (in ms).       |
| Query Result Count    | Number of rows/documents returned by the query.                              |
| Query Result Size     | Size of the query result set (in bytes).                                     |
| Query Service Load    | Load on the query service, indicating how busy the query engine is.          |

## Sample Image :
<img width="1652" height="756" alt="image" src="https://github.com/user-attachments/assets/f160f86b-037d-4a96-963d-c7170d22bad4" />
