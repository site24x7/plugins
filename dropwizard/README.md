# Dropwizard Monitoring 

## Prerequisites
- Download and install the latest version of the Site24x7 agent on the server where you plan to run the plugin.
- Python 3 must be installed.

### **Installation**  

- Create a directory named `dropwizard`.

	```bash
 	mkdir dropwizard
 	cd dropwizard/
 	```
### Download Plugin Script
 - Download the below files and place it under the `dropwizard` directory.

	```bash
    wget https://raw.githubusercontent.com/site24x7/plugins/master/dropwizard/dropwizard.py && sed -i "1s|^.*|#! $(which python3)|" dropwizard.py
    wget https://raw.githubusercontent.com/site24x7/plugins/master/dropwizard/dropwizard.cfg
	```
### Execute the plugin
 
- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	 python3 dropwizard.py –-host "localhost" -–port "8081" --protocol "http" --timeout "30"
	 ```
---

## **Configuration (dropwizard.cfg)**

```bash

[dropwizard]
protocol = http
host = localhost
port = 8081
timeout = 30

```
---

### Move Plugin to Agent Directory
 
 #### Linux

- Place the `dropwizard` folder under the Site24x7 Linux Agent plugins directory:
  
	```bash
 	mv dropwizard /opt/site24x7/monagent/plugins
 	```
 
#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

-  Further, move the folder `dropwizard` into the  Site24x7 Windows Agent plugin directory:

        C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

## Supported Metrics 

### **Summary**

| Name | Description |
| ----- | ----- |
| HealthCheck Pool Created | Health check thread-pool ‘created’ events (count) |
| HealthCheck Pool Terminated | Health check thread-pool ‘terminated’ events (count) |
| collected_at | The UNIX timestamp (in seconds) indicating when the Dropwizard metrics were collected by the plugin. It helps correlate data collection time and detect delays in polling or transmission | 

### **Connection**

| Name | Description |
| ----- | ----- |
| Total Requests | Total requests served by the app since start (count) |
| Get Requests | HTTP GET request count |
| Post Requests | HTTP POST request count |
| Put Requests | HTTP PUT request count |
| Delete Requests | HTTP DELETE request count |
| Connections at 8080 | Active Jetty connections on port 8080 (connections) |
| Connections at 8081 | Active Jetty connections on port 8081 (connections) |
| Connections at 8443 | Active Jetty connections on port 8443 (connections) |
| Connections at 8444 | Active Jetty connections on port 8444 (connections) |

### **Events**

| Name | Description |
| ----- | ----- |
| Log Count | Total number of log entries (all levels) |
| Debug Logs | Count of DEBUG-level log entries |
| Error Logs | Count of ERROR-level log entries |
| Info Logs | Count of INFO-level log entries |
| Trace Logs | Count of TRACE-level log entries |
| Warn Logs | Count of WARN-level log entries |
| 1xx Responses | Count of 1xx informational HTTP responses |
| 2xx Responses | Count of 2xx successful HTTP responses |
| 3xx Responses | Count of 3xx redirection HTTP responses |
| 4xx Responses | Count of 4xx client error HTTP responses |
| 5xx Responses | Count of 5xx server error HTTP responses |

### **JVM**

| Name | Description |
| ----- | ----- |
| JVM Uptime | JVM uptime in milliseconds |
| Threads Count | Total number of JVM threads |
| Threads Runnable Count | Number of threads currently runnable |
| Classloader Loaded | Total classes loaded by JVM (count) |
| Classloader Unloaded | Total classes unloaded by JVM (count) |
| File Descriptor Ratio | File descriptor usage metric (ratio/gauge) |
| GC G1 Young Generation Count	|	Number of G1 young-generation (minor) GC events |
| GC G1 Young Generation Time	|	Time spent in young-generation GC (ms) |
| GC G1 Old Generation Count	|	Number of G1 old-generation (major) GC events |
| GC G1 Old Generation Time	|	Time spent in old-generation GC (ms) |
| GC G1 Concurrent GC Count	|	Number of concurrent G1 GC cycles |
| GC G1 Concurrent GC Time	|	Time spent in concurrent G1 GC (ms) |

---

### **Memory**

| Name | Description |
| ----- | ----- |
| Heap Used | Heap memory currently used (MB) |
| Heap Max | Maximum heap memory (MB) |
| Non-Heap Used | Non-heap memory currently used (MB) |
| Non-Heap Max | Maximum non-heap memory (MB) |
| Max Memory | JVM total max memory (MB) |
| Used Memory | JVM total used memory (MB) |
| Memory Total Committed | Total committed memory (MB) |
| Metaspace Used | Metaspace used (MB) |
| Compressed Class Space Used | Compressed class space used (MB) |
| Code Cache Used | Code cache used (MB) |
| G1 Eden Space Used | G1 Eden pool used (MB) |
| G1 Old Gen Used | G1 Old Gen pool used (MB) |
| G1 Survivor Space Used | G1 Survivor pool used (MB) |

### **Jetty**

| Name | Description |
| ----- | ----- |
| Jetty DW Pool Size | Worker thread pool size (units) for main/dropwizard pool |
| Jetty DW Utilization | Worker pool utilization (ratio) |
| Jetty DW Utilization Max | Observed max worker pool utilization (ratio) |
| Jetty DW Jobs | Pending jobs in worker queue (count) |
| Jetty DW Queue Utilization | Worker queue utilization ratio |
| Jetty DW Admin Pool Size | Admin thread pool size (units) |
| Jetty DW Admin Utilization | Admin pool utilization (ratio) |
| Jetty DW Admin Utilization Max | Observed max admin pool utilization (ratio) |
| Jetty DW Admin Jobs | Pending admin jobs (count) |
| Jetty DW Admin Queue Utilization | Admin queue utilization ratio |
| Active Requests | Active requests in the servlet context (count) |
| Active Dispatches | Active dispatch handlers in the servlet context (count) |
| Active Suspended | Active suspended (async) requests (count) |

---

### Sample Image 
<img width="1438" height="820" alt="Screenshot 2025-10-08 at 5 49 32 PM" src="https://github.com/user-attachments/assets/c5b42635-fe0e-4eb8-9b5c-65a6c58f8618" />
