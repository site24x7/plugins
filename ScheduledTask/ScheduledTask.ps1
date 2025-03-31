<#   
.SYNOPSIS   
Script that returns details of scheduled task

.DESCRIPTION
This script is used as Site24x7 Windows Plugin for monitoring a specified scheduled task.

Metrics :
----------
lastRunBefore :  Time of Previous Schedule task performed.
author :  Task's owner
Status :  Current state of the task,
lastRunTime :  Previous Datetime of Task Scheduled. 
Start_Date :  Task Started time 
Error Code : Error code of Previous Scheduled task.

Log Report 
----------
Reason :  Error code description

.NOTES
Name: ScheduledTask.ps1
DateCreated: 2016-10-05
Site: http://www.site24x7.com

Requires -Version 3.0
#>

param([string]$taskName)

$version = "1"

$taskNameParts = $taskName -split '\\'
$actualTaskName  = $taskNameParts[-1]

$displayname = $actualTaskName  + "-ScheduledTask"
$heartbeat = "True"

if (-not $taskName) {
    $mainJson = @{
        "version" = $version
        "heartbeat" = $heartbeat
        "status" = 0
        "msg" = "Task name is not provided"
    }
    $mainJson | ConvertTo-Json
    exit 1
}

$Status = 1
$status_msg = $null

Function GetErrorMessage
([long]$ErrorCode)
{
    $msg = ""
    switch($ErrorCode)
    {
        0 { $msg="The operation completed successfully";break}
        1 { $msg="An incorrect or unsupported function was called within the task, or a function that is not recognized was executed.";break}
        2 { $msg="The specified file for the task could not be located. This could be due to incorrect file paths or missing files.";break}
        10 { $msg="The environment in which the task or application is running is not set up properly. This could involve system settings, missing dependencies, or incorrect configurations.";break}
        267008 { $msg="The task is scheduled to run but has not yet started. It is waiting for its next scheduled trigger.";break}
        267009 { $msg="Task is currently running.";break}
        267010 { $msg="The task is currently disabled and won't run until re-enabled.";break}
        267011 { $msg="The task has been created or scheduled, but it has not executed yet.";break}
        267012 { $msg="There are no more runs scheduled for this task.";break}
        267014 { $msg="The task was stopped prematurely, likely due to an error or manual termination.";break}
        2147750671 { $msg="Credentials became corrupted (*)";break}
        2147750687 { $msg="Another instance of the task is already executing. The task cannot be started again until the current instance finishes.";break}
        2147942402 { $msg="A required file for the task is unavailable, likely due to missing or inaccessible files.";break}
        2147942667 { $msg="Action 'start in' directory can not be found.";break}
        2147943645 { $msg="The service required for the task is unavailable, possibly due to restrictions like 'Run only when a user is logged on'.";break}
        3221225786 { $msg="The application terminated as a result of a CTRL+C.";break}
        3228369022 { $msg="A software exception occurred while fetching the task, which does not match any predefined error codes. This often indicates an unexpected issue with the application or system.";break}
        267264 { $msg="Task is ready to run at its next scheduled time."; break}
        267265 { $msg="The task is currently running."; break}
        267266 { $msg="The task has been disabled."; break}
        267267 { $msg="The task has not yet run."; break}
        267268 { $msg="There are no more runs scheduled for this task."; break}
        267269 { $msg="One or more of the properties that are needed to run this task have not been set."; break}
        267270 { $msg="The last run of the task was terminated by the user."; break}
        267271 { $msg="Either the task has no triggers or the existing triggers are disabled or not set."; break}
        267272 { $msg="Event triggers do not have set run times."; break}
        -2147418110 { $msg="Call was canceled by the message filter."; break}
        -2147217831 { $msg="A task's trigger is not found."; break}
        -2147217826 { $msg="One or more of the properties required to run this task have not been set."; break}
        -2147217825 { $msg="There is no running instance of the task."; break}
        -2147217824 { $msg="The Task Scheduler service is not installed on this computer."; break}
        -2147217823 { $msg="The task object could not be opened."; break}
        -2147217822 { $msg="The object is either an invalid task object or is not a task object."; break}
        -2147217821 { $msg="No account information could be found in the Task Scheduler security database for the task indicated."; break}
        -2147217820 { $msg="Unable to establish existence of the account specified."; break}
        -2147217819 { $msg="Corruption was detected in the Task Scheduler security database."; break}
        -2147217818 { $msg="Task Scheduler security services are available only on Windows NT."; break}
        -2147217817 { $msg="The task object version is either unsupported or invalid."; break}
        -2147217816 { $msg="The task has been configured with an unsupported combination of account settings and run time options."; break}
        -2147217815 { $msg="The Task Scheduler Service is not running."; break}
        -2147217814 { $msg="The task XML contains an unexpected node."; break}
        -2147217813 { $msg="The task XML contains an element or attribute from an unexpected namespace."; break}
        -2147217812 { $msg="The task XML contains a value which is incorrectly formatted or out of range."; break}
        -2147217811 { $msg="The task XML is missing a required element or attribute."; break}
        -2147217810 { $msg="The task XML is malformed."; break}
        267275 { $msg="The task is registered, but not all specified triggers will start the task."; break}
        267276 { $msg="The task is registered, but may fail to start. Batch logon privilege needs to be enabled for the task principal."; break}
        -2147217803 { $msg="The task XML contains too many nodes of the same type."; break}
        -2147217802 { $msg="The task cannot be started after the trigger end boundary."; break}
        -2147217801 { $msg="An instance of this task is already running."; break}
        -2147217800 { $msg="The task will not run because the user is not logged on."; break}
        -2147217799 { $msg="The task image is corrupt or has been tampered with."; break}
        -2147217798 { $msg="The Task Scheduler service is not available."; break}
        -2147217797 { $msg="The Task Scheduler service is too busy to handle your request. Please try again later."; break}
        -2147217796 { $msg="The Task Scheduler service attempted to run the task, but the task did not run due to one of the constraints in the task definition."; break}
        267277 { $msg="The Task Scheduler service has asked the task to run."; break}
        -2147217795 { $msg="The task is disabled."; break}
        -2147217794 { $msg="The task has properties that are not compatible with earlier versions of Windows."; break}
        -2147217793 { $msg="The task settings do not allow the task to start on demand."; break}
        -2147024894 { $msg="The Task Scheduler cannot find the file."; break}
        -2147020552 { $msg="The operator or administrator has refused the request."; break}
        -1073741514 { $msg="The application terminated as a result of a CTRL+C."; break}
        -1073741502 { $msg="The application failed to initialize properly."; break}
        
        default { 
            return "An error $ErrorCode occurred. Check the scheduled task to troubleshoot.";
            break
        }
    }
    return $msg
}

