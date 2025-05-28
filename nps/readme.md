# Network Policy Server Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `nps`.
  
```bash
mkdir nps
cd .\nps\
```
      
- Download below files and place it under the "nps" directory.

```bash
https://github.com/site24x7/plugins/blob/master/nps/nps.ps1
```

- Execute the below command to check for the valid json output:

```bash
powershell .\nps.ps1
```


### Move the plugin under the Site24x7 agent directory

- Move the "nps" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

# Network Policy Server Monitoring Metrics

| **Metric**                         | **Description**                                                                 |
|-----------------------------------|---------------------------------------------------------------------------------|
| `Connection per Second`           | Number of access requests received per second by the NPS server.               |
| `Total Connections`               | Total number of access requests received by the NPS server.                    |
| `Rejected Connection Attempts`    | Number of access requests rejected by the server.                              |
| `Successful Connection Attempts`  | Number of access requests accepted by the server.                              |
| `Packets Received`                | Total RADIUS packets received by the server.                                   |
| `Packets Sent`                    | Total RADIUS packets sent by the server.                                       |
| `Malformed Packets Received`      | Number of malformed RADIUS packets received.                                   |
| `Accounting Requests`             | Total number of accounting requests received by the NPS server.                |
| `Accounting Requests per Second`  | Number of accounting requests received per second.                             |


## Sample Image

![image](https://github.com/user-attachments/assets/9c9d4e04-725c-442b-bcd7-70b37e633a38)
