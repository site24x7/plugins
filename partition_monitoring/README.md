# Plugin for monitoring Disk Partitions

This plugin monitors the disk partitions and gives information about the total size, used size, available size and used percentage.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin installation

---

##### Linux

- Create a directory "partition_monitoring" under Site24x7 Linux Agent plugin directory :

      Linux             ->   /opt/site24x7/monagent/plugins/partition_monitoring

---

- Download all the files using the following commands and place it under the "partition_monitoring" directory

  	wget https://raw.githubusercontent.com/site24x7/plugins/master/partition_monitoring/partition_monitoring.py
      
  	wget https://raw.githubusercontent.com/site24x7/plugins/master/partition_monitoring/partition_monitoring.cfg

- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.

      python partition_monitoring.py --mount_name=<Mount Name in which Disk is mounted on>

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations

---

    [display_name]
    mount_name=<Mount Name>

### Metrics Captured

---

      file_system - The name of the file system
      size - The total size of the file system
      used_size - The total amount of space allocated to existing files in the file system
      available_size - The total amount of space available within the file system for the creation of new files
      used_percentage - The percentage of the space which is currently allocated to all files on the file system
      mounted_on - The directory below which the file system hierarchy appears
