$ErrorActionPreference = "Stop"

$version = "1"
$heartbeat = "True"
$statusValue = -1
$statusValueText = "No Value Found"
$firewallProfileArray = @()
$threatDetected = 0
$message = "No threats detected"
$TamperProtectionSource = "No Value Found"
$RealTimeProtectionEnabled = $false
$QuickScanStartTime = "No Value Found"
$QuickScanEndTime = "No Value Found"
$OnAccessProtectionEnabled = $false
$FullScanStartTime = "No Value Found"
$FullScanEndTime = "No Value Found"
$AntivirusSignatureLastUpdated = "No Value Found"
$AntispywareSignatureLastUpdated = "No Value Found"
$AMServiceEnabled = $false
$AntispywareEnabled = $false
$AntivirusEnabled = $false
$FullScanAge = -1
$QuickScanAge = -1
$NISEnabled = $false
$IsTamperProtected = $false
$AntispywareSignatureAge = -1
$AntivirusSignatureAge = -1
$NISSignatureAge = -1
$QuickScanSignatureVersion = "No Value Found"
$AntispywareSignatureVersion = "No Value Found"
$FullScanSignatureVersion = "No Value Found"
$NISSignatureVersion = "No Value Found"
$AntivirusSignatureVersion = "No Value Found"

$status = 1
$msg = ""

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

try {
    $service = Get-Service -Name windefend
    $statusValue = $service.Status.value__
    $statusValueText = $service.Status.ToString()
} catch {
    $msg += "Error getting Windows Defender service status: $_. "
}

try {
    $firewallProfiles = Get-NetFirewallProfile
    foreach ($profile in $firewallProfiles) {
        $firewallProfileArray += @{
            name = $profile.Name
            Enabled_status = if ($profile.Enabled -eq $true) { 1 } else { 0 }
            LogMaxSizeKilobytes = $profile.LogMaxSizeKilobytes
        }
    }
} catch {
    $msg += "Error getting firewall profiles: $_. "
}

try {
    $threatDetections = Get-MpThreatDetection
    if ($threatDetections) {
        $successfulThreats = $threatDetections | Where-Object { $_.ActionSuccess -eq $true }
        $threatDetected = $successfulThreats.Count
        if ($successfulThreats -is [System.Array]) {
            $threatDetected = $successfulThreats.Count
        } elseif ($successfulThreats) {
            $threatDetected = 1
        } else {
            $threatDetected = 0
        }
    } else {
        $threatDetected = 0
    }
    if ($threatDetected -gt 0) {
        $status = 0
        $message = "Threats detected"
    } else {
        $status = 1
        $message = "No threats detected"
    }
} catch {
    $msg += "Error getting threat detections: $_. "
}

try {
    $mpStatus = Get-MpComputerStatus
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
    $FullScanAge = if ($mpStatus.FullScanAge -eq 4294967295 -or $mpStatus.FullScanAge -eq 65535){-1} else {$mpStatus.FullScanAge}
    $QuickScanAge = if ($mpStatus.QuickScanAge -eq 4294967295 -or $mpStatus.QuickScanAge -eq 65535){-1} else {$mpStatus.QuickScanAge}
    $NISEnabled = $mpStatus.NISEnabled
    $IsTamperProtected = $mpStatus.IsTamperProtected
    $AntispywareSignatureAge  = if ($mpStatus.AntispywareSignatureAge -eq 4294967295 -or $mpStatus.AntispywareSignatureAge -eq 65535){-1} else {$mpStatus.AntispywareSignatureAge}
    $AntivirusSignatureAge  = if ($mpStatus.AntivirusSignatureAge -eq 4294967295 -or $mpStatus.AntivirusSignatureAge -eq 65535){-1} else {$mpStatus.AntivirusSignatureAge}
    $NISSignatureAge = if ($mpStatus.NISSignatureAge -eq 4294967295 -or $mpStatus.NISSignatureAge -eq 65535){-1} else {$mpStatus.NISSignatureAge}
    $QuickScanSignatureVersion = if ($mpStatus.QuickScanSignatureVersion) { $mpStatus.QuickScanSignatureVersion } else { "No Value Found" }
    $AntispywareSignatureVersion = if ($mpStatus.AntispywareSignatureVersion) { $mpStatus.AntispywareSignatureVersion } else { "No Value Found" }
    $FullScanSignatureVersion   = if ($mpStatus.FullScanSignatureVersion  ) { $mpStatus.FullScanSignatureVersion   } else { "No Value Found" }
    $NISSignatureVersion     = if ($mpStatus.NISSignatureVersion    ) { $mpStatus.NISSignatureVersion   } else { "No Value Found" }
    $AntivirusSignatureVersion = if ($mpStatus.AntivirusSignatureVersion) { $mpStatus.AntivirusSignatureVersion } else { "No Value Found" }
} catch {
    $msg += "Error getting Defender computer status: $_. "
}

$mainJson = @{
    "plugin_version" = $version
    "heartbeat_required" = $heartbeat
    "WindefenderStatus" = $statusValue
    "WindefenderStatusText" = $statusValueText
    "FirewallProfile" = $firewallProfileArray
    "ThreatDetected" = $threatDetected
    "status" = $status
    "msg" = if ($msg) { $msg } else { $message }
    "TamperProtectionSource" = $TamperProtectionSource
    "RealTimeProtectionEnabled" = $RealTimeProtectionEnabled
    "QuickScanStartTime" = $QuickScanStartTime
    "QuickScanEndTime" = $QuickScanEndTime
    "OnAccessProtectionEnabled" = $OnAccessProtectionEnabled
    "FullScanStartTime" = $FullScanStartTime
    "FullScanEndTime" = $FullScanEndTime
    "AntivirusSignatureLastUpdated" = $AntivirusSignatureLastUpdated
    "AntispywareSignatureLastUpdated" = $AntispywareSignatureLastUpdated
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
    "AntivirusSignatureVersion" = $AntivirusSignatureVersion

}

# Convert the JSON to a formatted string
$mainJson | ConvertTo-Json -compress
