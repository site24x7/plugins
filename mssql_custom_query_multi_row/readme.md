# MSSQL Custom Query Monitoring

This Plugin will fetch the SQL query output and write it into a log file. The plugin generates a log pattern in a file and writes SQL query output as a log file. After configuring a log profile with a custom pattern matching the generated query output, the plugin pushes the query results to Site24x7 as logs.
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Plugin Installation  

- Create a folder named `mssql_custom_query_multi_row`.
      
- Download the files [mssql_custom_query_multi_row.ps1](https://github.com/site24x7/plugins/blob/master/mssql_custom_query_multi_row/mssql_custom_query_multi_row.ps1), [mssql_custom_query_multi_row.cfg](https://github.com/site24x7/plugins/blob/master/mssql_custom_query_multi_row/mssql_custom_query_multi_row.cfg), [query.sql](https://github.com/site24x7/plugins/blob/master/mssql_custom_query_multi_row/query.sql) and place it under the `mssql_custom_query_multi_row` folder.
  ```bash
  wget https://raw.githubusercontent.com/site24x7/plugins/master/mssql_custom_query_multi_row/mssql_custom_query_multi_row.ps1
  wget https://raw.githubusercontent.com/site24x7/plugins/master/mssql_custom_query_multi_row/mssql_custom_query_multi_row.cfg
  wget https://raw.githubusercontent.com/site24x7/plugins/master/mssql_custom_query_multi_row/query.sql
  ```

- Enter your custom query in the `query.sql` file.


- Provide your configurations in mssql_custom_query_multi_row.cfg file.

  ```ini
  [mssql]
  SQLServer = "test"
  SQLDBName = "product"
  sqlusername = "sa"
  sqlpassword  = "test"
  ```

**Move the plugin under the Site24x7 agent folder**

##### Windows

- Move the **mssql_custom_query_multi_row** folder under the Site24x7 Windows Agent plugin folder:

  ```
  C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
  ```
- The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 -> Plugins -> Plugin Integrations.

- After the first execution, two files will be created:

  - **`log_pattern.txt`** - Contains the query output log pattern.
  - **`query_output*.txt`** - Stores the query output data.

**File Location:**

- **Windows**: `C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mssql_custom_query_multi_row`

## Creating a Custom Log Type

1. Use `log_pattern.txt` and `query_output*.txt` to define a custom log type:
   - Follow [this guide](https://www.site24x7.com/help/log-management/add-log-type.html) to set up a custom log type.
   
2. Configure a log profile for the new log type:
   - Refer to [this guide](https://www.site24x7.com/help/log-management/add-log-profile.html) to create a log profile.

3. **Map the Log File Paths** for log tracking:

   - **Windows**:
   
     ```
     C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\mssql_custom_query_multi_row\query_output*
     ```

Once the custom app logs are set up, you will be able to continuously monitor your query outputs in Site24x7.
