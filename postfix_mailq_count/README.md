Plugin for Monitoring the Postfix Mail Queue Count
==================================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin.

- Download and install Python version 3 or higher.

- Plugin Uses "mailq" command to get the count in mailq and "qshape" to get the counts of each queue names.

### Plugin installation
---
##### Linux 

- Create a directory "postfix_mailq_count".

- Download the file "postfix_mailq_count.py" and place it under the "postfix_mailq_count" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/postfix_mailq_count/postfix_mailq_count.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the postfix_mailq_count.py script.
		
- Move the directory "postfix_mailq_count" under Site24x7 Linux Agent plugin directory

		 /opt/site24x7/monagent/plugins/
	
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---
  
  mailq_count       - Total Number of messages present in mailq
	deferred_count    - Total Number of deferred messages present in postfix
	active_count      - Total Number of active messages present in postfix
	hold_count        - Total Number of hold messages present in postfix
	incoming_count    - Total Number of incoming messages present in postfix
	bounce_count      - Total Number of bounce messages present in postfix
	corrupt_count     - Total Number of corrupted messages present in postfix
