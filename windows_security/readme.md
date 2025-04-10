# Windows security monitoring

This plugin monitors key Windows security activities such as failed login attempts, antivirus status, malware detections, account lockouts, and more. It helps in tracking and ensuring the health of your system's security posture.

## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named `windows_security`.

2. Download the file [windows_security.bat](https://github.com/site24x7/plugins/blob/master/windows_security/windows_security.bat) , [security_events.ps1](https://github.com/site24x7/plugins/blob/master/windows_security/security_events.ps1) and place them under the `windows_security` directory.

3. Further move the folder `windows_security` into the Site24x7 Windows Agent plugin directory:
    ```
    C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
    ```
The agent will automatically execute the plugin within few minutes and user can see the plugin monitor under Site24x7 -> Plugins -> Plugin Integrations.

## **Log Tracking for Windows Security Events**  
Once the plugin monitor is successfully registered in Site24x7, you can also track the **Windows Security Event Logs** directly within the **Applog** tab under the log name **WinSecurityLog**.  

This feature automatically collects and displays security-related logs, providing insights into critical events such as failed login attempts, malware detections, and other security activities.  

## Supported Metrics

Track the following metrics with the plugin:

| Name                         | Description                                                                                      |
|------------------------------|--------------------------------------------------------------------------------------------------|
| `Failed Login Attempts`       | Tracks the number of unsuccessful login attempts on the monitored system.                                        |
| `Account Lockouts`            | Represents the number of user accounts that have been locked due to multiple failed login attempts.                                        |
| `Antivirus Status`            | Displays `1` if antivirus and real-time protection are enabled, otherwise `0`.                    |
| `Malware Detections`          | Displays the number of malware instances identified by windows security software.                                 |
| `Security Threats Actions`    | Tracks the number of actions taken against identified security threats, such as quarantining infected files, removing malware, or blocking suspicious processes. |
| `Failed Software Updates`     | Total number of failed software updates.                                     |
| `Malware Remediation Failed`  | Monitors the number of unsuccessful attempts to remove or neutralize identified malware.        |
| `Threat Detected Quarantined` | Represents the number of threats that were successfully identified and quarantined by security software.|
| `Malware Action Failed`       | Tracks the number of failed actions attempted by security software to respond to malware threats.                      |

![image](https://github.com/user-attachments/assets/745889f9-3418-4277-ac1f-2fd6ca0a2ea6)

