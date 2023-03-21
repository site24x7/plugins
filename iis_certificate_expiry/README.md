# IIS CERTIFICATE EXPIRY DATE MONITORING

=================================================================

- This plugin is used to monitor the days left for IIS certificate expiry.

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Run the below query in PowerShell and get the thumbprint of the IIS certificate.

		$path="Cert:\LocalMachine\My"
		Get-ChildItem -Path $path

---

### Plugin Installation 

- Create a folder named "iis_certificate_expiry".
		
- Download all the files in "iis_certificate_expiry" folder and place it under the "iis_certificate_expiry" directory.

		https://raw.githubusercontent.com/site24x7/plugins/master/iis_certificate_expiry/iis_certificate_expiry.ps1
		https://raw.githubusercontent.com/site24x7/plugins/master/iis_certificate_expiry/iis_certificate_expiry.cfg

- Configurations:
  Add the thumbprint that you received  from the executed command in  the Prerequisites section and path of the certificate in iis_certificate_expiry.cfg file:


		﻿﻿[IIS_certificate]
		thumbprint="thumbprint"
		path="Cert:\LocalMachine\My"
		
- Execute the plugin manually by using below command and check for the valid JSON output.

		.\iis_certificate_expiry.ps1 -thumbprint "thumbprint" -path "path" 
		
- Move the folder named "iis_certificate_expiry" under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Metric Monitored

		Days Left to Expiry	->	No of days left for IIS Certificate to expire

---





