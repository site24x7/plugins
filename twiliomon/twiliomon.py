#!/usr/bin/python

"""

__author__ = Vijay, Zoho Corp
Language = Python

Tested in Ubuntu, Windows 8

"""

import json
import twilio

if int(twilio.__version_info__[0]) >= 6:
    from twilio.rest import Client as twilioclient
else:
    from twilio.rest import TwilioRestClient as twilioclient


######################### config section start ###################################

ACCOUNT_SID = ""          	# Your Account SID from www.twilio.com/console
AUTH_TOKEN  = ""		# Your Auth Token from www.twilio.com/console

######################### config section  end ###################################

COUNT_CATEGORIES = ["calls-inbound", "calls-outbound", "calls-sip-inbound", "calls-sip-outbound", "calls-client", "sms", "sms-inbound", "sms-outbound"]
USAGE_CATEGORIES = ["calls-inbound", "calls-outbound", "calls-sip-inbound", "calls-sip-outbound", "calls-client", "totalprice"]

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

class TwilioMon():
    metrics = {}
    units = {}

    def __init__(self):
        try:
            self.client = twilioclient(ACCOUNT_SID, AUTH_TOKEN)
        except twilio.exceptions.TwilioException as e:
            self.metrics["msg"] = "Check your credentials"
            self.client = None
        self.metrics['plugin_version'] = PLUGIN_VERSION
        self.metrics['heartbeat_required'] = HEARTBEAT

    def get_metrics(self):
        try :
            todays_usage = self.client.usage.records.today.list()

            for category in todays_usage:
                if category.category.lower() in COUNT_CATEGORIES:
                    if category.count:
                        cnt_key = category.category+"-"+"count"
                        cnt_key = cnt_key.replace("-","_")
                        self.metrics[cnt_key] = category.count
                        self.units[cnt_key] = category.count_unit
                if category.category.lower() in USAGE_CATEGORIES:       
                    if category.usage:
                        usage_key = category.category+"-"+"usage"
                        usage_key = usage_key.replace("-","_")
                        self.metrics[usage_key] = category.usage
                        self.units[usage_key] = category.usage_unit

            self.metrics["units"] = self.units

        except Exception as e:
            pass
        return self.metrics

if __name__ == '__main__':
    mon = TwilioMon()
    metrics = mon.get_metrics()

    print(json.dumps(metrics))
