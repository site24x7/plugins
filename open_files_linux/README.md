
Plugin for collecting number of open files 
==========================================

open-files-linux plugin is used for collecting the stats regarding the number of files currently opened and the total number of files that could be opened
  
open file stats plugin installation:
==============

- Create a directory "open_files_linux".

- Open a terminal inside the open_files_linux folder created on the above step and execute the below mentioned commands to download the plugin files.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/open_files_linux/open_files_linux.py

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the open_files_linux.py script.
	
- Configure the PROC_FILE to be monitored in the open_files_linux.py file, as mentioned below.

		PROC_FILE = "/proc/sys/fs/file-nr"

- Execute the below command with appropriate arguments to check for the valid json output.  

		python open_files_linux.py

- Move the directory "open_files_linux" under Site24x7 Linux Agent plugin directory : 

		Linux       ->   /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

open_files_linux Attributes:
===========================

	open_files	: Number of files that are open. 		
	total_files	: Number of files that are present

