# Plugin for Monitoring Host Ping

### Plugin installation
---
##### Linux 

- Create a directory "ping_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/ping_check

- Download the files "ping_check.py" and place it under the "ping_check" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/ping_check/ping_check.py

##### Windows

- Create a directory "ping_check" under Site24x7 Windows Agent plugin directory - C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\ping_check

- Download the  "ping_check.py" file and place it under the "ping_check" directory

### Plugin configurations
---

- Configure the Host to be monitored in the file ping_check.py

- Configure INTERFACE_IP if the ping has to be happen via a specific source else leave it to None.

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured
---

- Ping status
- Packet Loss