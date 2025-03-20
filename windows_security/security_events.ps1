function Get-SecurityEventLogs {
    param (
        [Hashtable]$logNamesAndEventIDs,  
        [string]$logFilePath,
        [bool]$logFileStatus              
    )

    try {
        $eventCounts = @{
            "Failed Windows Updates"        = 0
            "Malware Detections"            = 0
            "Malware Action Failed"         = 0
            "Threat Detected Quarantined"  = 0
            "Security Threats Actions"     = 0
            "Failed Login Attempts"        = 0
            "Account Lockouts"              = 0
            "Malware Remediation Failed"   = 0
        }
        

        $eventIDNames = @{
            4625 = "Failed Login Attempts"
            4740 = "Account Lockouts"
            1116 = "Malware Detections"
            1117 = "Security Threats Actions"
            1118 = "Malware Action Failed"
            1006 = "Threat Detected Quarantined"
            1010 = "Malware Remediation Failed"
            20 ="Failed Windows Updates"
        }

    
        foreach ($logName in $logNamesAndEventIDs.Keys) {

      
            $eventIDs = $logNamesAndEventIDs[$logName]
            
            $events = Get-WinEvent -FilterHashtable @{
                LogName   = $logName
                ID        = $eventIDs
                StartTime = (Get-Date).AddMinutes(-3)  
            } -ErrorAction SilentlyContinue

            if ($events) {
                $events | ForEach-Object {
                    $eventId = $_.Id
                    $message = $_.Message
                    
 
                    $eventName = $eventIDNames[$eventId]

                    if ($eventCounts.ContainsKey($eventName)) {
                        $eventCounts[$eventName]++
                    }

                    $logEntry = [ordered]@{
                        LogName  = $logName
                        ID       = $eventId  
                        Message  = $message  
                    }

                    try {
                    if($logFileStatus){
                        $logEntry | ConvertTo-Json -Compress | Out-File -FilePath $logFilePath -Append -Encoding UTF8 -ErrorAction SilentlyContinue
                        }
                    } catch {
                       
                    }
                }
            } else {
                
            }
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

        
        $output = @{
            "plugin_version"       = 1
            "heartbeat_required"  = "true"
            "Antivirus Status"    = Get-AntivirusStatus
            "Failed Windows Updates" = $eventCounts["Failed Windows Updates"]
            "Malware Detections"  = $eventCounts["Malware Detections"]
            "Malware Action Failed" = $eventCounts["Malware Action Failed"]
            "Threat Detected Quarantined" = $eventCounts["Threat Detected Quarantined"]
            "Security Threats Actions" = $eventCounts["Security Threats Actions"]
            "Failed Login Attempts" = $eventCounts["Failed Login Attempts"]
            "Account Lockouts"    = $eventCounts["Account Lockouts"]
            "Malware Remediation Failed" = $eventCounts["Malware Remediation Failed"]
            "applog"             = @{
            "logs_enabled"    = $true
            "log_file_path"  = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
            "log_type_name"  = "WinSecurityLog"
        }
        }


        $output | ConvertTo-Json -Compress

    } catch {
        
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
$logFileStatus = $false
try {
    if (!(Test-Path $logFilePath -ErrorAction SilentlyContinue)) {
       New-Item -Path $logFilePath -ItemType File -Force -ErrorAction SilentlyContinue | Out-Null
       $logFileStatus = $true
    }
} catch {
   }


$logNamesAndEventIDs = @{
    "Security" = @(4625, 4740)  
    "Microsoft-Windows-Windows Defender/Operational" = @(1116, 1117, 1118, 1006, 1010) 
    "System" = @(20)
}

Get-SecurityEventLogs -logNamesAndEventIDs $logNamesAndEventIDs -logFilePath $logFilePath -logFileStatus $logFileStatus
