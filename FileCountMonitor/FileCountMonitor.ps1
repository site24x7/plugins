
$directory = "" #directoryName


$alertonpathnotpresent = $true

$filepresent = $false
$output = @{}

$version = 1 
$heartbeat = "true" 



Function Get-Data
{
    $dataObj = @{}
    $lastmodified = 0
    $creationtime = 0
    $lastaccess = 0
    if(($directory -ne $null -and $directory.Length -gt 0))
    {
        $path = $directory+"\"
        if(Test-Path $path -PathType Container)
        {
            $filepresent = $true
            $data = Get-Item -Path $path
   
            $filecount = Get-ChildItem -File $path | Measure-Object | %{$_.Count}
            $directoryCount = Get-ChildItem -Directory $path | Measure-Object | %{$_.Count}
            $totalCount = Get-ChildItem $path | Measure-Object | %{$_.Count}
            
        }
        else
        {
           
        }
       
    }
    $dataObj.Add("file_Count",$filecount)
    $dataObj.Add("dir_Count",$directoryCount)
    $dataObj.Add("total_Count",$totalCount) 
    $dataObj.Add("Path_Exists",$filepresent) 
    return $dataObj
}



$output.Add("plugin_version", $version)
$output.Add("heartbeat_required", $heartbeat)
$data =Get-Data

if($alertonpathnotpresent -and $data["Path_Exists"] -eq $false)
{
    $output.Add("Status", 0)
}
$output.Add("data", ($data))

$output | ConvertTo-Json
