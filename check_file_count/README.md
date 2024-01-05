Plugin for monitoring File count and File size
==============================================

This plugin is to check the size of the directory , number of files in the directory and number of folders in the directory.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

---
### Plugin Installation

- Create a directory "check_file_count".

- Download all the files in "check_file_count" folder and place it under the "check_file_count" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_file_count/check_file_count.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_file_count/check_file_count.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python check_file_count.py --folder_name="folder_path"


#### Configurations
- Edit the check_file_count.cfg file with appropriate arguments

		[check_file_count]
		folder_name="folder_path"
#### Linux

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the check_file_count.py script.

- Place the "check_file_count" under the Site24x7 Linux Agent plugin directory:

        Linux    ->   /opt/site24x7/monagent/plugins/check_file_count

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further move the folder "check_file_count" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\check_file_count


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


		
### Metrics monitored



		directory_count                    ->	 Number of folder in the giver directory.
		file_count		           ->  Number of files in the given directory.
		directory_size                     ->	 Size of the given directory (MB).


