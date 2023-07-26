# Plugin for monitoring File metadata

This plugin monitors the collection of File metrics.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent / Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin installation

---

- Create a directory "file_monitoring".

- Download all the files using the following commands and place it under the "file_monitoring" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/file_monitoring/file_monitoring.py
      
		wget https://raw.githubusercontent.com/site24x7/plugins/master/file_monitoring/file_monitoring.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the file_monitoring.py script.

- Configure the keys to be monitored, as mentioned in the configuration section below.

- Execute the below command with appropriate arguments to check for the valid json output.

		python file_monitoring.py --filename="<YOUR FILE NAME>" --hashtype="<HASH TYPE OF YOUR CHOICE>" --search_text="<SEARCH TEXT OF YOUR CHOICE>" --case_sensitive="True"

##### Linux

- Move the directory "file_monitoring" under Site24x7 Linux Agent plugin directory :

		Linux             ->   /opt/site24x7/monagent/plugins/file_monitoring

##### Windows

- Move the directory "file_monitoring" under Site24x7 Windows Agent plugin directory :

		Windows           ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\file_monitoring
      
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Configurations

---

    [display_name]
    filename = "<YOUR FILE NAME>"
    hashtype = "<HASH TYPE OF YOUR CHOICE (OPTIONAL)>"
    search_text = "<SEARCH TEXT OF YOUR CHOICE (OPTIONAL)>"
    case_sensitive = "<True (OPTIONAL - By default 'False')>"

### Metrics Captured

---

      file_size                              ->      Size of the File in KB
      file_index                             ->      Inode Number of the File 
      file_owner_id                          ->      User Identifier of the File
      hash_value_changed                     ->      Boolean value that returns 1 when the hash value of the file changes else 0
      content_match                          ->      If search_text value is None, it will skip content searching, else will return True if there is a match and false if there is no match
      content_occurrence_count               ->      Count of number of times the content occurred
      read_access                            ->      Read Access Enabled
      write_access                           ->      Write Access Enabled
      execution_access                       ->      Execution Access Enabled
      last_access_time                       ->      Last File Accessed Time
      last_modified_time                     ->      Last File Modified Time
      time_since_last_accessed               ->      hours before the file was accessed
      time_since_last_modified               ->      hours before the file was modified
      
