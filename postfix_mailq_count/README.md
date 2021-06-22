Plugin for Monitoring the Postfix Mail Queue Count
==================================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "mailq" command to get the count in mailq.

### Plugin installation
---
##### Linux 

- Create a directory "postfix_mailq_stats" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/postfix_mailq_stats

- Download the file "postfix_mailq_stats.py" and place it under the "postfix_mailq_stats" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/postfix_mailq_count/postfix_mailq_count.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---

mailq_count - Total Number of messages present in mailq
