param([string]$queueName)
$result=@{}

$heartbeat = "true" 
$version=1

Function Get-MSMQServiceCounters {
    try {
        
        $counterPaths = @{
            "Incoming Messages Per Sec" = "\MSMQ Service\Incoming Messages/sec"
            "Outgoing Messages Per Sec" = "\MSMQ Service\Outgoing Messages/sec"
            "MSMQ Incoming Messages" = "\MSMQ Service\MSMQ Incoming Messages"
            "MSMQ Outgoing Messages" = "\MSMQ Service\MSMQ Outgoing Messages"
            "Total Bytes All Queues" = "\MSMQ Service\Total bytes in all queues"
            "Total Messages All Queues" = "\MSMQ Service\Total messages in all queues"
            "Sessions" = "\MSMQ Service\Sessions"
            "IP Sessions" = "\MSMQ Service\IP Sessions"
        }

        $reverseLookup = @{}
        foreach ($metric in $counterPaths.Keys) {
            $reverseLookup[$counterPaths[$metric].ToLower()] = $metric
        }

        $allPaths = @($counterPaths.Values)
        $counterResult = Get-Counter -Counter $allPaths -MaxSamples 1 -ErrorAction Stop

        $foundMetrics = @{}
        foreach ($sample in $counterResult.CounterSamples) {
            $pathLower = ($sample.Path -replace "^\\\\[^\\]+", "").ToLower()
            if ($reverseLookup.ContainsKey($pathLower)) {
                $metric = $reverseLookup[$pathLower]
                $result[$metric] = [math]::Round($sample.CookedValue, 2)
                $foundMetrics[$metric] = $true
            }
        }

        foreach ($metric in $counterPaths.Keys) {
            if (-not $foundMetrics.ContainsKey($metric)) {
                $result[$metric] = -1
                $counterError = "Counter '$metric' not found in results"
                if ($result.ContainsKey("msg")) {
                    $result["msg"] = $result["msg"] + "; " + $counterError
                } else {
                    $result.add("msg", $counterError)
                }
            }
        }
    }
    catch {
        foreach ($metric in @("Incoming Messages Per Sec", "Outgoing Messages Per Sec",
            "MSMQ Incoming Messages", "MSMQ Outgoing Messages",
            "Total Bytes All Queues", "Total Messages All Queues",
            "Sessions", "IP Sessions")) {
            $result[$metric] = -1
        }
        
        $serviceError = "MSMQ Service Error: " + $_.Exception.Message
        if ($result.ContainsKey("msg")) {
            $result["msg"] = $result["msg"] + "; " + $serviceError
        } else {
            $result.add("msg", $serviceError)
        }
    }
}

Function Get-MSMQOutgoingQueues {
    try {
        $outgoing = @(Get-MsmqOutgoingQueue)
        $outgoing_count = @($outgoing).Count

        if ($outgoing_count -eq 0) {
            $result.add("Total Outgoing Queues", 0)
            $result.add("Total Outgoing Messages", 0)
            $result.add("Total Outgoing Bytes", 0)
            $result.add("Total Unacknowledged Messages", 0)
            $result.add("Total Unprocessed Messages", 0)
        } else {
            $totalMessages = ($outgoing | Measure-Object -Property MessageCount -Sum).Sum
            $totalBytes = ($outgoing | Measure-Object -Property BytesInQueue -Sum).Sum
            $totalUnacknowledged = ($outgoing | Measure-Object -Property UnacknowledgedMessageCount -Sum).Sum
            $totalUnprocessed = ($outgoing | Measure-Object -Property UnprocessedMessageCount -Sum).Sum

            $result.add("Total Outgoing Queues", $outgoing_count)
            $result.add("Total Outgoing Messages", $totalMessages)
            $result.add("Total Outgoing Bytes", $totalBytes)
            $result.add("Total Unacknowledged Messages", $totalUnacknowledged)
            $result.add("Total Unprocessed Messages", $totalUnprocessed)
        }
    }
    catch {
        $result.add("Total Outgoing Queues", -1)
        $result.add("Total Outgoing Messages", -1)
        $result.add("Total Outgoing Bytes", -1)
        $result.add("Total Unacknowledged Messages", -1)
        $result.add("Total Unprocessed Messages", -1)

        $outgoingError = "MSMQ Outgoing Queue Error: " + $_.Exception.Message
        if ($result.ContainsKey("msg")) {
            $result["msg"] = $result["msg"] + "; " + $outgoingError
        } else {
            $result.add("msg", $outgoingError)
        }
    }
}

