$heartbeat = "true" 
$version = 1

Function Convert-IdleTimeToMinutes {
    param($idleTime, [ref]$errorMsg)
    
    try {
        if ($idleTime -eq "." -or [string]::IsNullOrEmpty($idleTime)) {
            return 0
        }
        
        if ($idleTime -eq 0 -or $idleTime -eq "0") {
            return 0
        }
        
        $idleStr = $idleTime.ToString().Trim()
        
        if ($idleStr -match "^(\d+):(\d+)$") {
            $hours = [int]$matches[1]
            $minutes = [int]$matches[2]
            return ($hours * 60) + $minutes
        }
        elseif ($idleStr -match "^(\d+)$") {
            return [int]$matches[1]
        }
        else {
            return 0
        }
    } catch {
        $newError = "Error converting idle time '$idleTime': $($_.Exception.Message)"
        if ($errorMsg.Value) {
            $errorMsg.Value += "; $newError"
        } else {
            $errorMsg.Value = $newError
        }
        return -1
    }
}

Function Get-Data {
    try {
        $activeUser = Get-LocalUser | Select *
        $active = 0
        $userName = @()
        $userDetails = @()
        $errorMsg = ""

        $userInfo = query user 2>$null

        if ($userInfo -ne $null -and $userInfo.Count -ne 0) {
            $userCount = ($userInfo.Count - 1)
            $query_user = $userInfo -split "\n" -replace '\s{18}\s+', "  blank  "
            $qu_object = $query_user -split "\n" -replace '\s\s+', "," | ConvertFrom-Csv

            $qu_object | ForEach-Object {
                $updated_user = $_.USERNAME -replace ">", ""
                
                $status = ""
                $logonFlag = 0
                
                if ($_.STATE -eq "Disc") {
                    $status = "Disconnected"
                    $logonFlag = 0
                }
                elseif ($_.STATE -eq "Active") {
                    $status = "Active"
                    $active += 1
                    $logonFlag = 1
                }
                else {
                    $status = $_.STATE
                    $logonFlag = 0
                }

                $userName += $updated_user
                
                $userDetails += [PSCustomObject]@{
                    name = $updated_user
                    idletime = (Convert-IdleTimeToMinutes $_.'IDLE TIME' ([ref]$errorMsg))
                    user_status = if ($status -eq "Active") { 1 } else { 0 }
                    user_status_text = $status
                    "logon_logout" = $logonFlag
                    last_logon_time = $_.'LOGON TIME'
                }
            }
        }

        for ($user = 1; $user -lt $activeUser.Count; $user = $user + 1) {
            $date = $activeUser[$user].LastLogon
            $date = $date -replace '[a-z]', ''
            
            if ($userName -notcontains ($activeUser[$user].Name)) {
                $userDetails += [PSCustomObject]@{
                    name = $activeUser[$user].Name
                    idletime = 0
                    user_status = 0
                    user_status_text = "DisConnected"
                    logon_logout = 0
                    last_logon_time = $date
                }
            }
        }

        if ($userDetails.Count -eq 0) {
            $userDetails += [PSCustomObject]@{
                name = "-"
                idletime = -1
                user_status = -1
                user_status_text = "-"
                logon_logout = -1
                last_logon_time = "-"
            }
        }

        $dataObj = @{
            plugin_version = $version
            heartbeat_required = $heartbeat
            active_user = $active
            User_Details = $userDetails
            units = @{
                User_Details = @{
                    "idletime" = "mins"
                }
            }
        }

        if ($errorMsg) {
            $dataObj["msg"] = $errorMsg
        }

        return $dataObj

    } catch {
        $catchError = $_.Exception.Message
        $finalErrorMsg = if ($errorMsg) { "$errorMsg; $catchError" } else { $catchError }
        
        $errorObj = @{
            plugin_version = $version
            heartbeat_required = $heartbeat
            active_user = 0
            User_Details = @(
                [PSCustomObject]@{
                    name = "-"
                    idletime = -1
                    user_status = -1
                    user_status_text = "-"
                    logon_logout = -1
                    last_logon_time = "-"
                }
            )
            units = @{
                User_Details = @{
                    "idletime" = "mins"
                }
            }
            msg = $finalErrorMsg
        }
        return $errorObj
    }
}

$result = Get-Data
$result | ConvertTo-Json -Depth 3 -Compress
