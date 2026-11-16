param(
    [Parameter(Mandatory = $true)]
    [string]$Server,
    
    [Parameter(Mandatory = $true)]
    [string]$username,
    
    [Parameter(Mandatory = $true)]
    [string]$password
)

$version = 1
$heartbeat = "true"  
$Status = 1
$msg = $null

Function Get-Data() {
    $data = @{}
    try {

        $yellow = 0
        $red = 0
        $info = 0
        $current_time = Get-Date
        $cutoff = (Get-Date).AddHours(-12)
        $count = 0
        $alreadyLogged = @{}

        # Set PowerCLI config
        Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false -Confirm:$false -ErrorAction Stop | Out-Null
        Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false -ErrorAction Stop | Out-Null
        Connect-VIServer -Server $Server -User $username -Password $password -WarningAction SilentlyContinue -ErrorAction Stop | Out-Null

        # Get the current working directory
        $dirPath = Get-Location

        # Get all alarm files
        $allAlarmFiles = Get-ChildItem -Path $dirPath -Filter "alarms*" -File |
            Sort-Object CreationTime -Descending

        # Delete files older than 1 day based on creation time
        $oneDayAgo = (Get-Date).AddDays(-1)
        $filesToDelete = $allAlarmFiles | Where-Object { $_.CreationTime -lt $oneDayAgo }
        
        if ($filesToDelete) {
            $filesToDelete | Remove-Item -Force
        }

        # Get the latest remaining file (after deletion)
        $latestFile = Get-ChildItem -Path $dirPath -Filter "alarms*" -File |
            Sort-Object CreationTime -Descending | 
            Select-Object -First 1

        # Determine if we need a new file (every 6 hours)
        $needNewFile = $false
        if ($latestFile) {
            $fileAge = (Get-Date) - $latestFile.CreationTime
            if ($fileAge.TotalHours -ge 6) {
                $needNewFile = $true
            }
        }
        else {
            $needNewFile = $true
        }

        # Read previously logged alarms from ALL files within the cutoff window (last 12 hours)
        $relevantFiles = Get-ChildItem -Path $dirPath -Filter "alarms*" -File |
            Where-Object { $_.CreationTime -gt $cutoff } |
            Sort-Object CreationTime

        if ($relevantFiles) {
            foreach ($file in $relevantFiles) {
                $existingContent = Get-Content -Path $file.FullName -ErrorAction SilentlyContinue
                
                if (-not $existingContent) {
                    continue
                }
                
                foreach ($line in $existingContent) {
                    if ($line -match '^(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}), Entity: ([^,]+), State: ([^,]+), Alarm: (.+), vCenter: ([^,]+), EntityType: (.+)$') {
                        $fileTimestamp = $matches[1]
                        $fileEntity = $matches[2]
                        $fileState = $matches[3]
                        $fileAlarm = $matches[4]
                        $fileEntityType = $matches[6]
                        
                        # Create unique key for this alarm instance
                        $key = "$fileTimestamp|$fileEntity|$fileAlarm|$fileState|$fileEntityType"
                        $alreadyLogged[$key] = $true
                    }
                }
            }
        }

        $logLines = ""
        $newAlarmCount = 0

        # Get triggered alarms from all Datacenters
        $events = foreach ($dc in (Get-Datacenter | Where-Object { $_.ExtensionData.triggeredAlarmState })) {
            $dc.ExtensionData.triggeredAlarmState | Select-Object `
                @{N = "Entity"; E = { (Get-View $_.Entity).Name }},
                @{N = "EntityType"; E = { $_.Entity.Type }},
                @{N = "Alarm"; E = { (Get-View $_.Alarm).Info.Name }},
                Time,
                OverallStatus,
                @{N = "vCenter"; E = { $Server }}
        }

        foreach ($alarm in $events) {
            # Skip if critical properties are null
            if (-not $alarm.Time) {
                continue
            }

            # Ensure alarmName is a string, not an array
            $alarmName = if ($alarm.Alarm -is [array]) { 
                ($alarm.Alarm -join " ") -replace "`r`n|`n|`r", " "
            } else { 
                "$($alarm.Alarm)" -replace "`r`n|`n|`r", " "
            }
            $timestamp = $alarm.Time.ToString("yyyy-MM-dd-HH-mm-ss")
            $entity = if ($alarm.Entity) { $alarm.Entity } else { "Unknown" }
            $entityType = if ($alarm.EntityType) { $alarm.EntityType } else { "Unknown" }
            $vcenter = $alarm.vCenter
            $state = $alarm.OverallStatus.ToString()

            # Normalize state
            if ($state -and (($state.ToLower() -eq "red") -or ($state.ToLower() -eq "critical") -or ($state.ToLower() -eq "error"))) {
                $state = "red"
            }
            elseif ($state -and (($state.ToLower() -eq "yellow") -or ($state.ToLower() -eq "warning"))) {
                $state = "yellow"
            }
            elseif ($state -and ($state.ToLower() -eq "info")) {
                $state = "info"
            }

            # Create unique key for this alarm instance
            $alarmKey = "$timestamp|$entity|$alarmName|$state|$entityType"

            # Only log and count if this specific alarm hasn't been logged before
            if (-not $alreadyLogged.ContainsKey($alarmKey)) {
                # Count by severity
                if ($state -eq "red") {
                    $red += 1
                }
                elseif ($state -eq "yellow") {
                    $yellow += 1
                }
                elseif ($state -eq "info") {
                    $info += 1
                }

                # Build log line
                $logLine = "{0}, Entity: {1}, State: {2}, Alarm: {3}, vCenter: {4}, EntityType: {5}`n" -f 
                    $timestamp, $entity, $state, $alarmName, $vcenter, $entityType
                $logLines += $logLine
                $newAlarmCount++
                $alreadyLogged[$alarmKey] = $true

            }
            $count += 1
        }

        # Disconnect from vCenter
        Disconnect-VIServer -Server $Server -Confirm:$false -ErrorAction SilentlyContinue

        # Write new alarms to file if any exist
        if ($logLines) {
            $logLines = $logLines.TrimEnd("`r", "`n")
            
            if ($needNewFile) {
                # Create new file with current timestamp
                $currentTimestamp = $current_time.ToString("yyyy-MM-dd-HH-mm-ss")
                $alarmLogPath = Join-Path $dirPath "alarms-$currentTimestamp.txt"
                Set-Content -Path $alarmLogPath -Value $logLines
                $Script:msg = "Created new file with $newAlarmCount alarm(s): alarms-$currentTimestamp.txt"
            }
            else {
                # Append to existing file if less than 6 hours old
                Add-Content -Path $latestFile.FullName -Value "`n$logLines"
                $Script:msg = "Appended $newAlarmCount new alarm(s) to $($latestFile.Name)"
            }
        }
        else {
            $Script:msg = "No new alarms to log (total active alarms: $count)"
        }

    }
    catch {
        $Script:Status = 0
        $Script:msg = $_.Exception.Message
        Write-Verbose "Error: $($_.Exception)"
        Write-Host "Stack Trace: $($_.ScriptStackTrace)"
    }

    $data.Add("Alert State Red", $red)
    $data.Add("Alert State Yellow", $yellow)
    $data.Add("Total alerts", $count)
    #$data.Add("Events with status as Info", $info)

    return $data
}

# Main execution
$mainJson = @{}
$mainJson.Add("data", (Get-Data))
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)

if ($Status -eq 0) {
    $mainJson.Add("status", 0)
}
if ($null -ne $Script:msg) {
    $mainJson.Add("msg", $Script:msg)
}

return $mainJson | ConvertTo-Json -Compress