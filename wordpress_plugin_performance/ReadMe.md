# Wordpress Plugin Performance Monitor:

This plugin monitors the No of Process,CPU and Memory usage of the wordpress plugins running under '/var/www/html/wp-content/plugins/' folder.

## Wordpress:

WordPress is a free and open-source content management system written in hypertext preprocessor language and paired with a MySQL or MariaDB database with supported HTTPS. Features include a plugin architecture and a template system, referred to within WordPress as "Themes".

WordPress is a CMS that enables you to manage your website’s content (CMS for short). It’s a powerful tool for building and managing websites. WordPress is used by 74 million websites of all types and sizes to publish fresh content every second.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 
-The plugin is using "http://yourwebsite.com/wp-json/wp/v2/plugins" Wordpress API endpoint to fetch plugins state. Incase if user disabled the Wordpress API, please enable for this end point.
- Install linux/windows agent in the server where wordpress application is running.

### Plugin Installation  

- Create a directory named "wordpress_plugin_performance" under the Site24x7 Linux Agent plugin directory: 

        Linux             ->   /opt/site24x7/monagent/plugins/wordpress_plugin_performance
      
- Download all the files in the "wordpress_plugin_performance" folder and place it under the "wordpress_plugin_performance" directory.
```
wget https://raw.githubusercontent.com/site24x7/plugins/master/wordpress_plugin_performance/wordpress_plugin_performance.cfg
wget https://raw.githubusercontent.com/site24x7/plugins/master/wordpress_plugin_performance/wordpress_plugin_performance.py
```

- Execute the below command with appropriate arguments to check for the valid json output:
```
python3 wordpress_plugin_performance.py --url="http://<Domain or Website>/wp-json/wp/v2/plugins" --username="<Wordpress UserName>" --app_password="<Application Password>"
```
### Configurations

- Provide your wordpress_plugin_performance configurations in wordpress_plugin_performance.cfg file.
```
[Wordpress Plugin Process]
url = "http://<Domain or Website>/wp-json/wp/v2/plugins"
username = "<Wordpress UserName>"
app_password = "<Application Password>"
```
- The "http://yourwebsite.com/wp-json/wp/v2/plugins" is the REST API endpoint for fetching the status of the wordpress plugins. Provide the equivalent endpoint with 'http or https://localhost or domain name/wp-json/wp/v2/plugins'. Provide equivalent URL used for your Wordpress setup.
- Make sure that Wordpress username is the administrator or an user with access to the REST API. And enter the application password generated in your wordpress site->Admin login->users->all users->Application password. Do not enter the password of the user.
#### Generating Application password
- Open your wordpress site and login in wp-admin page.
- Go to users->all users and Click on the username which you want to generate the appllication password. 
- Scroll down to the end and there will be the option to generate application passwords. Provide the application name and click on generate password. 
- Make sure that the user is an administrator or an user with access to the REST API.

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the wordpress_plugin_performance Plugin
 
```
1) <Plugin Name> - Status of the plugin (Active or Inactive)
2) <Plugin Folder Name> CPU Usage - The Total CPU Usage of all the process running inside the plugin folder.
3) <Plugin Folder Name> Memory Usage - The Total Memory Usage of all the process running inside the plugin folder.
4) <Plugin Folder Name> Process Count - The Total No of the process running inside the plugin folder.
```
