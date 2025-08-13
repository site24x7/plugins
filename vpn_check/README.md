# VPN Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `vpn_check`.
  
```bash
mkdir vpn_check
cd vpn_check/
```
      
- Download below files and place it under the "vpn_check" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/vpn_check/vpn_check.py 

wget https://raw.githubusercontent.com/site24x7/plugins/master/vpn_check/vpn_check.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 vpn_check.py --host localhost --port 943 --url 'https://localhost:943/admin' --vpn_interface 'None'
```

- Provide your vpn_check configurations in vpn_check.cfg file.

#### For linux

```bash
[global_configurations]
use_agent_python=1

[vpn_check]
host=localhost
port=943
url=https://localhost:943/admin
vpn_interface=None
```

#### For windows

```bash
[vpn_check]
host='localhost'
port='943'
url='https://localhost:943/admin'
vpn_interface='None'
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "vpn_check" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv vpn_check /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "vpn_check" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## VPN Server Monitoring Plugin Metrics

| **Metric Name**       | **Description**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| VPN Status             | Shows whether the VPN server is reachable (`1` for reachable, `0` for unreachable). |
| VPN Connected          | Indicates if the VPN interface is active on the machine (`1` for connected, `0` for disconnected). |
| Packet Loss            | The percentage of packet loss detected while pinging the VPN server.            |
| Latency                | Average round-trip latency (ping time) to the VPN server. |
| URL Response Time      | Time taken to get a response from the specified URL behind the VPN. |
| URL Status Code        | HTTP status code received when accessing the URL behind the VPN.               |
| ISP                    | The name of the Internet Service Provider (ISP) detected for the current public IP. |

## Sample Image
![image](https://github.com/user-attachments/assets/53e207bf-281a-4f9c-acfa-25b520e7ef86)
