# The plugin to monitor TCP and UDP connections

## Metrics Reported

| Metric Name              | Description                                                       |
|--------------------------|-------------------------------------------------------------------|
| `TCP_Listening_Ports`    | Number of TCP ports in the listening state                        |
| `TCP_Packets_Received`   | Number of TCP packets received                       |
| `TCP_Packets_Sent`       | Number of TCP packets sent                       |
| `TCP_Retransmissions`    | Number of TCP segments retransmitted                              |
| `UDP_Listening_Ports`    | Number of UDP ports in the listening state                        |
| `UDP_Datagrams_Received` | Number of UDP datagrams received                                  |
| `UDP_Datagrams_Sent`     | Number of UDP datagrams sent                                      |
| `UDP_Packet_Loss`        | Number of UDP input errors                      |
| `UDP_Dropped_Packets`    | Number of UDP packets dropped due to receive/send buffer issues   |

### Plugin Installation

- Create a folder named "tcp_udp_connections"

#### For Linux servers - 

- Download the file "tcp_udp_connections.py", "tcp_udp_connections.cfg" and place it under the "tcp_udp_connections" directory using below command 
	
		wget https://raw.githubusercontent.com/site24x7/plugins/master/tcp_udp_connections/tcp_udp_connections.py
  		wget https://raw.githubusercontent.com/site24x7/plugins/master/tcp_udp_connections/tcp_udp_connections.cfg

- Move the folder "tcp_udp_connections" under "/opt/site24x7/monagent/plugins/" 

#### For Windows servers - 

- Follow the steps in the below link to run the python plugin in windows.
		https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
		
- Download the file "tcp_udp_connections.py" and place it under the "tcp_udp_connections" directory 

		https://raw.githubusercontent.com/site24x7/plugins/master/tcp_udp_connections/tcp_udp_connections.py

- Move the folder "tcp_udp_connections" under "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins"

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
