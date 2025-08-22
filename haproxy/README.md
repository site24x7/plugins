
Plugin for Haproxy Monitoring
  
Get to know how to configure the HAProxy plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of HAProxy servers.


## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.
- Install Pandas library using the following command,

		pip install pandas

---


## Enabling HAProxy Stats  

To enable the HAProxy stats URL, add the following section to your **HAProxy configuration file** (`/etc/haproxy/haproxy.cfg`):

### With Username and Password
```cfg
listen stats
    bind 0.0.0.0:8404
    mode http
    stats enable
    stats uri /stats
    stats realm Strictly\ Private
    stats auth username:password
```

In this case, provide the same credentials in the **plugin configuration file** (`haproxy/haproxy.cfg`):
```ini
[haproxy]
username="username"
password="password"
url="http://localhost:8404/stats;csv"
```

### Without Username and Password
```cfg
listen stats
    bind 0.0.0.0:8404
    mode http
    stats enable
    stats uri /stats
    stats realm Strictly\ Private
```

In this case, update the **plugin configuration file** (`haproxy/haproxy.cfg`) like this:
```ini
[haproxy]
username=None
password=None
url="http://localhost:8404/stats;csv"
```

### Plugin Installation  

- Create a directory named "haproxy"


- Download the below files and place it under the "haproxy" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/haproxy/haproxy.py
  		wget https://raw.githubusercontent.com/site24x7/plugins/master/haproxy/haproxy.cfg

  #### Note:
  	- The cfg file given here is different from the /etc/haproxy/haproxy.cfg. This file is for plugin configuration and used only by site24x7 agent.

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the haproxy.py script.
  
- Execute the below command with appropriate arguments to check for the valid JSON output:
  
	```
	python haproxy.py --username "username" --password "password" --url "http://localhost:8404/stats;csv"
	```

- Example configuration for haproxy.cfg. The password given here will be encrypted.
	```
	[haproxy]
	username="username"
	password="password"
	url="http://localhost:8404/stats;csv"
	logs_enabled="True"
	log_type_name="haproxy"
	log_file_path="/var/log/haproxy.log"
	```

- Move the folder "haproxy" under Site24x7 Linux Agent plugin directory : 

		mv haproxy /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Supported Metrics  

The HAProxy plugin collects the following metrics for monitoring performance, availability, and usage statistics.  

### System Metrics

Name                | Description
---                 | ---
Sys Ttime Max       | Maximum time taken for a session to complete
Sys Agent Status    | Current status of the agent
Sys Cache Lookups   | Number of cache lookups performed
Sys Cache Hits      | Number of successful cache hits
Sys Chkfail         | Number of failed health checks
Sys Hanafail        | Number of failed health checks caused by the agent
Sys Throttle        | Number of requests that were throttled
Sys Check Status    | Status of the latest health check
Sys Check Duration  | Time taken for the latest health check (ms)
Sys Cli Abrt        | Number of data transfers aborted by the client
Sys Srv Abrt        | Number of data transfers aborted by the server
Sys Comp In         | Bytes added to the HTTP compression input
Sys Comp Out        | Bytes emitted by the HTTP compression
Sys Comp Byp        | Bytes that bypassed the compression
Sys Comp Rsp        | Number of HTTP responses compressed
Sys Algo            | Load-balancing algorithm used
Sys Eint            | Total internal errors
Sys Reuse           | Number of connections reused
Sys Wrew            | Number of failed writes due to connection reuse
Sys Mode            | Mode of HAProxy (http/tcp)

---

### Frontend Metrics

Name                       | Description
---                        | ---
Frontend Qcur              | Current queued requests
Frontend Qmax              | Maximum queued requests
Frontend Qtime             | Average queue time in ms
Frontend Ctime             | Average connect time in ms
Frontend Scur              | Current active sessions
Frontend Smax              | Maximum concurrent sessions
Frontend Bin               | Bytes received
Frontend Bout              | Bytes sent
Frontend Dses              | Sessions denied
Frontend Dreq              | Requests denied
Frontend Dcon              | Connections denied
Frontend Ereq              | Request errors
Frontend Econ              | Connection errors
Frontend Wretr             | Retries due to server failure
Frontend Wredis            | Redispatches to a different server
Frontend Rate              | Number of sessions per second
Frontend Rate Max          | Maximum sessions per second
Frontend Req Rate          | HTTP requests per second
Frontend Req Rate Max      | Maximum HTTP requests per second
Frontend Connect           | Connection count
Frontend Conn Rate         | Connections per second
Frontend Conn Rate Max     | Maximum connections per second
Frontend Conn Tot          | Total connections
Frontend Srv Icur          | Current number of idle connections
Frontend Qtime Max         | Maximum queue time in ms
Frontend Ctime Max         | Maximum connect time in ms
Frontend Idle Conn Cur     | Current idle connections
Frontend Safe Conn Cur     | Current safe connections
Frontend Used Conn Cur     | Current used connections
Frontend Need Conn Est     | Estimated needed connections

---

### Backend Metrics

Name               | Description
---                | ---
BACKEND Rtime      | Average response time in ms
BACKEND Rtime Max  | Maximum response time in ms
BACKEND Dresp      | Number of denied responses
BACKEND Eresp      | Number of response errors
BACKEND Act        | Number of active servers
BACKEND Bck        | Number of backup servers
BACKEND Chkdown    | Number of health check failures
BACKEND Lastchg    | Time since last state change (in seconds)
BACKEND Downtime   | Total downtime (in seconds)
BACKEND Lbtot      | Total number of load-balanced requests
BACKEND Hrsp 5Xx   | Number of HTTP 5xx responses
BACKEND Hrsp 4Xx   | Number of HTTP 4xx responses
BACKEND Hrsp 3Xx   | Number of HTTP 3xx responses
BACKEND Hrsp 2Xx   | Number of HTTP 2xx responses
BACKEND Hrsp 1Xx   | Number of HTTP 1xx responses
BACKEND Hrsp Other | Number of other HTTP responses
BACKEND Lastsess   | Time since last session (ms)
BACKEND Cookie     | Cookie usage for persistence

## Sample Images