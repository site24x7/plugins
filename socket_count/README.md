Plugin for Monitoring the TCP/UDP Port counts
==============================================

### PreRequisites
- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "ss -s" command to get the tcp / udp count	
	
- Plugin Uses command line json parser 'jq' to provide the output in json
      To install this utitlity
      For Ubuntu , Debian use the command -> apt-get install jq
      For Redhat , Centos use the comman -> yum install jq


### Plugin installation
---
##### Linux 

- Create a directory "socket_count".

- Download the file "socket_count.py" and place it under the "socket_count" directory
  
		wget https://raw.githubusercontent.com/site24x7/plugins/master/socket_count/socket_count.sh
		
- Execute the below command to check for the valid json output.

		sh socket_count.sh
  
- Move the directory "socket_count" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/
	
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---

tcp_total - total tcp connections

udp_total - total udp connections

tcp_ip - total tcp connections ( ipv4 )

tcp_ipv6 - total tcp connections ( ipv6 )

udp_ip - total udp connections ( ipv4 )

udp_ipv6 - total udp connections ( ipv6 )
