param([string]$Scope_ID)
$dataObj = @{}
$heartbeat = "true" 
$version=1
$Status = 1
$msg = $null



Function Get-Data
{

$data = @{}


try
{

$scope_data=Get-DhcpServerv4ScopeStatistics -ScopeId $Scope_ID -ErrorAction Stop
$data.add("Free IPs" ,$scope_data.Free)
$data.add("In Use IPs" ,$scope_data.InUse)
$data.add("Percentage In Use" ,$scope_data.PercentageInUse)
$data.add("Reserved IPs" ,$scope_data.Reserved)
$data.add("Pending IPs" ,$scope_data.Pending)
$data.add("Scope Id" ,$Scope_ID)
$data.add("Superscope Name" ,$scope_data.SuperscopeName)

$scope_data=Get-DhcpServerv4Scope -ScopeId $Scope_ID -ErrorAction Stop
$data.Add("State",$scope_data.State)
$data.Add("Name",$scope_data.Name)
$data.Add("Subnet Mask",$scope_data.SubnetMask.IPAddressToString)
$data.Add("Start Range",$scope_data.StartRange.IPAddressToString)
$data.Add("End Range",$scope_data.EndRange.IPAddressToString)
$data.Add("Lease Duration",$scope_data.LeaseDuration.ToString())
$data.Add("Lease Duration in Hours",$scope_data.LeaseDuration.TotalHours)

}
catch
{

$Script:Status = 0
$Script:msg = $_.Exception.Message

}

return $data

}

Function Set-Units() 
{

    $units = @{}
    $units.Add("Percentage In Use","%")
    $units.Add("Lease Duration in Hours","hours")
    return $units

}

$mainJson = @{}
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("data", (Get-Data))
$mainJson.Add("units", (Set-Units)) 

if($Status -eq 0)
{

   $mainJson.Add("status",0)

}
if($msg -ne $null)
{

   $mainJson.Add("msg",$msg)

}

return $mainJson | ConvertTo-Json
