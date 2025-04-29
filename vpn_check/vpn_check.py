#!/usr/bin/python3
import sys, json, time, subprocess, requests, urllib3, argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PLUGIN_VERSION = "1"
HEARTBEAT = "true"
METRICS_UNITS={'URL Response Time':'ms','Packet Loss':'%','Latency':'ms'}

parser = argparse.ArgumentParser()
parser.add_argument('--host', help='intranet url to be monitored', default="localhost")
parser.add_argument('--url', help='intranet url to be monitored', default="https://localhost:943/admin/")
parser.add_argument('--port', help='intranet url to be monitored', default="943")
parser.add_argument('--vpn_interface', help='intranet url to be monitored', default=None)
args, unknown = parser.parse_known_args()

VPN_HOST = args.host
VPN_PORT = args.port
VPN_INTERFACE = args.vpn_interface
URL_BEHIND_VPN = args.url

def metric_collector(URL, vpn_data):
    try:
        start_time = time.time() * 1000
        response = requests.get(URL, verify=False)
        Latency = round((time.time() * 1000) - start_time)
        vpn_data['URL Response Time'] = Latency
        
        if response.status_code >= 400:
            vpn_data['status'] = 0
        vpn_data['URL Status Code'] = response.status_code
    except Exception as e:
        vpn_data['status'] = 0
        vpn_data['msg'] = str(e)
    return vpn_data

def check_connected_to_vpn(VPN_INTERFACE, vpn_data):
    try:
        if sys.platform == 'win32':
            output = get_command_output(f"ipconfig | findstr /I {VPN_INTERFACE}")
        else:
            output = get_command_output("ifconfig | grep -w " + VPN_INTERFACE + "")
        if output:
            vpn_data['VPN Connected'] = 1
        else:
            vpn_data['VPN Connected'] = 0
    except Exception as e:
        pass
    return vpn_data

def check_vpn(VPN_HOST, VPN_PORT):
    vpn_data = {}
    try:
        response = requests.head(f'https://{VPN_HOST}:{VPN_PORT}', 
                              timeout=5, 
                              verify=False)
        vpn_data['VPN Status'] = 1
        return vpn_data, True
    except requests.RequestException:
        vpn_data['VPN Status'] = 0
        vpn_data['status'] = 0
        vpn_data['msg'] = "failed to connect to vpn server"
        return vpn_data, False

def get_command_output(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return output

def get_packet_loss(VPN_HOST, vpn_data):
    try:
        cmd = 'ping -c 3 ' + VPN_HOST
        if sys.platform == 'win32':
            cmd = 'ping -n 3 ' + VPN_HOST
        output = get_command_output(cmd)
        if output:
            if sys.platform == 'win32':
                for x in output.decode('utf-8').split('\n'):
                    if 'loss' in x:
                        x = x.split('%')
                        packetloss = float(x[0].split(' ')[-1].split('(')[-1])
                    if 'Average' in x:
                        x = x.split(',')
                        for y in x:
                            if 'Average' in y:
                                Latency = float((y.split(' ')[-1].strip()).split('ms')[0])
            else:
                for x in output.decode('utf-8').split('\n'):
                    if 'packet loss' in x:
                        x = x.split(',')
                        packetloss = float(x[2].split('%')[0])
                        Latency = x[3].split('time')[1].split('ms')[0].strip()
            vpn_data['Packet Loss'] = packetloss
            vpn_data['Latency'] = Latency
    except Exception as e:
        pass
    return vpn_data

def get_public_ip():
    services = [
        'https://api.ipify.org?format=json',
        'https://ipinfo.io/json',
        'https://ifconfig.me/ip',
        'https://icanhazip.com',
        'https://checkip.amazonaws.com'
    ]
    for service in services:
        try:
            response = requests.get(service, timeout=10, verify=False)
            if response.status_code == 200:
                if "json" in response.headers.get('Content-Type', ''):
                    data = response.json()
                    return data.get('ip') or data.get('ip_address')
                else:
                    return response.text.strip()
        except Exception:
            continue
    return None

def get_isp_info(vpn_data):
    try:
        ip = get_public_ip()
        if not ip:
            raise Exception("Unable to retrieve public IP")
        isp_response = requests.get(f"http://ip-api.com/json/{ip}", timeout=30, verify=False)
        isp_data = isp_response.json()
        vpn_data['ISP'] = isp_data.get("isp", "unknown")
    except Exception as e:
        vpn_data['ISP'] = "unknown"
    return vpn_data


def run(param=None):
    vpn_data, vpn_status = check_vpn(VPN_HOST, int(VPN_PORT))
    if VPN_INTERFACE:
        vpn_data = check_connected_to_vpn(VPN_INTERFACE, vpn_data)
    if vpn_status:
        vpn_data = get_packet_loss(VPN_HOST, vpn_data)
        vpn_data = metric_collector(URL_BEHIND_VPN, vpn_data)
        vpn_data = get_isp_info(vpn_data)
    vpn_data['plugin_version'] = PLUGIN_VERSION 
    vpn_data['heartbeat_required'] = HEARTBEAT
    vpn_data['units'] = METRICS_UNITS
    return vpn_data

if __name__ == '__main__':
    print(json.dumps(run()))
