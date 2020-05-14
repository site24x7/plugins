#!/usr/bin/python

import sys,json,time,subprocess

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

METRICS_UNITS={'url_response_time':'ms','packet_loss':'%','latency':'ms'}

VPN_HOST='vpn-test'

VPN_PORT=10443

#specify the interface name if you want to check whether your server is connected to VPN or not.
VPN_INTERFACE=None

URL_BEHIND_VPN='http://intranet-url'

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
    from http.client import InvalidURL
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError
    from httplib import InvalidURL

def metric_collector(URL,vpn_data):
    try:
        start_time = time.time() * 1000
        response = urlconnection.urlopen(URL, timeout=30)
        latency = round(((time.time() * 1000) - start_time))
        vpn_data['url_response_time']=latency
        http_status_code = response.getcode()
        if  http_status_code >= 400:
               vpn_data['status']=0
        vpn_data['url_status_code'] = http_status_code
    except Exception as e:
        vpn_data['status']=0
        vpn_data['msg']="Kindly check if the server is connected to VPN (or) URL is down" 
    return vpn_data

def check_connected_to_vpn(VPN_INTERFACE,vpn_data):
    try:
        if sys.platform == 'win32':
            output = get_command_output("ipconfig | grep -w "+VPN_INTERFACE+"")
        else:
            output = get_command_output("ifconfig | grep -w "+VPN_INTERFACE+"")
        if output:
            vpn_data['vpn_connected'] = 1
        else:
            vpn_data['vpn_connected'] = 0
    except Exception as e:
        pass
    return vpn_data

def check_vpn(VPN_HOST,VPN_PORT):
    vpn_data={}
    vpn_status = False
    try:
        import socket
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((VPN_HOST,VPN_PORT))
        if result == 0:
            vpn_data['vpn_status'] = 1
            vpn_status = True
        else:
            vpn_data['vpn_status'] = 0
            vpn_data['status'] = 0
            vpn_data['msg'] = "failed to connect to vpn server"
    except Exception as e:
        vpn_data['status']=0
        vpn_data['msg']=str(e)

    return vpn_data , vpn_status

def get_command_output(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

def get_packet_loss(VPN_HOST,vpn_data):
    try:
        cmd='ping -c 3 '+VPN_HOST
        if sys.platform == 'win32':
            cmd='ping -n 3 '+VPN_HOST
        output = get_command_output(cmd)
        if output:
            if sys.platform == 'win32':
                for x in output.decode('utf-8').split('\n'):
                    if 'loss' in x:
                        x = x.split('%')
                        packetloss=float(x[0].split(' ')[-1].split('(')[-1])
                    if 'Average' in x:
                        x = x.split(',')
                        for y in x:
                            if 'Average' in y:
                               latency = float((y.split(' ')[-1].strip()).split('ms')[0])
            else:
                for x in output.decode('utf-8').split('\n'):
                    if 'packet loss' in x:
                        x = x.split(',')
                        packetloss=float(x[2].split('%')[0])
                        latency=x[3].split('time')[1].split('ms')[0].strip()
            vpn_data['packet_loss'] = packetloss
            vpn_data['latency'] = latency
    except Exception as e:
        pass
    return vpn_data

def get_isp_info(vpn_data):
    try:
        if sys.platform == 'win32':
            import json
            import base64
            response = urlconnection.urlopen("https://api6.ipify.org?format=json", timeout=30)
            iplist = response.read()
            decoded_ip = iplist.decode()
            ipobj = json.loads(decoded_ip)
            ip = ipobj["ip"]
            url = "http://ip-api.com/json/"+ip
            ispresponse = urlconnection.urlopen(url, timeout=30)
            isplist = ispresponse.read()
            decoded_isp = isplist.decode()
            ispobj = json.loads(decoded_isp)
            output = ispobj["isp"]
        else:
            cmd='bash /opt/site24x7/monagent/plugins/vpn_check/isp.sh'
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
        if output:
            vpn_data['isp']= str(output.rstrip('\n'))
    except Exception as e:
        pass
    return vpn_data

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='intranet url to be monitored')
    parser.add_argument('--url', help='intranet url to be monitored')
    parser.add_argument('--port', help='intranet url to be monitored')
    args = parser.parse_args()
    if args.url:
        URL_BEHIND_VPN = args.url
    if args.host:
        VPN_HOST=args.host
    if args.port:
        VPN_PORT=args.port
    vpn_data,vpn_status = check_vpn(VPN_HOST,int(VPN_PORT))
    if VPN_INTERFACE:
        vpn_data = check_connected_to_vpn(VPN_INTERFACE,vpn_data)
    if vpn_status:
        vpn_data = get_packet_loss(VPN_HOST,vpn_data)
        vpn_data = metric_collector(URL_BEHIND_VPN,vpn_data)
        vpn_data = get_isp_info(vpn_data)
    vpn_data['plugin_version'] = PLUGIN_VERSION
    vpn_data['heartbeat_required'] = HEARTBEAT
    vpn_data['units']=METRICS_UNITS
    print((json.dumps(vpn_data,indent=4)))
