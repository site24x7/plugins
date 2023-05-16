Plugin to monitor Active Directory Replication status
===========

A plugin to monitor Active Directory replication's metadata for a set of one or more replication partner with data 
describing an Active Directory replication failure.

The following metrics are provided for this plugin:
### Active Directory Replication metadata metrics -
* InboundLastAttempt: The last inbound attempted.
* InboundLastAttemptPartner: The last inbound attempted by a partner.
* InboundLastSuccess: The last inbound succeeded.
* InboundLastSuccessPartner: The last inbound succeeded by a partner
* InboundLastResult: The last inbound resulted.
* OutboundLastAttempt: The last outbound attempted.
* OutboundLastAttemptPartner: The last outbound attempted by a partner.
* OutboundLastSuccess: The last outbound succeeded.
* OutboundLastSuccessPartner: The last outbound succeeded by a partner.
* OutboundLastResult: The last outbound resulted.

### Active Directory Replication failure metrics - 
* FailureCount: The number of failure count in Replication
* FailureType: The type of failure in Replication.
* FirstFailureTime: The time which first failure happened.
* LastError: The last error occurred in Replication.
* ErrorPartner: The Replication error which thrown for partner.
* ErrorServer: The Replication error which thrown for server.

### Prerequisites 
Make sure following powershell cmdlets installed in the server where you going to add the Active Directory Replication status plugin
1. Get-ADDomainController
2. Get-ADReplicationPartnerMetadata
3. Get-ADReplicationFailure

### Plugin Installation
1. Download the latest version of Site24x7WindowsAgent and install in your server. 
    https://www.site24x7.com/help/admin/adding-a-monitor/windows-server-monitoring.html
2. In your windows server goto powershell console and execute below commands
                ```
                    Import-Module ServerManager
                    Install-WindowsFeature -Name RSAT-AD-PowerShell
                ```
3. And to import the PowerShell Active Directory module, run the below command in the powershell console
                ```
                Import-Module ActiveDirectory
                ```
4. Create a folder named 'ActiveDirectoryReplicationStatus' and place the 'ActiveDirectoryReplicationStatus.ps1' script file under created folder.
5. Move the folder "ActiveDirectoryReplicationStatus" into the Plugins directory "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins"
6. Further in the next DC i.e after 5 mins, user can see the plugin monitor under Plugin > Plugin Integrations. The plugin monitor will also be listed under the respective server monitor's Plugins tab (Server > Server Monitor > Servers > click on the desired server monitor > Plugins Integration). 
7. User can set up threshold profiles and be alerted when the configured value exceeds.
    https://www.site24x7.com/help/admin/configuration-profiles/threshold-and-availability/plugin-monitor.html



