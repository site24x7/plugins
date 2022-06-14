### Mandatory - If any attributes added or removed in the plugin, increment the plugin version here to update the plugins template.
$version = 1

### Mandatory - Setting this to true will alert you when there is a communication problem while posting plugin data to server
$heartbeat = "true" 

### OPTIONAL - Display name to be displayed in Site24x7 client
$displayname = "Office365 products subscription license check"  

### The Get-Data method contains Sample data. Replace you code logic to populate the monitoring data
Function Get-Data()  
{
    # $name = "Process"
    # $CPU = 81
    # $Memory = 85
    
    # if($Memory -gt 80)
    # {
    # 	### OPTIONAL- Set the message to be displayed in the "Reason" in Log Report
    #     $msg = "Memory Usage increases to "+$Memory +"%" 
    # }
    
    # $data = @{}
    # $data.Add("CPU", $CPU)
    # $data.Add("Memory", $Memory)
    # $data.Add("name", $name)
    
    # ### Set the message to be displayed in the "Reason" in Log Report
    # $data.Add("msg", $msg)
    
    # return $data
        
    Param 
    ( 
        [Parameter(Mandatory = $false)] 
        [switch]$Trial, 
        [switch]$Free, 
        [switch]$Purchased, 
        [Switch]$Expired, 
        [Switch]$Active,
        [string]$UserName="yourUserName",  
        [string]$Password="yourPassword" 
    ) 
    try{

        #Check for MSOnline module 
        $Module=Get-Module -Name MSOnline -ListAvailable  
        if($Module.count -eq 0) 
        { 
            Write-Host MSOnline module is not available  -ForegroundColor yellow  
            $Confirm= Read-Host Are you sure you want to install module? [Y] Yes [N] No 
            if($Confirm -match "[yY]") 
            { 
                Install-Module MSOnline 
                Import-Module MSOnline
            } 
            else 
            { 
                Write-Host MSOnline module is required to connect AzureAD.Please install module using Install-Module MSOnline cmdlet. 
                Exit
            }
        } 
        
        #Storing credential in script for scheduling purpose/ Passing credential as parameter  
        if(($UserName -ne "") -and ($Password -ne ""))  
        {  
            $SecuredPassword = ConvertTo-SecureString -AsPlainText $Password -Force  
            $Credential  = New-Object System.Management.Automation.PSCredential $UserName,$SecuredPassword  
            Connect-MsolService -Credential $credential 
        }  
        else  
        {  
            Connect-MsolService | Out-Null  
        } 

        $Result=""   
        $Results=@()  
        $Print=0
        $ShowAllSubscription=$False
        $PrintedOutput=0

        #Output file declaration 
        $ExportCSV=".\details.csv" 

        #delete already existing csv
        if (Test-Path $ExportCSV) {
            Remove-Item $ExportCSV
        }

        #Check for filters
        if((!($Trial.IsPresent)) -and (!($Free.IsPresent)) -and (!($Purchased.IsPresent)) -and (!($Expired.IsPresent)) -and (!($Active.IsPresent)))
        {
            $ShowAllSubscription=$true
        }

        #FriendlyName list for license plan 
        $FriendlyNameHash=@()
        $FriendlyNameHash=Get-Content -Raw -Path .\LicenseFriendlyName.txt -ErrorAction Stop | ConvertFrom-StringData 

        #Get available subscriptions in the tenant
        $Subscriptions= Get-MsolSubscription | foreach{
        $SubscriptionName=$_.SKUPartNumber
        $SubscribedOn=$_.DateCreated
        $ExpiryDate=$_.NextLifeCycleDate
        $Status=$_.Status
        $TotalLicenses=$_.TotalLicenses
        $Print=0

        #Convert Skuid to friendly name  
        $EasyName=$FriendlyNameHash[$SubscriptionName] 
        $EasyName
        if(!($EasyName)) 
        {
            $NamePrint=$SubscriptionName
        } 
        else 
        {
            $NamePrint=$EasyName
        } 

        #Convert Subscribed date to friendly subscribed date
        $SubscribedDate=(New-TimeSpan -Start $SubscribedOn -End (Get-Date)).Days
        if($SubscribedDate -eq 0)
        {
            $SubscribedDate="Today"
        }
        else
        {
            $SubscribedDate="$SubscribedDate days ago"
        }
        $SubscribedDate="(" + $SubscribedDate + ")"
        $SubscribedDate="$SubscribedOn $SubscribedDate"

        #Determine subscription type
        If($_.IsTrial -eq $False)
        {
            if(($SubscriptionName -like "*Free*") -or ($ExpiryDate -eq $null))
            {
                $SubscriptionType="Free"
            }
            else
            {
                $SubscriptionType="Purchased"
            }
        }
        else
        {
            $SubscriptionType="Trial"
        }

        #Friendly Expiry Date
        if($ExpiryDate -ne $null)
        {
            $FriendlyExpiryDate=(New-TimeSpan -Start (Get-Date) -End $ExpiryDate).Days
            if($Status -eq "Enabled")
            {
                $FriendlyExpiryDate=$FriendlyExpiryDate
            }
            elseif($Status -eq "Warning")
            {
                $FriendlyExpiryDate="Already Expired. Will suspend in $FriendlyExpiryDate days"
            }
            elseif($Status -eq "Suspended")
            {
                $FriendlyExpiryDate="Already Expired. Will delete in $FriendlyExpiryDate days"
            }
            elseif($Status -eq "LockedOut")
            {
                $FriendlyExpiryDate="Subscription is locked. Please contact Microsoft"
            }
        }
        else
        {
            $ExpiryDate="-"
            $FriendlyExpiryDate="Never Expires"
        }

        #Check for filters
        if($ShowAllSubscription -eq $true)
        {
            $Print=1
        }
        else
        {
            if(($Trial.IsPresent) -and ($SubscriptionType -eq "Trial"))
            {
                $Print=1
            }
            if(($Free.IsPresent) -and ($SubscriptionType -eq "Free"))
            {
                $Print=1
            }
            if(($Purchased.IsPresent) -and ($SubscriptionType -eq "Purchased"))
            {
                $Print=1
            }
            if(($Expired.IsPresent) -and ($Status -ne "Enabled"))
            {
                $Print=1
            }
            if(($Active.IsPresent) -and ($Status -eq "Enabled"))
            {
                $Print=1
            }
        }
        


        #Export result to csv
        if($Print -eq 1)
        {
            $PrintedOutput++
            $Result=@{'SubscriptionName'=$SubscriptionName;'FriendlySubscriptionName'=$NamePrint;'SubscribedDate'=$SubscribedDate;'TotalLicenses'=$TotalLicenses;'LicenseExpiryDate/NextLifeCycleActivityDate'=$ExpiryDate;'FriendlyExpiryDate'=$FriendlyExpiryDate;'SubscriptionType'=$SubscriptionType;'Status'=$Status}
            $Results= New-Object PSObject -Property $Result  
            $Results | Select-Object 'SubscriptionName','FriendlySubscriptionName','SubscribedDate','TotalLicenses','SubscriptionType','LicenseExpiryDate/NextLifeCycleActivityDate','FriendlyExpiryDate','Status' | Export-Csv -Path $ExportCSV -Notype -Append
        }
        }

        #Reading the required data from csv file

        $pdetails= @{}
        $num=1

        Import-Csv ./details.csv | ForEach-Object {
            #Write-Host "$($_.SubscriptionName) $($_.FriendlySubscriptionName) Expiry: $($_.FriendlyExpiryDate)"


            $subs=$_.FriendlySubscriptionName
            $expiry=$_.FriendlyExpiryDate
            $subsType=$_.SubscriptionType
            $subsDate=$_.SubscribedDate
            $totalLicenses=$_.TotalLicenses
            $pname="Product Name $($num)"
            $pdetails.Add($pname,$subs)
            $sdate="$($subs) Subscribed Date"
            $pdetails.Add($sdate,$subsDate)
            $tlicenses="$($subs) Total Licenses"
            $pdetails.Add($tlicenses,$totalLicenses)
            $stype="$($subs) Subscription Type"
            $pdetails.Add($stype,$subsType)
            $exp="$($subs) Expires in"
            $pdetails.Add($exp,$expiry)
            $num++
        }
        return $pdetails

    }
    catch{
        $pdetails=@{}
        $pdetails.Add("message",$Error[0].Exception.Message)
        return $pdetails
    }


}

### These units specified will be displayed in the Dashboard
Function Set-Units() 
{
    $units = @{}
    Import-Csv ./details.csv | ForEach-Object {
        #Write-Host "$($_.SubscriptionName) $($_.FriendlySubscriptionName) Expiry: $($_.FriendlyExpiryDate)"
    
    
        $subs=$_.FriendlySubscriptionName
        $exp="$($subs) Expires in"
        $units.Add($exp,"days")
    }
    return $units
}

$mainJson = @{}

$mainJson=(Get-Data)
### Configuration info for the plugin
$mainJson.Add("plugin_version", $version)
$mainJson.Add("heartbeat_required", $heartbeat)
$mainJson.Add("displayname", $displayname) 

### Populates the monitoring data and its units
$mainJson.Add("units", (Set-Units)) 

### Returns the monitoring data to Site24x7 servers
return $mainJson | ConvertTo-Json



