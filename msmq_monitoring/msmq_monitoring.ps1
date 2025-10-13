param([string]$queueName)
$result=@{}

$heartbeat = "true" 
$version=1

Function Get-MSMQServiceCounters {
    try {
        
        $counterPaths = @{
            "Incoming_Messages_PerSec" = "\MSMQ Service\Incoming Messages/sec"
            "Outgoing_Messages_PerSec" = "\MSMQ Service\Outgoing Messages/sec"
            "MSMQ_Incoming_Messages" = "\MSMQ Service\MSMQ Incoming Messages"
            "MSMQ_Outgoing_Messages" = "\MSMQ Service\MSMQ Outgoing Messages"
            "Total_Bytes_All_Queues" = "\MSMQ Service\Total bytes in all queues"
            "Total_Messages_All_Queues" = "\MSMQ Service\Total messages in all queues"
            "Sessions" = "\MSMQ Service\Sessions"
            "IP_Sessions" = "\MSMQ Service\IP Sessions"
        }
        
        foreach ($metric in $counterPaths.Keys) {
            try {
                $counterResult = Get-Counter -Counter $counterPaths[$metric] -MaxSamples 1 -ErrorAction SilentlyContinue
                if ($counterResult -and $counterResult.CounterSamples) {
                    $counterValue = $counterResult.CounterSamples.CookedValue
                    $result[$metric] = [math]::Round($counterValue, 2)
                } else {
                    $result[$metric] = -1
                    $counterError = "Counter '$metric' not found or invalid path: $($counterPaths[$metric])"
                    if ($result.ContainsKey("msg")) {
                        $result["msg"] = $result["msg"] + "; " + $counterError
                    } else {
                        $result.add("msg", $counterError)
                    }
                }
            }
            catch {
                $result[$metric] = -1
                $counterError = "Counter '$metric' failed: " + $_.Exception.Message
                if ($result.ContainsKey("msg")) {
                    $result["msg"] = $result["msg"] + "; " + $counterError
                } else {
                    $result.add("msg", $counterError)
                }
            }
        }
    }
    catch {
        $result.add("Incoming_Messages_PerSec", -1)
        $result.add("Outgoing_Messages_PerSec", -1)
        $result.add("MSMQ_Incoming_Messages", -1)
        $result.add("MSMQ_Outgoing_Messages", -1)
        $result.add("Total_Bytes_All_Queues", -1)
        $result.add("Total_Messages_All_Queues", -1)
        $result.add("Sessions", -1)
        $result.add("IP_Sessions", -1)
        
        $serviceError = "MSMQ Service Error: " + $_.Exception.Message
        if ($result.ContainsKey("msg")) {
            $result["msg"] = $result["msg"] + "; " + $serviceError
        } else {
            $result.add("msg", $serviceError)
        }
    }
}

Function Get-Data($name) {
    try {
        $msmq = @(Get-MsmqQueue -QueueType Private -Name ("*" + $name + "*") | 
                Select @{Name="name";Expression={($_.QueueName -split "\\")[-1]}}, 
                       @{Name="Bytes_In_Queue"; Expression={$_.BytesInQueue}},  
                       @{Name="Bytes_In_Journal"; Expression={$_.BytesInJournal}},  
                       @{Name="Message_Count"; Expression={if ($_.MessageCount -ne $null) { $_.MessageCount } else { 0 }}},  
                       @{Name="Message_Journal_Size_MB"; Expression={ [math]::Round($_.MaximumJournalSize / 1MB, 2)}},  
                       @{Name="Message_Queue_Size_MB"; Expression={ [math]::Round($_.MaximumQueueSize / 1MB, 2)}},  
                       @{Name="Is_Transactional"; Expression={if ($_.Transactional) { 1 } else { 0 }}})

        $msmq = $msmq | Select-Object name, "Bytes_In_Queue", "Bytes_In_Journal", 
                                     "Message_Count", "Message_Journal_Size_MB", 
                                     "Message_Queue_Size_MB", "Is_Transactional"

        $queues_count = @($msmq).Count
        
        Get-MSMQServiceCounters

        if ($queues_count -eq 0) {
            $defaultQueue = @{
                "name" = "No Queue"
                "Bytes_In_Queue" = -1
                "Bytes_In_Journal" = -1
                "Message_Count" = -1
                "Message_Journal_Size_MB" = -1
                "Message_Queue_Size_MB" = -1
                "Is_Transactional" = -1
            }
            
            $result.add("Message Count in average", 0)
            $result.add("Bytes In Queue in average", 0)
            $result.add("Total No of queues", 0)
            $result.add("Queue", @($defaultQueue))
            $result.add("msg", "No queues found")
        } else {
            $msg_avg = ($msmq | Measure-Object -Property "Message_Count" -Average).Average
            $bytes_in_queue_avg = ($msmq | Measure-Object -Property "Bytes_In_Queue" -Average).Average

            $result.add("Message Count in average", $msg_avg)
            $result.add("Bytes In Queue in average", $bytes_in_queue_avg)
            $result.add("Total No of queues", $queues_count)
            $result.add("Queue", @($msmq))
        }
    }
    catch {
        $defaultQueue = @{
            "name" = "-"
            "Bytes_In_Queue" = -1
            "Bytes_In_Journal" = -1
            "Message_Count" = -1
            "Message_Journal_Size_MB" = -1
            "Message_Queue_Size_MB" = -1
            "Is_Transactional" = -1
        }
        
        $result.add("Message Count in average", -1)
        $result.add("Bytes In Queue in average", -1)
        $result.add("Total No of queues", -1)
        $result.add("Queue", @($defaultQueue))
        
        $queueError = "MSMQ Queue Error: " + $_.Exception.Message
        if ($result.ContainsKey("msg")) {
            $result["msg"] = $result["msg"] + "; " + $queueError
        } else {
            $result.add("msg", $queueError)
        }
    }
}

Get-Data $queueName
$result.Add("heartbeat_required", $heartbeat)
$result.Add("plugin_version", $version)

$units = @{}
$units.Add("Bytes In Queue in average", "Bytes")
$units.Add("Message Count in average", "messages")
$units.Add("Queue", @{
    "Bytes_In_Queue" = "Bytes"
    "Bytes_In_Journal" = "Bytes"
    "Message_Journal_Size_MB" = "MB"
    "Message_Queue_Size_MB" = "MB"
})
$units.Add("Total_Bytes_All_Queues", "Bytes")

$result.Add('units', $units)

$s247config = @{}
$s247config.Add("childdiscovery", @("Queue"))
$result.Add('s247config', $s247config)

$tabs = @{
    "Queues" = @{
        "order" = 1
        "tablist" = @("Queue")
    }
    "Service" = @{
        "order" = 2
        "tablist" = @("Incoming_Messages_PerSec",
            "Outgoing_Messages_PerSec",
            "MSMQ_Incoming_Messages",
            "MSMQ_Outgoing_Messages",
            "Total_Bytes_All_Queues",
            "Total_Messages_All_Queues",
            "Sessions",
            "IP_Sessions"
        )
    }
}
$result.Add('tabs', $tabs)

$result | ConvertTo-Json -Depth 5 -Compress
