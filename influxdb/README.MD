
# **InfluxDB Monitoring**

## About Influxdb
InfluxDB is an open-source time series database developed by InfluxData. It's designed to handle high write and query loads, making it ideal 
for storing, querying, and managing time-stamped data.

### Plugin Installation
- Create a directory named "influxdb" 
  
- Download all the files in the "influxdb" folder.
  ```
  wget https://raw.githubusercontent.com/site24x7/plugins/master/influxdb/influxdb.py && sed -i "1s|^.*|#! $(which python3)|" influxdb.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/influxdb/influxdb.cfg
  ```

- Execute the below command with appropriate arguments to check for the valid json output:
    
        python3 influxdb.py --host_name "hosname or ipaddress" --port "port no" 

- After above command with parameters gives expected output, please configure the relevant parameters in the influxdb.cfg file.

      [influxdb_instance]
      host_name = "localhost"
      port = "8086"

#### Linux

- Place the "influxdb" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/influxdb

#### Windows
        
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "kafka" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\influxdb

## Performance Metrics
Name		            	| 	Description
---         		   	|   	---
influxdb_buckets_total		|	The total number of buckets created in InfluxDB. A bucket is a named location where time series data is stored.
influxdb_dashboards_total		|	The total number of dashboards created. Dashboards are used for visualizing and analyzing time series data in InfluxDB.
