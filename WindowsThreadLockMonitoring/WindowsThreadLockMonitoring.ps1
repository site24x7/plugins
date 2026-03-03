$ErrorActionPreference = "Stop"

$version = "1"
$heartbeat = "true"

$status = 1
$msg = ""

$DotnetLocksTotalContentions = 0
$DotnetLocksTotalContentionsDelta = 0
$DotnetLocksContentionRatePerSecGlobal = 0
$DotnetLocksCurrentQueueLengthGlobal = 0
$DotnetLocksQueueLengthPerSecGlobal = 0
$DotnetLocksQueueLengthPeakGlobal = 0
$DotnetLocksCurrentLogicalThreads = 0
$DotnetLocksCurrentPhysicalThreads = 0
$DotnetLocksRateRecognizedThreadsPerSec = 0
$DotnetLocksCurrentRecognizedThreads = 0
$DotnetLocksTotalRecognizedThreads = 0

$SystemProcessorQueueLength = 0
$CpuTotalUsagePercent = 0
$ProcessThreadCount = 0
$SystemContextSwitchesPerSec = 0
$SystemThreads = 0

$processTable = @()


try {    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\Total # of Contentions' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksTotalContentions = if ($null -eq $v) { 0 } else { [long]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksTotalContentions = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\Contention Rate / sec' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksContentionRatePerSecGlobal = if ($null -eq $v) { 0 } else { [math]::Round($v, 2) }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksContentionRatePerSecGlobal = -1
}

try {    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\Current Queue Length' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksCurrentQueueLengthGlobal = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksCurrentQueueLengthGlobal = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\Queue Length / sec' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksQueueLengthPerSecGlobal = if ($null -eq $v) { 0 } else { [math]::Round($v, 2) }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksQueueLengthPerSecGlobal = -1
}

try {    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\Queue Length Peak' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksQueueLengthPeakGlobal = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksQueueLengthPeakGlobal = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\# of current logical Threads' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksCurrentLogicalThreads = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksCurrentLogicalThreads = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\# of current physical Threads' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksCurrentPhysicalThreads = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksCurrentPhysicalThreads = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\Rate of recognized threads / sec' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksRateRecognizedThreadsPerSec = if ($null -eq $v) { 0 } else { [math]::Round($v, 2) }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksRateRecognizedThreadsPerSec = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\# of current recognized threads' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksCurrentRecognizedThreads = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksCurrentRecognizedThreads = -1
}

