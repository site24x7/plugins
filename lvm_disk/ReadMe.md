# LVM monitoring
Logical volume management (LVM) is a form of storage virtualization that offers system administrators a more flexible approach to managing disk storage space than traditional partitioning. This type of virtualization tool is located within the device-driver stack on the operating system.

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
- Download and install Python version 3 or higher.

### Plugin Installation  

- Create a directory named "lvm_disk"

- Download the below files and place it under the "lvm_disk" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/lvm_disk/lvm_disk.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/lvm_disk/lvm_disk.cfg



- Edit the lvm_disk.py file with appropriate arguments and execute the below command to check for the valid JSON output:

		python lvm_disk.py  --vg = '<volume-group>'  --lvm = '<lvm>,<lvm1>'

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the lvm_disk.py script.
- Update the following configurations in lvm_disk.cfg file,
  
		[LVM Disk Space]
		vg = '<Volume Group Name>'
		lvm = '<LVM Name>,<LVM Name>'
		plugin_version = 1 

- For the above configuration,
   - In the vg line, enter the Volume Group Name.
   - In the lvm line, enter the LVM names separated by commas. If you want to monitor only one LVM, give one LVM name without commas.
   - The third line is the plugin version. Increase the value by one if you want to add any additional metrics or to add another LVM after the plugin has been registered successfully. 
- Place the "lvm_disk" folder under Site24x7 Linux Agent plugin directory : 

		Linux             ->   /opt/site24x7/monagent/plugins/lvm_disk
