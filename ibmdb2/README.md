# IBM DB2 performance monitoring

Detect database outages and failures faster by monitoring DB2 database with Site24x7 plugins. Use these key indicators to ensure continuous functioning of your DB2 servers.

Get to know how to configure the DB2 plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of IBM DB2 servers.

Learn more https://www.site24x7.com/plugins/db2-monitoring.html

# PREREQUISITES

This plugin works only for IBM DB2 plugin with version upto 10.5.

# Plugin installation
---
## Linux 

- Create a directory "ibmdb2" under Site24x7 Linux Agent plugin directory : 

      Linux       ->   /opt/site24x7/monagent/plugins/ibmdb2

- Open a terminal inside the ibmdb2 folder created on the above step and execute the below mentioned commands to download the plugin files.

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/ibmdb2/ibmdb2.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/ibmdb2/ibmdb2.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the ibmdb2.py script.
	
- Configure the mount point to be monitored in the ibmdb2.cfg file, as mentioned below.

	  [display_name]
	  host 	= "<hostname>"
	  port 	= "<port>"
	  username	= "<username>"
	  password 	= "<password>"
	  sample_db	= "<sample_db>"
	
- Execute the below command with appropriate arguments to check for the valid json output.  

		python ibmdb2.py --host="<hostname>" --port="<port>" --username="<username>" --password="<password>" sample_db="<sample_db>"


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

