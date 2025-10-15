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

        function Get-RDPConnections {
            try {
                $rdpConnections = @()
                
                try {
                    $rdpPort = (Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -ErrorAction SilentlyContinue).PortNumber
                    if (-not $rdpPort -or $rdpPort -eq $null) {
                        $rdpPort = 3389 
                    }
                } catch {
                    $rdpPort = 3389  
                }
                
                $connections = Get-NetTCPConnection -LocalPort $rdpPort -ErrorAction SilentlyContinue
                
                if ($connections) {
                    foreach ($conn in $connections) {
                        if ($conn.RemoteAddress -notmatch "::" -and 
                            $conn.RemoteAddress -ne "0.0.0.0" -and
                            $conn.RemoteAddress -ne "127.0.0.1") {
                            
                            $connectionInfo = @{
                                "name" = "IP_$($conn.RemoteAddress)"
                                "RDPLocalAddress" = $conn.LocalAddress
                                "RDPLocalPort" = $conn.LocalPort 
                                "RDPRemoteAddress" = $conn.RemoteAddress
                                "RDPRemotePort" = $conn.RemotePort
                                "RDPState" = $conn.State
                                "RDPAppliedSettings" = if ($conn.AppliedSetting) { $conn.AppliedSetting } else { "-" }
                                "RDPOwningProcess" = $conn.OwningProcess
                            }
                            
                            $rdpConnections += $connectionInfo
                        }
                    }
                }
                
                if ($rdpConnections.Count -eq 0) {
                    $defaultRDPConnection = @{
                        "name" = "-"
                        "RDPLocalAddress" = "-"
                        "RDPLocalPort" = -1
                        "RDPRemoteAddress" = "-"
                        "RDPRemotePort" = -1
                        "RDPState" = "-"
                        "RDPAppliedSettings" = "-"
                        "RDPOwningProcess" = -1
                    }
                    $rdpConnections += $defaultRDPConnection
                }
                
                return ,$rdpConnections
                
            } catch {
                $errorConnection = @{
                    "name" = "-"
                    "RDPLocalAddress" = "-"
                    "RDPLocalPort" = -1
                    "RDPRemoteAddress" = "-"
                    "RDPRemotePort" = -1
                    "RDPState" = "-"
                    "RDPAppliedSettings" = "-"
                    "RDPOwningProcess" = -1
                }
                return ,@($errorConnection)
            }
        }

        function Get-RemoteConnectionsWithProcessDetails {
            try {
                $remoteConnections = @()
                
                $connections = Get-NetTCPConnection -ErrorAction SilentlyContinue |
                    Where-Object {
                        $_.RemoteAddress -and
                        $_.RemoteAddress -notin @('0.0.0.0', '::', '127.0.0.1', '::1') -and
                        $_.State -eq 'Established'
                    } |
                    Group-Object -Property RemoteAddress |
                    Select-Object -First 15
                
                if ($connections) {
                    foreach ($group in $connections) {
                        try {
                            $conn = $group.Group[0]
                            
                            $processName = "-"
                            try {
                                $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
                                if ($proc) {
                                    $processName = $proc.ProcessName
                                }
                            } catch {
                                $processName = "-"
                            }
                            
                            $connectionInfo = @{
                                "name" = "IP_$($conn.RemoteAddress)"
                                "RemoteAddress" = $conn.RemoteAddress
                                "RemotePort" = $conn.RemotePort
                                "LocalAddress" = $conn.LocalAddress
                                "LocalPort" = $conn.LocalPort
                                "State" = $conn.State
                                "ProcessName" = $processName
                                "PID" = $conn.OwningProcess
                            }
                            
                            $remoteConnections += $connectionInfo
                        } catch {
                        }
                    }
                }
                
                if ($remoteConnections.Count -eq 0) {
                    $defaultRemoteConnection = @{
                        "name" = "-"
                        "RemoteAddress" = "-"
                        "RemotePort" = -1
                        "LocalAddress" = "-"
                        "LocalPort" = -1
                        "State" = "-"
                        "ProcessName" = "-"
                        "PID" = -1
                    }
                    $remoteConnections += $defaultRemoteConnection
                }
                
                return ,$remoteConnections
                
            } catch {
                $errorConnection = @{
                    "name" = "-"
                    "RemoteAddress" = "-"
                    "RemotePort" = -1
                    "LocalAddress" = "-"
                    "LocalPort" = -1
                    "State" = "-"
                    "ProcessName" = "-"
                    "PID" = -1
                }
                return ,@($errorConnection)
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
            "RDP_Connections"     = Get-RDPConnections
            "Remote_Connections" = Get-RemoteConnectionsWithProcessDetails
            "applog"             = @{
            "logs_enabled"    = $true
            "log_file_path"  = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\windows_security\logs*.txt"
            "log_type_name"  = "WinSecurityLog"
        }
            "tabs" = @{
                "RDP Connections" = @{
                    "order" = 1
                    "tablist" = @("RDP_Connections")
                }
                "Remote Connections Process details" = @{
                    "order" = 2
                    "tablist" = @("Remote_Connections")
                }
            }
        }


        $output | ConvertTo-Json -Compress -Depth 10

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
