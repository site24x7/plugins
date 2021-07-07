param([string]$path)

$version = 1 
$heartbeat = "true"

# $path = "Cert:/LocalMachine/AuthRoot/51501FBFCE69189D609CFAF140C576755DCC1FDF"
$cert_info = Get-ChildItem -path $path
$displayname = "$($cert_info.FriendlyName) certificate_monitoring"

Function Get-Data() 
{    
    # Version , Signature algorithm ,Valid from,valid to ,Friendly name, how many day left , Subject Name, the certificate is expired
    $data = @{}
    $data.Add("certificate_version", $cert_info.Version)
    $data.Add("signature_algorithm", $cert_info.SignatureAlgorithm.FriendlyName)
    $data.Add("subject_name", $cert_info.Subject)
    $data.Add("friendly_name", $cert_info.FriendlyName)
    $data.Add("valid_from", $cert_info.NotBefore.DateTime)
    $data.Add("valid_to", $cert_info.NotAfter.DateTime)

    $is_the_certificate_expired = $true
    $present_date = Get-Date
    $days_left = $cert_info.NotAfter.Subtract($present_date).TotalDays
    
    if( $days_left -gt 0)
    {
        $is_the_certificate_expired = $false
        $data.Add("days_left", $days_left)
    }

    $data.Add("is_the_certificate_expired", $is_the_certificate_expired)
    return $data
}


$mainJson = @{}
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) 
$mainJson.Add("data", (Get-Data)) 
return $mainJson | ConvertTo-Json
