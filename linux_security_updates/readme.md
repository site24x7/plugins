# Linux Security Updates Monitoring

Supported Distros: Debian, Fedora, Suse
## Quick Installation

If you're using Linux servers, use the linux_security_updates plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/installer/Site24x7LinuxSecurityUpdatesPluginInstaller.sh && sudo bash Site24x7LinuxSecurityUpdatesPluginInstaller.sh
```

## Plugin Installation
---
##### Linux 

- Execute below command to download the `linux_security_updates` plugin.
  
	```bash
 	mkdir -p linux_security_updates && wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.py && sed -i "1s|^.*|#! $(which python3)|" linux_security_updates.py && wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.cfg && mv linux_security_updates.py linux_security_updates.cfg linux_security_updates
	```

- Move the directory `linux_security_updates` into the Site24x7 Linux Agent plugin directory.

	```
	mv linux_security_updates /opt/site24x7/monagent/plugins/
	```

  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Log Tracking for Pending Updates

Once the plugin monitor is successfully registered in Site24x7, you can also track the Linux Pending Security Updates directly within the Applog tab under the log name "Linux Pending Security Updates".

  To view pending update details, navigate to the following: Site24x7 web client > linux_security_updates plugin monitor > select AppLog tab > User can choose logtype as "Linux Pending Security Updates" to check the details of packages which have been not updated. 
  
### Metrics Captured

- Installed Packages Count
- Upgrades Available For Installed Packages
- Security Updates
- Packages to be Updated
- Reboot Required for packages
- Reboot Required Packages Count

![image](https://github.com/user-attachments/assets/562eee3e-731e-4ac3-98c1-7057b722ec91)
![image](https://github.com/user-attachments/assets/3f5235fd-3e9b-4fec-88e7-1dd0b4df7ca8)




