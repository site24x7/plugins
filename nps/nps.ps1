function Get-CounterValue {
    param (
        [string]$CounterPath,
        [ref]$ErrorList
    )
    try {
        $value = (Get-Counter -Counter $CounterPath -ErrorAction Stop).CounterSamples[0].CookedValue
        return [math]::Round($value, 2)
    } catch {
        $ErrorList.Value += $CounterPath
        return 0
    }
}

$npsService = Get-Service -Name 'IAS' -ErrorAction SilentlyContinue

if (-not $npsService -or $npsService.Status -ne 'Running') {
    $output = @{
        plugin_version = "1"
        heartbeat_required = "true"
        status = 0
        msg = "NPS server is not running"
    }
    $output | ConvertTo-Json -Depth 3
    exit 0
}

$failedCounters = @()

$metrics = @{
    "Connection per Second"           = Get-CounterValue "\NPS Authentication Server\Access-Requests / sec." ([ref]$failedCounters)
    "Total Connections"               = Get-CounterValue "\NPS Authentication Server\Access-Requests" ([ref]$failedCounters)
    "Rejected Connection Attempts"    = Get-CounterValue "\NPS Authentication Server\Access-Rejects" ([ref]$failedCounters)
    "Successful Connection Attempts"  = Get-CounterValue "\NPS Authentication Server\Access-Accepts" ([ref]$failedCounters)
    "Packets Received"                = Get-CounterValue "\NPS Authentication Server\Packets Received" ([ref]$failedCounters)
    "Packets Sent"                    = Get-CounterValue "\NPS Authentication Server\Packets Sent" ([ref]$failedCounters)
    "Malformed Packets Received"      = Get-CounterValue "\NPS Authentication Server\Malformed Packets" ([ref]$failedCounters)
    "Accounting Requests"             = Get-CounterValue "\NPS Accounting Server\Accounting-Requests" ([ref]$failedCounters)
    "Accounting Requests per Second"  = Get-CounterValue "\NPS Accounting Server\Accounting-Requests / sec." ([ref]$failedCounters)
}

$plugin_output = @{
    plugin_version = "1"
    heartbeat_required = "true"
    data= $metrics
}

if ($failedCounters.Count -gt 0) {
    $plugin_output["msg"] = "Failed to collect: " + ($failedCounters -join ", ")
}

$plugin_output | ConvertTo-Json -Depth 3
