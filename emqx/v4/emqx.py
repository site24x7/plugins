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
        self.username=args.username
        self.password=args.password
    
    def metriccollector(self):

        try:
            url = f"http://{self.host}:{self.port}/api/v4/metrics"
            response = requests.get(url, auth=(self.username, self.password))
            response.raise_for_status()
            data = response.json()
            raw_metric_data = data.get("data", [{}])[0].get("metrics", {})
            metric_data = {}
            for key, value in raw_metric_data.items():
                key_new = key.title().replace(".", " ")
                metric_data[key_new.title()] = value

            self.maindata.update(metric_data)
            
            self.maindata['tabs'] = {
            'Delivery': {
                'order': 1,
                'tablist': [
                    "Delivery Dropped",
                    "Delivery Dropped Expired",
                    "Delivery Dropped No_Local",
                    "Delivery Dropped Qos0_Msg",
                    "Delivery Dropped Queue_Full",
                    "Delivery Dropped Too_Large"
                ]
            },
            'Client': {
                'order': 2,
                'tablist': [
                    "Client Acl Allow",
                    "Client Acl Cache_Hit",
                    "Client Acl Deny",
                    "Client Auth Failure",
                    "Client Auth Success",
                    "Client Auth Success Anonymous",
                    "Client Authenticate",
                    "Client Check_Acl",
                    "Client Connack",
                    "Client Connect",
                    "Client Connected",
                    "Client Disconnected",
                    "Client Subscribe",
                    "Client Unsubscribe"
                ]
            },
            'Messages': {
                'order': 3,
                'tablist': [
                    "Messages Acked",
                    "Messages Delayed",
                    "Messages Delivered",
                    "Messages Dropped",
                    "Messages Dropped Await_Pubrel_Timeout",
                    "Messages Dropped No_Subscribers",
                    "Messages Forward",
                    "Messages Publish",
                    "Messages Qos0 Received",
                    "Messages Qos0 Sent",
                    "Messages Qos1 Received",
                    "Messages Qos1 Sent",
                    "Messages Qos2 Received",
                    "Messages Qos2 Sent",
                    "Messages Received",
                    "Messages Retained",
                    "Messages Sent"
                ]
            },
            'Packets': {
                'order': 4,
                'tablist': [
                    "Packets Auth Received",
                    "Packets Auth Sent",
                    "Packets Connack Auth_Error",
                    "Packets Connack Error",
                    "Packets Connack Sent",
                    "Packets Connect Received",
                    "Packets Disconnect Received",
                    "Packets Disconnect Sent",
                    "Packets Pingreq Received",
                    "Packets Pingresp Sent",
                    "Packets Puback Inuse",
                    "Packets Puback Missed",
                    "Packets Puback Received",
                    "Packets Puback Sent",
                    "Packets Pubcomp Inuse",
                    "Packets Pubcomp Missed",
                    "Packets Pubcomp Received",
                    "Packets Pubcomp Sent",
                    "Packets Publish Auth_Error",
                    "Packets Publish Dropped",
                    "Packets Publish Error",
                    "Packets Publish Inuse",
                    "Packets Publish Received",
                    "Packets Publish Sent",
                    "Packets Pubrec Inuse",
                    "Packets Pubrec Missed",
                    "Packets Pubrec Received",
                    "Packets Pubrec Sent",
                    "Packets Pubrel Missed",
                    "Packets Pubrel Received",
                    "Packets Pubrel Sent",
                    "Packets Received",
                    "Packets Sent",
                    "Packets Suback Sent",
                    "Packets Subscribe Auth_Error",
                    "Packets Subscribe Error",
                    "Packets Subscribe Received",
                    "Packets Unsuback Sent",
                    "Packets Unsubscribe Error",
                    "Packets Unsubscribe Received"
                ]
            }
        }

        except Exception as e:
            self.maindata["msg"]=f"{e}"
            self.maindata["status"]=0
        
        return self.maindata
        
        
if __name__=="__main__":
    
    host="localhost"
    port=18083
    username="user"
    password="user"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host', help='emqx host',default=host)
    parser.add_argument('--port', help='emqx port',default=port)
    parser.add_argument('--username', help='emqx user name',default=username)
    parser.add_argument('--password', help='emqx password',default=password)
    args=parser.parse_args()
    obj=emqx(args)

    result=obj.metriccollector()
    print(json.dumps(result))
