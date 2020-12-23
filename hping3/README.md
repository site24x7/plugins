Plugin for monitoring the packet transmission details using hping3
===================================================================

Hping is a command-line oriented TCP/IP packet assembler/analyzer. The interface is inspired to the ping(8) unix command, but hping isn't only able to send ICMP echo requests. It supports TCP, UDP, ICMP and RAW-IP protocols, has a traceroute mode, the ability to send files between a covered channel, and many other features. This plugin is used to monitor the packet transmission in the host.  

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses the subprocess modules to execute the hping3 command.

- How to install libvirt :

		apt-get install hping3
		
For more details on the hping3 library , refer http://wiki.hping.org/94. 


### Plugin installation
---
##### Linux 

- Create a directory "hping3" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/hping3

- Download all the files in "hping3" folder and place it under the "hping3" directory

	  wget https://raw.githubusercontent.com/site24x7/plugins/master/hping3/hping3.py
	  wget https://raw.githubusercontent.com/site24x7/plugins/master/hping3/hping3.cfg
	
- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.  

		python hping3.py --host "localhost" --plugin-version "1" --heartbeat "True"


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations
---

	host - Host to be monitored
	plugin_version = 1
	heartbeat = True

### Metrics Captured
---
		packets loss - Total number of packets lost 
		packets received - Total number of packets received 
		packets transmitted -  Total number of packets transmitted
		rt max -  Max time taken for the round trip
		rt min -  Min time taken for the round trip
		rt avg -  Avg time taken for the round trip
		host -  Hostname
