$plugin_version = "1" 
$heartbeat_required = "true" 
$displayname = "Azuresecretkey_v1" 

# Function to collect app names and expiry days
function Get-Data {
    # Connect to Microsoft Graph
    Connect-MgGraph -Identity -NoWelcome

    # Initialize array to hold the data
    $Data = @()

    # Define retry parameters
    $maxRetries = 5
    $retryInterval = 5 # in seconds

    $attempt = 0
    $success = $false

    while (-not $success -and $attempt -lt $maxRetries) {
        try {
            # Get all app registrations
            $Apps = Get-MgApplication -All
            $success = $true
        } catch {
            $attempt++
            if ($attempt -ge $maxRetries) {
                Write-Error "Failed to retrieve applications after $maxRetries attempts: $_"
                throw
            }
            Write-Warning "Attempt $attempt failed. Retrying in $retryInterval seconds..."
            Start-Sleep -Seconds $retryInterval
            $retryInterval *= 2 # Exponential backoff
        }
    }

    # Loop through each application
    foreach ($App in $Apps) {
        # Check if the application has password credentials
        if ($App.PasswordCredentials) {
            foreach ($PasswordCredential in $App.PasswordCredentials) {
                # Calculate days left until expiry
                $currentDate = Get-Date
                $daysLeft = ($PasswordCredential.EndDateTime - $currentDate).Days
                
                # Only include credentials that are not expired and expire within the next 365 days
                if ($daysLeft -ge 0 -and $daysLeft -le 365) {
                    # Add to data array
                    $Data += @{
                        "AppName" = $App.DisplayName
                        "DaysLeft" = $daysLeft
                    }
                }
            }
        }
    }

    return $Data
}

# Get app data
$Data = Get-Data

# Prepare the main JSON output
$mainJson = @{}

if ($Data.Count -eq 0) {
    $mainJson["Message"] = "No apps credentials are expiring in another 365 days"
} else {
    foreach ($item in $Data) {
        $mainJson[$item.AppName] = $item.DaysLeft
    }
}

# Add version and heartbeat information
$mainJson["plugin_version"] = $plugin_version
$mainJson["heartbeat_required"] = $heartbeat_required

# Convert to JSON and return
$mainJson | ConvertTo-Json
