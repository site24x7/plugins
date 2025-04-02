param(
    [string]$path = "C:\Users\Site24x7Plugins\",
    [int]$timedifference = 5
)

$mainJson = @{}

$version = 1

$timedif = $timedifference

$heartbeat = "true" 

$folderName = (Split-Path -Path $path -Leaf)
$displayname = "$folderName-FolderMonitoring"

if (-not (Test-Path -Path $path -PathType Container)) {
    $mainJson = @{
        "msg" = "Unable to find the provided folder, please check the folder path."
    }
}

Function Get-Data()
{
    $s = (Get-ChildItem -Force -Path $path -Recurse -ErrorAction SilentlyContinue)

    $timedifneg = -1 * $timedif

    $time = (Get-Date).AddMinutes($timedifneg)
    $size = 0
    $filecount = 0
    $dirCount = 0
    $fileCreated = 0
    $dirCreated = 0
    $filemodify = 0
    $dirmodify = 0
    $changesOccurred = $false
    foreach($file in $s)
    {

        if(($file.Attributes.value__ -band 16) -eq 16)
        {
            if(($file.Attributes.value__ -band 4) -eq 4)
            {
                continue
            
            }
            else
            {
                if($file.CreationTime -gt $time)
                {
                    $dirCreated++
                    $changesOccurred = $true
                }
                elseif($file.LastWriteTime -gt $time)
                {
                    $dirmodify++
                    $changesOccurred = $true
                }
                $dirCount++
            }
        }
        else
        {
            if(($file.Attributes.value__ -band 4) -eq 4)
            {
                continue
            
            }
            else
            {
            
                if($file.CreationTime -gt $time)
                {
                    $fileCreated++
                    $changesOccurred = $true
                }
                elseif($file.LastWriteTime -gt $time)
                {
                    $filemodify++
                    $changesOccurred = $true
                }
                $filecount++
                $size+=$file.Length
            }
        } 
    }

    $formattedSize = "{0:F4}" -f ($size / 1GB)

    $idleTime = if ($changesOccurred) { 0 } else { 1 }
    $fileCreatedstr = "Files Created"
    $dirCreatedstr = "Folders Created"
    $filemodifystr = "Files Modified"
    $dirmodifystr = "Folders Modified"
    $data = @{}
    $data.Add("Folder Size", $formattedSize)
    $data.Add("Files Count", $filecount)
    $data.Add("Folders Count", $dirCount)
    $data.Add($fileCreatedstr, $fileCreated)
    $data.Add($dirCreatedstr, $dirCreated)
    $data.Add($filemodifystr, $filemodify)
    $data.Add($dirmodifystr, $dirmodify)
    $data.Add("Is Folder Idle", $idleTime)
    $data.Add("Tracking Folder", $path)
    return $data
}
Function Set-Units() 
{
    $units = @{}
    $units.Add("Folder Size", "GB")
    return $units
}

$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) 
$mainJson.Add("data", (Get-Data))
$mainJson.Add("units", (Set-Units))

return $mainJson | ConvertTo-Json
