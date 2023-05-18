# The plugin to monitor TCP and UDP connections

The plugin will report the following metrics.

1. Number_of_TCP_connections - 
      The number of TCP connections are listening.

2. Number_of_UDP_connections - 
      The number of UDP connections are listening.
      
### Plugin Installation

- Create a folder named "tcp_udp_connections"

#### For Linux servers - 

- Download the file "tcp_udp_connections.py" and place it under the "tcp_udp_connections" directory using below command 

		wget https://raw.githubusercontent.com/site24x7/plugins/master/tcp_udp_connections/tcp_udp_connections.py

- Move the folder "tcp_udp_connections" under "/opt/site24x7/monagent/plugins/" 

#### For Windows servers - 

- Follow the steps in the below link to run the python plugin in windows.
		https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
		
- Download the file "tcp_udp_connections.py" and place it under the "tcp_udp_connections" directory 

		https://raw.githubusercontent.com/site24x7/plugins/master/tcp_udp_connections/tcp_udp_connections.py

- Move the folder "tcp_udp_connections" under "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins"

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
