# Plugin for Gearman Monitoring

Monitor gearman servers performance.

### Prerequisites
---
- Site24X7 Gearman plugin uses python's "gearman" package to collect metrics.
    - Installation
    
            easy_install gearman
            (OR)
            pip install gearman

- For more detail refer  [How to install gearman?]

### Gearman Plugin installation

##### Linux

---
- Create a directory "gearmanmon" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/gearmanmon
- Download the file [gearmanmon.py] and place it under the "gearmanmon" directory

##### Windows
 
- Create a directory "gearmanmon" under Site24x7 Linux Agent plugin directory - C:\Program Files\Site24x7\WinAgent\monitoring\Plugins\gearmanmon
- Download the file [gearmanmon.py] and place it under the "gearmanmon" directory
- Download [gearmanmon.ps1] and place it under "gearmanmon" directory
- Replace `$python="C:\Python27\python.exe"` in "gearmanmon.ps1" file with your python path `$python=<python exe path>`

### Gearman Plugin configuration
---

- `host = "localhost"`  Gearman host
- `port = 4730` Gearman port

### Gearman Metrics
---

Name            | Description
---             |   ---
workers      	| Number of workers
running			| Number of running jobs
queued       	| Number of queued jobs
unique_tasks    | Number of unique tasks
response_time	| Response time

[gearmanmon.py]: <https://raw.githubusercontent.com/site24x7/plugins/master/gearmanmon/gearmanmon.py>
[gearmanmon.ps1]: <https://raw.githubusercontent.com/site24x7/plugins/master/gearmanmon/gearmanmon.ps1>
[How to install gearman?]: <https://pypi.python.org/pypi/gearman/>
