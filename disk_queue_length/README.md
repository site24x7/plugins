# Plugin for Monitoring Disk Queue Length


### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/monitors-configure/SERVER/linux) in the server where you plan to run the plugin.
- Ensure the 'iostat' command is installed in the server to fetch the performance metrics.

### Plugin installation

---

##### Linux

- Create a directory "disk_queue_length" under Site24x7 Linux Agent plugin directory :

      Linux      ->   /opt/site24x7/monagent/plugins/disk_queue_length

- Download the files "disk_queue_length.py" and "disk_queue_length.cfg" and place them under "disk_queue_length" directory

      wget https://raw.githubusercontent.com/site24x7/plugins/master/disk_queue_length/disk_queue_length.py
      wget https://raw.githubusercontent.com/site24x7/plugins/master/disk_queue_length/disk_queue_length.cfg

- Configure the disks to be monitored in "disk_queue_length.cfg" as mentioned in the configuration section below, by default the plugin will capture the queue length of all disks

- Execute the below command with appropriate arguments to check for the valid json output.

      python disk_queue_length.py --disks="<disks that you want to monitor sepearated by commas>"
      
The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configuration
---
       [display_name]
       disks="<disks that you want to monitor sepearated by commas>"

- Example

      [server-3873]
      disks="nvme0n1,dm-0"
