# The plugin to monitor TCP and UDP connections

The plugin will report the following metrics.

1. Number_of_TCP_connections - 
      The number of TCP connections are listening.

2. Number_of_UDP_connections - 
      The number of UDP connections are listening.
      
### Plugin Installation

#### For Linux servers - 

1. Create a folder named "tcp_udp_connections" under "/opt/site24x7/monagent/plugins/" 

2. Download the file "tcp_udp_connections.py" and place it under the "tcp_udp_connections" directory

3. wget https://raw.githubusercontent.com/site24x7/plugins/master/tcp_udp_connections/tcp_udp_connections.py


#### For Windows servers - 

1. Follow the steps in the below link to run the python plugin in windows.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers

2. Once above steps done, Unzip the tcp_udp_connections.zip and copy the tcp_udp_connections folder under the folder "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins"

Once plugin placed in respective folder, in the next agent data collection, the plugin will be discovered and marked up for monitoring. You can see the monitor under Server > Plugin Integrations.

The plugin monitor "tcp_udp_connections" will also be listed under the respective server monitor's Plugins tab (Server > Server Monitor > Servers > click on the desired server monitor > Plugins). You can also set up threshold profiles and be alerted when the configured value exceeds.
