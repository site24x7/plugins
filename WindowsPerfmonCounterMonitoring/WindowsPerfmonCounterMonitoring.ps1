param([string]$counters)


$output = @{}
$heartbeat = "true"
$version = 1
$flag=0
$msg=""
$Status=1
$counters_present=$false

Function Get-Data
{
    try{
    $countarr = $counters -split "#"

    $units = @{}

        for($count=0;$count -lt $countarr.Length;$count=$count+1)
        {
            try{
            $decimal=(Get-Counter -Counter $countarr[$count] -errorAction Stop).CounterSamples.CookedValue

            }catch{
             $Script:msg+=$_.Exception.Message+"`n"
             continue

            }
            $Script:counters_present=$true
            $unit=$countarr[$count] -split" "
            $unit=$unit[-1]

            $output.Add($countarr[$count],[math]::round($decimal,2));
            $units.Add($countarr[$count],$unit)
            
        }
        $output.Add("units",$units)
    }catch
    {

      $Script:Status = 0
      $Script:msg = $_.Exception.Message

    }
  
    return 1
}


$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$output.Add("plugin_version", $version)

if ($counters_present -eq $false){

    $Status = 0
    $msg = "No counters returned value`n"+$msg

}


if($Status -eq 0)
{

   $output.Add("status",0)

}
if($msg -ne $null)
{

   $output.Add("msg",$msg)

}

$output | ConvertTo-Json
