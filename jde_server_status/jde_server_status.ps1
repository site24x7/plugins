﻿param([string]$url,[string]$agentHostName,[string]$jdeHome,[string]$instanceName,[string]$username,[string]$password)


$params = @{

    "agentHostName" = $agentHostName

    "jdeHome" = $jdeHome

    "instanceName" = $instanceName

}



$base64Auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${password}"))



$headers = @{

    "Authorization" = "Basic $base64Auth"

}



$version = 1

$heartbeat = "true"

$Status = 1

$msg = $null



try {


    $data=@{}


    $path = "/manage/mgmtrestservice/targettype?instanceName="+$instanceName

    $response = Invoke-RestMethod -Uri ($url+$path) -Method Get -Headers $headers

    $data.add( "Instance Name", $response.instanceName)

    $data.add( "Target Type",$response.targetType)

    $path = "/manage/mgmtrestservice/instancestate?instanceName="+$instanceName

    $response = Invoke-RestMethod -Uri ($url+$path) -Method Get -Headers $headers

    $data.add( "Instance State", $response.instanceState )

} catch {

    $Status = 0

    $msg =  $_.Exception.Message + ' ' + $url + $path + ' ' + $response.StatusCode

}



$mainJson = @{

    "plugin_version" = $version

    "heartbeat_required" = $heartbeat

    "data" = $data

}




if ($Status -eq 0) {

    $mainJson["status"] = 0

}


if ($msg -ne $null) {

    $mainJson["msg"] = $msg

}


return $mainJson | ConvertTo-Json
