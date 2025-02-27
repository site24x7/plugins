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

$scope_data=Get-DhcpServerv4ScopeStatistics -ScopeId $Scope_ID 
$data.add("Free" ,$scope_data.Free)
$data.add("In Use" ,$scope_data.InUse)
$data.add("Percentage In Use" ,$scope_data.PercentageInUse)
$data.add("Reserved" ,$scope_data.Reserved)
$data.add("Pending" ,$scope_data.Pending)
$data.add("Scope Id" ,$Scope_ID)

$scope_data=Get-DhcpServerv4Scope -ScopeId $Scope_ID
$data.Add("State",$scope_data.State)
$data.Add("Name",$scope_data.Name)
$data.Add("Subnet Mask",$scope_data.SubnetMask.IPAddressToString)
$data.Add("Start Range",$scope_data.StartRange.IPAddressToString)
$data.Add("End Range",$scope_data.EndRange.IPAddressToString)

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
