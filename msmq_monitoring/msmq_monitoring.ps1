param([string]$queueName)
$result=@{}

$heartbeat = "true" 
$version=1


Function Get-Data($name)
{

try{
$msmq=Get-MsmqQueue -QueueType Private -Name ("*"+$name+"*") | Select  @{Name="name";Expression={($_.QueueName -split "\\")[-1]}}, @{Name="Bytes_In_Queue"; Expression={$_.BytesInQueue}},  @{Name="Bytes_In_Journal"; Expression={$_.BytesInJournal}},  @{Name="Message_Count"; Expression={$_.MessageCount}},  @{Name="Maximum_Journal_Size_MB"; Expression={ [math]::Round($_.MaximumJournalSize/ 1MB,2)}},  @{Name="Maximum_Queue_Size_MB"; Expression={ [math]::Round($_.MaximumQueueSize/ 1MB,2)}}, Transactional

$msmq | ForEach-Object{

    $result.add($_.name+" Transactional",$_.Transactional)

}

$msmq= $msmq | Select name, Bytes_In_Queue, Bytes_In_Journal, Message_Count, Maximum_Journal_Size_MB, Maximum_Queue_Size_MB

$queues_count=$msmq.Count
if ( $queues_count -gt 24){
$queues_count=25
}

$msg_avg=($msmq | Measure-Object -Property Message_Count -Average).Average
$bytes_in_queue_avg=($msmq | Measure-Object -Property Bytes_In_Queue -Average).Average
$result.add("Message Count [average]",$msg_avg)
$result.add("Bytes In Queue [average]",$bytes_in_queue_avg)
$result.add("No of queues monitored",([string]$queues_count+" queues"))

$result.add("queue",$msmq)

}
catch{

$result.add("status",0)
$result.add("msg", $Error[0])

}
}

Get-Data $queueName
$result.Add("heartbeat_required", $heartbeat)
$result.Add("plugin_version", $version)
$units=@{}
$units.Add("Bytes In Queue [average]","Bytes")
$units.Add("Message Count [average]","messages")
$result.Add('units',$units)

$result | ConvertTo-Json -Compress
