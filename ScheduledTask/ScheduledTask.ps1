
<#   
.SYNOPSIS   
Script that returns details of scheduled task

.DESCRIPTION
This script used as Site24x7 Windows Plugin for monitoring specified scheduled task 


Metrics :
----------
lastRunBefore :  Time of Previous Schedule task performed.
author :  Task's owner
Status :  Current state of the task,
lastRunTime :  Previous Datetime of Task Scheduled. 
Start_Date :  Task Started time 
errorCode : Error code of Previous Scheduled task.

Log Report 
----------
Reason :  Error code description


.NOTES
Name: ScheduledTask.ps1
Author: Hisham Thorakkal , Zoho Corp
DateCreated: 2016-10-05
Site: http://www.site24x7.com

Requires -Version 3.0
#>

param([string]$taskName)

Function GetErrorMessage
([int]$errorcode)

{
    $msg = ""
    switch($errorcode)
    {
        0 { $msg="The operation completed successfully";break}
        1 { $msg="Incorrect function called or unknown function called. (did you use the correct start in folder and/or environment path for the bat/exe?)";break}
        2 { $msg="File not found.";break}
        10 { $msg="The environment is incorrect.";break}
        267008 { $msg="Task is ready to run at its next scheduled time.";break}
        267009 { $msg="Task is currently running.";break}
        267010 { $msg="Task is disabled.";break}
        267011 { $msg="Task has not yet run.";break}
        267012 { $msg="There are no more runs scheduled for this task.";break}
        267014 { $msg="Task is terminated.";break}
        2147750671 { $msg="Credentials became corrupted (*)";break}
        2147750687 { $msg="An instance of this task is already running.";break}
        2147942402 { $msg="Basically something like file not available (2147942402)";break}
        2147942667 { $msg="Action 'start in' directory can not be found.";break}
        2147943645 { $msg="The service is not available (is 'Run only when an user is logged on' checked?)";break}
        3221225786 { $msg="The application terminated as a result of a CTRL+C.";break}
        3228369022 { $msg="Unknown software exception.";break}
        default {"Something else happened"; break}
    }
    return $msg
}

Function Get-ScheduledJobDetails($jobName)
{
    $ret = New-Object -TypeName PSObject
    $attributeList = @("TaskName","Author","Scheduled Task State","Start Date","Next Run Time","Status","Last Run Time","Last Result")
    $jobDetails  = schtasks /QUERY /FO LIST /V /TN $jobName
    foreach($attribute in $attributeList)
    {
        $temp = ($jobDetails | Select-String -Pattern $attribute| Select-Object -Last 1).ToString()
        $key,$value = $temp.Split(':',[StringSplitOptions]"None")
        $key = ($key.trim()).Replace(' ',"_");
        $value = ($value -join ':').trim()
        $ret | Add-Member -Type NoteProperty -Name $key -Value $value
    }
    return $ret
}



#data collection 
$data = @{}


$task = Get-ScheduledJobDetails $taskName 
$task2= Get-ScheduledTaskInfo $taskName

$author = $task.Author
$data.Add("author",$author)
$Start_Date = $task.Start_Date
$data.Add("Start_Date",$Start_Date)
#$statestr = $task.Status
#$data.Add("Status",$statestr.ToString())
$lastRunTime = $task.Last_Run_Time
$data.Add("lastRunTime",$lastRunTime)
$lastTaskResult = $task.Last_Result
$data.Add("errorCode",$lastTaskResult)

$status=$task.Status
if($status -eq "Ready"){
$value_status=3
}

if($status -eq "Disabled"){
$value_status=1
}

if($status -eq "Queued"){
$value_status=2
}

if($status -eq "Running"){
$value_status=4
}


$data.Add("state_value",$value_status)
 

$data.Add("numberOfMissedRuns",$task2.NumberOfMissedRuns)




$timenow = Get-Date
$timespan  = NEW-TIMESPAN -Start $lastRunTime -End $timenow

$timediff = $timespan.Days.ToString() + " Days "+ $timespan.Hours.ToString() + " Hours " + $timespan.Minutes.ToString() + " Minutes " + $timespan.Seconds.ToString() + " Seconds " 
$data.Add("lastRunBefore",$timediff)

#Site24x7 Plugin Metrics 

$version = "1"

$displayname = "Monitor Task - " + $taskName

$heartbeat = "True"

$mainJson = @{}

$mainJson.Add("version",$version)
$mainJson.Add("displayname",$displayname)
$mainJson.Add("heartbeat",$heartbeat)
$mainJson.Add("data",$data)
if($lastTaskResult -ge 0)
{
    $msg = GetErrorMessage($lastTaskResult)
    $mainJson.Add("msg",$msg)
}
$mainJson | ConvertTo-Json
