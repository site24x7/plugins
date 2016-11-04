
Plugin for collecting number of open files 
==========================================

open-files-linux plugin is used for collecting the stats regarding the number of files currently opened and the total number of files that could be opened
  
open file stats plugin installation:
==============
In order to change the monitoring configurations, go to plugins directory and edit the required plugin file.

For e.g. open\_files\_linux => /opt/site24x7agent/monagent/plugins/open\_files\_linux/open\_files\_linux.py

commands to perform the above steps:

	cd /opt/site24x7/monagent/plugins/
	mkdir open_file_stats
	cd open_file_stats
	wget https://raw.githubusercontent.com/site24x7/plugins/master/open_file_stats/open_file_stats.py


open_files_linux Attributes:
===========================

	open_files	: Number of files that are open. 		
    total_files: Number of files that are present

