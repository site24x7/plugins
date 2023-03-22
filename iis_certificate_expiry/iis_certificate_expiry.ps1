param([string]$thumbprint,[string]$path)
$output = @{}
$heartbeat = "true"
$version = 1

Function Get-Data
{
    $data=@{}
    $units = @{}
    $now = Get-Date
    $expirationDate=(Get-ChildItem -Path $path | Where-Object {$_.Thumbprint -eq $thumbprint}).NotAfter
    $expirydays=($expirationDate - $now).Days
    $data.Add("Days Left to Expiry",$expirydays)
    
    $units.Add("Days Left to Expiry","days")
    $data.Add("units",$units)
    return $data
}
$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data
$output.Add("data", ($data))
$output.Add("plugin_version", $version)

$output | ConvertTo-Json
