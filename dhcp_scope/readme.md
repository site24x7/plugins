# Plugin for DHCP scope monitoring


## **Prerequisites**

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder `dhcp_scope`.

2. Download the files [dhcp_scope.ps1](https://github.com/site24x7/plugins/blob/master/dhcp_scope/dhcp_scope.ps1), [dhcp_scope.cfg](https://github.com/site24x7/plugins/blob/master/dhcp_scope/dhcp_scope.cfg) and place it under the `dhcp_scope` folder.


3. Modify the dhcp_scope.cfg file with the scope id to monitor the particular DHCP scope.

   For example:

    ```
    [dhcp_scope]
    Scope_ID="192.168.255.0"
    ```

4. To manually verify if the plugin is functioning correctly, navigate to the `dhcp_scope` folder in terminal (Command Prompt) and run the following command:
    ```
    powershell .\dhcp_scope.ps1 -Scope_ID '192.168.255.0'
    ```
   Replace `192.168.255.0` with your specific scope id.

5. To monitor multiple tasks, modify the .cfg file accordingly. 

   Here's an example below:

    ```
    [dhcp_scope-255.0]
    Scope_ID="192.168.255.0"
    
    [dhcp_scope-50.0]
    Scope_ID="192.168.50.0"
    ```

6. Further move the folder `dhcp_scope` into the  Site24x7 Windows Agent plugin folder:

    ```
    C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
    ```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## Metrics
Track the following metrics with the plugin:

| Metric Name              | Description                                                                   |
|--------------------------|-------------------------------------------------------------------------------|
|Free                      | Number of available IP addresses in the scope                                 |
|In Use                    | Number of actively assigned IP addresses                                      |
|Percentage In Use         | Percentage of scope utilization                                               |
|Reserved                  | Number of reserved IP addresses                                               |
|Pending                   | Number of pending lease requests                                              |  
|Scope Id                  | Network identifier for the DHCP range                                         |
