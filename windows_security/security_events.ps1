$TimeoutSeconds = 3

function Get-SecurityEventLogs {
    param (
        [string]$logFilePath,
        [string]$logName,
        [int]$eventID,
        [string]$customMessage,
        [bool]$logFileStatus
    )
        $job = Start-Job -ScriptBlock {
        param($logFilePath, $logName, $eventID, $customMessage, $logFileStatus)

        try {
            $events = Get-WinEvent -FilterHashtable @{
                LogName   = $logName
                ID        = $eventID
                StartTime = (Get-Date).AddMinutes(-3)
            } -ErrorAction SilentlyContinue

            $eventMessages = @()

            $events | ForEach-Object {
                $message = $_.Message
                $logEntry = [ordered]@{
                    LogName  = $customMessage
                    ID       = $eventID
                    Message  = $message  
                }
                $eventMessages += $logEntry

                if ($logFileStatus) {
                    try {
                        $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8 -ErrorAction SilentlyContinue
                    } catch {}
                }
            }

            return $eventMessages
        } catch {
            return -1
        }
    } -ArgumentList $logFilePath, $logName, $eventID, $customMessage, $logFileStatus

    $job | Wait-Job -Timeout $TimeoutSeconds | Out-Null -ErrorAction SilentlyContinue

    if ($job.State -eq 'Running') {
        $job | Stop-Job -PassThru | Remove-Job -ErrorAction SilentlyContinue
        return -1 
    }

    $result = Receive-Job -Job $job -ErrorAction SilentlyContinue
    Remove-Job -Job $job -ErrorAction SilentlyContinue
    return ($result | Measure-Object).Count
}


function Get-AntivirusStatus {
    try {
        $avStatus = Get-MpComputerStatus -ErrorAction SilentlyContinue
        if ($avStatus.AntivirusEnabled -and $avStatus.RealTimeProtectionEnabled) {
            return 1
        } else {
            return 0
        }
    } catch {
        return -1
    }
}


$currentDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path


try {
    $logFiles = Get-ChildItem -Path $currentDirectory -Filter "logs_*.txt" -ErrorAction SilentlyContinue
    if ($logFiles) {
        $logFiles | ForEach-Object {
            try {
                Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
            } catch {
            }
        }
    }
} catch {
}

$logFileName = "logs_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$logFilePath = "$currentDirectory\$logFileName"
$logFileCreated = $false
try {
    if (!(Test-Path $logFilePath)) {
       New-Item -Path $logFilePath -ItemType File -Force -ErrorAction SilentlyContinue | Out-Null
       $logFileCreated = $true
    }
} catch {
   }


$logFile = if ($logFileCreated) { $logFilePath } else { $null }

$metrics = @{
    "plugin_version"           = 1
    "heartbeat_required"       = "true"
    "Failed Login Attempts"    = Get-SecurityEventLogs -logFilePath $logFile -logName 'Security' -eventID 4625 -customMessage "FailedLoginAttempts" -logFileStatus $logFileCreated
    "Account Lockouts"         = Get-SecurityEventLogs -logFilePath $logFile -logName 'Security' -eventID 4740 -customMessage "AccountLockout" -logFileStatus $logFileCreated
    "Antivirus Status"         = Get-AntivirusStatus
    "Malware Detections"       = Get-SecurityEventLogs -logFilePath $logFile -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1116 -customMessage "MalwareDetection" -logFileStatus $logFileCreated
    "Security Threats Actions" = Get-SecurityEventLogs -logFilePath $logFile -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1117 -customMessage "SecurityThreatsActions" -logFileStatus $logFileCreated
    "Failed Windows Updates"   = Get-SecurityEventLogs -logFilePath $logFile -logName "System" -eventID 20 -customMessage "FailedWindowsUpdate"
    "Malware Action Failed"    = Get-SecurityEventLogs -logFilePath $logFile -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1118 -customMessage "MalwareActionFailed" -logFileStatus $logFileCreated
    "Threat Detected Quarantined" = Get-SecurityEventLogs -logFilePath $logFile -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1006 -customMessage "ThreatDetectedQuarantined" -logFileStatus $logFileCreated
    "Malware Remediation Failed"  = Get-SecurityEventLogs -logFilePath $logFile -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1010 -customMessage "MalwareRemediationFailed" -logFileStatus $logFileCreated
    "applog" = @{
        "log_file_path" = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
        "log_type_name" = "WinSecurityLog"
        "logs_enabled"  = $true
    }
}

$metrics | ConvertTo-Json -Compress
