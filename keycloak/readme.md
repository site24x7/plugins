# Keycloak Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `keycloak`.
  
```bash
mkdir keycloak
cd keycloak/
```
      
- Download below files and place it under the "tomcat" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/keycloak/keycloak.py && sed -i "1s|^.*|#! $(which python3)|" tomcat.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/keycloak/keycloak.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 keycloak.py --host localhost --port 8080 --username admin --password admin --client_id admin-cli
```

- Provide your Tomcat configurations in tomcat.cfg file.

```bash
[Keycloak]
host= "localhost"
port= "8080"
username = "admin"
password = "admin"
client_id = "admin-cli"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "tomcat" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv tomcat /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "tomcat" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Keycloak Server Monitoring Plugin Metrics

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Keycloak Version         | The version of Keycloak currently running on the server.               |
| Server Uptime            | The total time the Keycloak server has been running without a restart. |
| Total Memory             | The total amount of memory available to the Keycloak server.|
| Used Memory              | The amount of memory currently being used by the Keycloak server.|
| Free Memory              | The amount of memory that is currently free and available.  |
| Free Memory Percentage   | The percentage of total memory that is currently free.                 |
| Total Formatted Memory   | The total amount of memory available, formatted for readability.|
| **Used Formatted Memory**    | The amount of memory currently used, formatted for readability.|
| **Free Formatted Memory**    | The amount of memory currently free, formatted for readability.|


