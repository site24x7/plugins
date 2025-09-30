Plugin for CouchDB Monitoring
===========

Apache CouchDB is open source database software which has a document-oriented NoSQL architecture. Install and use our CouchDB monitoring tool and get detailed insights into database activity and health.

Get to know how to configure the CouchDB plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of CouchDB servers.

Learn more https://www.site24x7.com/plugins/couchdb-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.


### Plugin Installation  

- Create a directory named "couchdb"

- Download the below files and place it under the "couchdb" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchdb/couchdb.py


- Edit the couchdb.py file with appropriate arguments and Execute the below command to check for the valid JSON output:

		python3 couchdb.py
  #### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the couchdb.py script.

- Place the "couchdb" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/couchdb

  #### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

- Move the folder "couchdb" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\couchdb


## Metrics Captured

| Metric Name                              | Description                                                                 |
|-----------------------------------------|-----------------------------------------------------------------------------|
| couchdb.couch_log.level.alert            | Number of log messages at ALERT level in CouchDB.                            |
| couchdb.couch_log.level.critical         | Number of log messages at CRITICAL level in CouchDB.                         |
| couchdb.couch_log.level.error            | Number of log messages at ERROR level in CouchDB.                            |
| couchdb.couch_log.level.warning          | Number of log messages at WARNING level in CouchDB.                          |
| couchdb.couch_log.level.info             | Number of log messages at INFO level in CouchDB.                             |
| couchdb.couchdb.document_inserts         | Total number of documents inserted into the database.                        |
| couchdb.couchdb.document_writes          | Total number of write operations (inserts/updates) performed.               |
| couchdb.couchdb.open_databases           | Number of databases currently open in CouchDB.                                |
| couchdb.couchdb.open_os_files            | Number of OS-level files currently open by CouchDB.                           |
| couchdb.couchdb.request_time.histogram.0_bucket | Count of requests falling into the first request-time bucket.          |
| couchdb.couchdb.request_time.histogram.0_count  | Total number of requests recorded in the first request-time bucket.     |
| couchdb.couchdb.request_time.histogram.1_bucket | Count of requests falling into the second request-time bucket.         |
| couchdb.couchdb.request_time.histogram.1_count  | Total number of requests recorded in the second request-time bucket.    |
| couchdb.couchdb.request_time.n           | Total number of requests recorded for request-time statistics.               |
| database_reads                           | Total number of read operations performed on the database.                   |
| database_writes                          | Total number of write operations performed on the database.                  |
| open_databases                            | Number of databases currently open (alternate metric).                       |
| open_os_files                             | Number of OS-level files currently open (alternate metric).                  |
| request_time                              | Average time taken to process requests in CouchDB (ms).                       |

## Database
| Metric Name                                   | Description                                                                 |
|-----------------------------------------------|-----------------------------------------------------------------------------|
| auth_cache_hits                               | Number of times authentication requests were successfully served from cache. |
| auth_cache_misses                             | Number of times authentication requests were not found in cache.           |
| couchdb.couchdb.local_document_writes         | Total number of writes to local documents in CouchDB.                        |
| couchdb.couchdb.document_purges.total         | Total number of document purge operations attempted.                         |
| couchdb.couchdb.document_purges.success       | Number of document purge operations that succeeded.                          |
| couchdb.couchdb.document_purges.failure       | Number of document purge operations that failed.                             |
| couchdb.couchdb.dbinfo.n                      | Total number of databases in CouchDB.                                        |
| couchdb.couchdb.dbinfo.max                    | Maximum number of documents in a single database.                            |
| couchdb.couchdb.dbinfo.min                    | Minimum number of documents in a single database.                            |
| couchdb.couchdb.dbinfo.median                 | Median number of documents across all databases.                              |
| couchdb.active_tasks.db_compaction.count      | Number of active database compaction tasks currently running.                 |
| couchdb.active_tasks.indexer.count            | Number of active indexing tasks currently running.                            |
| couchdb.active_tasks.view_compaction.count    | Number of active view compaction tasks currently running.                     |

