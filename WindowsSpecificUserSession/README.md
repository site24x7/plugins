# Plugin for monitoring User session on Windows

Monitor the specific user's status, and the time of login for Windows servers

	
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named "WindowsSpecificUserSession" under the Site24x7 Windows Agent plugin directory:

    Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsSpecificUserSession

2. Download all the files from the "WindowsSpecificUserSession" folder and place them under the "WindowsSpecificUserSession" directory.

```
wget https://raw.githubusercontent.com/site24x7/plugins/master/WindowsUsersSessionMonitor/WindowsSpecificUserSession.ps1
wget https://raw.githubusercontent.com/site24x7/plugins/master/WindowsUsersSessionMonitor/WindowsSpecificUserSession.cfg
```

3. Modify the WindowsSpecificUserSession.cfg file with the user name to monitor.

```
For example:
[USER_NAME]
UserName="USER_NAME"
```

4. To monitor multiple user, modify the .cfg file accordingly. 

Here's an example below:

```
[USER_NAME1]
UserName="USER_NAME1"

[USER_NAME2]
UserName="USER_NAME2"
```
5. Execute the below command to execute the plugin manually in terminal.

```
.\WindowsSpecificUserSession.ps1 -UserName "USER_NAME1"
```

  The agent will automatically execute the plugin within five minutes and send metrics to the Site24x7 data center.
  
## Supported Metrics

Track the following metrics with the plugin:

	1. user_status - Displays the user's status as active or disconnected
	2. user_logon_logout(1/0) - Displays 1 if a user is logged in and 0 if auser is logged out.
	3. user_last_logon_time - Last logged in date and time of the user 
	4. user_idletime - Displays the idle time of the user.
