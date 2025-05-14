param(
    [string]$Username,
    [string]$Password
)

$version=1
$heartbeat=$true

try {

    $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
    $UserCredential = New-Object System.Management.Automation.PSCredential($Username, $SecurePassword)

    Login-PowerBIServiceAccount -Credential $UserCredential -ErrorAction Stop | Out-Null

    $Reports = Get-PowerBIReport
    $Datasets = Get-PowerBIDataset
    $Dataflows = Get-PowerBIDataflow
    $Workspaces = Get-PowerBIWorkspace

    $result = @{
        "plugin_version"=$version
        "heartbeat_required"=$heartbeat
        "Total Reports"    = $Reports.Count
        "Total Datasets"   = $Datasets.Count
        "Total Dataflows"  = $Dataflows.Count
        "Total Workspaces" = $Workspaces.Count
    }

    $jsonResult = $result | ConvertTo-Json -Depth 3

    Write-Output $jsonResult

    Logout-PowerBIServiceAccount
}
catch {
    $errorResult = @{
        "plugin_version"=$version
        "heartbeat_required"=$heartbeat
        "Status" = 0
        "msg"    = $_.Exception.Message
    }

    $jsonErrorResult = $errorResult | ConvertTo-Json -Depth 3
    Write-Output $jsonErrorResult
}
