#!/usr/bin/python3
import json
import requests
import base64

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class emqx:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.host=args.host
        self.port=args.port
        self.api_key=args.api_key
        self.secret_key=args.secret_key

        

    
    def metriccollector(self):
        

        credentials = f"{self.api_key}:{self.secret_key}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        # Construct the API request URL
        url = f"http://{self.host}:{self.port}/api/v5/metrics"

        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers)
        raw_metric_data=response.json()[0]
        metric_data={}
        for key, value in raw_metric_data.items():
            key_new=key.title().replace(".", " ")
            metric_data[key_new.title()] = value

        self.maindata.update(metric_data)

        return self.maindata




if __name__=="__main__":
    
    host="localhost"
    port=18083
    api_key="api_key"
    secret_key="api_secret_key"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host', help='emqx host',default=host)
    parser.add_argument('--port', help='emqx port',default=port)
    parser.add_argument('--api_key', help='emqx api key',default=api_key)
    parser.add_argument('--secret_key', help='emqx api secret key',default=secret_key)

    args=parser.parse_args()

    obj=emqx(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
