# Plugin for monitoring Windows Schedule task

The plugins will helps to monitor the below metrics of Scheduled tasks. 

## Metrics details
| Metric Name   | Description                                       |
| ------------- | ------------------------------------------------- |
| lastRunBefore |  Time of Previous Schedule task performed.        |
| author        |  Task's owner.                                    |
| Status        |  Current state of the task                        |
| lastRunTime   |  Previous Datetime of Task Scheduled.             |
| Start_Date    |  Task Started time                                |
| errorCode     |  Error code of Previous Scheduled task.           |

To monitor multiple scheduled tasks, please update in the ScheduleTask.cfg file with task name.
