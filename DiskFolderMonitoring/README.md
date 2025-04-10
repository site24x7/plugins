# Disk Folder monitoring #

A plugin to monitor the specfic folder in a disk. For IT operation team, there are critical application folders that they have to 
monitor with the below metrics during operations. This will ensure technicans that whether the critical application folders are in 
idle state or growing beyond the limit or folder runs in usual state. 

## Folder Monitoring Metrics

| Metric Name           | Description                                                             |
|-----------------------|-------------------------------------------------------------------------|
| `Tracking Folder`     | The absolute path of the monitored folder.                              |
| `Folder Size`         | The total size of the folder in gigabytes (GB).                         |
| `Files Count`         | The total number of files present in the folder.                        |
| `Folders Count`       | The total number of subfolders within the monitored folder.             |
| `Files Created`       | The count of new files created within the specified time interval.      |
| `Folders Created`     | The count of new folders created within the specified time interval.    |
| `Files Modified`      | The number of files modified within the specified time interval.        |
| `Folders Modified`    | The number of folders modified within the specified time interval.      |
| `Is Folder Idle`      | Indicates if any changes have occurred within the specified time interval (`0` for changes, `1` for idle). |
    
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder `DiskFolderMonitoring`.

2. Download the files [DiskFolderMonitoring.ps1](https://github.com/site24x7/plugins/blob/master/DiskFolderMonitoring/DiskFolderMonitoring.ps1), [DiskFolderMonitoring.cfg](https://github.com/site24x7/plugins/blob/master/DiskFolderMonitoring/DiskFolderMonitoring.cfg) and place it under the `DiskFolderMonitoring` folder.

3. Modify the DiskFolderMonitoring.cfg file with the folder path to monitor the particular folder.


   For example:

```
[DiskFolderMonitoring]
path="C:\Users\Site24x7Plugins\"
timedifference=5
```

4. To manually verify if the plugin is functioning correctly, navigate to the `DiskFolderMonitoring` folder in terminal (Command Prompt) and run the following command:
```
powershell .\DiskFolderMonitoring.ps1 -path "C:\Users\Site24x7Plugins\" -timedifference "5"
```
Replace `C:\Users\Site24x7Plugins\` and `5` with your specific folder path and time difference.

5. To monitor multiple tasks, modify the .cfg file accordingly. 

Here's an example below:

```
[DiskFolderMonitoring]
path="C:\Users\Site24x7Plugins\"
timedifference=5

[DiskFolderMonitoring2]
path="C:\Users\Site24x7Plugins\Folders"
timedifference=5
```

6. Further move the folder `DiskFolderMonitoring` into the  Site24x7 Windows Agent plugin folder:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
