# Plugin to monitor windows certificates

This plugin monitors the certificates in windows certificate store

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/monitors-configure/SERVER/windows) in the server where you plan to run the plugin.

### Plugin installation

---

##### Windows

- Create a directory "certificate_monitoring" under Site24x7 Windows Agent plugin directory :

      Windows     ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\certificate_monitoring

- Download the files "certificate_monitoring.ps1" and "certificate_monitoring.cfg".

- Configure the path of the certificate in the certificate store (cert:\) and the name of the certificate that needs to be monitored in "certificate_monitoring.cfg" as mentioned in the configuration section below, multiple certificates can be monitoried by providing multiple configurations..

- Place "certificate_monitoring.ps1" and "certificate_monitoring.cfg" files under the "certificate_monitoring" directory

- Execute the below command with appropriate arguments to check for the valid json output.

      .\certificate_monitoring.ps1 -certPath "<path to the certificate store>" -certName "<Certificate Name>"

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configuration
---
       [display_name]
       certPath=<cerificate path>
       certName=<certificate name>
       
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
