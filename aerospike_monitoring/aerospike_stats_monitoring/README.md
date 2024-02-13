# Aerospike Stats Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.
- Install aerospike module for python
```
  pip3 install aerospike
```
---



### Plugin Installation  

- Create a directory named "aerospike_stats_monitoring".

		mkdir aerospike_stats_monitoring
  		cd aerospike_stats_monitoring/
      
- Download all the files in the "aerospike_stats_monitoring" folder and place it under the "aerospike_stats_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/aerospike_monitoring/aerospike_stats_monitoring/aerospike_stats_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/aerospike_monitoring/aerospike_stats_monitoring/aerospike_stats_monitoring.cfg

- Execute the following command in your server to install aerospike: 

		pip3 install aerospike

- Execute the below command with appropriate arguments to check for the valid json output:

		python3 aerospike_stats_monitoring.py --hostname "localhost" --port "3000" --tls_enable "true/false" --tls_name "tls name" --cafile "cafile path"  --username "username" --password "password"  --node_id "node id"

#### Configurations

- Provide your aerospike_stats_monitoring configurations in aerospike_stats_monitoring.cfg file.
    ```
    [Aerospike Stats Monitoring]
    hostname="localhost"
    port="3000"
    tls_enable=false
    tls_name=None
    cafile=None
    username="USERNAME"
    password="PASSWORD"
    node_id="NODE ID"
    logs_enabled=False
    log_type_name="LOG TYPE NAME"
    log_file_path="LOG FILE PATH"
    ```	

#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the aerospike_stats_monitoring.py script.

- Place the "aerospike_stats_monitoring" under the Site24x7 Linux Agent plugin directory:

        mv aerospike_stats_monitoring /opt/site24x7/monagent/plugins/aerospike_stats_monitoring

#### Windows

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

-  Further move the folder "aerospike_stats_monitoring" into the  Site24x7 Windows Agent plugin directory:

        C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\aerospike_stats_monitoring





The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

---

## Supported Metrics
The following metrics are captured in the aerospike_stats_monitoring Plugin

- **Client Connections**

    The number of active client connections to this node

- **Client Connections Opened**

    The number of client connections that are opened

- **Cluster Size**

    Size of the Cluster

- **Fabric Connections Opened**

    The number of active fabric connections to this node


- **Heartbeat Connections Opened**

    The number of active heartbeat connections to this node


- **System Free Mem kbytes**

    Free system memory kb

- **System Free mem %**

    Free system memory in %

- **Batch Index Error**

    The number of batch index requests that were rejected because of errors


- **Heap Efficiency %**

    The heapallocatedkbytes / heapmappedkbytes ratio


- **RW In Progres**

    The number of rw transactions in progress