$culture = Get-Culture

$shortDatePattern = $culture.DateTimeFormat.ShortDatePattern

function Convert-DateWithCultureFormat {
    param (
        [string]$dateString
    )

    try {
        $date = [datetime]::ParseExact($dateString, $shortDatePattern, $culture)
        return $date
    } catch {
        return $null
    }
}


Function Get-ScheduledJobDetails($jobName) {

    try {
        $jobDetails = schtasks /QUERY /FO LIST /V /TN $jobName 2>&1
        if ($jobDetails -match "ERROR: The system cannot find the file specified.") {
            return $null
        }
    } catch {
        return $null
    }

    $jobDetails = schtasks /QUERY /FO LIST /V /TN $jobName
    $details = @{}
    $repeatAttributes = ""
    $lines = $jobDetails -split "rn"
    $inRepeatSection = $false

    foreach ($line in $lines) {
        if ($line -match '^\s*([^:]+):\s*(.*)$') {
            $key = $matches[1].Trim().Replace(' ', ' ')
            $value = $matches[2].Trim()

            if ($key -eq 'Repeat_Attributes') {
                $inRepeatSection = $true
                $repeatAttributes += ($line.Trim() + "rn")
            } elseif ($line -match '^\s*Repeat:') {
                $inRepeatSection = $true
                $repeatAttributes += ($line.Trim() + "rn")
            } else {
                if ($inRepeatSection -and $line -eq "") {
                    $inRepeatSection = $false
                } elseif ($inRepeatSection) {
                    $repeatAttributes += ($line.Trim() + "rn")
                } else {
                    $details[$key] = $value
                }
            }
        }
    }
    
    if ($repeatAttributes) {
        $repeatLines = $repeatAttributes -split "rn"
        foreach ($repeatLine in $repeatLines) {
            if ($repeatLine -match '^\s*Repeat:\s*(.*):\s*(.*)$') {
                $repeatKey = "Repeat-" + $matches[1].Trim().Replace(' ', ' ').Replace(':', '')
                $repeatValue = $matches[2].Trim()
                $details[$repeatKey] = $repeatValue
            }
        }
    }

    if ($details.ContainsKey('TaskName')) {
        $details['Task Name'] = $details['TaskName'] -replace '^\\+', ''
        $details['Task Name'] = $details['TaskName'] -replace '\\$', ''
    }


    if ($details.ContainsKey('Task_To_Run')) {
        $details['Task_To_Run'] = $details['Task_To_Run'] -replace '\\\\', '\'
        $details['Task_To_Run'] = $details['Task_To_Run'] -replace '\"', ''   
    }
    
    return $details
}

