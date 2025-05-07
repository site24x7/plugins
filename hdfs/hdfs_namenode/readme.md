# HDFS NameNode Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `hdfs_namenode`.
  
```bash
mkdir hdfs_namenode
cd hdfs_namenode/
```
      
- Download below files and place it under the "hdfs_namenode" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/hdfs/hdfs_namenode/hdfs_namenode.py && sed -i "1s|^.*|#! $(which python3)|" hdfs_namenode.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/hdfs/hdfs_namenode/hdfs_namenode.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python hdfs_namenode.py --host "hostname" --port "port"
```

- Provide your HDFS NameNode configurations in hdfs_namenode.cfg file.

### For Linux

```bash
[global_configurations]
use_agent_python=1

[hdfs]
host=localhost
port=9870
```

### For Windows

```bash
[HDFS]
host="localhost"
port="9870"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "hdfs_namenode" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv hdfs_namenode /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "hdfs_namenode" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## HDFS NameNode Server Monitoring Plugin Metrics

