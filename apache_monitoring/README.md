# Plugin for Apache Monitoring
---
The Apache HTTP Server, commonly known as Apache, is the world's most used web server software. Configure Site24x7 Apache plugin to monitor the performance of your apache server and stay on top of issues at all times.

## Performance Metrics

- **Requests per Second**
req_per_sec records the total number of HTTP requests the web server is processing per second.
- **Busy Workers**
Use the metric busy_workers to get the total number of processes actively processing an HTTP request.
- **Idle Workers**
idle_workers is the total number of idle workers/idle processes waiting for an HTTP request.
- **Bytes per Second**
bytes_per_sec records the total amount of data the web server is transferring per second.
- **Bytes per Request**
The average number of bytes being transferred per HTTP request is obtained using the metric bytes_per_req.
- **Processes**
Processes denotes the number of async processes.
- **Connections Async Closing**
Connections Async Closing shows the number of async connections that are in the closing state.
- **Connections Async Keep Alive**
Connections Async Keep Alive displays the number of async connections that are in the keep-alive state.
- **Connections Async Writing**
Connections Async Writing denotes the number of async connections that are in the writing state.
- **CPU Load**
Use the metric cpu_load and get the total percentage of CPU used by the web server.
- **CPU System**
CPU System shows the percentage of time taken by the Apache process to access the system resources.
- **CPU User**
CPU User displays the percentage of time taken by the Apache process to process the code.
- **Load1**
Load1 shows the one-minute load average.
- **Load5**
Load5 denotes the five-minute load average.
- **Load15**
Load15 displays the 15-minute load average.
- **Total Accesses**
The total number of accesses on the server is monitored using the metric total_accessess.
- **Total Connections**
Total Connections depicts the total number of connections on the Apache server.
- **Total kbytes**
Total kbytes records the total kilobytes served.
- **Uptime**
Uptime shows the total amount of time the server has been up and running.
- **Version**
Version denotes the Apache server version.

## Prerequisites
- Ensure the latest version of the Site24x7 Linux Server Monitoring agent is installed in the server where you plan to run the plugin.
- Status module mod_status should be enabled for the server to be available at http://localhost:80/server-status.

## Automatic Applogs Integration Configuration
To analyze the metrics with Apache logs and find the exact root cause of issues, you can perform configuration changes in the apache_monitoring.cfg file.

**Example:**
   logs_enabled = true
   log_type_name = "Apache Access Logs"
   log_file_path = "/var/log/apache2/access.log"
