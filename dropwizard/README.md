# Dropwizard Monitoring 

## Prerequisites
- Download and install the latest version of the Site24x7 agent on the server where you plan to run the plugin.
- Python 3 must be installed.

## Quick installation

To quickly test the plugin against a local Dropwizard app:

```bash

python3 dropwiz.py –host localhost –port 8081

```

To test the raw metrics endpoint from the agent host:

```bash

curl \-sS http://localhost:8081/metrics | head \-n 2

```

## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### **Installation**  

- Create a directory named `dropwizard`.

	```bash
 	mkdir dropwizard
 	cd dropwizard/
 	```

 - Download the below files [oracle.cfg](https://github.com/site24x7/plugins/blob/master/oracle/oracle.cfg) and [oracle.py](https://github.com/site24x7/plugins/blob/master/oracle/oracle.py) place it under the `oracle` directory.

	```bash
	wget https://raw.githubusercontent.com/Deepak-Bhuvaneswaran/plugins/refs/heads/deepakbhuvaneswaran/dropwizard/dropwizard.py
	wget https://raw.githubusercontent.com/Deepak-Bhuvaneswaran/plugins/refs/heads/deepakbhuvaneswaran/dropwizard/dropwizard.cfg
	```
### Execute the plugin
 
- Execute the below command with appropriate arguments to check for the valid json output:

	```bash
	 python3 /opt/site24x7/monagent/plugins/dropwiz/dropwiz.py –host \<DROPWIZ_HOST\> –port \<DROPWIZ_PORT\>
	 ```
### Move Plugin to Agent Directory
 
 #### Linux

- Place the `dropwizard` under the Site24x7 Linux Agent plugin directory:
  
	```bash
 	mv dropwizard /opt/site24x7/monagent/plugins
 	```
 
#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

-  Further, move the folder `dropwizard` into the  Site24x7 Windows Agent plugin directory:

        C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\dropwizard


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---


## **Configuration (dropwizard.cfg)**

Put dropwizard.cfg beside dropwizard.py (or edit values via CLI).
```bash

[dropwizard]

protocol = http
host = localhost
port = 8081
timeout = 30

```

* protocol — http or https.

* host — hostname or IP for the Dropwizard app.

* port — port where /metrics is served.

* timeout — seconds to wait for the /metrics response before failing.

CLI overrides config file: \--host, \--port, \--protocol, \--timeout.

---

## **How to install (Linux agent)**

1. Create plugin directory on the agent host (if not present) and copy files:

```bash

sudo mkdir \-p /opt/site24x7/monagent/plugins/dropwizard

sudo cp dropwizard.py dropwizard.cfg /opt/site24x7/monagent/plugins/dropwizard/

sudo chmod \+x /opt/site24x7/monagent/plugins/dropwizard/dropwizard.py

```

2. Test locally:

```bash

python3 /opt/site24x7/monagent/plugins/dropwizard/dropwizard.py –host \<DROPWIZARD\_HOST\> –port \<DROPWIZARD\_PORT\>

```

3. The Site24x7 agent will pick up the plugin output automatically (typically within 5 minutes). If not, check agent logs and file permissions.

---

## Supported Metrics 

Below are the metrics grouped exactly as the plugin uses them. Each table uses the Name | Description format so you can copy/paste into the repo.

### **Summary tab**

| Name | Description |
| ----- | ----- |
| HealthCheck Pool Created | Health check thread-pool ‘created’ events (count) |
| HealthCheck Pool Terminated | Health check thread-pool ‘terminated’ events (count) |
| collected_at | The UNIX timestamp (in seconds) indicating when the Dropwizard metrics were collected by the plugin. It helps correlate data collection time and detect delays in polling or transmission | 

### **Connection tab**

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

### **Events tab**

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

### **JVM tab**

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

### **Memory tab**

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

### **Jetty tab**

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

## **Units mapping (as used in the plugin)**

| Name | Unit |
| ----- | ----- |
| Connections at 8080 / 8081 / 8443 / 8444 | connections |
| JVM Uptime | ms |
| Threads Count / Threads Runnable Count | units |
| File Descriptor Ratio | ratio |
| Heap Used / Heap Max / Non-Heap Used / Non-Heap Max / Max Memory / Used Memory / Memory Total Committed / Metaspace Used / Compressed Class Space Used / Code Cache Used / G1 pool metrics | MB |

## **Why these metrics matter (short)**

* **Total Requests & per-method counts** — measure throughput and traffic composition; useful to detect traffic spikes or drops.

* **Active Connections** — indicates current client concurrency on Jetty connectors; helps spot connection saturation.

* **Log counts & response codes** — detect errors and client issues quickly (rising 4xx/5xx or ERROR logs).

* **JVM / Memory / GC** — detect memory leaks, GC pressure, increased pause times, OOM risk.

* **Jetty threadpool & queue** — detect thread starvation or queue buildup (slow downstream, blocked requests).

---

## **Gauges vs Meters vs Timers (concise)**

* **Gauges**: instantaneous values (e.g., heap used, thread counts).

* **Meters**: measures of throughput/rate (e.g., counts that imply a rate).

* **Timers**: measure duration distributions — in this explicit-mapping plugin we collect timer counts; percentiles are not emitted except if you extend mappings.

---

