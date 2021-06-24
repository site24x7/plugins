Function Get-Data()
{
    $data = @{}
    $memory = Get-WmiObject -Query "Select SystemDriverTotalBytes,PoolPagedResidentBytes,StandbyCacheCoreBytes,StandbyCacheNormalPriorityBytes,StandbyCacheReserveBytes,SystemCacheResidentBytes,SystemCodeResidentBytes,SystemCodeTotalBytes,SystemDriverResidentBytes,FreeAndZeroPageListBytes,FreeSystemPageTableEntries,ModifiedPageListBytes,PoolNonpagedBytes,PoolPagedBytes,CommitLimit,AvailableKBytes,CacheBytes,CommittedBytes,PercentCommittedBytesInUse from Win32_PerfFormattedData_PerfOS_Memory"
    $data.Add("CommitLimit",$memory.CommitLimit)
    $data.Add("AvailableKBytes",$memory.AvailableKBytes)
    $data.Add("CacheBytes",$memory.CacheBytes)
    $data.Add("CommittedBytes",$memory.CommittedBytes)
    $data.Add("PercentCommittedBytesInUse",$memory.PercentCommittedBytesInUse)
    $data.Add("FreeAndZeroPageListBytes",$memory.FreeAndZeroPageListBytes)
    $data.Add("FreeSystemPageTableEntries",$memory.FreeSystemPageTableEntries)
    $data.Add("ModifiedPageListBytes",$memory.ModifiedPageListBytes)
    $data.Add("PoolNonpagedBytes",$memory.PoolNonpagedBytes)
    $data.Add("PoolPagedBytes",$memory.PoolPagedBytes)
    $data.Add("SystemDriverTotalBytes",$memory.SystemDriverTotalBytes)
    $data.Add("PoolPagedResidentBytes",$memory.PoolPagedResidentBytes)
    $data.Add("StandbyCacheCoreBytes",$memory.StandbyCacheCoreBytes)
    $data.Add("StandbyCacheNormalPriorityBytes",$memory.StandbyCacheNormalPriorityBytes)
    $data.Add("StandbyCacheReserveBytes",$memory.StandbyCacheReserveBytes)
    $data.Add("SystemCacheResidentBytes",$memory.SystemCacheResidentBytes)
    $data.Add("SystemCodeResidentBytes",$memory.SystemCodeResidentBytes)
    $data.Add("SystemCodeTotalBytes",$memory.SystemCodeTotalBytes)
    $data.Add("SystemDriverResidentBytes",$memory.SystemDriverResidentBytes)
    return $data
}
Function Get-Units()
{
    $units = @{}
    $units.Add("CommitLimit","Bytes")
    $units.Add("AvailableKBytes","KB")
    $units.Add("CacheBytes","Bytes")
    $units.Add("CommittedBytes","Bytes")
    $units.Add("PercentCommittedBytesInUse","%")
    $units.Add("FreeAndZeroPageListBytes","Bytes")
    $units.Add("FreeSystemPageTableEntries","Bytes")
    $units.Add("ModifiedPageListBytes","Bytes")
    $units.Add("PoolNonpagedBytes","Bytes")
    $units.Add("PoolPagedBytes","Bytes")
    $units.Add("SystemDriverTotalBytes","Bytes")
    $units.Add("PoolPagedResidentBytes","Bytes")
    $units.Add("StandbyCacheCoreBytes","Bytes")
    $units.Add("StandbyCacheNormalPriorityBytes","Bytes")
    $units.Add("StandbyCacheReserveBytes","Bytes")
    $units.Add("SystemCacheResidentBytes","Bytes")
    $units.Add("SystemCodeResidentBytes","Bytes")
    $units.Add("SystemCodeTotalBytes", "Bytes")
    $units.Add("SystemDriverResidentBytes","Bytes")
    return $units
}
$version = 1 
$displayname = "Memory Performance Monitor" #OPTIONAL - Display name to be displayed in Site24x7 client 
$heartbeat = "true"
$mainJson = @{}
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) 
$mainJson.Add("data", (Get-Data))
$mainJson.Add("units", (Get-Units)) 
return $mainJson | ConvertTo-Json