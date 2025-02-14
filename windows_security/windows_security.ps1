function Get-SecurityEventLogs {
    param (
        [string]$logFilePath,
        [string]$logName,
        [int]$eventID,
        [string]$messageRegex,
        [string]$customMessage,
        [bool]$isAccountLockout = $false  
    )
    try {
        $events = Get-WinEvent -FilterHashtable @{
            LogName = $logName
            ID = $eventID
            StartTime = (Get-Date).AddMinutes(-1000)
        } -ErrorAction SilentlyContinue

        $eventMessages = @()

        $events | ForEach-Object {
            $message = $_.Message

            # Handle special case for account lockouts
            if ($isAccountLockout) {
                $startIndex = $message.IndexOf('Account That Was Locked Out:')
                if ($startIndex -gt -1) {
                    $subMessage = $message.Substring($startIndex)
                    if ($subMessage -match "Account Name:\s+([^\r\n]+)") {
                        $accountName = $matches[1].Trim()
                        
                        $logEntry = @{
                            LogName = "AccountLockout"
                            ID = $eventID
                            Message = "Account name $accountName. A user account was locked out."
                        }

                        $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8
                        $eventMessages += $logEntry
                    }
                }
            }
            else {
                if ($message -match $messageRegex) {
                    $logEntry = @{
                        LogName = $customMessage
                        ID = $eventID
                        Message = "$customMessage : $($matches[1])"
                    }

                    $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8
                    $eventMessages += $logEntry
                }
            }
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

function Get-FailedSecurityUpdates {
    try {
        $failedUpdates = Get-WinEvent -FilterHashtable @{
            LogName = "System"
            ProviderName = "Microsoft-Windows-WindowsUpdateClient"
            ID = 20
            StartTime = (Get-Date).AddDays(-1)
        } -ErrorAction SilentlyContinue | Measure-Object
        return $failedUpdates.Count
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
    "plugin_version" = 1
    "heartbeat_required" = "true"
    "failed_login_attempts" = Get-SecurityEventLogs -logFilePath $logFilePath -logName 'Security' -eventID 4625 -messageRegex "Failure Reason:\s+(.*?)\r?\n" -customMessage "FailedLoginAttempts"
    "account_lockouts" = Get-SecurityEventLogs -logFilePath $logFilePath -logName 'Security' -eventID 4740 -messageRegex "Account Name:\s+([^\r\n]+)" -customMessage "AccountLockout" -isAccountLockout $true
    "antivirus_status" = Get-AntivirusStatus
    "malware_detections" = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1116 -messageRegex "Path:\s+(.+?)\r?\n" -customMessage "MalwareDetection"
    "security_threats_actions" = Get-SecurityEventLogs -logFilePath $logFilePath -logName "Microsoft-Windows-Windows Defender/Operational" -eventID 1117 -messageRegex "Path:\s+(.+?)\r?\n" -customMessage "SecurityThreatsActions"
    "security_updates_pending" = Get-SecurityUpdatesPending
    "failed_security_updates" = Get-FailedSecurityUpdates
    "applog" = @{
        "log_file_path" = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
        "log_type_name" = "WinSecurityLog"
        "logs_enabled" = $true
    }
}

$metrics | ConvertTo-Json -Compress
