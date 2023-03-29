param([string]$counters,[string]$units,[string]$displaynames)


$output = @{}
$heartbeat = "true"
$version = 1
$flag=0

Function Get-Data
{
    $countarr = $counters -split ","
    $unitarr = $units -split ","
    $disparr = $displaynames -split ","
    $units = @{}
    if(($countarr.Length -eq $unitarr.length) -and ($unitarr.Length -eq $disparr.Length) )
    {
        for($count=0;$count -lt $countarr.Length;$count=$count+1)
        {
            $decimal=(Get-Counter -Counter $countarr[$count]).CounterSamples.CookedValue
            $output.Add($disparr[$count],[math]::round($decimal,2));
            $units.Add($disparr[$count],$unitarr[$count])
            
        }
        $output.Add("units",$units)
    }
    else
    {
        if($countarr.Length -ne $unitarr.length)
        {
            $output.Add("msg","unit does not match with counters")
        }
        else
        {
            $output.Add("msg","dispay name does not match with counters")
        }
    }
    return 1
}
$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$output.Add("plugin_version", $version)

$output | ConvertTo-Json


