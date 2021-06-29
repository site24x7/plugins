Plugin for Monitoring the Postfix Mail Queue Count
==================================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "mailq" command to get the count in mailq and "qshape" to get the counts of each queue names.

### Plugin installation
---
##### Linux 

- Create a directory "postfix_mailq_count" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/postfix_mailq_count

- Download the file "postfix_mailq_count.py" and place it under the "postfix_mailq_count" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/postfix_mailq_count/postfix_mailq_count.sh
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Metrics Captured
---

mailq_count       - Total Number of messages present in mailq
deferred_count    - Total Number of deferred messages present in postfix
active_count      - Total Number of active messages present in postfix
hold_count        - Total Number of hold messages present in postfix
incoming_count    - Total Number of incoming messages present in postfix
bounce_count      - Total Number of bounce messages present in postfix
corrupt_count     - Total Number of corrupted messages present in postfix
