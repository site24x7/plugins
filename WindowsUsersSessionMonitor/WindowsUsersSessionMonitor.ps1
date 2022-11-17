$output = @{}
$units = @{}
$heartbeat = "true" 
$version=1
Function Get-Data
{
    $userInfo=query user
    $activeUser = Get-LocalUser | Select *
    $dataObj = @{}
    $active = 0
    $disconn = 0
    $userName=@()
    $date1 = Get-Date -Date "01/01/1970"
    [hashtable]$userName_list=[ordered]@{}
    $userCount=($userInfo.Count-1)
    for($user=1; $user -lt $userInfo.Count; $user=$user+1)
    {
       $userInfo[$user] = $userInfo[$user].Substring(1,($userInfo[$user].Length-1));
       $userarr = ($userInfo[$user] -replace '\s+', ' ') -split " "
       if($userarr[3] -eq "Active")
       {
          $active=$active+1
          $userName += $userarr[0]
       }
    }

    for($user=1; $user -lt $activeUser.Count; $user=$user+1)
    {
        $date=$activeUser[$user].LastLogon
	$date = $date -replace '[a-z]', ''
        $dataObj.Add($activeUser[$user].Name+"_last_logon_time",$date)
        if($userName.Contains($activeUser[$user].Name))
        {
             $dataObj.Add($activeUser[$user].Name+"_status","Active")
	     $dataObj.Add($activeUser[$user].Name+"_logon_logout(1/0)",1)
        }
        else
        {
             $dataObj.Add($activeUser[$user].Name+"_status","DisConnected")
	     $dataObj.Add($activeUser[$user].Name+"_logon_logout(1/0)",0)
        }
    }
    $dataObj.Add("active_user",$active)
    return $dataObj
}

$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$output.Add("data", ($data))
$output.Add("units",($units))
$output.Add("plugin_version", $version)

$output | ConvertTo-Json
