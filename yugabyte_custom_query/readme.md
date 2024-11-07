# yugabyte_custom_query Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `yugabyte_custom_query`.
  
```bash
mkdir yugabyte_custom_query
cd yugabyte_custom_query/
```
      
- Download below files and place it under the "yugabyte_custom_query" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/yugabyte_custom_query/yugabyte_custom_query.py && sed -i "1s|^.*|#! $(which python3)|" yugabyte_custom_query.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/yugabyte_custom_query/yugabyte_custom_query.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 yugabyte.py --host "localhost" --port "5433" --username "yugabyte" --password "yugabyte" --db 'demo'
```

- Provide your yugabyte_custom_query configurations in yugabyte_custom_query.cfg file.

```bash
[Demo]
host = "localhost"
port = "5433"
username = "yugabyte"
password = "yugabyte"
db = "demo"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "yugabyte_custom_query" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv yugabyte_custom_query /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "yugabyte_custom_query" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
