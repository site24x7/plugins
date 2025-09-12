$dataObj = @{}
$heartbeat = "true" 
$version = 1
Function Get-Data 
{
        $activeUser = Get-LocalUser | Select *
        $active = 0
        $disconn = 0
        $userName = @()

        $userInfo = query user 2>$null

        if ($userInfo -ne $null -and $userInfo.Count -ne 0) {
            $userCount = ($userInfo.Count - 1)
            $query_user = $userInfo -split "\n" -replace '\s{18}\s+', "  blank  "
            $qu_object = $query_user -split "\n" -replace '\s\s+', "," | ConvertFrom-Csv

            $qu_object | ForEach-Object {
                $updated_user = $_.USERNAME -replace ">", ""
                
                if ($_.STATE -eq "Disc") {
                    $dataObj[$updated_user + "_status"] = "Disconnected"
                    $dataObj[$updated_user + "_logon_logout(1/0)"] = 0
                }
                elseif ($_.STATE -eq "Active") {
                    $dataObj[$updated_user + "_status"] = $_.STATE
                    $active += 1
                    $dataObj[$updated_user + "_logon_logout(1/0)"] = 1
                }
                else {
                    $dataObj[$updated_user + "_status"] = $_.STATE
                    $dataObj[$updated_user + "_logon_logout(1/0)"] = 0
                }

                $userName += $updated_user
                $dataObj[$updated_user + "_idletime"] = $_.'IDLE TIME'
                $dataObj[$updated_user + "_last_logon_time"] = $_.'LOGON TIME'
            }
        }

    for ($user = 1; $user -lt $activeUser.Count; $user = $user + 1) {
        $date = $activeUser[$user].LastLogon
        $date = $date -replace '[a-z]', ''
        
        if ($userName -notcontains ($activeUser[$user].Name)) {
            $dataObj[$activeUser[$user].Name + "_status"] = "DisConnected"
            $dataObj[$activeUser[$user].Name + "_logon_logout(1/0)"] = 0
            $dataObj[$activeUser[$user].Name + "_idletime"] = 0
            $dataObj[$activeUser[$user].Name + "_last_logon_time"] = $date
        }
    }
    $dataObj["active_user"] = $active
    return 1
}
$dataObj["heartbeat_required"] = $heartbeat
$data = Get-Data
$dataObj["plugin_version"] = $version

$dataObj | ConvertTo-Json -Compress
