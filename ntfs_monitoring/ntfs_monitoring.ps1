param(
    [string]$mountpointpath
)

$output = @{}
$heartbeat = "true" 
$version=1
$msg=""
$status=1
$outdata=@{}

Function Get-Data{

try{


$mountpointpaths=$mountpointpath -split ","
foreach ($mountpoint in $mountpointpaths){


$data=Get-WmiObject Win32_Volume | Where-Object { $_.Name -eq $mountpoint } 
$free_data=$data | Select-Object -ExpandProperty FreeSpace
$capacity_data=$data | Select-Object -ExpandProperty Capacity


if($capacity_data -ne $null -and $capacity -ne 0){

$usage = ([Math]::Round((($capacity_data - $free_data)/$capacity_data)*100,2)) 
$free = ([Math]::Round(($free_data/$capacity_data)*100,2))
}
else{
$usage=0
$free=0
}

$outdata.Add($mountpoint+"_free",$free)
$outdata.Add($mountpoint+"_usage",$usage)

}
}

catch{

$status=0
$msg=$Error[0]

}
$outdata
}



$output = Get-Data 
$output.Add("heartbeat_required",$heartbeat)
$output.Add("plugin_version", $version)
$output | ConvertTo-Json
