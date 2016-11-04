SendGrid Monitoring
===================
Sendgrid allow users to send emails without having to maintain email servers.

This plugin will query the '/v3/stats' with the start_date param as today's date and get the details.

Requirements
------------
SendGrid account and a valid api key has to generated in the account

SendGrid plugin installation
=============

Download sendgrid plugin from https://github.com/site24x7/plugins/blob/master/sendgrid/sendgrid.py

Place the plugin folder 'sendgrid/sendgrid.py' under agent plugins directory (/opt/site24x7/monagent/plugins/)

Commands to execute the above steps:

	cd /opt/site24x7/monagent/plugins/
	mkdir sendgrid
	cd sendgrid
	wget https://raw.githubusercontent.com/site24x7/plugins/master/sendgrid/sendgrid.py
	
Configuration
=============
The generated api key has to passed as input to this plugin

>API_KEY = <a valid api key>


SendGrid plugin attributes
--------------------------
	{
	"blocks": 0,
    "bounce_drops": 0,
    "bounces": 0,
    "clicks": 0,
    "deferred": 0,
    "delivered": 2,
    "invalid_emails": 0,
    "opens": 0,
    "processed": 0,
    "requests": 2,
    "spam_report_drops": 0,
    "spam_reports": 0,
    "unique_clicks": 0,
    "unique_opens": 0,
    "units": {},
    "unsubscribe_drops": 0,
    "unsubscribes": 0
    }


Each attribute represents the count of emails w.r.t their state

Monitoring additional metrics:
==============================
To monitor additional metrics, edit the "sendgrid.py" file and add the new metrics that need monitoring
 
Increment the plugin version value in the file "sendgrid.py" to view the newly added metrics ( For e.g. Change the default plugin version from PLUGIN_VERSION = "1" to "PLUGIN_VERSION = "2") 
