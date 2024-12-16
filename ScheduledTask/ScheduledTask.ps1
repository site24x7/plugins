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
Author: Hisham Thorakkal , Zoho Corp
DateCreated: 2016-10-05
Site: http://www.site24x7.com

Requires -Version 3.0
#>

param([string]$taskName)

$Status = 1
$status_msg = $null

Function GetErrorMessage
([int]$ErrorCode)
{
    $msg = ""
    switch($ErrorCode)
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
        2147943645 { $msg="The service is not available (is 'Run only when a user is logged on' checked?)";break}
        3221225786 { $msg="The application terminated as a result of a CTRL+C.";break}
        3228369022 { $msg="Unknown software exception.";break}
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
        
        default {"Something else happened"; break}
    }
    return $msg
}

$culture = Get-Culture

$shortDatePattern = $culture.DateTimeFormat.ShortDatePattern
$longTimePattern = $culture.DateTimeFormat.LongTimePattern

function Convert-DateWithCultureFormat {
    param (
        [string]$dateString
    )

    try {
        $date = [datetime]::ParseExact($dateString, $shortDatePattern, $culture)
        return $date
    } catch {
        Write-Host "Error parsing the date string."
        return $null
    }
}


Function Get-ScheduledJobDetails($jobName) {
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
foreach ($key in $task.Keys) {
    if (-not $data.ContainsKey($key)) {
        $data[$key] = $task[$key]
    }
}

$data["author"] = $data["Author"]
$data["lastRunTime"] = $data["Last Run Time"]
$data["Error Code"] = $data["Last Result"]

$status = $data["Status"]
if ($status -eq "Ready") {
    $value_status = 3
} elseif ($status -eq "Disabled") {
    $value_status = 1
    $Status = 0
    $status_msg = "The task is disabled"
} elseif ($status -eq "Queued") {
    $value_status = 2
} elseif ($status -eq "Running") {
    $value_status = 4
}

$data["State Value"] = $value_status
$data["State"] = $status

if ($data["Last Result"] -eq "0") {
    $data["Task Fails or Crashes Unexpectedly"] = 0
} else {
    $data["Task Fails or Crashes Unexpectedly"] = 1
}

$task2 = Get-ScheduledTaskInfo $taskName
$data["Number Of Missed Runs"] = $task2.NumberOfMissedRuns

$timenow = Get-Date
$timespan = New-Timespan -Start $data["Last Run Time"] -End $timenow
$timediff = $timespan.Days.ToString() + " Days " + $timespan.Hours.ToString() + " Hours " + $timespan.Minutes.ToString() + " Minutes " + $timespan.Seconds.ToString() + " Seconds "
$data["Last Run Before"] = $timediff

if ($data["Start Date"] -eq "N/A") {
    $data["Start Date"] = "N/A"
} else{
    $startDateString = $data["Start Date"]
    $startDate = [datetime]::ParseExact($startDateString, $shortDatePattern, $culture)
    $ageTimespan = New-Timespan -Start $startDate -End $timenow
    $data["Task Age"] = $ageTimespan.Days
}

if ($data.ContainsKey('TaskName')) {
    $data.Remove('TaskName')
}

if ($data.ContainsKey('HostName')) {
    $data["Host Name"] = $data["HostName"]
    $data.Remove('HostName')
}

if ($data.ContainsKey('lastRunTime')) {
    $data.Remove('lastRunTime')
}

$taskProcessingTimeInSeconds = 0

function ManageInfoFileAndTask {
    param (
        [Parameter(Mandatory=$true)]
        [string]$TaskName
    )

    $filePath = ".\info.txt"

    if (-not (Test-Path $filePath) -or (Get-Content -Path $filePath -Raw).Trim() -eq "") {
        $defaultContent = @{}
        $defaultContent | ConvertTo-Json -Depth 2 | Set-Content -Path $filePath
    }

    $content = Get-Content -Path $filePath -Raw
    $jsonContent = $null

    try {
        $jsonContent = $content | ConvertFrom-Json
    }
    catch {
        $jsonContent = @{}
    }

    
    if (-not ($jsonContent -is [hashtable])) {
           
        $hashtable = @{}
        $jsonContent.PSObject.Properties | ForEach-Object {
            $hashtable[$_.Name] = $_.Value
        }

        $jsonContent = $hashtable
    }

     $global:taskProcessingTimeInSeconds = 0

    if ($jsonContent.ContainsKey($TaskName) -and $data.ContainsKey("Last Run Time")) {
    $previousRunTime = $jsonContent[$TaskName]
    $lastRunTime = $data["Last Run Time"]

    $previousRunTimeDt = $null
    $lastRunTimeDt = $null

    try {
        if (-not [string]::IsNullOrEmpty($previousRunTime)) {
            $previousRunTimeDt = [datetime]::ParseExact($previousRunTime, "$shortDatePattern $longTimePattern", $culture)
        }
        if (-not [string]::IsNullOrEmpty($lastRunTime)) {
            $lastRunTimeDt = [datetime]::ParseExact($lastRunTime, "$shortDatePattern $longTimePattern", $culture)
        }
    } catch {
        return
    }

    if ($previousRunTimeDt -and $lastRunTimeDt -and $lastRunTimeDt -gt $previousRunTimeDt) {
        $timeDifference = $lastRunTimeDt - $previousRunTimeDt
        $global:taskProcessingTimeInSeconds = $timeDifference.TotalSeconds
    } 
    }

    $data["Task Execution Time"] = $global:taskProcessingTimeInSeconds

    if ($data.ContainsKey("Next Run Time")) {
        $nextRunTime = $data["Next Run Time"]

        $jsonContent[$TaskName] = $nextRunTime
        $modifiedContent = $jsonContent | ConvertTo-Json -Depth 2
        $modifiedContent | Set-Content -Path $filePath
    }
    else {
        Write-Output "No 'Next Run Time' found in \$data."
    }
}


ManageInfoFileAndTask -TaskName $taskName

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
    "Task Fails or Crashes Unexpectedly"
)

foreach ($key in $keysToRemove) {
    if ($data.ContainsKey($key)) {
        $data.Remove($key)
    }
}

# Site24x7 Plugin Metrics
$version = "1"
$displayname = "Monitor Task - " + $data["Task Name"]
$heartbeat = "True"
$working_codes = @(0, 267008, 267009)

$mainJson = @{}
$mainJson["version"] = $version
$mainJson["displayname"] = $displayname
$mainJson["heartbeat"] = $heartbeat
$mainJson["data"] = $data

$mainJson["units"] = @{
    "Task Age" = "days"
    "Task Execution Time" = "seconds"
}

if ($working_codes -contains $data["Error Code"]) {
    $msg = GetErrorMessage($data["Error Code"])
    if ($Status -eq 0) {
        $mainJson["status"] = 0
    }
    if ( $null -ne $status_msg ) {
        $mainJson["msg"] = $status_msg
    } else {
        $mainJson["msg"] = ($msg | Out-String)
    }
} else {
    $msg = GetErrorMessage($data["Error Code"])
    $err_msg = "error_code: " + $data["Error Code"] + ", msg: " + $msg
    $mainJson["msg"] = $err_msg
    $mainJson["status"] = 0
}

$mainJson | ConvertTo-Json
