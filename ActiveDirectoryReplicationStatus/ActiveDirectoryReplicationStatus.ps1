$msg= ""
try
{
    $domainControlerName = (Get-ADDomainController).HostName
    $replicationPartners = Get-ADReplicationPartnerMetadata -Target $domainControlerName -PartnerType Both | select Server,@{n="Partner";e={(Resolve-DnsName $_.PartnerAddress).NameHost}},Partition,PartnerType,LastReplicationAttempt,LastReplicationResult,LastReplicationSuccess # | Where-Object { $_.Partner -eq 'win-76qkdkpe00a.mylocal.com'}
    $replicationfailure = Get-ADReplicationFailure -Target $domainControlerName | select Server,@{n="Partner";e={(Resolve-DnsName $_.PartnerAddress).NameHost}},FailureCount,FailureType,FirstFailureTime,LastError # | Where-Object { $_.Partner -eq 'win-76qkdkpe00a.mylocal.com'}
    $InboundData = $replicationPartners | Where-Object {$_.PartnerType -eq 'Inbound'}
    $OutboundData = $replicationPartners | Where-Object {$_.PartnerType -eq 'Outbound'}
    $InboundPartners = if($InboundData.Partner) { $InboundData.Partner -join ',' } else { "-" }
    $OutboundPartners = if($OutboundData.Partner) { $OutboundData.Partner -join ',' } else { "-" }
}
catch
{
    $msg = $Error[0].Exception.Message
}
if($InboundData.Count -gt 0)
{
    $InboundLastAttempt = (($InboundData | Sort-Object -Property LastReplicationAttempt -Descending )[0].LastReplicationAttempt).Tostring()
}
else
{
    $InboundLastAttempt = "-"
}
if($InboundData.Count -gt 0)
{
    $InboundLastAttemptPartner = ($InboundData | Sort-Object -Property LastReplicationAttempt -Descending )[0].Partner
}
else
{
    $InboundLastAttemptPartner = "-"
}
if($InboundData.Count -gt 0)
{
    $InboundLastSuccess = (($InboundData | Sort-Object -Property LastReplicationSuccess -Descending )[0].LastReplicationSuccess).Tostring()
}
else
{
    $InboundLastSuccess = "-"
}
if($InboundData.Count -gt 0)
{
    $InboundLastSuccessPartner = ($InboundData | Sort-Object -Property LastReplicationSuccess -Descending )[0].Partner
}
else
{
    $InboundLastSuccessPartner = "-"
}
if($InboundData.Count -gt 0)
{
    $InboundLastResult = ($InboundData | Sort-Object -Property LastReplicationSuccess -Descending )[0].LastReplicationResult
}
else
{
    $InboundLastResult = -1
}
if($OutboundData.Count -gt 0)
{
    $OutboundLastAttempt = (($OutboundData | Sort-Object -Property LastReplicationAttempt -Descending )[0].LastReplicationAttempt).Tostring()
}
else
{
    $OutboundLastAttempt = "-"
}
if($OutboundData.Count -gt 0)
{
    $OutboundLastAttemptPartner = ($OutboundData | Sort-Object -Property LastReplicationAttempt -Descending )[0].Partner
}
else
{
    $OutboundLastAttemptPartner = "-"
}
if($OutboundData.Count -gt 0)
{
    $OutboundLastSuccess = (($OutboundData | Sort-Object -Property LastReplicationSuccess -Descending )[0].LastReplicationSuccess).Tostring()
}
else
{
    $OutboundLastSuccess = "-"
}
if($OutboundData.Count -gt 0)
{
    $OutboundLastSuccessPartner = ($OutboundData | Sort-Object -Property LastReplicationSuccess -Descending )[0].Partner
}
else
{
    $OutboundLastSuccessPartner = "-"
}
if($OutboundData.Count -gt 0)
{
    $OutboundLastResult = ($OutboundData | Sort-Object -Property LastReplicationSuccess -Descending )[0].LastReplicationResult
}
else
{
    $OutboundLastResult = -1
}
$FailureCount = 0
$FailureType = "-"
$FirstFailureTime = "-"
$LastError = -1
$ErrorPartner = "-"
$ErrorServer = "-"
$Status = 1
if($replicationfailure -ne $null)
{

    if ($replicationfailure -eq 1){
        $FailureCount = $replicationfailure.FailureCount
        $FailureType = $replicationfailure.FailureType
        $FirstFailureTime = $replicationfailure.FirstFailureTime
        $LastError = $replicationfailure.LastError
        $ErrorPartner = $replicationfailure.Partner
        $ErrorServer = $replicationfailure.Server
    }
    else{

        $FailureCount = ($replicationfailure | Measure-Object -Property FailureCount -sum).sum
        $FailureType = $replicationfailure.FailureType  -join ','
        $FirstFailureTime = $replicationfailure.FirstFailureTime  -join ','
        $LastError = $replicationfailure.LastError  -join ','
        $ErrorPartner = $replicationfailure.Partner  -join ','
        $ErrorServer = $replicationfailure.Server  -join ','

    }
    
    if($FailureCount -eq $null)
    {
        $FailureCount = 0
    }
    if($FailureType -eq $null)
    {
        $FailureType = "-"
    }
    if($FirstFailureTime -eq $null)
    {
        $FirstFailureTime = "-"
    }
    if($LastError -eq $null)
    {
        $LastError = -1
    }
    if($ErrorPartner -eq $null)
    {
        $ErrorPartner = "-"
    }
    if($ErrorServer -eq $null)
    {
        $ErrorServer = "-"
    }
    $replicationfailure | ForEach-Object {
    
    $diff = New-TimeSpan -Start $_.FirstFailureTime -End (Get-Date)
    if($diff.TotalSeconds -gt -300 -and $diff.TotalSeconds -lt 300)
    {
        $Status = 0
        $msg="The difference in First Failure Time and current time is $($diff.TotalSeconds)s"
    }
    }
} 

