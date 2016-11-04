# Plugin for Supervisord Monitoring

For monitoring supervisord using Site24x7 Server Monitoring Plugins. 

### Prerequisites
---
- Site24X7 Supervisord plugin uses python's "supervisor" package to collect metrics.
    - Installation
    
            pip install supervisor
            easy_install supervisor

- For more detail refer  [How to install supervisor?]

### Supervisord Plugin installation
---
- Create a directory "supervisord" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/supervisord
- Download the file [supervisord.py] and place it under the "supervisord" directory

### Supervisord Plugin configuration
---

- `SERVER_URL = "unix:///var/run//supervisor.sock"`  Give full unix socket path or http server path. eg: http://localhost:9001 or unix:///var/run//supervisor.sock
- `USER_NAME = None` If authentication required, provide username
- `PASSWORD = None`  If authentication required, provide password
- `MONITOR_PROCESS_NAMES = []` List of process to monitor.

### Supervisord Metrics
---

Name				            | Description
---             				|   ---
supervisord_state      			| Status of supervisord server.
total_process_count       		| Total number of process
stopped_process_count       	| Number of stopped process
running_process_count    		| Number of running process
unknown_status_process_count	| Number of process with unknown status

[How to install supervisor?]: <http://supervisord.org/installing.html>
[supervisord.py]: <https://raw.githubusercontent.com/site24x7/plugins/master/supervisord/supervisord.py>