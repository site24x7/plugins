param([string]$counters,[string]$displaynames)


$output = @{}
$heartbeat = "true"
$version = 1
$flag=0

Function Get-Data
{
    $countarr = $counters -split ","
    $disparr = $displaynames -split ","
    $data=@{}
    if($countarr.Length -eq $disparr.Length)
    {
        for($count=0;$count -lt $countarr.Length;$count=$count+1)
        {
            $decimal=(Get-Counter -Counter $countarr[$count]).CounterSamples.CookedValue
            $data.Add($disparr[$count],[math]::round($decimal,2));
            
        }
    }
    else
    {
        $data.Add("msg","dispay name does not match with counters")
    }
    return $data
}
$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$output.Add("data", ($data))
$output.Add("plugin_version", $version)

$output | ConvertTo-Json

