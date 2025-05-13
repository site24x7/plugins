param(
    [string]$portNumber,
    [string]$ipAddress = "localhost"
)

$output = @{ }
$heartbeat = "true"
$version = 1

function Check-PortStatus {
    param (
        [string]$Address,
        [int]$Port
    )

    $outdata = @{ }

    try {
        $tcpClient = New-Object Net.Sockets.TcpClient
        try {
            $tcpClient.Connect($Address, $Port)
            $outdata.Add("Port Status", 1)
        } catch {
            $outdata.Add("Port Status", 0)
        } finally {
            $tcpClient.Dispose()
        }
    } catch {
        $outdata.Add("status", 0)
        $outdata.Add("msg", $Error[0])
    }

    return $outdata
}

function Get-PortProcesses {
    param ([int]$Port)

    $processes = netstat -ano | Select-String ":$Port\s" | ForEach-Object {
        $processId = ($_ -split '\s+')[-1]
        try {
            $process = Get-Process -Id $processId -ErrorAction Stop
            [PSCustomObject]@{
                ProcessName = $process.ProcessName
                ProcessId   = $processId
                CPUTime     = $process.CPU
                Memory      = $process.WorkingSet / 1MB
            }
        } catch {
            $null
        }
    }

    return $processes
}

function Get-UniqueProcesses {
    param ([array]$Processes)

    $uniqueProcesses = $Processes | Group-Object -Property ProcessId | ForEach-Object {
        $firstProcess = $_.Group | Select-Object -First 1  
        [PSCustomObject]@{
            ProcessName = $firstProcess.ProcessName
            ProcessId   = $firstProcess.ProcessId
            CPUTime     = ($_.Group | ForEach-Object { $_.CPUTime }) | Measure-Object -Sum | Select-Object -ExpandProperty Sum
            Memory      = $firstProcess.Memory 
        }
    }

    return $uniqueProcesses
}



function Get-CPUPercent {
    param([int]$ProcessId)

    try {
        $process = Get-Process -Id $ProcessId -ErrorAction Stop
        $name = $process.Name
        $counterPath = "\Process($name*)\% Processor Time"

        $counterSamples = Get-Counter $counterPath -ErrorAction Stop |
            Select-Object -ExpandProperty CounterSamples |
            Where-Object { $_.InstanceName -match "^$name($|#\d+)$" }

        foreach ($sample in $counterSamples) {
            try {
                $proc = Get-Process -Name $sample.InstanceName -ErrorAction SilentlyContinue | Where-Object { $_.Id -eq $ProcessId }
                if ($proc) {
                    return [math]::Round($sample.CookedValue / [Environment]::ProcessorCount, 2)
                }
            } catch { }
        }
    } catch { }

    return 0
}

$portStatus = Check-PortStatus -Address $ipAddress -Port $portNumber
$portStatusValue = $portStatus["Port Status"]
$portStatusText = if ($portStatusValue -eq 1) { "Open" } else { "Close" }

$output.Add("Port Status", $portStatusValue)
$output.Add("Port Status Text", $portStatusText)
$output.Add("heartbeat_required", $heartbeat)
$output.Add("plugin_version", $version)

$processes = Get-PortProcesses -Port $portNumber

$uniqueProcesses = @(Get-UniqueProcesses -Processes $processes)

if ($uniqueProcesses) {
    $totalProcesses = $uniqueProcesses.Count
    $totalMemory = ($uniqueProcesses | Measure-Object -Property Memory -Sum).Sum

    $totalCPUPercent = 0

    foreach ($proc in $uniqueProcesses) {
        $cpuPercent = Get-CPUPercent -ProcessId $proc.ProcessId
        $totalCPUPercent += $cpuPercent
    }

    $output.Add("Total Processes", $totalProcesses)
    $output.Add("Total CPU Usage", [math]::Round($totalCPUPercent, 2))
    $output.Add("Total Memory Usage", [math]::Round($totalMemory, 2))
} else {
    $output.Add("Total Processes", 0)
    $output.Add("Total CPU Usage", 0)
    $output.Add("Total Memory Usage", 0)
}

$units = @{
    "Total Memory Usage" = "MB"
    "Total CPU Usage"    = "%"
}
$output.Add("units", $units)

$output | ConvertTo-Json -Compress
