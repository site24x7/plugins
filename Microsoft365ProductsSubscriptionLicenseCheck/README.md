# Microsoft 365 Products Subscription License Check
---------------------------------------------------------------------------
Configure the Site24x7 Microsoft365ProductsSubscriptionLicenseCheck plugin to monitor your Microsoft 365 Subscription Name, Subscription Date, Total Licenses, and the Number of Days to License Expiry. This plugin will notify technicians of product expiry well in advance so that they can renew their license.


## Prerequisites

- Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

- Install the MSOnline module manually.
  
      Install-Module MSOnline
      Import-Module MSOnline
      

### Plugin Installation  

- Create a folder named `Microsoft365ProductsSubscriptionLicenseCheck`.
      
- Download all the files [LicenseFriendlyName.txt](https://github.com/site24x7/plugins/blob/master/Microsoft365ProductsSubscriptionLicenseCheck/LicenseFriendlyName.txt), [Microsoft365ProductsSubscriptionLicenseCheck.ps1](https://github.com/site24x7/plugins/blob/master/Microsoft365ProductsSubscriptionLicenseCheck/Microsoft365ProductsSubscriptionLicenseCheck.ps1), [SubscriptionName.csv](https://github.com/site24x7/plugins/blob/master/Microsoft365ProductsSubscriptionLicenseCheck/SubscriptionName.csv)
 and place it under the `Microsoft365ProductsSubscriptionLicenseCheck` directory.
	        
      wget https://raw.githubusercontent.com/site24x7/plugins/master/Microsoft365ProductsSubscriptionLicenseCheck/Microsoft365ProductsSubscriptionLicenseCheck.ps1




- Execute the below command to check for the valid json output:

	 ```
	  .\Microsoft365ProductsSubscriptionLicenseCheck.ps1
	 ```
 
 - Move the folder into the  Site24x7 Windows Agent plugin directory: 

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\Microsoft365ProductsSubscriptionLicenseCheck
		
---
