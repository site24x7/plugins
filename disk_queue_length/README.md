# Plugin for Monitoring Disk Queue Length

This plugin monitors the queue length of disks on server.

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/monitors-configure/SERVER/linux) in the server where you plan to run the plugin.
- Ensure the 'iostat' command is installed in the server to fetch the performance metrics.

### Plugin installation

---

##### Linux

- Create a directory "disk_queue_length".

- Download the files "disk_queue_length.py" and "disk_queue_length.cfg" and place them under "disk_queue_length" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/disk_queue_length/disk_queue_length.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/disk_queue_length/disk_queue_length.cfg

      
-  By default, the plugin will capture the queue length of all disks,  If any specific disk queue length needs to be monitored, provide the disks name seperated by commas in the 'disks' field present in the 'disk_queue_length.cfg' file.

- For example, if 'nvme0n1' and  'dm-0' needs to be monitored, configure as:

		disks = "nvme0n1,dm-0"

- Execute the below command with appropriate arguments to check for the valid json output. for default ( --disks="")

		python disk_queue_length.py --disks="<your_disk_names>"
      
- Move the directory "disk_queue_length" under Site24x7 Linux Agent plugin directory :

		Linux      ->   /opt/site24x7/monagent/plugins/
      
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

