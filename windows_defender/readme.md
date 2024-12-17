# Windows Defender Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin Installation  

- Create a directory named `windows_defender`.
  
```bash
mkdir windows_defender
cd .\windows_defender\
```
      
- Download below files and place it under the "windows_defender" directory.

```bash
https://github.com/site24x7/plugins/blob/master/windows_defender/windows_defender.ps1
```

- Execute the below command to check for the valid json output:

```bash
powershell .\windows_defender.ps1
```


### Move the plugin under the Site24x7 agent directory

- Move the "windows_defender" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

# Windows Defender Monitoring Metrics

| **Metric**                       | **Description**                                                                 |
|-----------------------------------|---------------------------------------------------------------------------------|
| `FullScanStartTime`              | The start time of the last full system scan.                                    |
| `FullScanEndTime`                | The end time of the last full system scan.                                      |
| `FullScanSignatureVersion`       | Signature version used during the last full scan.                              |
| `FullScanAge`                    | Age in days since the last full scan. Returns `-1` if no value is available.    |
| `QuickScanStartTime`             | The start time of the last quick scan.                                         |
| `QuickScanEndTime`               | The end time of the last quick scan.                                           |
| `QuickScanSignatureVersion`      | Signature version used during the last quick scan.                             |
| `QuickScanAge`                   | Age in days since the last quick scan. Returns `-1` if no value is available.   |
| `AntivirusSignatureVersion`      | Current antivirus signature version.                                           |
| `AntivirusSignatureLastUpdated`  | The last time the antivirus signature was updated.                             |
| `AntivirusSignatureAge`          | Age in days since the antivirus signature was last updated. Returns `-1` if no value is available. |
| `AntispywareSignatureVersion`    | Current antispyware signature version.                                         |
| `AntispywareSignatureLastUpdated`| The last time the antispyware signature was updated.                           |
| `AntispywareSignatureAge`        | Age in days since the antispyware signature was last updated. Returns `-1` if no value is available. |
| `NISSignatureVersion`            | Current Network Inspection System (NIS) signature version.                    |
| `NISSignatureAge`                | Age in days since the NIS signature was last updated. Returns `-1` if no value is available. |
| `OnAccessProtectionEnabled`      | Indicates if on-access protection is enabled. (`true` or `false`)              |
| `RealTimeProtectionEnabled`      | Indicates if real-time protection is enabled. (`true` or `false`)              |
| `AMServiceEnabled`               | Indicates if the antimalware service is enabled. (`true` or `false`)           |
| `NISEnabled`                     | Indicates if the Network Inspection System (NIS) is enabled. (`true` or `false`)|
| `AntivirusEnabled`               | Indicates if the antivirus is enabled. (`true` or `false`)                     |
| `AntispywareEnabled`             | Indicates if the antispyware is enabled. (`true` or `false`)                   |
| `TamperProtectionSource`         | Source of tamper protection settings.                                          |
| `IsTamperProtected`              | Indicates if tamper protection is enabled. (`true` or `false`)                 |
| `FirewallProfile`                | Lists the configuration for each firewall profile (Domain, Private, Public).   |
| `ThreatDetected`                 | Number of threats detected during scans.                                       |
| `WindefenderStatus`              | Windows Defender operational status.                                           |
| `WindefenderStatusText`          | Textual status of Windows Defender.                                            |
| `msg`                            | Message describing the current state of threat detection.                      |

