Plugin for Monitoring the Postfix Mail Queue Count
==================================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin.

Plugin Uses the following Postfix and system commands:
- "mailq" - Get total message count and message sizes
- "qshape" - Get counts for each queue type (deferred, active, hold, incoming, bounce, corrupt, maildrop)
- "postconf" - Query Postfix configuration (queue directory path)
- "du" - Calculate disk space used by queue directories
- "ps" - Monitor Postfix process CPU usage, memory usage, and process count


### Plugin installation
---
##### Linux 

- Create a directory "postfix_mailq_count".

- Download the file "postfix_mailq_count.py", "postfix_mailq_count.cfg" and place it under the "postfix_mailq_count" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/postfix_mailq_count/postfix_mailq_count.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/postfix_mailq_count/postfix_mailq_count.cfg

- Move the directory "postfix_mailq_count" under Site24x7 Linux Agent plugin directory

		 /opt/site24x7/monagent/plugins/
	
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---

Name		        			| 	Description
---         					|   	---
Total Messages in Queue					|	Total number of messages across all queues
Total Message Size					|	Sum of all message sizes in the queue (KB)
Messages in Deferred Queue				|	Number of messages that failed delivery and are waiting for retry
Messages in Active Queue				|	Number of messages currently being delivered
Messages in Hold Queue					|	Number of messages administratively held from delivery
Messages in Incoming Queue				|	Number of messages being received from network
Messages in Bounce Queue				|	Number of bounce notifications being generated
Messages in Corrupt Queue				|	Number of damaged or unreadable message files
Messages in Maildrop Queue				|	Number of messages in maildrop (injected via sendmail)
Total Queue Size					|	Total disk space used by all queue directories (MB)
Postfix CPU Usage					|	Total CPU usage by all Postfix processes (%)
Postfix Memory Usage					|	Total memory usage by all Postfix processes (%)
Postfix Process Count					|	Number of running Postfix processes
Average Message Size in Queue				|	Average size per message in the queue (KB)

### Sample Image