# Plugin for monitoring Windows Scheduled tasks

Monitor the status of scheduled tasks in Windows Task Scheduler with the Windows Scheduled Tasks plugin. Leverage the plugin to track the task's status, view meta information, and ensure the success of its execution.

## Metrics
Track the following metrics with the plugin:

| Metric Name   | Description                                       |
| ------------- | ------------------------------------------------- |
| lastRunBefore |  Time of Previous Schedule task performed.        |
| author        |  Task's owner.                                    |
| Status        |  Current state of the task                        |
| lastRunTime   |  Previous Datetime of Task Scheduled.             |
| Start_Date    |  Task Started time                                |
| errorCode     |  Error code of Previous Scheduled task.           |

## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder "ScheduledTask".

2. Download all the files in "ScheduledTask" folder and place it under the "ScheduledTask" directory.

```
wget https://raw.githubusercontent.com/site24x7/plugins/master/ScheduledTask/ScheduledTask.ps1

wget https://raw.githubusercontent.com/site24x7/plugins/master/ScheduledTask/ScheduledTask.cfg
```

3. Modify the ScheduledTask.cfg file with the task name to monitor the particular task.


   For example:

```
[Scheduled_task]
taskName="\OfficeSoftwareProtectionPlatform\SvcRestartTask"
```

  **NOTE:**
  To fill in the task name in the .cfg file, add the location of the task you want to monitor from the General tab of Windows Task Scheduler followed by    a slash and the task name.


4. To monitor multiple tasks, modify the .cfg file accordingly. 

Here's an example below:

```
[Scheduled_task1]
taskName="\OfficeSoftwareProtectionPlatform\SvcRestartTask"

[Scheduled_task2]
taskName="\Microsoft\Windows\AppId\Work Room"
```

5. Further move the folder "ScheduledTask" into the  Site24x7 Windows Agent plugin directory:

```
    Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\ScheduledTask
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

