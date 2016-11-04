# Plugin for Monitoring statsd

Monitor your statsd server metrics.

### statsd Plugin installation
---
##### Linux 

- Create a directory "statsd" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/statsd
- Download the file "statsd.py" and place it under the "statsd" directory

##### Windows
 
- Create a directory "statsd" under Site24x7 Linux Agent plugin directory - C:\Program Files\Site24x7\WinAgent\monitoring\Plugins\statsd
- Download the file "statsd.py" and place it under the "statsd" directory
- Download "statsd.ps1" and place it under "statsd" directory
- Replace `$python="C:\Python27\python.exe"` in "statsd.ps1" file with your python path `$python=<python exe path>`

### etcd_self Plugin configurations
---

- `host = "localhost" `  The statsd server host to monitor.
- `port = 8126` The port of statsd server

### statsd Metrics
---

Name		            	| Description
---         		   	 	|   ---
health						| health status of statsd
messages.last_msg_seen		| the number of elapsed seconds since statsd received a message
messages.bad_lines_seen		| the number of bad lines seen since startup
gauges.count			 	| count of all the current gauges
timers.count				| count of all the current timers
counters.count				| count of all the current counters
uptime			    		| statsd server uptime
graphite.flush_length		| the length of the string sent to graphite
graphite.last_exception		| unix timestamp of last exception thrown whilst flushing to graphite
graphite.flush_time			| the time it took to send the data to graphite
graphite.last_flush			| unix timestamp of last successful flush to graphite