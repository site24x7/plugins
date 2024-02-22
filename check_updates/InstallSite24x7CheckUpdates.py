#!/usr/bin/python3
import os
import requests
import subprocess
import json
import warnings
import re

warnings.filterwarnings("ignore")

def move_folder(source, destination):
    try:
        os.rename(source, destination)
    except Exception as e:
        print(str(e))
        return False
    return True


def move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
    try:
        if not check_directory(agent_plugin_path):
            print(f"    {agent_plugin_path} Agent Plugins Directory not Present")
            return False
        if not move_folder(plugins_temp_path+plugin_name, agent_plugin_path+plugin_name): 
            return False

    except Exception as e:
        print(str(e))
        return False
    return True


def plugin_config_setter(plugin_name, plugins_temp_path, args):
    try:
        full_path=plugins_temp_path+plugin_name+"/"
        config_file_path=full_path+plugin_name+".cfg"
        pattern = re.compile(rf"\(.*\)", re.MULTILINE)
        params=pattern.findall(str(args))[0].strip("(,)").replace(",","\n").replace(" ","")
        with open(config_file_path, "w") as f:
            f.write(f"[{args.sid}]\n"+params)

    except Exception as e:
        print(str(e))
        return False
    return True


def plugin_validator(output):
    try:
        result=json.loads(output.decode())
        if "status" in result:
            if result['status']==0:
                print("Plugin execution encountered a error")
                if "msg" in result:
                    print(result['msg'])
            return False

    except Exception as e:
        print(str(e))
        return False
    
    return True


def download_file(url, path):
    filename=url.split("/")[-1]
    response=requests.get(url, stream=True)
    if response.status_code == 200 :
        with open(os.path.join(path,filename), "wb") as f:
            f.write(response.content)
        print(f"      {filename} Downloaded")
    else:
        print(f"      {filename} Download Failed with response code {str(response.status_code)}")
        return False
    return True


def down_move(plugin_name, plugin_url, plugins_temp_path):
    temp_plugin_path=os.path.join(plugins_temp_path,plugin_name+"/")
    if not check_directory(temp_plugin_path):
        if not make_directory(temp_plugin_path):return False

    py_file_url=plugin_url+plugin_name+"/"+plugin_name+".py"
    cfg_file_url=plugin_url+plugin_name+"/"+plugin_name+".cfg"
    if not download_file(py_file_url, temp_plugin_path):return False
    if not download_file(cfg_file_url, temp_plugin_path):return False
    return True


def execute_command(cmd, need_out=False):
    try:
        cmd=cmd.split()
        result=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"    {cmd} execution failed with return code {result.returncode}")
            print(f"    {str(result.stderr)}")
            return False
        if need_out:
            return result.stdout
        return True
    except Exception as e:
        print(    str(e))
        return False


def make_directory(path):
    if not check_directory(path):
        try:
            os.mkdir(path)
            print(f"    {path} directory created.")
        
        except Exception as e:
            print(f"    Unable to create {path} Directory  : {str(e)}")
            return False
    return True


def check_directory(path):
    return os.path.isdir(path)

def initiate(plugin_name, plugin_url, args=None):

    print("------------------------------ Starting Plugin Automation ------------------------------")
    print()


    agent_path="/opt/site24x7/monagent/"
    agent_temp_path=agent_path+"temp/"
    agent_plugin_path=agent_path+"plugins/"

    if not check_directory(agent_temp_path):
        print("    Agent Directory does not Exist")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return
    print("    Creating Temporary Plugins Directory")
    plugins_temp_path=os.path.join(agent_temp_path,"plugins/")
    if not check_directory(plugins_temp_path):
        if not make_directory(plugins_temp_path):
            print("")
            print("------------------------------ Plugin Automation Failed ------------------------------")
            return 
    print("    Created Temporary Plugins Directory")
    print()

    print("    Downloading check_updates Plugin Files")
    if not down_move(plugin_name, plugin_url, plugins_temp_path):
       print("")
       print("------------------------------ Plugin Automation Failed ------------------------------")
       return 
    print("    Downloaded check_updates Plugin Files")
    print()

    print("    Creating executable plugin file")
    cmd=f"chmod 744 {plugins_temp_path}/{plugin_name}/{plugin_name}.py"
    if not execute_command(cmd):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
    print("    Created executable plugin file")
    print("")

    print("    Validating the python plugin output")
    cmd=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.py"
    result=execute_command(cmd, need_out=True)
    if not plugin_validator(result):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return
    print("    Plugin output validated sucessfully")
    print("")    

    if args:
        # Setting the plugin config file
        print("    Setting plugin configuration")
        if not plugin_config_setter(plugin_name, plugins_temp_path, args):
            print("")
            print("------------------------------ Plugin Automation Failed ------------------------------")
            return 
        print("    Plugin configuration set sucessfully")
        print()
    

    print("    Moving the plugin into the Site24x7 Agent directory")
    if not move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
    print("    Moved the plugin into the Site24x7 Agent directory")
    print()

    print("------------------------------ Sucessfully Completed Plugin Automation ------------------------------")


if __name__ == "__main__":
    plugin_name="check_updates"
    plugin_url="https://raw.githubusercontent.com/site24x7/plugins/master/"

    initiate(plugin_name, plugin_url)
