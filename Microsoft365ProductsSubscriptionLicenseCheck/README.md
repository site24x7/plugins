# Read Me for the plugin "Microsoft 365 Products Subscription License Check"

Configure the Site24x7 Microsoft365ProductsSubscriptionLicenseCheck plugin to monitor your Microsoft 365 Subscription Name, Subscription Date, Total Licenses, and the Number of Days to License Expiry. This plugin will notify technicians of product expiry well in advance so that they can renew their license.

## _Prerequisites_
- Windows environment
- The Microsoft365ProductsSubscriptionLicenseCheck plugin will automatically verify, download, and install the 'MSOnline' module required to monitor your Microsoft365 product license details. This can be viewed in the Microsoft365ProductsSubscriptionLicenseCheck.ps1 file. 
If the 'MSOnline' module is not installed, follow the instructions given below to manually install it.

## _How to install the MSOnline module manually_
- Install-Module MSOnline
- Import-Module MSOnline