Function Get-Data($name) {
    try {
        $msmq = @(Get-MsmqQueue -QueueType Private -Name ("*" + $name + "*") | 
                Select @{Name="name";Expression={($_.QueueName -split "\\")[-1]}}, 
                       @{Name="Bytes In Queue"; Expression={$_.BytesInQueue}},  
                       @{Name="Bytes In Journal"; Expression={$_.BytesInJournal}},  
                       @{Name="Message Count"; Expression={if ($_.MessageCount -ne $null) { $_.MessageCount } else { 0 }}},  
                       @{Name="Journal Message Count"; Expression={if ($_.JournalMessageCount -ne $null) { $_.JournalMessageCount } else { 0 }}},  
                       @{Name="Message Journal Size"; Expression={ "$([math]::Round($_.MaximumJournalSize / 1MB, 2)) MB"}},  
                       @{Name="Message Queue Size"; Expression={ "$([math]::Round($_.MaximumQueueSize / 1MB, 2)) MB"}},  
                       @{Name="Is Transactional"; Expression={if ($_.Transactional) { "Yes" } else { "No" }}})

        $msmq = $msmq | Select-Object name, "Bytes In Queue", "Bytes In Journal", 
                                     "Message Count", "Journal Message Count", 
                                     "Message Journal Size", "Message Queue Size", 
                                     "Is Transactional"

        $queues_count = @($msmq).Count
        
        Get-MSMQServiceCounters

        Get-MSMQOutgoingQueues

        if ($queues_count -eq 0) {
            $defaultQueue = @{
                "name" = "No Queue"
                "Bytes In Queue" = -1
                "Bytes In Journal" = -1
                "Message Count" = -1
                "Journal Message Count" = -1
                "Message Journal Size" = "-"
                "Message Queue Size" = "-"
                "Is Transactional" = "-"
            }
            
            $result.add("Message Count In Average", 0)
            $result.add("Bytes In Queue In Average", 0)
            $result.add("Total No Of Queues", 0)
            $result.add("Queue", @($defaultQueue))
            if ($result.ContainsKey("msg")) {
                $result["msg"] = $result["msg"] + "; No queues found"
            } else {
                $result.add("msg", "No queues found")
            }
        } else {
            $msg_avg = ($msmq | Measure-Object -Property "Message Count" -Average).Average
            $bytes_in_queue_avg = ($msmq | Measure-Object -Property "Bytes In Queue" -Average).Average

            $result.add("Message Count In Average", $msg_avg)
            $result.add("Bytes In Queue In Average", $bytes_in_queue_avg)
            $result.add("Total No Of Queues", $queues_count)
            $result.add("Queue", @($msmq))
        }
    }
    catch {
        $defaultQueue = @{
            "name" = "-"
            "Bytes In Queue" = -1
            "Bytes In Journal" = -1
            "Message Count" = -1
            "Journal Message Count" = -1
            "Message Journal Size" = "-"
            "Message Queue Size" = "-"
            "Is Transactional" = "-"
        }
        
        $result.add("Message Count In Average", -1)
        $result.add("Bytes In Queue In Average", -1)
        $result.add("Total No Of Queues", -1)
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
$units.Add("Bytes In Queue In Average", "Bytes")
$units.Add("Message Count In Average", "Messages")
$units.Add("Queue", @{
    "Bytes In Queue" = "Bytes"
    "Bytes In Journal" = "Bytes"
})
$units.Add("Total Bytes All Queues", "Bytes")
$units.Add("Total Outgoing Bytes", "Bytes")
$units.Add("Total Outgoing Messages", "Messages")
$units.Add("Total Unacknowledged Messages", "Messages")
$units.Add("Total Unprocessed Messages", "Messages")

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
        "tablist" = @("Incoming Messages Per Sec",
            "Outgoing Messages Per Sec",
            "MSMQ Incoming Messages",
            "MSMQ Outgoing Messages",
            "Total Bytes All Queues",
            "Total Messages All Queues",
            "Sessions",
            "IP Sessions"
        )
    }
    "Outgoing" = @{
        "order" = 3
        "tablist" = @("Total Outgoing Queues",
            "Total Outgoing Messages",
            "Total Outgoing Bytes",
            "Total Unacknowledged Messages",
            "Total Unprocessed Messages"
        )
    }
}
$result.Add('tabs', $tabs)

$result | ConvertTo-Json -Depth 5 -Compress