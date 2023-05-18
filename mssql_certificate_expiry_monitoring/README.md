# MSSQL Certificate Expiry Monitoring

=================================================================

- Monitoring the expiration date of a SQL server encryption certificate is important to ensure the ongoing security of your data. When a certificate expires, any data that was encrypted using that certificate isno longer accessible. This can cause data loss and security breaches.

 Using this plugin to view the certificate name, certificate issuer name, certificate start date, certificate expiry date.

### Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- To run the PowerShell plugin, ensure the below policy has been set.

  1.  Login to your server.
  2.  Run the PowerShell prompt as Admin and execute the following:
   Set-ExecutionPolicy RemoteSigned
  3.  Restart the plugin agent service.
---

### Plugin Installation 

- Create a folder named "mssql_certificate_expiry_monitoring".
		
- Download the below files and place it in the "mssql_certificate_expiry_monitoring" directory.

		https://raw.githubusercontent.com/site24x7/plugins/master/mssql_certificate_expiry_monitoring/mssql_certificate_expiry_monitoring.ps1
		https://raw.githubusercontent.com/site24x7/plugins/master/mssql_certificate_expiry_monitoring/mssql_certificate_expiry_monitoring.cfg

- Add the below configurations in mssql_certificate_expiry_monitoring.cfg file:

		[1]
		server="server_name"
		database="master"
		username="user_name"
		password="password"
		
- Move the folder "mssql_certificate_expiry_monitoring" under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

### Metrics Monitored

		Certificate Name
		Certificate Issuer Name 
		Certificate Start Date
		Certificate Expiry Date





