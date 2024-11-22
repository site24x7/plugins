# Striim Monitoring

Striim is a real-time data integration and streaming platform designed to move, process, and analyze data in real time across various sources and destinations. It is particularly useful for organizations that need to handle large volumes of data continuously and make insights available quickly. 
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `striim`.
  
```bash
mkdir striim
cd striim/
```
      
- Download below files and place it under the "striim" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/striim/striim.py && sed -i "1s|^.*|#! $(which python3)|" striim.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/striim/striim.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 striim.py --host localhost --port 8080 --token "api-token"
```

- Provide your striim configurations in striim.cfg file.

```bash
[striim]
host= "localhost"
port= "9080"
token= "token"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "striim" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv striim /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "striim" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
