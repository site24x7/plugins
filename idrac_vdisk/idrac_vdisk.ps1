$version = "1"

$displayname = "idrac_vdisk"

$heartbeat = "False"

$python = "<python-installed-path>\Python36-32\python.exe"  #change the pytho path
$plugin = "idrac_vdisk.py"
$data = & $python $plugin
$dataHash = $data | ConvertFrom-Json
$mainJson = @{"version" = $version; "displayname" = $displayname; "heartbeat" = $heartbeat;}
$ht2 =@{}
$dataHash.psobject.properties | Foreach { $ht2[$_.Name] = $_.Value }
foreach( $dataelem in $ht2.Keys)
{
    $mainJson.Add($dataelem,$ht2[$dataelem])
}
return $mainJson | ConvertTo-Json

