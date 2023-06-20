# RADIUS (Remote Authentication Dial-In User Service)  Server

#### What is RADIUS (Remote Authentication Dial-In User Service)?

RADIUS (Remote Authentication Dial-In User Service) is a client-server protocol and software that enables remote access servers to communicate with a central server to authenticate dial-in users and authorise their access to the requested system or service.
RADIUS enables a company to maintain user profiles in a central database that all remote servers can share. Having a central database provides better security, enabling a company to set up a policy that can be applied at a single administered network point.

## Prerequisites: 

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

## Installation Steps:

- Create a directory "radius_server_status"

- Download the below files and place under the above created directory
          ```
           https://raw.githubusercontent.com/site24x7/plugins/master/radius_server_status/radius_server_status.cfg
           https://github.com/site24x7/plugins/raw/master/radius_server_status/radius_server_status.ps1
          ```
- Open and edit the downloaded file radius_server_status.cfg

- The radius_server_status.cfg file will contains the below content

          [Radius Server Status]
          ip = localhost
          port = 1812
          device_password = testing123


- [Radius Server Status] is the name of the monitor, you can change the name based on your need.
- ip is the IP address of your radius server          
- port is the port used by the radius server for authentication
- device_password is the shared secret key 

After finish the configuration, move the folder "radius_server_status" into the Site24x7 Linux Agent plugin directory:

        radius_server_status  -->  /opt/site24x7/monagent/plugins/

- Execute the below command with appropriate arguments to check for the valid json output:
```
python3 radius_server_status.py --ip=<ip-of-radius-server> --port=<port-no-of-radius-server> --device_password=<shared-secret-key> 
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

The plugin only checks if the radius server is online by sending a Access-Request packet. If the Access-Accept packet is received the plugin monitor will be in up state and down in vice versa. 
