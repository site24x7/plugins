param([string]$UserName)

$output = @{}
$flag = 0
$heartbeat = "true" 
$version=1
$date1 = Get-Date -Date "01/01/1970"
Function Get-Data
{
    $userInfo=query user
    $dataObj = @{}
    for($user=1; $user -lt $userInfo.Count; $user=$user+1)
    {
       $userInfo[$user] = $userInfo[$user].Substring(1,($userInfo[$user].Length-1));
       $userarr = ($userInfo[$user] -replace '\s+', ' ') -split " "
      
       if($userarr[0] -eq $UserName)
       {
           if($userarr[3] -eq "Active")
           {
               if($userarr[4] -eq '.')
               {
                   $dataObj.Add($userarr[0]+"_idletime","0")
               }
               else
               {
                   $dataObj.Add($userarr[0]+"_idletime",$userarr[4])
               }
           }
           $dataObj.Add($userarr[0]+"_status","Active")
           $dataObj.Add($userarr[0]+"_logon_logout(1/0)",1)
           $dataObj.Add($userarr[0]+"_last_logon_time",$userarr[5]+" "+$userarr[6]+" "+$userarr[7])
           $flag = 1
           break
        }
    }
    if($flag -eq 0)
    {
        $activeUser = Get-LocalUser | Select *
        for($user=1; $user -lt $activeUser.Count; $user=$user+1)
        {
            if($activeUser[$user].Name -eq $UserName)
            {
                $date=$activeUser[$user].LastLogon
                $date = $date -replace '[a-z]', ''
                $dataObj.Add($activeUser[$user].Name+"_last_logon_time",$date)
                $dataObj.Add($activeUser[$user].Name+"_status","DisConnected")
                $dataObj.Add($activeUser[$user].Name+"_logon_logout(1/0)",0)
                $dataObj.Add($activeUser[$user].Name+"_idletime","0")
                break
            }
        }
    }

    if($dataObj.Count -eq 0)
    {
        $dataObj.Add("msg","User not found")
    }
    return $dataObj
}
$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$output.Add("data", ($data))
$output.Add("plugin_version", $version)

$output | ConvertTo-Json
