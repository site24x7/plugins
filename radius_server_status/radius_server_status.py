#!/usr/bin/python3

import subprocess,sys,json,argparse


PLUGIN_VERSION="1"
HEARTBEAT="true"
data={}

def msg(cout):
  cout=cout.split("\n")
  cout.remove("")
  return cout[-1]


def request(ip,port,device_pass):

  try:
   s= "echo 'Message-Authenticator = 0x00, FreeRADIUS-Statistics-Type = 1, Response-Packet-Type = Access-Accept' | radclient -x "+ip+":"+port+" status "+device_pass
   out=subprocess.check_output(s,shell=True, stderr=subprocess.PIPE).decode()
   if "Received Access-Accept" in out:
    return "Received",1
  except subprocess.CalledProcessError as e:
    out = e.output.decode()
    err=e.stderr.decode()
    if 'No reply from server'in err:
       out=err
    else:
       try:
         out=msg(out)
       except :
         out=str(e)
    return 0,out

if __name__ == "__main__":

  parser=argparse.ArgumentParser()
  parser.add_argument('--ip',help="IP of the Radius Server to be authenticated",default="localhost")
  parser.add_argument('--port',help="Port No",default="1812")
  parser.add_argument('--device_password',help="Device Password")
  args=parser.parse_args()
  Reply,Status=request(args.ip,args.port,args.device_password)
  if Reply=="Received":
    data["Access Accept Status"]=Reply
    data["Server Status"]=Status
  elif Reply==0:
    data["status"] = 0
    data["msg"] = Status
    data["Server Status"]=0
  data['plugin_version'] = PLUGIN_VERSION
  data['heartbeat_required']=HEARTBEAT
  print(json.dumps(data, indent=4, sort_keys=True))
