# Oracle Custom Query Mutiple row Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.7 or higher version should be installed.
- Install **oracledb** module for python

  ```
  pip3 install oracledb
  ```
## Plugin Installation  

- Create a directory named `oracle_custom_query_muti_row`.
  
```bash
mkdir oracle_custom_query_muti_row
cd oracle_custom_query_muti_row/
```
      
- Download below files under the `oracle_custom_query_muti_row` directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query_muti_row/oracle_custom_query_muti_row.py && sed -i "1s|^.*|#! $(which python3)|" oracle_custom_query_muti_row.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query_muti_row/oracle_custom_query_muti_row.cfg
wget https://raw.githubusercontent.com/site24x7/plugins/master/oracle_custom_query_muti_row/query.sql
```

- Enter your custom query in the `query.sql` file.

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 oracle_custom_query_muti_row.py --hostname "localhost" --port "1521" --sid "xe" --username "site" --password "plugin" 
```

- Provide your oracle_custom_query_muti_row configurations in oracle_custom_query_muti_row.cfg file.

```ini
[oracle]
hostname="localhost"
port="1521"
sid="xe"
username="site"
password="plugin"
oracle_home="None"

```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the `oracle_custom_query_muti_row` directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv oracle_custom_query_muti_row /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the `oracle_custom_query_muti_row` directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

After the first execution, an file will be created:

- **`query_output*.txt`** - Stores the query output data.

**File Locations:**

- **Linux**: `/opt/site24x7/monagent/plugins/oracle_custom_query_muti_row`
- **Windows**: `C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\oracle_custom_query_muti_row`

## Creating a Custom Log Type

1. Use `query_output*.txt` to define a custom log type:
   - Follow [this guide](https://www.site24x7.com/help/log-management/add-log-type.html) to set up a custom log type.
   
2. Configure a log profile for the new log type:
   - Refer to [this guide](https://www.site24x7.com/help/log-management/add-log-profile.html) to create a log profile.

3. **Map the Log File Paths** for log tracking:

   - **Linux**: `/opt/site24x7/monagent/plugins/oracle_custom_query_muti_row/query_output*`
   - **Windows**: `C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\oracle_custom_query_muti_row\query_output*`

Once the custom app logs are set up, you will be able to continuously monitor your query outputs in Site24x7.
