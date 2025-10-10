Plugin for CouchDB Monitoring
===========

Apache CouchDB is open source database software which has a document-oriented NoSQL architecture. Install and use our CouchDB monitoring tool and get detailed insights into database activity and health.

Get to know how to configure the CouchDB plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of CouchDB servers.

Learn more https://www.site24x7.com/plugins/couchdb-monitoring.html


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.

## Create a Dedicated User for Monitoring

### Steps to Create and Grant Permissions

1. Log in to CouchDB as an admin or a user with sufficient privileges.

2. Run the following commands to create a new user :

   ```bash
   curl -X PUT http://USERNAME:PASSWORD@127.0.0.1:5984/_users/org.couchdb.user:your_username \
   -H "Content-Type: application/json" \
   -d '{
     "name": "your_username",
     "password": "your_password",
     "roles": [],
     "type": "user"
   }'
## Give the new user system-wide admin privileges

Run the following command to make `your_username` a CouchDB admin:

```bash
curl -X PUT -u USERNAME:PASSWORD http://127.0.0.1:5984/_node/_local/_config/admins/your_username \
-H "Content-Type: application/json" \
-d '"your_username"'
```
## Verify the user has admin privileges
Run the following command to check the user's privileges:

```bash
curl -u your_username:your_password http://127.0.0.1:5984/_users/_security
```
- You should see `your_username` listed under "admins"

### Plugin Installation  

- Create a directory named "couchdb"

- Download the below files and place it under the "couchdb" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchdb/couchdb.py && sed -i "1s|^.*|#! $(which python3)|" couchdb.py
  		wget https://raw.githubusercontent.com/site24x7/plugins/master/couchdb/couchdb.cfg

- Execute the below command with appropriate arguments to check for the valid JSON output:

		python3 couchdb.py --host 127.0.0.1 --port 5984 --user your_username --password your_password
  
#### Linux

- Place the "couchdb" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins

#### Windows 

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

- Move the folder "couchdb" under Site24x7 Windows Agent plugin directory: 

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins
  ## Metrics Captured
| **Metric Name** | **Description** |
|------------------|-----------------|
| couchdb_document_inserts | Number of new documents inserted into the CouchDB database. |
| couchdb_document_writes | Total number of document write operations (including inserts and updates). |
| couchdb_request_time_histogram.[num]_bucket  | Bucket range for the nth segment of request response times.         |
| couchdb_request_time_histogram.[num]_count   | Number of requests that fall into the nth time bucket range.   |
| database_reads | Total number of read operations performed on CouchDB databases. |
| open_os_files | Number of open file descriptors currently used by CouchDB. High values may indicate resource usage issues. |
| request_time | Average time (in milliseconds) taken by CouchDB to handle incoming requests. |
## Database
| **Metric Name** | **Description** |
|------------------|-----------------|
| auth_cache_hits | Number of successful authentication requests served from the cache (faster responses). |
| auth_cache_misses | Number of authentication requests that were not found in the cache (required full verification). |
| couchdb_local_document_writes | Number of local (non-replicated) documents written to the database. |
| database_writes| Total number of write operations performed on CouchDB databases. |
| open_databases | Number of databases currently opened by the CouchDB server. Indicates active connections and resource usage. |
## HTTP
| **Metric Name** | **Description** |
|------------------|------------------|
| No_of_http_Post_Requests | Total number of HTTP POST requests handled by CouchDB |
| No_of_http_Copy_Requests | Total number of HTTP COPY requests received |
| No_of_http_Get_Requests | Total number of HTTP GET requests handled by CouchDB |
| No_of_http_Head_Requests | Total number of HTTP HEAD requests handled |
| No_of_http_Move_Requests | Total number of HTTP MOVE requests processed |
| No_of_http_Put_Requests | Total number of HTTP PUT requests handled |
| No_of_http_200_Responses | Count of successful 200 (OK) HTTP responses |
| No_of_http_201_Responses | Count of 201 (Created) HTTP responses |
| No_of_http_202_Responses | Count of 202 (Accepted) HTTP responses |
| No_of_http_301_Responses | Count of 301 (Redirect) HTTP responses |
| No_of_http_304_Responses | Count of 304 (Not Modified) HTTP responses |
| No_of_http_400_Responses | Count of 400 (Bad Request) HTTP responses |
| No_of_http_401_Responses | Count of 401 (Unauthorized) HTTP responses |
| No_of_http_403_Responses | Count of 403 (Forbidden) HTTP responses |
| No_of_http_404_Responses | Count of 404 (Not Found) HTTP responses |
| No_of_http_405_Responses | Count of 405 (Method Not Allowed) HTTP responses |
| No_of_http_409_Responses | Count of 409 (Conflict) HTTP responses |
| No_of_http_412_Responses | Count of 412 (Precondition Failed) HTTP responses |
| No_of_http_500_Responses | Count of 500 (Internal Server Error) HTTP responses |
| view_reads | Number of view index reads performed |
| bulk_requests | Number of bulk document write requests received |
| temporary_view_reads | Number of temporary (ad-hoc) view reads |
| clients_requesting_changes | Number of clients currently requesting change feeds |
## Performance
| **Metric Name** | **Description** |
|------------------|------------------|
| couchdb_request_time.arithmetic_mean | Average (mean) time taken to process HTTP requests. |
| couchdb_request_time.geometric_mean | Geometric mean of request times — gives a better sense of central tendency when data spans multiple magnitudes. |
| couchdb_request_time.harmonic_mean | Harmonic mean of request times — useful for averaging rates and avoiding skew from large outliers. |
| couchdb_request_time.kurtosis | Indicates how heavy or light the tails of the request time distribution are (measure of outlier presence). |
| couchdb_request_time.max | Maximum time taken by any single request. |
| couchdb_request_time.median | Middle value of all recorded request times (50% of requests are faster, 50% are slower). |
| couchdb_request_time.min | Minimum (fastest) time taken to process a request. |
| couchdb_request_time.skewness | Measures asymmetry in request time distribution — positive skew means more slow requests. |
| couchdb_request_time.standard_deviation | How much individual request times vary from the mean — indicates consistency. |
| couchdb_request_time.variance | Square of the standard deviation — shows overall spread of request times. |
| couchdb_request_time_percentile.50 | 50th percentile (median) — half of the requests completed faster than this time. |
| couchdb_request_time_percentile.75 | 75th percentile — 75% of requests completed faster than this time. |
| couchdb_request_time_percentile.90 | 90th percentile — 90% of requests completed faster than this time (shows upper performance boundary). |
| couchdb_request_time_percentile.95 | 95th percentile — only 5% of requests took longer than this time. |
| couchdb_request_time_percentile.99 | 99th percentile — only 1% of requests took longer than this time. |
| couchdb_request_time_percentile.999 | 99.9th percentile — extreme tail latency; helps identify rare, very slow requests. |
## Sample Image:
<img width="1653" height="742" alt="image" src="https://github.com/user-attachments/assets/92d06325-1cb8-411f-ab22-8fa67e495140" />


