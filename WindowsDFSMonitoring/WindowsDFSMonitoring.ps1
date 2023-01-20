param([string]$path)
$version=1
$heartbeat = "true"  
$Status = 1
$msg = $null

Function Get-Data()  
{

$data = @{}


try
{
$st=$path.split('\')
$data.add("Namespace",$st[-2])
$data.add("Server Name",$st[-3])
$Folders=Get-DfsnFolder -path $path
$Total_Count=$Folders | Measure-Object -line  | out-string
$Total_Count=$Total_Count -replace '\D'
$Online_Count=$folders | where State -eq Online | Measure-Object -line  | out-string
$Online_Count=$Online_Count -replace '\D'
$Offline_Count=$Total_Count - $Online_Count
$Share=Get-DfsnFolder -path $path | Select-Object -Property path,State 
$no=1

foreach ($val in $Share)
    {

    if(($val|Select-Object -ExpandProperty State) -eq "Online")
    {

    $name=$val|Select-Object -ExpandProperty path
    $name1=$name -replace "\\.DFSFolderLink",""
    $st=$name1.split('\')
    $data.Add($st[-1]+"_Status",1)
    $data.Add("Folder"+$no,$st[-1])

    }
    else
    {

    $name=$val|Select-Object -ExpandProperty path
    $name=$name -replace "\\.DFSFolderLink",""
    $st=$name.split('\')
    $data.Add($st[-1]+"_Status",0)
    $data.Add("Folder"+$no,$st[-1])

    }
    $no=$no+1
    }
    }
    catch
    {

      $Script:Status = 0
      $Script:msg = $_.Exception.Message

    }
    $data.Add("Total",($Total_Count+" Folders"))
    $data.Add("Total Online",$Online_Count)
    $data.Add("Total Offline",$Offline_Count)
    return $data

}

Function Set-Units() 
{

    $units = @{}
    $units.Add("Total Online","count")
    $units.Add("Total Offline", "count")
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
