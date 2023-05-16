# Aerospike Stats Monitoring


                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install aerospike module for python
```
  pip3 install aerospike
```
---



### Plugin Installation  

- Create a directory named "aerospike_stats_monitoring".
      
- Download all the files in the "aerospike_stats_monitoring" folder and place it under the "aerospike_stats_monitoring" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/aerospike_monitoring/aerospike_stats_monitoring/aerospike_stats_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/aerospike_monitoring/aerospike_stats_monitoring/aerospike_stats_monitoring.cfg

- Execute the following command in your server to install aerospike: 

		pip3 install aerospike

- Execute the below command with appropriate arguments to check for the valid json output:

		python3 aerospike_stats_monitoring.py --hostname=<name of the host> --port=<port> --tls_enable=<true/false> --tls_name=<tls name> --cafile=<cafile path>  --username=<username> --password=<password>  --node_id=<node id>


- Move the directory "aerospike_stats_monitoring" under Site24x7 Linux Agent plugin directory.




---

### Configurations

- Provide your aerospike_stats_monitoring configurations in aerospike_stats_monitoring.cfg file.
```
    [Aerospike Stats Monitoring]
    hostname=<HOSTNAME>
    port=<PORT>
    tls_enable=false
    tls_name=None
    cafile=None
    username=<USERNAME>
    password=<PASSWORD>
    node_id=<NODE ID>
    logs_enabled=False
    log_type_name=<LOG TYPE NAME>
    log_file_path=<LOG FILE PATH>
```	

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

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