## HTTP
| Metric Name                          | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| no_of_http_post_requests              | Total number of HTTP POST requests received by CouchDB.                     |
| no_of_http_copy_requests              | Total number of HTTP COPY requests received.                                |
| no_of_http_get_requests               | Total number of HTTP GET requests received.                                  |
| no_of_http_head_requests              | Total number of HTTP HEAD requests received.                                 |
| no_of_http_move_requests              | Total number of HTTP MOVE requests received.                                 |
| no_of_http_put_requests               | Total number of HTTP PUT requests received.                                  |
| no_of_http_200_responses              | Total number of HTTP 200 OK responses sent.                                  |
| no_of_http_201_responses              | Total number of HTTP 201 Created responses sent.                             |
| no_of_http_202_responses              | Total number of HTTP 202 Accepted responses sent.                            |
| no_of_http_301_responses              | Total number of HTTP 301 Moved Permanently responses sent.                   |
| no_of_http_304_responses              | Total number of HTTP 304 Not Modified responses sent.                        |
| no_of_http_400_responses              | Total number of HTTP 400 Bad Request responses sent.                         |
| no_of_http_401_responses              | Total number of HTTP 401 Unauthorized responses sent.                        |
| no_of_http_403_responses              | Total number of HTTP 403 Forbidden responses sent.                            |
| no_of_http_404_responses              | Total number of HTTP 404 Not Found responses sent.                            |
| no_of_http_405_responses              | Total number of HTTP 405 Method Not Allowed responses sent.                  |
| no_of_http_409_responses              | Total number of HTTP 409 Conflict responses sent.                             |
| no_of_http_412_responses              | Total number of HTTP 412 Precondition Failed responses sent.                  |
| no_of_http_500_responses              | Total number of HTTP 500 Internal Server Error responses sent.               |
| view_reads                            | Total number of CouchDB view reads performed.                                 |
| bulk_requests                          | Total number of bulk document requests handled.                               |
| temporary_view_reads                   | Total number of temporary view reads executed.                                 |
| clients_requesting_changes             | Number of clients actively requesting changes feeds.                          |

## Performance
| Metric Name                                         | Description                                                                 |
|-----------------------------------------------------|-----------------------------------------------------------------------------|
| couchdb.couchdb.request_time.min                    | Minimum request processing time observed in CouchDB (ms).                   |
| couchdb.couchdb.request_time.max                    | Maximum request processing time observed (ms).                               |
| couchdb.couchdb.request_time.arithmetic_mean       | Average request processing time using arithmetic mean (ms).                 |
| couchdb.couchdb.request_time.geometric_mean        | Average request processing time using geometric mean (ms).                  |
| couchdb.couchdb.request_time.harmonic_mean         | Average request processing time using harmonic mean (ms).                   |
| couchdb.couchdb.request_time.median                | Median request processing time (ms).                                        |
| couchdb.couchdb.request_time.variance              | Variance of request processing times, shows spread of data.                 |
| couchdb.couchdb.request_time.standard_deviation    | Standard deviation of request times, measures variability (ms).             |
| couchdb.couchdb.request_time.skewness              | Skewness of request time distribution, indicates asymmetry.                 |
| couchdb.couchdb.request_time.kurtosis              | Kurtosis of request time distribution, indicates “peakedness”.              |
| couchdb.couchdb.request_time.percentile.50         | 50th percentile (median) request time (ms).                                 |
| couchdb.couchdb.request_time.percentile.75         | 75th percentile request time (ms), high-normal threshold.                   |
| couchdb.couchdb.request_time.percentile.90         | 90th percentile request time (ms), high load threshold.                     |
| couchdb.couchdb.request_time.percentile.95         | 95th percentile request time (ms), near worst-case response.                |
| couchdb.couchdb.request_time.percentile.99         | 99th percentile request time (ms), extreme response time.                   |
| couchdb.couchdb.request_time.percentile.999       | 99.9th percentile request time (ms), rare slowest requests.                 |