$data = @{}

$task = Get-ScheduledJobDetails $taskName

if ($null -eq $task) {
    $mainJson = @{
        "version" = $version
        "heartbeat" = $heartbeat
        "status" = 0
        "msg" = "Task name `"$taskName`" is missing or invalid."
    }
    $mainJson | ConvertTo-Json
    exit 1
}

foreach ($key in $task.Keys) {
    if (-not $data.ContainsKey($key)) {
        $data[$key] = $task[$key]
    }
}

$data["author"] = $data["Author"]

$status_text = $data["Status"]
if ($status_text -eq "Ready") {
    $value_status = 3
} elseif ($status_text -eq "Disabled") {
    $value_status = 1
    $Status = 0
    $status_msg = "The task is disabled"
} elseif ($status_text -eq "Queued") {
    $value_status = 2
} elseif ($status_text -eq "Running") {
    $value_status = 4
}

$data["State Value"] = $value_status
$data["State"] = $data["Status"]

if ($data["Last Result"] -eq "0") {
    $data["Task Fails or Crashes Unexpectedly"] = 0
} else {
    $data["Task Fails or Crashes Unexpectedly"] = 1
}

$task2 = Get-ScheduledTaskInfo $taskName
$data["Number Of Missed Runs"] = $task2.NumberOfMissedRuns

if ($data["Last Run Time"] -eq "N/A" -or [string]::IsNullOrWhiteSpace($data["Last Run Time"])) {
    $data["Last Run Before"] = "-"
} else {
    $timenow = Get-Date
    $timespan = New-Timespan -Start $data["Last Run Time"] -End $timenow
    $timediff = $timespan.Days.ToString() + " Days " + $timespan.Hours.ToString() + " Hours " + $timespan.Minutes.ToString() + " Minutes " + $timespan.Seconds.ToString() + " Seconds "
    $data["Last Run Before"] = $timediff
}


if ($data["Start Date"] -eq "N/A" -or [string]::IsNullOrWhiteSpace($data["Start Date"])) {
    $data["Start Date"] = "-"
} else {
    $startDateString = $data["Start Date"]
    $startDate = Convert-DateWithCultureFormat -dateString $startDateString
    if ($startDate -ne $null) {
        $ageTimespan = New-Timespan -Start $startDate -End $timenow
        $data["Task Age"] = $ageTimespan.Days
    } else {
        $data["Task Age"] = 0
    }
}

if ($data.ContainsKey('TaskName')) {
    $data.Remove('TaskName')
}

if ($data.ContainsKey('HostName')) {
    $data["Host Name"] = $data["HostName"]
    $data.Remove('HostName')
}

$keysToRemove = @(
    "Comment",
    "Days",
    "Months",
    "Repeat-Stop If Still Running",
    "Repeat-Until Duration",
    "Repeat-Until Time",
    "Stop Task If Runs X Hours and X Mins",
    "Delete Task If Not Rescheduled",
    "Host Name",
    "Folder",
    "Status"
)

foreach ($key in $keysToRemove) {
    if ($data.ContainsKey($key)) {
        $data.Remove($key)
    }
}

$working_codes = @(0, 267008, 267009)

$mainJson = @{}
$mainJson["version"] = $version
$mainJson["displayname"] = $displayname
$mainJson["heartbeat"] = $heartbeat
$mainJson["data"] = $data

$mainJson["units"] = @{
    "Task Age" = "days"
}

if ($working_codes -contains $data["Last Result"]) {
    $msg = GetErrorMessage($data["Last Result"])
    if ($Status -eq 0) {
        $mainJson["status"] = 0
    }
    if ( $null -ne $status_msg ) {
        $mainJson["msg"] = $status_msg
    } else {
        $mainJson["msg"] = ($msg | Out-String)
    }
} else {
    $msg = GetErrorMessage($data["Last Result"])
    $err_msg =$msg
    $mainJson["msg"] = $err_msg
    $mainJson["status"] = 0
}

$mainJson | ConvertTo-Json
