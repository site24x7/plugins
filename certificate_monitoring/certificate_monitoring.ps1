param([string]$certPath , [string]$thumbprint)

$version = 1 
$heartbeat = "true"


Function Get-Data() 
{    
    param([string]$certpath , [string]$thumbprint)
    $certificates = Get-ChildItem -path $certpath
    $cert_info = $null
    foreach($cert in $certificates)
    {
    #Write-Host "----"( $cert | Select-Object thumbprint) "----"
        if($cert.thumbprint -eq $thumbprint)
        {
            $cert_info = $cert
            
            break;
        }
    }
    # Version , Signature algorithm ,Valid from,valid to ,Friendly name, how many day left , Subject Name, the certificate is expired
    $data = @{}
    #Write-Host $certificates
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
$mainJson.Add("data", (Get-Data $certPath $thumbprint)) 
return $mainJson | ConvertTo-Json
