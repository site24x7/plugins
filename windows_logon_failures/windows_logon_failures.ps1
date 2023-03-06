param([string]$threshold)
$output = @{}
$heartbeat = "true" 
$version=9
$msg=""
$status=1
Function Get-Data($count)
{

$outdata=@{}
  
$startTime = (Get-Date).AddMinutes(-5)
$Events=Get-EventLog -LogName Security -Source "Microsoft-Windows-Security-Auditing" -InstanceId 4625 -EntryType FailureAudit -After $startTime
$Log=[System.Collections.ArrayList]@()
$event_count=$Events.Count

$outdata.Add("failed_login_count",$event_count)
if($event_count -gt $count){

foreach($Event in $Events){

    
    $TimeStamp=$Event.TimeGenerated
    $UserTried=$Event.ReplacementStrings[5]
    $DomainTried=$Event.ReplacementStrings[6]
    $ClientNameFrom=$Event.ReplacementStrings[13] 
    $ClientIPFrom=$Event.ReplacementStrings[19]

    $msg1="`nLogin failure at $TimeStamp : User '$UserTried' from domain '$DomainNameFrom' attempted to log in from IP address $ClientIPFrom." -replace '[^a-zA-Z0-9.,:\s]' , ""
    
    $global:msg+=$msg1

}  
$global:status=0

}

$outdata
}


$output.Add("heartbeat_required", $heartbeat)
try{
  $data =Get-Data $threshold
  $output.Add("data", ($data))

  if($global:status -eq 0){

    $output.Add("status",0)
    $output.Add("msg",$global:msg)

  }

}
catch{

  $output.add("Status",0)
  $output.add("msg", $Error[0])
  $output
}
$output.Add("plugin_version", $version)
$output | ConvertTo-Json
