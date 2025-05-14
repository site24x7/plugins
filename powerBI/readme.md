# Plugin for monitoring PowerBI desktop

Monitor the status and availability of Power BI assets using the Power BI Desktop Check plugin.

## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder `powerBI`.

2. Download the files [powerBI.ps1](https://github.com/site24x7/plugins/blob/master/powerBI/powerBI.ps1), [powerBI.cfg](https://github.com/site24x7/plugins/blob/master/powerBI/powerBI.cfg) and place it under the `powerBI` folder.

3. Modify the powerBI.cfg file with correct credentials.

For example:

```
[PowerBI]
Username="Username" 
Password="Password"
```

4. To manually verify if the plugin is functioning correctly, navigate to the `powerBI` folder in terminal (Command Prompt) and run the following command:
```
powershell .\powerBI.ps1 -Username "username" -Password "password"
```

5. Further move the folder `powerBI` into the  Site24x7 Windows Agent plugin folder:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Metrics
Track the following metrics with the plugin:

| Metric Name         | Description                                                                    |
|---------------------|--------------------------------------------------------------------------------|
| Total Reports       | The number of Power BI reports available in the account.                      |
| Total Datasets      | The number of datasets accessible under the signed-in Power BI account.       |
| Total Dataflows     | The number of Power BI dataflows configured in the account.                   |
| Total Workspaces    | The number of Power BI workspaces available to the user.                      |

## Sample Images

![image](https://github.com/user-attachments/assets/49a4ce42-e767-4b48-ae21-1e93d1555495)
