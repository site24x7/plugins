# Plugin for Twilio usage Monitoring

Monitor twilio usage using Site24x7 Server Monitoring Plugins. 

### Prerequisites
---
- Site24X7 twiliomon plugin uses python's "twilio" package to collect metrics.
    - Installation
    
            easy_install twilio
            pip install twilio

- For more detail refer  [How to install twilio?]

### TwilioMon Plugin installation
---

##### Linux

- Create a directory "twiliomon" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/twiliomon
- Download the file [twiliomon.py] and place it under the "twiliomon" directory

##### Windows
 
- Create a directory "twiliomon" under Site24x7 Linux Agent plugin directory - C:\Program Files\Site24x7\WinAgent\monitoring\Plugins\twiliomon
- Download the file [twiliomon.py] and place it under the "twiliomon" directory
- Download [twiliomon.ps1] and place it under "twiliomon" directory
- Replace `$python="C:\Python27\python.exe"` in "twiliomon.ps1" file with your python path `$python=<python exe path>`


### TwilioMon Plugin configuration
---

- `ACCOUNT_SID = ""`	Your Account SID from [Twilio console]
- `AUTH_TOKEN  = ""`	Your Auth Token from [Twilio console]

### TwilioMon Metrics
---

All metrics are based on day(today) stats.

Name						| Description
---            			 	|   ---
calls_inbound_count      	| Number of all inbound voice calls, to mobile, toll-free and local numbers.
calls_inbound_usage			| Inbound call minutes.
calls_outbound_count		| Number of all outbound voice calls.
calls_outbound_usage		| Outbound call minutes.
calls_sip_inbound_count     | All inbound SIP calls count.
calls_sip_inbound_usage		| All inbound SIP call minutes.
calls_sip_outbound_count    | All outbound SIP calls count.
calls_sip_outbound_usage	| All inbound SIP call minutes.
calls_client_count			| All TwilioClient voice calls count.
calls_client_usage			| All TwilioClient voice call minutes.
sms_count					| Count of all SMS messages, both inbound and outbound
sms_inbound_count			| Count of only inbound SMS messages.
sms_outboubd_count			| Count of only inbound SMS messages.
totalprice_usage			| Total Usage Price.

[How to install twilio?]: <https://www.twilio.com/docs/libraries/python#installation>
[Twilio console]: <http://www.twilio.com/console>
[twiliomon.py]: <https://raw.githubusercontent.com/site24x7/plugins/master/twiliomon/twiliomon.py>
[twiliomon.ps1]: <https://raw.githubusercontent.com/site24x7/plugins/master/twiliomon/twiliomon.ps1>