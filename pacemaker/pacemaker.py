#!/usr/bin/python3

import json
import traceback
import subprocess

data={}
data['plugin_version']=1
data['heartbeat_required']=True

data['units']={
  "Expected Votes": "votes",
  "Highest Expected": "votes",
  "Nodes Configured": "nodes",
  "Offline nodes": "nodes",
  "Online nodes": "nodes",
  "Resource Instances Configured": "resources",
  "Total Votes": "votes"
}

data["tabs"]={
  "Nodes": {
    "order": 1,
    "tablist": [
      "Nodes"
    ]
  },
  "Quorum": {
    "order": 2,
    "tablist": [
      "Quorum",
      "Expected Votes",
      "Highest Expected",
      "Total Votes"
    ]
  }
}


online_nodes=[]
offline_nodes=[]


def parse_output(line):
    try:
        data_line=line.strip().split(":")
        data[data_line[0].title()]=data_line[1].strip()
    except Exception as e:
        data["status"]=0
        data["msg"]= str(e)

def node_status(nodes,status_code):
    try:
        rows=[]
        nodes_count=0
        for node in nodes:
            node_dict={}
            if node != "":
                node_dict["name"]=node
                node_dict["status"]=status_code
                rows.append(node_dict)
                nodes_count+=1
    except Exception as e:
        data["status"]=0
        data["msg"]= str(e)
        return [],0
    return rows,nodes_count

def parse_nodes(line):
    try:
        data_line=line.strip().split("[")
        data_line=data_line[-1].replace("]","")
    except Exception as e:
        data["status"]=0
        data["msg"]= str(e)
        return []
        
    return data_line.split(" ")
            
def run_command(command):
    try:

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)
        (updates_output, err) = p.communicate()
        p_status = p.wait()

        if p.returncode != 0:   
            error="Command failed with return code:"+str(p.returncode)+"\nError:"+err.decode()
            data["status"]=0
            data["msg"]= error

    except Exception as e:
        data["status"]=0
        data["msg"]= str(e)+"\n"+err.decode()
        return ""
    return updates_output


def pcs_status():
    global online_nodes,offline_nodes
    try:
        output=run_command("pcs status").decode()
        output=output.split("\n")
        online_nodes=[]
        offline_nodes=[]
        node_list=False
        daemon_list=False
        cluster_summary=False
        resources=False
        for line in output:
            
            if line =="":
                node_list=False
                daemon_list=False
                cluster_summary=False
                resources=False

            if "Cluster name:" in line:
                parse_output(line)

            if "Cluster Summary:" in line:
                cluster_summary=True
            if cluster_summary and line != "":
                if "Stack:" in line:
                    data_line=line.replace("*","")
                    parse_output(data_line)
                if "nodes configured" in line:
                    data_line=line.strip().replace("*","")
                    data["Nodes Configured"]=data_line.replace("nodes configured","")
                if "resource instances configured" in line:
                    data_line=line.strip().replace("*","")
                    data["Resource Instances Configured"]=data_line.replace("resource instances configured","")

            if "Node List:" in line:
                node_list=True
            if node_list:
                if "Online" in line:
                    online_nodes+=parse_nodes(line)
                    continue
                if "OFFLINE" in line:
                    offline_nodes+=parse_nodes(line)
                    continue
                if "  *" in line:
                    offline_nodes.append(parse_nodes(line))
                    continue

            if "Full List of Resources:" in line:
                resources=True
                continue
            if resources:
                if "  *" in line:
                    data_line=line.strip().replace("*","").replace("\t"," ")
                    data_line=data_line.split("):")
                    data[(data_line[0]+")").title()]=data_line[-1].strip()
 

            if "Daemon Status:" in line:
                daemon_list=True
                continue
            if daemon_list and line !="":
                parse_output(line)
                continue
        

    except Exception as e:
        data["status"]=0
        data["msg"]=repr(e)
        return False

    return True

def quorum():
    try:
        output=run_command("pcs quorum status").decode()
        output=output.split("\n")
        quorum=False
        for line in output:

            if line =="":
                quorum=False

            if "Votequorum information" in line:
                quorum=True
                continue
            if quorum:
                if not ("---" in line):
                    parse_output(line)
    except Exception as e:
        data["status"]=0
        data["msg"]=repr(e)
        return False

    return True

            
def metric_collector():
    try:
        status=pcs_status()
        if not status:
            return 
        
        nodes1,online=node_status(online_nodes,1)
        nodes2,offline=node_status(offline_nodes,0)

        data["Online nodes"]=online
        data["Offline nodes"]=offline
        data["Nodes"]=nodes1+nodes2
      
        status=quorum()
        if not status:
            return
          
    except Exception as e:
        data["status"]=0
        data["msg"]=repr(e)


if __name__ == '__main__':
    metric_collector()
    print(json.dumps(data))
