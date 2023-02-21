# Wordpress Single Plugin Performance Monitor:

This plugin monitors the No of Process,CPU and Memory usage of the particular wordpress  plugin specified under  '/var/www/html/wp-content/plugins/<Plugin Name>'  folder.

## Wordpress:

WordPress is a free and open-source content management system written in hypertext preprocessor language and paired with a MySQL or MariaDB database with supported HTTPS. Features include a plugin architecture and a template system, referred to within WordPress as "Themes".

WordPress is a CMS that enables you to manage your website’s content (CMS for short). It’s a powerful tool for building and managing websites. WordPress is used by 74 million websites of all types and sizes to publish fresh content every second.

## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin. 

### Plugin Installation  

- Create a directory named "Wordpress_Single_Plugin" under the Site24x7 Linux Agent plugin directory: 

        Linux             ->   /opt/site24x7/monagent/plugins/Wordpress_Single_Plugin
      
- Download all the files in the "Wordpress_Single_Plugin" folder and place it under the "Wordpress_Single_Plugin" directory.

- Execute the below command with appropriate arguments to check for the valid json output:
```
python3 wordpress_mon.py --url="http://<Domain or Website>/wp-json/wp/v2/plugins" --username="<Wordpress UserName>" --app_password="<Application Password>" --plugin_path="<Exact Name of Plugin>,<path to the plugin folder>"

```
### Configurations

- Provide your Wordpress_Single_Plugin configurations in Wordpress_Single_Plugin.cfg file.
```
[Wordpress Plugin Process]
url = "http://<Domain or Website>/wp-json/wp/v2/plugins"
username = "<Wordpress UserName>"
app_password = "<Application Password>"
plugin_path = "<Exact Name of Plugin>,<path to the plugin folder>"
```

- Make sure that Wordpress username is the administrator or an user with permissions. And enter the application password generated under user->Application password. Do not enter the password of the user.

- Specify the correct name of the plugin and the folder path separtated by commas. If you dont know the path to the folder go under '/var/www/html/wp-content/plugins/', you will find the plugin folder. 

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics
The following metrics are captured in the Wordpress_Plugin_Performance Plugin
 
```
1) <Plugin Name> - Status of the plugin (Active or Inactive)
2) <Plugin Name>  CPU Usage - The Total CPU Usage of all the process running inside the plugin folder.
3) <Plugin Name>  Memory Usage - The Total Memory Usage of all the process running inside the plugin folder.
3) <Plugin Name>  Process Count - The Total No of the process running inside the plugin folder.
```

