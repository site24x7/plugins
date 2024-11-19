# Apache Spark Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `apache_spark`.
  
```bash
mkdir apache_spark
cd apache_spark/
```
      
- Download below files and place it under the "apache_spark" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_spark/apache_spark.py && sed -i "1s|^.*|#! $(which python3)|" apache_spark.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/apache_spark/apache_spark.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 apache_spark.py --host localhost --port 4040
```

- Provide your apache_spark configurations in apache_spark.cfg file.

```bash
[apache_spark]
host= "localhost"
port= "4040"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "apache_spark" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv apache_spark /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "apache_spark" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## apache_spark Server Monitoring Plugin Metrics



