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
                result['status'] = 0
                result['msg'] = str(e)
                return result
            result['units'] = METRIC_UNITS
        else:
            result['status'] = 0
            result['msg'] = 'API key is absent'
        result['plugin_version'] = PLUGIN_VERSION 
        result['heartbeat_required']=HEARTBEAT
        return result

if __name__ == "__main__":

    import argparse

    parser=argparse.ArgumentParser()
    parser.add_argument("--api_key",help="api key for sendgrid",default=None)
    args=parser.parse_args()

    s = SendGrid(args.api_key)
    
    result = s.metricsCollector()
    
    print(json.dumps(result, indent=4, sort_keys=True))
