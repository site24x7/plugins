
$diskpartition  = "C" #update the disk partion name 
$version = 1 #Mandatory - If any changes in the plugin metrics, increment the plugin version here. 
$displayname = $env:computername +"-Disk partition IO-"+$diskpartition #OPTIONAL - Display name to be displayed in Site24x7 client 
$heartbeat = "true" #Mandatory - Setting this to true will alert you when there is a communication problem while posting plugin data to server

Function Get-Data() #The Get-Data method contains Sample data. User can enhance the code to fetch Original data 
{
#It is enough to edit this function and return the metrics required in $data
    $query = "select * from win32_perfformatteddata_perfdisk_Logicaldisk where name like '%"+ $diskpartition +"%'"
    $result  = Get-WmiObject  -Query $query
    $data = @{}
    $data.Add("Name", $result.Name)
    $data.Add("AvgDiskQueueLength", $result.AvgDiskQueueLength)
    $data.Add("AvgDisksecPerTransfer", $result.AvgDisksecPerTransfer)
    $data.Add("CurrentDiskQueueLength", $result.CurrentDiskQueueLength)
    $data.Add("DiskBytesPersec", $result.DiskBytesPersec)
    $data.Add("DiskTransfersPersec", $result.DiskTransfersPersec)
    $data.Add("PercentDiskReadTime", $result.PercentDiskReadTime)
    $data.Add("PercentDiskTime", $result.PercentDiskTime)
    $data.Add("PercentDiskWriteTime", $result.PercentDiskWriteTime)
    $data.Add("PercentIdleTime", $result.PercentIdleTime)
    $data.Add("DiskWriteBytesPersec", $result.DiskWriteBytesPersec)
    $data.Add("DiskReadBytesPersec", $result.DiskReadBytesPersec)
    $data.Add("DiskReadsPersec", $result.DiskReadsPersec)
    $data.Add("DiskWritesPersec", $result.DiskWritesPersec)
    return $data
}
Function Set-Units() #OPTIONAL - These units will be displayed in the Dashboard
{
    $units = @{}
    $units.Add("AvgDisksecPerTransfer", "sec")
    $units.Add("DiskBytesPersec", "Bytes")
    $units.Add("PercentDiskReadTime", "%")
    $units.Add("PercentDiskTime", "%")
    $units.Add("PercentDiskWriteTime", "%")
    $units.Add("PercentIdleTime", "%")
    $units.Add("DiskWriteBytesPersec", "Bytes")
    $units.Add("DiskReadBytesPersec", "Bytes")
    return $units
}

$mainJson = @{}
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) #Comment this if you don't display name
$mainJson.Add("data", (Get-Data))
$mainJson.Add("units", (Set-Units)) #Comment this if you don't have Units
return $mainJson | ConvertTo-Json



