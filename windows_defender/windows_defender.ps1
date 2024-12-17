$version = "1"
$heartbeat = "True"

$statusValue = (Get-Service -Name windefend).Status.value__
$statusValueText = (Get-Service -Name windefend).Status.ToString()

$firewallProfiles = Get-NetFirewallProfile

$firewallProfileArray = @()

foreach ($profile in $firewallProfiles) {
    $firewallProfileArray += @{
        name = $profile.Name
        Enabled_status = if ($profile.Enabled -eq $true) { 1 } else { 0 }
        LogMaxSizeKilobytes = $profile.LogMaxSizeKilobytes
    }
}

$threatDetections = Get-MpThreatDetection

$threatDetected = 0

if ($threatDetections) {
    $threatDetected = ($threatDetections | Where-Object { $_.ActionSuccess -eq $true }).Count
}

if ($threatDetected -gt 0) {
    $threatstatus = 0
    $message = "Threats detected"
} else {
    $threatstatus = 1
    $message = "No threats detected"
}

$mpStatus = Get-MpComputerStatus

function Convert-ToReadableDate {
    param (
        [Parameter(Mandatory=$true)]
        $dateInput
    )
    
    if ($dateInput -is [System.DateTime]) {
        return $dateInput.ToString("yyyy-MM-dd HH:mm:ss")
    }
    elseif ($dateInput -match '\/Date\((\d+)\)\/') {
        $epochTime = [int64]$matches[1]
        $epochStart = Get-Date "1970-01-01 00:00:00"
        return $epochStart.AddMilliseconds($epochTime).ToString("yyyy-MM-dd HH:mm:ss")
    }
    return $null
}

$TamperProtectionSource = $mpStatus.TamperProtectionSource
$RealTimeProtectionEnabled = $mpStatus.RealTimeProtectionEnabled
$QuickScanStartTime = if ($mpStatus.QuickScanStartTime) { Convert-ToReadableDate $mpStatus.QuickScanStartTime } else { "No Value Found" }
$QuickScanEndTime = if ($mpStatus.QuickScanEndTime) { Convert-ToReadableDate $mpStatus.QuickScanEndTime } else { "No Value Found" }
$OnAccessProtectionEnabled = $mpStatus.OnAccessProtectionEnabled
$FullScanStartTime = if ($mpStatus.FullScanStartTime) { Convert-ToReadableDate $mpStatus.FullScanStartTime } else { "No Value Found" }
$FullScanEndTime = if ($mpStatus.FullScanEndTime) { Convert-ToReadableDate $mpStatus.FullScanEndTime } else { "No Value Found" }
$AntivirusSignatureLastUpdated = if ($mpStatus.AntivirusSignatureLastUpdated) { Convert-ToReadableDate $mpStatus.AntivirusSignatureLastUpdated } else { "No Value Found" }
$AntispywareSignatureLastUpdated = if ($mpStatus.AntispywareSignatureLastUpdated) { Convert-ToReadableDate $mpStatus.AntispywareSignatureLastUpdated } else { "No Value Found" }

$AMServiceEnabled = $mpStatus.AMServiceEnabled
$AntispywareEnabled = $mpStatus.AntispywareEnabled
$AntivirusEnabled = $mpStatus.AntivirusEnabled
$FullScanAge = if ($mpStatus.FullScanAge -eq 4294967295){-1} else {$mpStatus.FullScanAge}
$QuickScanAge = if ($mpStatus.QuickScanAge -eq 4294967295){-1} else {$mpStatus.QuickScanAge}
$NISEnabled = $mpStatus.NISEnabled
$IsTamperProtected = $mpStatus.IsTamperProtected

$AntispywareSignatureAge  = if ($mpStatus.AntispywareSignatureAge -eq 4294967295){-1} else {$mpStatus.AntispywareSignatureAge}
$AntivirusSignatureAge  = if ($mpStatus.AntivirusSignatureAge -eq 4294967295){-1} else {$mpStatus.AntivirusSignatureAge}
$NISSignatureAge = if ($mpStatus.NISSignatureAge -eq 4294967295){-1} else {$mpStatus.NISSignatureAge}

$QuickScanSignatureVersion = if ($mpStatus.QuickScanSignatureVersion) { $mpStatus.QuickScanSignatureVersion } else { "No Value Found" }
$AntispywareSignatureVersion = if ($mpStatus.AntispywareSignatureVersion) { $mpStatus.AntispywareSignatureVersion } else { "No Value Found" }
$FullScanSignatureVersion   = if ($mpStatus.FullScanSignatureVersion  ) { $mpStatus.FullScanSignatureVersion   } else { "No Value Found" }
$NISSignatureVersion     = if ($mpStatus.NISSignatureVersion    ) { $mpStatus.NISSignatureVersion   } else { "No Value Found" }

$mainJson = @{
    "version" = $version
    "heartbeat" = $heartbeat
    "WindefenderStatus" = $statusValue
    "WindefenderStatusText" = $statusValueText
    "FirewallProfile" = $firewallProfileArray
    "ThreatDetected" = $threatDetected
    "status" = $threatstatus
    "msg" = $message
    "TamperProtectionSource" = $TamperProtectionSource
    "RealTimeProtectionEnabled" = $RealTimeProtectionEnabled
    "QuickScanStartTime" = $QuickScanStartTime
    "QuickScanEndTime" = $QuickScanEndTime
    "OnAccessProtectionEnabled" = $OnAccessProtectionEnabled
    "FullScanStartTime" = $FullScanStartTime
    "FullScanEndTime" = $FullScanEndTime
    "AntivirusSignatureLastUpdated" = $AntivirusSignatureLastUpdated
    "AntispywareSignatureLastUpdated" = $antispywareSignatureLastUpdated
    "AMServiceEnabled" = $AMServiceEnabled
    "AntispywareEnabled" = $AntispywareEnabled
    "AntivirusEnabled" = $AntivirusEnabled
    "FullScanAge" = $FullScanAge
    "QuickScanAge" = $QuickScanAge
    "NISEnabled" = $NISEnabled
    "IsTamperProtected" = $IsTamperProtected
    "AntispywareSignatureAge" = $AntispywareSignatureAge
    "AntivirusSignatureAge" = $AntivirusSignatureAge
    "NISSignatureAge" = $NISSignatureAge
    "QuickScanSignatureVersion" = $QuickScanSignatureVersion
    "AntispywareSignatureVersion" = $AntispywareSignatureVersion
    "FullScanSignatureVersion" = $FullScanSignatureVersion
    "NISSignatureVersion" = $NISSignatureVersion
}

$mainJson | ConvertTo-Json -compress
