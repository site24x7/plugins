# Hash Change
 A Plugin to alert when the hash value of a file changes.  It also provides the file size and extension of that file.
	
## Install site24x7 server agent
Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## How to Install Plugin

Create a directory "hash_change" under Site24x7 Agent plugin directory :

### For Linux
	
		Linux -> /opt/site24x7/monagent/plugins/hash_change
		
### For Windows

		Windows -> C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\hash_change
		
### Download the files 

Open terminal inside the hash_change folder created on the above step and execute the below mentioned commands to download the plugin files.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/hash_change/hash_change.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/hash_change/hash_change.cfg
		
### Configuration 

In the hash_change.cfg file, configure the filepath and hashtype to be monitored as mentioned below.

		[display_name]
		filepath="<file_name_that_needs_to_be_monitored_along_with_file_path>"
		hashtype="<hash_type_for_hashing>"	
		hash_storage_path="<storage_path_for_storing_current_hash"
		
## Metrics Captured

		hashing               ->  Provides the hash type of the given file.
		file_type             ->  Provides the extension of the file.
		file_size             ->  Provides size of the file.
		hash_value_changed    ->  Provides 1 if the hash value of the file is changed else 0.
