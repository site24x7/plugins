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

function Get-WindowsUpdatesPending {
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
    "Failed Login Attempts"    = Get-SecurityEventLogs -logFilePath $logFilePath -logName 'Security' -eventID 4625 -customMessage "FailedLoginAttempts"
    "Account Lockouts"         = Get-SecurityEventLogs -logFilePath $logFilePath -logName 'Security' -eventID 4740 -customMessage "AccountLockout"
    "Antivirus Status"         = Get-AntivirusStatus
    "Malware Detections"       = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1116 -customMessage "MalwareDetection"
    "Security Threats Actions" = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1117 -customMessage "SecurityThreatsActions"
    "Software Updates Pending" = Get-WindowsUpdatesPending
    "Failed Windows Updates"  = Get-SecurityEventLogs -logFilePath $logFilePath -logName "System" -eventID 20 -customMessage "FailedWindowsUpdate"
    "Malware Action Failed"    = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1118 -customMessage "MalwareActionFailed"
    "Threat Detected Quarantined" = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1006 -customMessage "ThreatDetectedQuarantined"
    "Malware Remediation Failed"  = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1010 -customMessage "MalwareRemediationFailed"
    "applog" = @{
        "log_file_path" = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
        "log_type_name" = "WinSecurityLog"
        "logs_enabled"  = $true
    }
}

$metrics | ConvertTo-Json -Compress
