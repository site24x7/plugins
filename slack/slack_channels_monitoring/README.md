### Plugin for monitoring Slack Channels

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

- Create a directory "slack_channels_monitoring".

- Download the files "slack_channels_monitoring.py" and "slack_channels_monitoring.cfg" and place it under the "slack_channels_monitoring" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/slack/slack_channels_monitoring/slack_channels_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/slack/slack_channels_monitoring/slack_channels_monitoring.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the slack_channels_monitoring.py script.
		
- Edit the "slack_channels_monitoring.cfg" file and add the configuration details to it.

 		[display_name]
		oauth_token = xoxp-1115218301570-1145293321776-1107217637223-sew12saq185c59db496cad2b6655868ac4e
		channel_name = agent_team
		channel_type = private
		
oauth_token - oauth token of your slack account
channel_name - name of the channel to be monitored with case sensitive
channel_type - type of the channel . Please choose any one of these channel type ids that you wish to monitor 
for eg : 1 - public | 2 : private | 3 : direct_message_user | 4 : multi_party_direct_message_channel

- Execute the below command to check for valid json output

		python slack_channels_monitoring.py --oauth_token="oauth_token" --channel_name="channel_name" --channel_type="channel_type"
            
- Move the directory "slack_channels_monitoring" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
    
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
    
