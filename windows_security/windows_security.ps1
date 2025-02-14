function Get-FailedLoginAttempts {
    param (
        [string]$logFilePath
    )
    try {
        $failedLogins = Get-WinEvent -FilterHashtable @{
            LogName='Security'
            ID=4625
            StartTime=(Get-Date).AddMinutes(-10)
        } -ErrorAction SilentlyContinue 

        $failedLogins | ForEach-Object {
            if ($_.Message -match "Failure Reason:\s+(.*?)\r?\n") {
                $logEntry = @{
                    LogName = "FailedLoginAttempts"
                    ID = 4625
                    Message = $matches[1]
                }
                $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8
            }
        }
        
        return $failedLogins.Count
    } catch {
        return 0
    }
}

function Get-AccountLockouts {
    param (
        [string]$logFilePath
    )
    try {
        $lockouts = Get-WinEvent -FilterHashtable @{
            LogName='Security'
            ID=4740
            StartTime=(Get-Date).AddMinutes(-10)
        } -ErrorAction SilentlyContinue

        $lockoutMessages = @() 

        $lockouts | ForEach-Object {
            $message = $_.Message
            $startIndex = $message.IndexOf('Account That Was Locked Out:')
            if ($startIndex -gt -1) {
                $subMessage = $message.Substring($startIndex)
                if ($subMessage -match "Account Name:\s+([^\r\n]+)") {
                    $accountName = $matches[1].Trim()
                    
                    $logEntry = @{
                        LogName = "AccountLockout"
                        ID = 4740
                        Message = "Account name $accountName. A user account was locked out."
                    }

                    $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8

                    $lockoutMessages += $logEntry
                }
            }
        }

        return $lockoutMessages.Count
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


function Get-MalwareDetections {
    param (
        [string]$logFilePath
    )
    try {
        $malwareEvents = Get-WinEvent -FilterHashtable @{
            LogName = "Microsoft-Windows-Windows Defender/Operational"
            ID = 1116
            StartTime = (Get-Date).AddMinutes(-10)
        } -ErrorAction SilentlyContinue

        $malwareEvents | ForEach-Object {
            if ($_.Message -match "Path:\s+(.+?)\r?\n") {
                $logEntry = @{
                    LogName = "MalwareDetection"
                    ID = 1116
                    Message = "Malware detected at path: $($matches[1])"
                }
                $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8
            }
        }

        return $malwareEvents.Count
    } catch {
        return -1
    }
}

function Get-SecurityThreatsActions {
    param (
        [string]$logFilePath
    )
    try {
        $threatEvents = Get-WinEvent -FilterHashtable @{
            LogName = "Microsoft-Windows-Windows Defender/Operational"
            ID = 1117
            StartTime = (Get-Date).AddMinutes(-10)
        } -ErrorAction SilentlyContinue

        $threatEvents | ForEach-Object {
            if ($_.Message -match "Path:\s+(.+?)\r?\n") {
                $logEntry = @{
                    LogName = "SecurityThreatsActions"
                    ID = 1117
                    Message = "Security threat action taken for $($matches[1])"
                }
                $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8
            }
        }

        return $threatEvents.Count
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
    "plugin_version"=1
    "heartbeat_required"="true"
    "failed_login_attempts" = Get-FailedLoginAttempts -logFilePath $logFilePath
    "account_lockouts" = Get-AccountLockouts -logFilePath $logFilePath
    "antivirus_status" = Get-AntivirusStatus
    "malware_detections" = Get-MalwareDetections -logFilePath $logFilePath
    "security_threats_actions" = Get-SecurityThreatsActions -logFilePath $logFilePath
    "security_updates_pending" = Get-SecurityUpdatesPending
    "failed_security_updates" = Get-FailedSecurityUpdates
    "applog" = @{
        "log_file_path" = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
        "log_type_name" = "WinSecurityLog"
        "logs_enabled" = $true
    }
}

$metrics | ConvertTo-Json -Compress
