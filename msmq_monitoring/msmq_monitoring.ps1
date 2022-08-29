param([string]$queueName)
$output = @{}

$heartbeat = "true" 
$version=1
Function Get-Data($name)
{

try{
  
  $outdata=@{}
  
  $msgc=(Get-MsmqQueue -Name $name | select MessageCount).MessageCount
  $msgb=(Get-MsmqQueue -Name $name | select BytesInQueue).BytesInQueue
  $msgbjournal=(Get-MsmqQueue -Name $name | select BytesInJournal).BytesInJournal
  $machinename=(Get-MsmqQueue -Name $name | select MachineName).MachineName

  [int]$maxjournalsize=((Get-MsmqQueue -Name $name | select MaximumJournalSize).MaximumJournalSize)/ 1MB
  [string]$maxjournalsize=$maxjournalsize
  $maxjournalsize=$maxjournalsize+" Mb"

  [int]$maxqueuesize=((Get-MsmqQueue -Name $name | select MaximumQueueSize).MaximumQueueSize)/ 1MB
  [string]$maxqueuesize=$maxqueuesize
  $maxqueuesize=$maxqueuesize+" Mb"

  $transactional=(Get-MsmqQueue -Name $name | select Transactional).Transactional


  $outdata.Add("Message Count",($msgc))
  $outdata.Add("Bytes In Queue",($msgb))
  $outdata.Add("Bytes In Journal",($msgbjournal))
  $outdata.Add("Machine Name",($machinename))
  
  $outdata.Add("Max Journal Size",($maxjournalsize))
  $outdata.Add("Max Queue Size",($maxqueuesize))
  
  $outdata.Add("Transactional",($transactional))
  $outdata.Add("Queue Name",($name))
  
  
  $outdata
  }
  catch{

  $outdata.add("status",0)
  $outdata.add("msg", $Error[0])
  $outdata

  }
}


$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data $queueName
$output.Add("data", ($data))
$output.Add("plugin_version", $version)
$units=@{}
$units.Add("Bytes In Queue","Bytes")
$units.Add("Bytes In Journal","Bytes")
$output.Add('units',$units)

$output | ConvertTo-Json
