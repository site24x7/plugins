# Oracle JDE Instance Info Metric Monitoring

Use this Plugin to monitor the status and online users of the JDE Web Server and Rest Server.

## Prerequisites: 

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- After installation of the Site24x7 Windows agent, to run Power shell plugin, ensure the below policy has been set.
- Run the PowerShell prompt as Admin and execute the following 

  ```
  Set-ExecutionPolicy RemoteSigned
  ```

## **Plugin installation**

1. Create a folder named "jde_instance_info".
2. Download the below files and place them under the created "jde_instance_info" directory.
	```
	wget https://raw.githubusercontent.com/site24x7/plugins/master/jde_instance_info/jde_instance_info.ps1
	wget https://raw.githubusercontent.com/site24x7/plugins/master/jde_instance_info/jde_instance_info.cfg
	```
3. The plugin uses "https://example.com:8999/manage/mgmtrestservice/instanceinfometric" api endpoint to fetch the data from the server. Please enable the endpoint if it is blocked.

4. Open the "jde_instance_info.cfg" and enter the url, agentHostName, jde home, etc,. in  the file. Eg:

	```
	[Instance_Info_EXP001]
	url="https://example.com:8999"
	agentHostName = "exp001.example.com"
	jdeHome = "C:\jde_home\SCFHA"
	instanceName = "EXP001"
	username = "Username"
	password = "Password"
	```

5. Further move the folder "jde_instance_info" into the Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\jde_instance_info

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations. 

Note: 
- Please ensure that the agentHostName, jdeHome, instanceName provided are correct. Kindly cross-check the data.

## Supported Metrics

Track the following metrics with the plugin:

	1. InstanceName
	2. InstanceState
	3. TargetType
	4. instanceUptime
	5. nodeName
	6. onlineUsers
	7. userLoginStatus

