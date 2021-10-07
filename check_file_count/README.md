Plugin for monitoring File count and File size
==============================================

This plugin is to check the size of the directory , number of files in the directory and number of folders in the directory.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

---
### Plugin Installation

##### Linux

- Create a directory "check_file_count" under Site24x7 Linux Agent plugin directory : 

        Linux             ->   /opt/site24x7/monagent/plugins/check_file_count
        
##### Windows 

- Create a directory "check_file_count" under Site24x7 Windows Agent plugin directory : 

      Windows           ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\check_file_count

---
- Download all the files in "check_file_count" folder and place it under the "check_file_count" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_file_count/check_file_count.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/check_file_count/check_file_count.cfg

- Execute the below command with appropriate arguments to check for the valid json output.  

		python check_file_count.py --folder_name=<folder_path> 


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.


### Configurations

		[check_file_count]
		folder_name=<folder_path>
		
### Metrics monitored



		directory_count                    ->	 Number of folder in the giver directory.
		file_count		            ->  Number of files in the given directory.
		directory_size                     ->	 Size of the given directory (MB).


