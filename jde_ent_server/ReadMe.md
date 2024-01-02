# Oracle JDE ENT Server Instance Monitoring

Use this Plugin to monitor the status and zombie process, etc,. of the jde ENT Server.
## Prerequisites: 

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- After installation of the Site24x7 Windows agent, to run Power shell plugin, ensure the below policy has been set.
- Run the PowerShell prompt as Admin and execute the following 

  ```
  Set-ExecutionPolicy RemoteSigned
  ```

## **Plugin installation**

1. Create a folder named "jde_entserver".
2. Download the below files and place them under the created "jde_entserver" directory.
	```
	wget https://raw.githubusercontent.com/site24x7/plugins/master/jde_entserver/jde_entserver.ps1
	wget https://raw.githubusercontent.com/site24x7/plugins/master/jde_entserver/jde_entserver.cfg
	```
3. The plugin uses "https://example.com:8999/manage/mgmtrestservice/entserverinstanceinfo","/manage/mgmtrestservice/targettype", "/manage/mgmtrestservice/instancestate" api endpoints to fetch the data from the server. Please enable the endpoints if it is blocked.

4. Open the "jde_entserver.cfg" and enter the url, agentHostName, jde home, etc,. in  the file. Eg:

	```
	[Ent_Server_Instance_EXP001]
	url="https://example.com:8999"
	agentHostName = "exp001.example.com"
	jdeHome = "C:\jde_home\SCFHA"
	instanceName = "EXP001"
	username = "Username"
	password = "Password"
	```

5. Further move the folder "jde_entserver" into the Site24x7 Windows Agent plugin directory:

		Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\jde_entserver

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations. 

Note: 
- Please ensure that the agentHostName, jdeHome, instanceName provided are correct. Kindly cross-check the data.

## Supported Metrics

Track the following metrics with the plugin:

	1. InstanceName
	2. InstanceState
	3. TargetType
	4. instanceUptime
	5. networkJobs
	6. kernelJobs
	7. zombieProcesses
	8. securityKernelUsers
	9. callObjectUsers
	10. instanceLevelCPU
	11. intanceLevelMemory





