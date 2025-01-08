# SAP Business Object Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `sap_business_object`.
  
```bash
mkdir sap_business_object
cd sap_business_object/
```
      
- Download below files and place it under the "sap_business_object" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/sap_business_object/sap_business_object.py && sed -i "1s|^.*|#! $(which python3)|" sap_business_object.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/sap_business_object/sap_business_object.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 sap_business_object.py --host localhost --port 6405 --username Administrator --password Admin123 
```

- Provide your sap_business_object configurations in sap_business_object.cfg file.

```bash
[SAPBO]
host = "localhost"
port = "6405"
username = "Administrator"
password = "Admin123"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "sap_business_object" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv sap_business_object /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "sap_business_object" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## SAP Business Object Server Monitoring Plugin Metrics

| **Metric**                          | **Description**                                                                                   |
|-------------------------------------|---------------------------------------------------------------------------------------------------|
| `BILaunchpadAvailability`           | Status of the BI Launchpad (e.g., "Available").                                                  |
| `BILaunchpadResponseTimeMS`         | Response time of the BI Launchpad in milliseconds.                                               |
| `TotalNoOfServers`                  | Total number of servers being monitored.                                                         |
| `TotalNoOfRunningServers`           | Total number of servers currently running.                                                       |
| `TotalNoOfStoppedServers`           | Total number of servers currently stopped.                                                       |
| `TotalNoOfEnabledServers`           | Total number of servers that are enabled.                                                        |
| `TotalNoOfDisabledServers`          | Total number of servers that are disabled.                                                       |
| `connections`                       | List of connections with their respective `name`, `connection_id`, and `connection_folder_id`.   |
| `TotalNoOfConnections`              | Total number of connections.                                                                     |
| `TotalJobsWarning`                  | Total number of jobs in a warning state.                                                         |
| `TotalFailedJobs`                   | Total number of failed jobs.                                                                     |
| `TotalJobs`                         | Total number of jobs.                                                                            |
| `TotalJobsRunning`                  | Total number of jobs currently running.                                                          |
| `TotalJobsExpired`                  | Total number of expired jobs.                                                                    |
| `TotalJobsPending`                  | Total number of pending jobs.                                                                    |
| `TotalJobsSuccess`                  | Total number of successfully completed jobs.                                                     |
| `publications`                      | List of publications with their respective `name`, `publication_id`, and `publication_folder_id`.|
| `TotalNoOfPublications`             | Total number of publications.                                                                    |
| `TotalNoOfUsers`                    | Total number of users in the system.                                                             |
| `TotalNoOfFolders`                  | Total number of folders in the system.                                                           |
| `users`                             | List of users with their respective `name`, `ownerid`, and `parentid`.                           |
| `folders`                           | List of folders with their respective `name`, `folder_id`, and `owner_id`.                       |
| `servers`                           | List of servers with their respective `name`, `status`, `server_process_id`, `enabled`, and IDs. |



## Sample ScreenShot

![Image](https://github.com/user-attachments/assets/f28f0f37-1e76-45eb-9b75-d4afee3a6c9e)
