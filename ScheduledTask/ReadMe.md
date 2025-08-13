# Plugin for monitoring Windows Scheduled tasks

Monitor the status of scheduled tasks in Windows Task Scheduler with the Windows Scheduled Tasks plugin. Leverage the plugin to track the task's status, view meta information, and ensure the success of its execution.

## Metrics
Track the following metrics with the plugin:

| Metric Name              | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Error Code               | The code representing any error encountered during task execution.           |
| Last Result              | The outcome of the last task execution.                                      |
| Number Of Missed Runs     | The count of scheduled task runs that were missed.                          |
| State Value              | The current state of the task.                                               |
| Task Age                 | The amount of time since the task was created.                               |
| Author                   | The user or entity that created the task.                                    |
| End Date                 | The date when the task is set to stop running.                               |
| Idle Time                | The amount of time the task stays idle before running.                       |
| Last Run Before           | The timestamp of the task's last run before the current one.                |
| Last Run Time            | The exact time of the most recent execution of the task.                     |
| Logon Mode               | The mode or type of user login required for task execution.                  |
| Next Run Time            | The scheduled time for the task's next execution.                            |
| Repeat-Every             | The interval at which the task is scheduled to repeat.                       |
| Run As User              | The user account under which the task runs.                                  |
| Schedule                 | The specific time or conditions when the task is scheduled to run.           |
| Schedule Type            | The method or type of scheduling.                                            |
| Scheduled Task State     | The status of the task in the scheduler.                                     |
| Start Date               | The date when the task is first scheduled to run.                            |
| Start In                 | The folder or directory where the task runs.                                 |
| Start Time               | The time of day when the task is scheduled to start.                         |
| State                    | The real-time state of the task.                                             |
| Status                   | The overall health or status of the task.                                    |
| Task Name                | The descriptive name given to the task.                                      |
| Task To Run              | The specific script or program that the task executes.                       |


## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder `ScheduledTask`.

2. Download the files [ScheduledTask.ps1](https://github.com/site24x7/plugins/blob/master/ScheduledTask/ScheduledTask.ps1), [ScheduledTask.cfg](https://github.com/site24x7/plugins/blob/master/ScheduledTask/ScheduledTask.cfg) and place it under the `ScheduledTask` folder.

3. Modify the ScheduledTask.cfg file with the task name to monitor the particular task.


   For example:

```
[Scheduled_task]
taskName='\OfficeSoftwareProtectionPlatform\SvcRestartTask'
```

 **NOTE:**
  To fill in the task name in the .cfg file, add the location of the task you want to monitor from the General tab of Windows Task Scheduler followed by a slash and the task name.

4. To manually verify if the plugin is functioning correctly, navigate to the `ScheduledTask` folder in terminal (Command Prompt) and run the following command:
```
powershell .\ScheduledTask.ps1 -taskName '\OfficeSoftwareProtectionPlatform\SvcRestartTask'
```
Replace `\OfficeSoftwareProtectionPlatform\SvcRestartTask` with your specific task name.

5. To monitor multiple tasks, modify the .cfg file accordingly. 

Here's an example below:

```
[Scheduled_task1]
taskName='\OfficeSoftwareProtectionPlatform\SvcRestartTask'

[Scheduled_task2]
taskName='\Microsoft\Windows\AppId\Work Room'
```

6. Further move the folder `ScheduledTask` into the  Site24x7 Windows Agent plugin folder:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

