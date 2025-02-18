# Plugin for monitoring Windows security

This plugin monitors key Windows security activities such as failed login attempts, antivirus status, malware detections, account lockouts, and more. It helps in tracking and ensuring the health of your system's security posture.

## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## **Plugin installation**

1. Create a folder named `windows_security`.

2. Download the file [windows_security.ps1](https://github.com/site24x7/plugins/blob/master/windows_security/windows_security.ps1) and place them under the `windows_security` directory.

3. Further move the folder `windows_security` into the Site24x7 Windows Agent plugin directory:
    ```
    C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
    ```
The agent will automatically execute the plugin within few minutes and user can see the plugin monitor under Site24x7 -> Plugins -> Plugin Integrations.
  
## Supported Metrics

Track the following metrics with the plugin:

| Name                         | Description                                                                                      |
|------------------------------|--------------------------------------------------------------------------------------------------|
| `failed_login_attempts`       | The number of failed login attempts in the last 6 minutes.                                        |
| `account_lockouts`            | The number of user account lockouts in the last 6 minutes.                                       |
| `antivirus_status`            | Displays `1` if antivirus and real-time protection are enabled, otherwise `0`.                    |
| `malware_detections`          | The number of malware detections recorded in the last 6 minutes.                                 |
| `security_threats_actions`    | The number of security threats actions taken in the last 6 minutes.                              |
| `software_updates_pending`    | The number of pending software updates.                                                          |
| `failed_software_updates`     | The number of failed software updates in the last 6 minutes.                                     |
| `malware_remediation_failed`  | The number of failed attempts to remediate malware in the last 6 minutes.        |
| `threat_detected_quarantined` | The number of threats detected and successfully quarantined in the last 6 minutes.|
| `malware_action_failed`       | The number of failed malware actions in the last 6 minutes.                      |
