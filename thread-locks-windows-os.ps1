<#
threadlocks.ps1
Collects only OS-level thread/lock metrics and outputs a single flat JSON object.
No .NET counters, no timestamps. Suitable for Site24x7 plugin ingestion.

Metrics (flat keys):
  - total_threads
  - blocked_threads_count
  - threads_waiting_on_sync_count
  - processor_queue_length
  - context_switches_per_sec

Also includes:
  - plugin_version (int)
  - heartbeat_required ("true")
  - units (map)
  - msg (string) for non-fatal errors/warnings

Run as-is. Get-CimInstance Win32_Thread enumeration can be slow on systems with many threads.
#>

# Helper conversions
function Safe-Int([object]$v) {
    try {
        if ($null -eq $v) { return $null }
        return [int]$v
    } catch {
        return $null
    }
}
function Safe-Double([object]$v) {
    try {
        if ($null -eq $v) { return $null }
        return [double]$v
    } catch {
        return $null
    }
}

# Base output
$output = @{
    plugin_version = 1
    heartbeat_required = "true"

    total_threads = $null
    blocked_threads_count = $null
    threads_waiting_on_sync_count = $null
    processor_queue_length = $null
    context_switches_per_sec = $null

    units = @{
        total_threads = "count"
        blocked_threads_count = "count"
        threads_waiting_on_sync_count = "count"
        processor_queue_length = "count"
        context_switches_per_sec = "per_sec"
    }

    msg = ""
}

# --- 1) Fast perf counters (system-level) ---
try {
    $sys = Get-CimInstance -Namespace root\cimv2 -ClassName Win32_PerfFormattedData_PerfOS_System -ErrorAction Stop
    if ($sys -ne $null) {
        if ($sys.Threads -ne $null) { $output.total_threads = Safe-Int($sys.Threads) }
        if ($sys.ProcessorQueueLength -ne $null) { $output.processor_queue_length = Safe-Int($sys.ProcessorQueueLength) }
        if ($sys.ContextSwitchesPersec -ne $null) { $output.context_switches_per_sec = Safe-Double($sys.ContextSwitchesPersec) }
    }
} catch {
    $err = $_.Exception.Message
    if ($output.msg -ne "") { $output.msg = $output.msg + " | perf_read_err:" + $err } else { $output.msg = "perf_read_err:" + $err }
}

# --- 2) Win32_Thread enumeration for blocked counts and sync waits (best-effort) ---
try {
    $threads = Get-CimInstance -ClassName Win32_Thread -ErrorAction Stop

    $total = 0
    $blocked = 0
    $syncWaits = 0

    foreach ($t in $threads) {
        $total += 1

        # ThreadWaitReason may be null/0 when not waiting on a reason
        $waitReason = $null
        try { $waitReason = $t.ThreadWaitReason } catch { $waitReason = $null }

        $hasWaitReason = ($waitReason -ne $null -and $waitReason -ne 0 -and $waitReason -ne "")
        if ($hasWaitReason) { $syncWaits += 1 }

        # ThreadState: 5 means Waiting (per Win32_Thread doc); treat Waiting or having a wait reason as blocked
        $isWaiting = $false
        try {
            $stateInt = 0
            if ($t.ThreadState -ne $null -and [int]::TryParse([string]$t.ThreadState, [ref]$stateInt) -and $stateInt -eq 5) {
                $isWaiting = $true
            }
        } catch {}

        if ($hasWaitReason) { $isWaiting = $true }
        if ($isWaiting) { $blocked += 1 }
    }

    # Fill totals if not provided by perf above
    if ($output.total_threads -eq $null) { $output.total_threads = $total }
    $output.blocked_threads_count = $blocked
    $output.threads_waiting_on_sync_count = $syncWaits

} catch {
    $err = $_.Exception.Message
    if ($output.msg -ne "") { $output.msg = $output.msg + " | wmi_thread_err:" + $err } else { $output.msg = "wmi_thread_err:" + $err }
}

# Ensure keys exist and are single scalar values
foreach ($k in @('total_threads','blocked_threads_count','threads_waiting_on_sync_count','processor_queue_length','context_switches_per_sec')) {
    if (-not $output.Contains($k)) { $output[$k] = $null }
    if (-not $output.units.ContainsKey($k)) { $output.units[$k] = "count" }
}

# Output compact JSON (flat)
$output | ConvertTo-Json -Depth 4 -Compress

exit 0
