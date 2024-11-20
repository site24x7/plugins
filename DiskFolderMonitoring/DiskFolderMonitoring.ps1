param(
    [string]$path = "C:\Users\Administrator\Documents\DiskFolderMonitorg"
)

$version = 1 #Mandatory - If any changes in the plugin metrics, increment the plugin version here. 

$timedif = 5 # time intrval 

#$displayname = "" #OPTIONAL - Display name to be displayed in Site24x7 client 
$heartbeat = "true" #Mandatory - Setting this to true will alert you when there is a communication problem while posting plugin data to server

Function Get-Data() #The Get-Data method contains Sample data. User can enhance the code to fetch Original data 
{
#It is enough to edit this function and return the metrics required in $data
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
                }
                elseif($file.LastWriteTime -gt $time)
                {
                    $dirmodify++
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
                }
                elseif($file.LastWriteTime -gt $time)
                {
                    $filemodify++
                }
                $filecount++
                $size+=$file.Length
            }
        } 
    }

    $fileCreatedstr = "Files Created In "+ $timedif + " mins"
    $dirCreatedstr = "Folders Created In "+ $timedif + " mins"
    $filemodifystr = "Files Modified In "+ $timedif + " mins"
    $dirmodifystr = "Folders Modified In "+ $timedif + " mins"
    $data = @{}
    $data.Add("Size", $size/1GB)
    $data.Add("Files Count", $filecount)
    $data.Add("Folders Count", $dirCount)
    $data.Add($fileCreatedstr, $dirCount)
    $data.Add($dirCreatedstr, $dirCreated)
    $data.Add($filemodifystr, $filemodify)
    $data.Add($dirmodifystr, $dirmodify)
    return $data
}
Function Set-Units() #OPTIONAL - These units will be displayed in the Dashboard
{
    $units = @{}
    $units.Add("Size", "GB")
    return $units
}

$mainJson = @{}
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) #Comment this if you don't display name
$mainJson.Add("data", (Get-Data))
$mainJson.Add("units", (Set-Units)) #Comment this if you don't have Units

return $mainJson | ConvertTo-Json

