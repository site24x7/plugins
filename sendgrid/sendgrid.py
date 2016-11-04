#!/usr/bin/python3
### Author: Vinoth Manoharan, Zoho Corp
### Language : Python
### Tested in Ubuntu

import datetime
import urllib.request
import json

PLUGIN_VERSION = 1

HEARTBEAT = "true"

'''
API_KEY is used for authorization while getting the stats from sendgrid server. 
Find more info on how to create API keys in the below url
https://sendgrid.com/docs/User_Guide/Settings/api_keys.html
'''
API_KEY = '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'

METRIC_UNITS = {}

class SendGrid:
    def __init__(self, apiKey=None):
        self.date = datetime.date.today()
        self.apiKey = apiKey
        self.url = 'https://api.sendgrid.com/v3/stats?start_date=%s'%format(self.date)
        self.headers = {'Authorization': 'Bearer %s'%format(apiKey)}
        self.req = urllib.request.Request(self.url, headers=self.headers)
        
    def metricsCollector(self):
        result = {}
        if self.apiKey is not None:
            try:
                with urllib.request.urlopen(self.req) as res:
                    stats = json.loads(res.read().decode())
                    result = stats[0]['stats'][0]['metrics']
            except Exception as e:
                result['error'] = str(e)
                return result
            result['units'] = METRIC_UNITS
        else:
            result['error'] = 'API key is absent'
        return result

if __name__ == "__main__":
    s = SendGrid(API_KEY)
    
    result = s.metricsCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))