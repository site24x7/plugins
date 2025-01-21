# Port Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Install the required Python module psutil by running the following command:
  ```bash
	pip install psutil
```

### Plugin Installation  

- Create a directory named `port`.
  
```bash
mkdir port
cd port/
```
      
- Download below files and place it under the "port" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/port/port.py && sed -i "1s|^.*|#! $(which python3)|" port.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/port/port.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 port.py --port 22
```

- Provide your port configurations in port.cfg file.

```bash
[port_check]
port=22

[port_check2]
port=88
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "port" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv port /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "port" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Port Monitoring Plugin Metrics

| **Metric Name**           | **Description**                                                                 |
|---------------------------|---------------------------------------------------------------------------------|
| **Connection Latency**    | The time taken to establish a connection to the port.         |
| **Cpu Usage**             | The percentage of CPU usage by the processes listening on the port.             |
| **Memory Usage**          | The amount of memory used by the processes listening on the port.       |
| **Active Connections**    | The number of active connections to the port.                                   |
| **Connection Rate**       | The rate of successful connections per second.                                  |
| **Port Status Text**      | Indicates whether the port is open or closed.                                   |
| **Processes Count**       | The number of processes actively using or listening on the port.                |
| **Throughput Sent**       | The total amount of data sent through the port during the monitoring period. |
| **Throughput Received**   | The total amount of data received through the port during the monitoring period. |
| **Port Status**           | Indicates the numeric status of the port (1 for open, 0 for closed).            |

![image](https://github.com/user-attachments/assets/5dbf5907-c25b-458d-9383-f96bd9625359)
