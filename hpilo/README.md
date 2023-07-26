# HP iLo server hardware monitoring

iLo server management software that enables you to configure, monitor and update your HPE servers seamlessly, from anywhere in the world. Hence, it is critical to know all kinds of hardware related events and its status including temperatures, fan speeds, power supply status, individual disk status and more.

Know how to configure the HP iLO plugin and the monitoring metrics for providing in-depth visibility into the performance, availability, and usage stats of iLO servers - https://www.site24x7.com/plugins/hp-ilo-monitoring.html

## Prerequisites

- Download and install the latest version of the [Site24x7 agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Download and install Python version 3 or higher.

---

### Plugin Installation  

- Create a directory named "hpilo<component>"

- Download the files and place it under the "hpilo<component>" directory.


- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the hpilo<component>.py script.
  
- Execute the below command with appropriate arguments to check for the valid JSON output:

      python ilo<component>.py 
