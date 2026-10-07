# MongoDB Insights Monitoring

## Standard Installation

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation

- Create a directory named `mongodb_insights` in your server.

	```bash
	mkdir mongodb_insights
 	cd mongodb_insights/
 	```
- Download the below files and place it under the "mongodb_insights" directory.

	```bash
	wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_insights/mongodb_insights.py  && sed -i "1s|^.*|#! $(which python3)|" mongodb_insights.py
	wget https://raw.githubusercontent.com/site24x7/plugins/master/mongodb_insights/mongodb_insights.cfg
 	wget https://github.com/site24x7/plugins/raw/refs/heads/master/mongodb_insights/pymongo.pyz
 	```
- Execute the below command with appropriate arguments to check for the valid JSON output:

	```bash
	python3 mongodb_insights.py --host "ip_address" --port "port_number" --username "username" --password "password" --dbname "dbname" --authdb "authdb" --tls "False" --long_query_duration "5" --slow_query_profile_lookback_minutes "5"
	```

	- `--long_query_duration` : Minimum running time (in seconds) for an active operation to be flagged and logged as a long-running query. Operations running for less than this value are ignored.
	- `--slow_query_profile_lookback_minutes` : Lookback window (in minutes) used to fetch recent entries from `system.profile` for the slow query log. Only requires the database profiler to be enabled on the databases you want to audit.

- After the above command with parameters gives the expected output, please configure the relevant parameters in the mongodb_insights.cfg file.

	```ini
	[mongo_db]
	host ="localhost"
	port ="27017"
	username ="None"
	password ="None"
	dbname ="mydatabase"
	authdb="admin"
	tls="False"
	tlscertificatekeyfile="None"
	tlscertificatekeyfilepassword="None"
	tlsallowinvalidcertificates="True"
	long_query_duration="5"
	slow_query_profile_lookback_minutes="5"
	```

	| Parameter | Description |
	| --- | --- |
	| `long_query_duration` | Minimum running time (in seconds) for an active operation to be reported as a long-running query via `$currentOp`. |
	| `slow_query_profile_lookback_minutes` | Lookback window (in minutes) used to pull recent entries from `system.profile` for the slow query log. |

#### Linux

- Place the `mongodb_insights` under the Site24x7 Linux Agent plugin directory:

	```bash
 	mv mongodb_insights /opt/site24x7/monagent/plugins
 	```

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

-  Further, move the folder `mongodb_insights` into the  Site24x7 Windows Agent plugin directory:

        C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Performance Metrics

Name		        			| Description
---         					|   ---
**Opcounters Insert per sec**			| The rate at which insert operations are counted per second.
**Opcounters Query per sec**			| The rate at which query operations are counted per second.
**Opcounters Update per sec**			| The rate at which update operations are counted per second.
**Opcounters Delete per sec**			| The rate at which delete operations are counted per second.
**Opcounters Getmore per sec**			| The rate at which "get more" operations are counted per second.
**Opcounters Command per sec**			| The rate at which command operations are counted per second.
**OpLatencies Reads Latency**			| Average latency for read operations, in milliseconds.
**OpLatencies Writes Latency**			| Average latency for write operations, in milliseconds.
**OpLatencies Commands Latency**		| Average latency for processing commands, in milliseconds.
**Scan Order Ratio**				| Ratio of total documents examined to documents returned.
**Index Scan Ratio**				| Ratio of total index keys examined to documents returned.
**InMemory Sorts**				| Count of operations that required an in-memory sort.
**Cache Dirty Pct**				| Percentage of the WiredTiger cache currently holding dirty (modified, not yet flushed) bytes.
**Cache Pages Read**				| Number of pages read into the WiredTiger cache from disk.
**Global Lock Queue Readers**			| Number of read operations currently queued and waiting for the global lock.
**Global Lock Queue Writers**			| Number of write operations currently queued and waiting for the global lock.
**Lock Wait Time Micros**			| Collection-level exclusive lock wait time, in microseconds.
**Connections Current**			| The current number of active database connections.
**Connections Available**			| The number of available database connections.
**Network Bytes In**				| The rate at which bytes are being received over the network per second.
**Network Bytes Out**				| The rate at which bytes are being sent out over the network per second.
**Active Reads**				| Number of active read operations currently in progress.
**Active Writes**				| Number of active write operations currently in progress.
**Oplog Window Hours**				| Time span covered by the oplog, calculated from the oldest to the newest entry, in hours.
**Oplog Size MB**				| Configured maximum size of the oplog, in megabytes.
**Oplog Used MB**				| Amount of oplog space currently used, in megabytes.
**Oplog Used Pct**				| Percentage of the oplog capacity currently used.
**MongoDB Version**				| The version of the MongoDB database.
**Total no of dbs**				| The total number of databases on the system.
**Replica Set Members**			| Child metric listing each replica set member's name, replica set name, and role (state), such as PRIMARY or SECONDARY.

### Slow Query and Long Running Query

Name		        				| Description
---         						|   ---
**Long Running Queries > 1s**				| Trend chart of operations running longer than 1 second.
**Long Running Queries > 30s**				| Trend chart of operations running longer than 30 seconds.
**Long Running Queries Top 10**			| Table of the top 10 longest-running operations.
**Long Running CollScan Secs Running by Host**		| Bar chart of max running time, grouped by host, for collection-scan operations.
**Long Running CollScan Top 10**			| Table of the top 10 longest-running collection-scan operations.
**Long Running IXScan Secs Running by Host**		| Bar chart of max running time, grouped by host, for index-scan operations.
**Long Running IXScan Top 10**				| Table of the top 10 longest-running index-scan operations.
**Slow Queries > 1s**					| Trend chart of queries taking longer than 1 second.
**Slow Queries > 30s**					| Trend chart of queries taking longer than 30 seconds.
**Slow Queries Top 10**				| Table of the top 10 slowest queries.
**CollScan Docs Examined by DB**			| Bar chart of total documents examined, grouped by database, for collection-scan queries.
**CollScan Efficiency Top 10**				| Table of the top 10 collection-scan queries by duration, with docs examined vs. docs returned.
**IXScan Docs Examined by DB**				| Bar chart of total documents examined, grouped by database, for index-scan queries.
**IXScan Efficiency Top 10**				| Table of the top 10 index-scan queries by duration, with docs examined vs. docs returned.

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7.

To see the mongodb_insights monitor in the Site24x7's web client, login Site24x7 with your account, navigate to Server tab -> Plugin Integration -> list of plugin monitors -> user can check the mongodb_insights monitor.