try {
    $v = (Get-Counter -Counter '\.NET CLR LocksAndThreads(_Global_)\# of total recognized threads' -ErrorAction Stop).CounterSamples[0].CookedValue
    $DotnetLocksTotalRecognizedThreads = if ($null -eq $v) { 0 } else { [long]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksTotalRecognizedThreads = -1
}

try {
    $stateFile = "$PSScriptRoot\locks_state.json"
    $prev = 0
    if (Test-Path $stateFile) {
        try { 
            $prev = (Get-Content $stateFile | ConvertFrom-Json).total 
        } catch {
        }
    }
    
    if ($DotnetLocksTotalContentions -ge 0) {
        $DotnetLocksTotalContentionsDelta = [math]::Max(0, $DotnetLocksTotalContentions - $prev)
        @{ total = $DotnetLocksTotalContentions } | ConvertTo-Json | Set-Content $stateFile -Force
    } else {
        $DotnetLocksTotalContentionsDelta = -1
    }
} catch {
    $msg += "$($_.Exception.Message) "
    $DotnetLocksTotalContentionsDelta = -1
}

try {    $v = (Get-Counter -Counter '\System\Processor Queue Length' -ErrorAction Stop).CounterSamples[0].CookedValue
    $SystemProcessorQueueLength = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $SystemProcessorQueueLength = -1
}

try {
    $v = (Get-Counter -Counter '\Processor(_Total)\% Processor Time' -ErrorAction Stop).CounterSamples[0].CookedValue
    $CpuTotalUsagePercent = if ($null -eq $v) { 0 } else { [math]::Round($v, 2) }
} catch {
    $msg += "$($_.Exception.Message) "
    $CpuTotalUsagePercent = -1
}

try {
    $v = (Get-Counter -Counter '\Process(_Total)\Thread Count' -ErrorAction Stop).CounterSamples[0].CookedValue
    $ProcessThreadCount = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $ProcessThreadCount = -1
}

try {
    $v = (Get-Counter -Counter '\System\Context Switches/sec' -ErrorAction Stop).CounterSamples[0].CookedValue
    $SystemContextSwitchesPerSec = if ($null -eq $v) { 0 } else { [math]::Round($v, 2) }
} catch {
    $msg += "$($_.Exception.Message) "
    $SystemContextSwitchesPerSec = -1
}

try {
    $v = (Get-Counter -Counter '\System\Threads' -ErrorAction Stop).CounterSamples[0].CookedValue
    $SystemThreads = if ($null -eq $v) { 0 } else { [int]$v }
} catch {
    $msg += "$($_.Exception.Message) "
    $SystemThreads = -1
}

try {
    $processCounter = 1
    Get-Process |
    Where-Object { $_.CPU -ne $null } |
    Sort-Object CPU -Descending |
    Select-Object -First 5 |
    ForEach-Object {
        $processTable += [ordered]@{
            "name"           = "Process$processCounter"
            "Process Name"   = $_.ProcessName
            "Thread Count"   = $_.Threads.Count
            "Memory"      = [math]::Round($_.WorkingSet64 / 1MB, 2)
        }
        $processCounter++
    }
} catch {
    $msg += "$($_.Exception.Message) "
}

$mainJson = @{
    "plugin_version" = $version
    "heartbeat_required" = $heartbeat
    "status" = $status
    "msg" = if ($msg) { $msg } else { "Success" }    
    "units" = @{
        "Dotnet Locks Total Contentions"               = "contentions"
        "Dotnet Locks Total Contentions Delta"         = "contentions"
        "Dotnet Locks Contention Rate Per Sec Global"  = "contentions/sec"
        "Dotnet Locks Current Queue Length Global"     = "waiting_threads"
        "Dotnet Locks Queue Length Per Sec Global"     = "queue_events/sec"
        "Dotnet Locks Queue Length Peak Global"        = "peak_waiting_threads"
        "Dotnet Locks Current Logical Threads"         = "threads"
        "Dotnet Locks Current Physical Threads"        = "threads"
        "Dotnet Locks Rate Recognized Threads Per Sec" = "threads/sec"
        "Dotnet Locks Current Recognized Threads"      = "threads"        
        "Dotnet Locks Total Recognized Threads"        = "threads"
        "System Processor Queue Length"                = "waiting_threads"
        "Cpu Total Usage Percent"                      = "percent"
        "Process Thread Count"                         = "threads"
        "System Context Switches Per Sec"              = "switches/sec"
        "System Threads"                               = "threads"
        "Top Processes"= @{
            "Thread Count" = "threads"
            "Memory" = "MB"
        }
    }
    "Dotnet Locks Total Contentions" = $DotnetLocksTotalContentions
    "Dotnet Locks Total Contentions Delta" = $DotnetLocksTotalContentionsDelta
    "Dotnet Locks Contention Rate Per Sec Global" = $DotnetLocksContentionRatePerSecGlobal
    "Dotnet Locks Current Queue Length Global" = $DotnetLocksCurrentQueueLengthGlobal
    "Dotnet Locks Queue Length Per Sec Global" = $DotnetLocksQueueLengthPerSecGlobal
    "Dotnet Locks Queue Length Peak Global" = $DotnetLocksQueueLengthPeakGlobal
    "Dotnet Locks Current Logical Threads" = $DotnetLocksCurrentLogicalThreads
    "Dotnet Locks Current Physical Threads" = $DotnetLocksCurrentPhysicalThreads
    "Dotnet Locks Rate Recognized Threads Per Sec" = $DotnetLocksRateRecognizedThreadsPerSec
    "Dotnet Locks Current Recognized Threads" = $DotnetLocksCurrentRecognizedThreads    
    "Dotnet Locks Total Recognized Threads" = $DotnetLocksTotalRecognizedThreads
    "System Processor Queue Length" = $SystemProcessorQueueLength
    "Cpu Total Usage Percent" = $CpuTotalUsagePercent
    "Process Thread Count" = $ProcessThreadCount
    "System Context Switches Per Sec" = $SystemContextSwitchesPerSec
    "System Threads" = $SystemThreads
}

if ($processTable.Count -gt 0) {
    $mainJson["Top Processes"] = $processTable
}

$mainJson | ConvertTo-Json -Depth 5 -Compress
