# Plugin for monitoring User session on Windows

Monitor the count of active users, the user's status, and the time of login for Windows servers.

	
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named `WindowsUsersSessionMonitor`.

2. Download the file [WindowsUsersSessionMonitor.ps1](https://github.com/site24x7/plugins/blob/master/WindowsUsersSessionMonitor/WindowsUsersSessionMonitor.ps1) and place them under the `WindowsUsersSessionMonitor` directory.

3. Further move the folder `WindowsUsersSessionMonitor` into the Site24x7 Windows Agent plugin directory:
    ```
    C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
    ```
The agent will automatically execute the plugin within few minutes and user can see the plugin monitor under Site24x7 -> Plugins -> Plugin Integrations.
  
## Supported Metrics

Track the following metrics with the plugin:

Name		        | 	 Description
---         		|   	 ---
active_user 		|	 The total number of active users.
user_status 		|	 Displays the user's status as active or disconnected.
user_logon_logout(1/0) 	|	 Displays 1 if a user is logged in and 0 if auser is logged out.
user_last_logon_time 	|	 Last logged in date and time of the user.
user_idletime 		|	 Displays the idle time of the user.
