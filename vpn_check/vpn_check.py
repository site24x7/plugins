#!/usr/bin/python

import sys,json,time,subprocess

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

METRICS_UNITS={'url_response_time':'ms','packet_loss':'%'}

VPN_HOST='vpn-test.com'

VPN_PORT=10443

URL_BEHIND_VPN='http://internalurl'

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
        vpn_data['status']=1
        http_status_code = response.getcode()
        if  http_status_code >= 400:
               vpn_data['status']=0
        vpn_data['url_status_code'] = http_status_code
    except Exception as e:
        vpn_data['url_status_code'] = -1
        vpn_data['url_response_time'] = -1
        vpn_data['status']=0
        if vpn_data['vpn_status'] == 1:
            vpn_data['msg']="cannot connect to the url. check you are connected to VPN"
        else:
            vpn_data['msg']=str(e)
    return vpn_data

def check_vpn():
    vpn_data={}
    vpn_status = False
    try:
        import socket
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
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

def get_packet_loss(vpn_data):
    try:
        cmd='ping -c 3 '+VPN_HOST
        if sys.platform == 'win32':
            cmd='ping -n 3 '+VPN_HOST

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if output:
            if sys.platform == 'win32':
                packetloss = float([x for x in output.decode('utf-8').split('\n') if x.find('loss') != -1][0].split('%')[0].split(' ')[-1].split('(')[-1])
            else:
                packetloss = float([x for x in output.decode('utf-8').split('\n') if x.find('packet loss') != -1][0].split('%')[0].split(' ')[-1])
            vpn_data['packet_loss']= str(packetloss)
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
    parser.add_argument('--url', help='intranet url to be monitored')
    args = parser.parse_args()
    if args.url:
        URL=args.url
    else:
        URL=URL_BEHIND_VPN
    vpn_data,vpn_status = check_vpn()
    if vpn_status:
        vpn_data = get_packet_loss(vpn_data)
        vpn_data = metric_collector(URL,vpn_data)
        vpn_data = get_isp_info(vpn_data)
    vpn_data['plugin_version'] = PLUGIN_VERSION
    vpn_data['heartbeat_required'] = HEARTBEAT
    vpn_data['units']=METRICS_UNITS
    print((json.dumps(vpn_data,indent=4)))