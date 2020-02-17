# Plugin for Monitoring File and Directory Count

### Plugin installation
---
### Linux 

- Create a directory "folder_check" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/folder_check

- Download the file "folder_check.py" and place it under the "folder_check" directory
  
  cd /opt/site24x7/monagent/plugins/folder_check

  wget https://raw.githubusercontent.com/site24x7/plugins/master/folder_check/folder_check.py
	
- The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configuration

- Provide the folder to be monitored in FOLDER_NAME field of folder_check.py

- Set INCLUDE_RECURSIVE_FILES as 1 to monitor the file count recursively.

### Metrics Captured

- file_count
- directory_count
