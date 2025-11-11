# Starlink dish Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- You must have starlink-grpc-tools installed and 'starlink_grpc' binary available.
  ```bash
	pip3 install grpcio grpcio-tools
  ```
- https://github.com/sparky8512/starlink-grpc-tools

### Plugin Installation  

- Create a directory named `starlink_dish_monitoring`.
  
```bash
mkdir starlink_dish_monitoring
cd starlink_dish_monitoring/
```
      
- Download below files and place it under the "starlink_dish_monitoring" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/starlink/starlink_dish_monitoring/starlink_dish_monitoring.py && sed -i "1s|^.*|#! $(which python3)|" starlink_dish_monitoring.py
wget https://raw.githubusercontent.com/site24x7/plugins/starlink/starlink_dish_monitoring/starlink_dish_monitoring.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 starlink_dish_monitoring.py --starlink_grpc_path "/usr/local/bin/starlink_grpc" --dish_address "localhost"
```

- Provide your starlink_dish_monitoring configurations in starlink_dish_monitoring.cfg file.

```bash
[starlink_dish_1]
starlink_grpc_path='/usr/local/bin/starlink_grpc'
dish_address='localhost'
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "starlink_dish_monitoring" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv starlink_dish_monitoring /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "starlink_dish_monitoring" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
