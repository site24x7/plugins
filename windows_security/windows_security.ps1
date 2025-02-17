function Get-SecurityEventLogs {
    param (
        [string]$logFilePath,
        [string]$logName,
        [int]$eventID,
        [string]$customMessage
    )
    try {
        $events = Get-WinEvent -FilterHashtable @{
            LogName   = $logName
            ID        = $eventID
            StartTime = (Get-Date).AddMinutes(-6)
        } -ErrorAction SilentlyContinue

        $eventMessages = @()

        $events | ForEach-Object {
            $message = $_.Message

            $logEntry = [ordered]@{
                LogName  = $customMessage
                ID       = $eventID
                Message  = $message  
            }

            $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8
            $eventMessages += $logEntry
        }

        return $eventMessages.Count
    } catch {
        return -1
    }
}

function Get-AntivirusStatus {
    try {
        $avStatus = Get-MpComputerStatus
        if ($avStatus.AntivirusEnabled -and $avStatus.RealTimeProtectionEnabled) {
            return 1
        } else {
            return 0
        }
    } catch {
        return -1
    }
}

function Get-SecurityUpdatesPending {
    try {
        $UpdateSession = New-Object -ComObject Microsoft.Update.Session
        $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
        $SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")
        return $SearchResult.Updates.Count
    } catch {
        return -1
    }
}

$currentDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$logFiles = Get-ChildItem -Path $currentDirectory -Filter "logs_*.txt"

if ($logFiles) {
    $logFiles | ForEach-Object { Remove-Item $_.FullName -Force }
}

$logFileName = "logs_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$logFilePath = "$currentDirectory\$logFileName"
if (!(Test-Path $logFilePath)) {
    New-Item -Path $logFilePath -ItemType File -Force | Out-Null
}

$metrics = @{
    "plugin_version"           = 1
    "heartbeat_required"       = "true"
    "failed_login_attempts"    = Get-SecurityEventLogs -logFilePath $logFilePath -logName 'Security' -eventID 4625 -customMessage "FailedLoginAttempts"
    "account_lockouts"         = Get-SecurityEventLogs -logFilePath $logFilePath -logName 'Security' -eventID 4740 -customMessage "AccountLockout"
    "antivirus_status"         = Get-AntivirusStatus
    "malware_detections"       = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1116 -customMessage "MalwareDetection"
    "security_threats_actions" = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1117 -customMessage "SecurityThreatsActions"
    "security_updates_pending" = Get-SecurityUpdatesPending
    "failed_security_updates"  = Get-SecurityEventLogs -logFilePath $logFilePath -logName "System" -eventID 20 -customMessage "FailedSecurityUpdate"
    "malware_action_failed"    = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1118 -customMessage "MalwareActionFailed"
    "threat_detected_quarantined" = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1006 -customMessage "ThreatDetectedQuarantined"
    "malware_remediation_failed"  = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1010 -customMessage "MalwareRemediationFailed"
    "applog" = @{
        "log_file_path" = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
        "log_type_name" = "WinSecurityLog"
        "logs_enabled"  = $true
    }
}

$metrics | ConvertTo-Json -Compress
