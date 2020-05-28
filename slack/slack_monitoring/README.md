### Plugin for monitoring Slack Application

### Prerequisites

* Make sure you have Installed python version 3.6 and above.

* python request module installation
     
    kindly install the requests module by using below command
 
         wget https://bootstrap.pypa.io/get-pip.py
	    
         python3.6 get-pip.py 
         
         pip3.6 install requests
       

* slackclient developer kit
       
         pip3.6 install slackclient

* OAuth Token of your slack account
    ### OAuth token Generation
    ---
        * First, you need to create the slack app.. Refer this link  https://api.slack.com/apps 
        * Select the workspace that you need to access using Slack Web Api
        * Navigate to "Permission" and you need to configure your "workspace URL" in Redirect URL
        * Navigate to "Scopes" and you can see the field "User Token Scopes"
        * Add this below  17 scopes one by one without fail
                1) users:read
                2) files:read
                3) groups:read
                4) im:read
                5) channels:read
                6) dnd:read
                7) emoji:read
                8) pins:read
                9) reactions:read
                10) reminders:read
                11) stars:read
                12) usergroups:read
                13) mpim:history
                14) mpim:read
                15) im:history
                16) groups:history
                17) channels:history
        * Finally, you can see the "Install app to Workspace" in that page..please click that button
        * Oauth token will be generated in that top of the page
        * Please copy the Oauth token and save it. This has to be configured in the plugin configuration file.

### Plugin Installation 

      	1) Create a directory "slack_monitoring" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/slack_monitoring
            
            mkdir /opt/site24x7/monagent/plugins/slack_monitoring

	2) Download the files "slack_monitoring.py" and place it under the "slack_monitoring" directory

		    wget https://raw.githubusercontent.com/site24x7/plugins/master/slack_monitoring/slack_monitoring.py

        3) Download the file "slack_monitoring.cfg" and place it under the "slack_monitoring" directory

            wget https://raw.githubusercontent.com/site24x7/plugins/master/slack_monitoring/slack_monitoring.cfg

### Plugin Configuration
---

    * Edit the "slack_monitoring.cfg" file and add the configuration details to it. Sample configuration file looks like: 
    
        #slack_monitoring.cfg

        [display_name]
        oauth_token = xoxp-1115218301570-1145293321776-1107217637223-sew12saq185c59db496cad2b6655868ac4e

        oauth_token - oauth token of your slack account
         
        display_name  - plugin monitor name to be displayed in site24x7 client

        
### Metrics Captured
    1) total_files
    2) total_users
    3) scheduled_messages
    4) remainder_count
    5) stars_count
    6) total_reaction_count
    7) total_file_size
    8) video_files
    9) audio_files
    10) image_files
    11) executable_files
    12) other_files
    13) do_not_distrub_enabled
    14) next_dnd_start_ts
    15) next_dnd_end_ts
    16) dnd_snooze_enabled
    17) configured channel message count
    