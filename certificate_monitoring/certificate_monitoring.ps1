param([string]$certPath , [string]$certName)

$version = 1 
$heartbeat = "true"

$displayname = $certName + " certificate_monitoring"

Function Get-Data() 
{    
    param([string]$certpath , [string]$certName)
    $certificates = Get-ChildItem -path $certpath
    $cert_info = $null
    foreach($cert in $certificates)
    {
        if($cert.FriendlyName -eq $certName)
        {
            $cert_info = $cert
            break;
        }
    }
    # Version , Signature algorithm ,Valid from,valid to ,Friendly name, how many day left , Subject Name, the certificate is expired
    $data = @{}
    $data.Add("certificate_version", $cert_info.Version)
    $data.Add("signature_algorithm", $cert_info.SignatureAlgorithm.FriendlyName)
    $data.Add("subject_name", $cert_info.Subject)
    $data.Add("friendly_name", $cert_info.FriendlyName)
    $data.Add("valid_from", ($cert.NotBefore.Day.ToString() + "-" + $cert.NotBefore.Month.ToString() + "-" + $cert.NotBefore.Year.ToString()))
    $data.Add("valid_to", $($cert.NotAfter.Day.ToString() + "-" + $cert.NotAfter.Month.ToString() + "-" + $cert.NotAfter.Year.ToString()))
    $data.Add("verified", $cert_info.Verify())

    $is_the_certificate_expired = $true
    $present_date = Get-Date
    $days_left = $cert_info.NotAfter.Subtract($present_date).TotalDays
    
    if( $days_left -gt 0)
    {
        $is_the_certificate_expired = $false
    }

    $data.Add("days_left", ([math]::round($days_left,2)))
    $data.Add("is_the_certificate_expired", $is_the_certificate_expired)
    return $data
}


$mainJson = @{}
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) 
$mainJson.Add("data", (Get-Data $certPath $certName)) 
return $mainJson | ConvertTo-Json

