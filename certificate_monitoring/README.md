# Plugin to monitor windows certificates

This plugin monitors the certificates in windows certificate store

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/monitors-configure/SERVER/windows) in the server where you plan to run the plugin.

### Plugin installation

---

##### Windows

- Create a directory "certificate_monitoring".

- Download the files "certificate_monitoring.ps1" and "certificate_monitoring.cfg".

- Configure the path of the certificate in the certificate store (cert:\) and the name of the certificate that needs to be monitored in "certificate_monitoring.cfg" as mentioned in the configuration section below, multiple certificates can be monitoried by providing multiple configurations..

- Place "certificate_monitoring.ps1" and "certificate_monitoring.cfg" files under the "certificate_monitoring" directory

- Execute the below command with appropriate arguments to check for the valid json output.

      powershell .\certificate_monitoring.ps1 -certPath "path to the certificate store" -certName "Certificate Name" -thumbprint "thumbprint of the certificate"
- Move the folder "certificate_monitoring"  into the Site24x7 Windows Agent plugin directory :

      Windows     ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\certificate_monitoring
      
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### Configuration
---
       [display_name]
       certPath="cerificate path"
       thumbprint="thumbprint of the certificate"
       certName="certificate name"

- certPath refers to the path of the certificate file on your system. Provide the full path to the certificate file in the configuration.

- certName is the name assigned to the certificate, which will also be used as the name of the plugin monitor. Choose a descriptive name for the certificate.

- thumbprint represents the thumbprint of the certificate. To obtain the thumbprint, follow these steps:

     - Navigate to the location where the certificate is stored on your system.
     - Double-click on the certificate file to open it.
     - In the certificate details, click on the "Details" tab.
     - Scroll down to locate the thumbprint value.
     - Copy the thumbprint value and paste it into the appropriate field in the configuration file.

       
### Metrics Captured

---

      certificate_version                           ->      Version of the certificate
      signature_algorithm                           ->      Algorithm used to sign certificate
      valid_from                                    ->      certificate is valid from (DD-MM-YYYY)
      valid_to                                      ->      certificate expiry date (DD-MM-YYYY)
      friendly_name                                 ->      Friendly name of the certificate
      days_left                                     ->      Number of days left before the certificate expires
      subject_name                                  ->      Subject name of the certificate
      is_the_certificate_expired                    ->      shows expiry status of certificate as true/false
      verified                                      ->      shows verification status of certificate as true/false
