# Plugin for monitoring Windows Port

Monitor the status of specific network ports and associated processes on Windows systems using the Windows Port Check plugin.

## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder `WindowsPortCheck`.

2. Download the files [WindowsPortCheck.ps1](https://github.com/site24x7/plugins/blob/master/WindowsPortCheck/WindowsPortCheck.ps1), [WindowsPortCheck.cfg](https://github.com/site24x7/plugins/blob/master/WindowsPortCheck/WindowsPortCheck.cfg) and place it under the `WindowsPortCheck` folder.

3. Modify the WindowsPortCheck.cfg file with the port number to monitor the particular port.


For example:

```
[port_check]
portNumber=80
```

4. To manually verify if the plugin is functioning correctly, navigate to the `WindowsPortCheck` folder in terminal (Command Prompt) and run the following command:
```
powershell .\WindowsPortCheck.ps1 -portNumber 80
```
Replace `80` with your specific port number.

5. To monitor multiple ports, modify the .cfg file accordingly. 

Here's an example below:

```
[port_check1]
portNumber=80

[port_check2]
portNumber=443
```

6. Further move the folder `WindowsPortCheck` into the  Site24x7 Windows Agent plugin folder:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Metrics
Track the following metrics with the plugin:

| Metric Name           | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| Port Processes       | The number of unique processes currently listening on the specified port.   |
| Port CPU Usage       | The total CPU usage percentage of all processes using the specified port.   |
| Port Memory Usage    | The total memory consumed (in MB) by all processes using the port.          |
| Port Status Text      | Indicates whether the specified port is currently open or closed.           |


## Sample Images

![image](https://github.com/user-attachments/assets/dc2fcb17-38d7-4d82-af9c-692f06448b25)
