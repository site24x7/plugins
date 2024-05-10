$dataObj = @{}
$heartbeat = "true" 
$version=1
Function Get-Data
{
    $userInfo=query user
    $activeUser = Get-LocalUser | Select *
    $active = 0
    $disconn = 0
    $userName=@()
    $date1 = Get-Date -Date "01/01/1970"
    [hashtable]$userName_list=[ordered]@{}
    $userCount=($userInfo.Count-1)


    $query_user=$userInfo -split "\n" -replace '\s{18}\s+', "  blank  "
    $qu_object=$query_user -split "\n" -replace '\s\s+', "," | convertfrom-csv

    $qu_object | ForEach-Object {
    $updated_user=$_.USERNAME  -replace ">", ""
    
    if ($_.STATE -eq "Disc"){
        $dataObj.Add($updated_user+"_status","Disconnected" )
        $dataObj.Add($updated_user+"_logon_logout(1/0)",0)
    }elseif($_.STATE -eq "Active") {
        $dataObj.Add($updated_user+"_status",$_.STATE )
        $active+=1
        $dataObj.Add($updated_user+"_logon_logout(1/0)",1)
    }else{
        $dataObj.Add($updated_user+"_status",$_.STATE )
        $dataObj.Add($updated_user+"_logon_logout(1/0)",0)
    
    }

    $userName+=$updated_user
    $dataObj.Add($updated_user+"_idletime", $_.'IDLE TIME')
   

        
    $dataObj.Add($updated_user+"_last_logon_time",$_.'LOGON TIME')
    }



    for($user=1; $user -lt $activeUser.Count; $user=$user+1)
    {
        $date=$activeUser[$user].LastLogon
	    $date = $date -replace '[a-z]', ''
        
        if($userName -notcontains ($activeUser[$user].Name))
        {
          
             $dataObj.Add($activeUser[$user].Name+"_status","DisConnected")
	         $dataObj.Add($activeUser[$user].Name+"_logon_logout(1/0)",0)
             $dataObj.Add($activeUser[$user].Name+"_idletime",0)
             $dataObj.Add($activeUser[$user].Name+"_last_logon_time",$date)
        }
    }
    $dataObj.Add("active_user",$active)
    return 1
}

$dataObj.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$dataObj.Add("plugin_version", $version)

$dataObj | ConvertTo-Json