$data = @{}
if($msg.Length -eq 0)
{
    $data.Add("InboundPartners",$InboundPartners)
    $data.Add("OutboundPartners",$OutboundPartners)
    $data.Add("InboundLastAttempt",$InboundLastAttempt)
    $data.Add("InboundLastAttemptPartner",$InboundLastAttemptPartner)
    $data.Add("InboundLastSuccess",$InboundLastSuccess)
    $data.Add("InboundLastSuccessPartner",$InboundLastSuccessPartner)
    $data.Add("InboundLastResult",$InboundLastResult)
    $data.Add("OutboundLastAttempt",$OutboundLastAttempt)
    $data.Add("OutboundLastAttemptPartner",$OutboundLastAttemptPartner)
    $data.Add("OutboundLastSuccess",$OutboundLastSuccess)
    $data.Add("OutboundLastSuccessPartner",$OutboundLastSuccessPartner)
    $data.Add("OutboundLastResult",$OutboundLastResult)
    $data.Add("FailureCount",$FailureCount)
    $data.Add("ErrorPartner",$ErrorPartner)
    $data.Add("ErrorServer",$ErrorServer)
    $data.Add("LastError",$LastError)
    $data.Add("FirstFailureTime",$FirstFailureTime)
    $data.Add("FailureType",$FailureType)
    $data.Add("Status",$Status)
}
else
{
    $data.Add("Status",0)
    $data.Add("msg",$msg)
}



### Mandatory - If any attributes added or removed in the plugin, increment the plugin version here to update the plugins template.
$version = 1  

### Mandatory - Setting this to true will alert you when there is a communication problem while posting plugin data to server
$heartbeat = "true" 

### OPTIONAL - Display name to be displayed in Site24x7 client
$displayname = $domainControlerName + " - AD Replication Status"  


$data.Add("plugin_version", $version)
$data.Add("heartbeat_required", $heartbeat)
$data.Add("displayname", $displayname) 

### Returns the monitoring data to Site24x7 servers
return $data | ConvertTo-Json
