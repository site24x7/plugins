# Plugin for monitoring User session on Windows

Monitor the count of active users, the user's status, and the time of login for Windows servers

	
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named "WindowsUsersSessionMonitor" under the Site24x7 Windows Agent plugin directory:

    Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsUsersSessionMonitor

2. Download all the files from the "WindowsUsersSessionMonitor" folder and place them under the "WindowsUsersSessionMonitor" directory.

```
wget https://raw.githubusercontent.com/site24x7/plugins/master/WindowsUsersSessionMonitor/WindowsUsersSessionMonitor.ps1
```

  The agent will automatically execute the plugin within five minutes and send metrics to the Site24x7 data center.
  
## Supported Metrics

Track the following metrics with the plugin:

	1. active_user - The total number of active users.
	2. user_status - Displays the user's status as active or disconnected
	3. user_logon_logout(1/0) - Displays 1 if a user is logged in and 0 if auser is logged out.
	4. user_last_logon_time - Last logged in date and time of the user 
	5. user_idletime - Displays the idle time of the user in minutes.
