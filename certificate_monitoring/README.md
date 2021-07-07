# Plugin to monitor windows certificates

This plugin monitors the certificates in windows certificate store

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

### Plugin installation

---

##### Windows

- Create a directory "certificate_monitoring" under Site24x7 Windows Agent plugin directory :

      Windows             ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\certificate_monitoring

- Download the files "certificate_monitoring.py" and "certificate_monitoring.json" and place them under the "certificate_monitoring" directory

      wget https://raw.githubusercontent.com/site24x7/plugins/master/certificate_monitoring/certificate_monitoring.ps1
      wget https://raw.githubusercontent.com/site24x7/plugins/master/certificate_monitoring/certificate_monitoring.json

- Provide the absolute path of the certificate(provide path with forward "/") that needs to be monitored in certificate_monitoring.json, multiple certificates can also be monitoried using the same plugin by adding multiple configurations as given in the certificate_monitoring.json.

- Execute the below command with appropriate arguments to check for the valid json output.

      .\certificate_monitoring.ps1 "< provide the path to the certificate>"

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metrics Captured

---

      certificate_version                           ->      Version of the certificate
      signature_algorithm                           ->      Algorithm used to sign certificate
      valid_from                                    ->      certificate is valid from
      valid_to                                      ->      certificate expiry date
      friendly_name                                 ->      Friendly name of the certificate
      days_left                                     ->      Number of days left before the certificate expires
      subject_name                                  ->      Subject name of the certificate
      is_the_certificate_expired                    ->      shows expiry status of certificate as true/false
