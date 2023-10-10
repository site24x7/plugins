param([string]$url,[string]$agentHostName,[string]$jdeHome,[string]$instanceName,[string]$username,[string]$password)

 

$params = @{
    "agentHostName" = $agentHostName
    "jdeHome" = $jdeHome
    "instanceName" = $instanceName
}

 

 

$base64Auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${password}"))

 

$headers = @{
    "Authorization" = "Basic $base64Auth"
}

 

$version = 4
$heartbeat = "true"
$Status = 1
$msg = $null


try {

    $path="/manage/mgmtrestservice/entserverinstanceinfo"
    $response = Invoke-RestMethod -Uri ($url+$path) -Method Get -Headers $headers -Body $params
    $data=@{}
    $data=$response.entServerInstanceInfoDetail[0]
    #$data | Add-Member -MemberType NoteProperty -Name "Instance Name" -Value $response.instanceName -Force
    $path = "/manage/mgmtrestservice/targettype?instanceName="+$instanceName
    $response = Invoke-RestMethod -Uri ($url+$path) -Method Get -Headers $headers
    $data | Add-Member -MemberType NoteProperty -Name "Instance Name" -Value $response.instanceName -Force
    $data | Add-Member -MemberType NoteProperty -Name "Target Type" -Value $response.targetType -Force
    $path = "/manage/mgmtrestservice/instancestate?instanceName="+$instanceName
    $response = Invoke-RestMethod -Uri ($url+$path) -Method Get -Headers $headers
    $data | Add-Member -MemberType NoteProperty -Name "Instance State" -Value $response.instanceState -Force
} catch {
    $Status = 0
    $msg = $_.Exception.Message + ' ' + $url + $path + ' ' + $response.StatusCode
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
