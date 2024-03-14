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

    java_file_url=plugin_url+plugin_name+"/"+plugin_name+".java"
    sh_file_url=plugin_url+plugin_name+"/"+plugin_name+".sh"
    jar1_file_url=plugin_url+plugin_name+"/"+"jconn4.jar"
    jar2_file_url=plugin_url+plugin_name+"/"+"json-20140107.jar"
    if not download_file(java_file_url, temp_plugin_path):return False
    if not download_file(sh_file_url, temp_plugin_path):return False
    if not download_file(jar1_file_url, temp_plugin_path):return False
    if not download_file(jar2_file_url, temp_plugin_path):return False
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
    """
    Creates Directories.

    Args:
        path: The path where the directory have to be created

    Returns:
        bool: True/ False
    """
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

def replace_string_in_file(file_path, old_string, new_string):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        modified_content = file_content.replace(old_string, new_string)

        with open(file_path, 'w') as file:
            file.write(modified_content)
        
        return True
    except Exception as e:
        print(    str(e))
        return False



def initiate(plugin_name, plugin_url, args=None):

    print("------------------------------ Starting Plugin Automation ------------------------------")
    print()


    agent_path="/opt/site24x7/monagent/" 
    agent_temp_path=agent_path+"temp/"
    agent_plugin_path=agent_path+"plugins/"

    # checking the existance of Agent Temporary Directory
    if not check_directory(agent_temp_path):
        print("    Agent Directory does not Exist")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return
    
    # Creating the Agent Plugin Temporary Directory
    print("    Creating Temporary Plugins Directory")
    plugins_temp_path=os.path.join(agent_temp_path,"plugins/")
    if not check_directory(plugins_temp_path):
        if not make_directory(plugins_temp_path):
            print("")
            print("------------------------------ Plugin Automation Failed ------------------------------")
            return 
    print("    Created Temporary Plugins Directory")
    print()

    # Downloading the files from GitHub
    print("    Downloading Plugin Files")
    if not down_move(plugin_name, plugin_url, plugins_temp_path):
       print("")
       print("------------------------------ Plugin Automation Failed ------------------------------")
       return 
    print("    Downloaded Plugin Files")
    print()

    #Configuring sybase.sh 
    print("   Configuring sybase.sh")
    cmd="which java"
    java_path=execute_command(cmd, need_out=True)
    java_path = java_path.decode('utf-8')
    java_path="/".join(java_path.split("/")[:-1])
    print(java_path)
    if not java_path:
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 

    cmd="which javac"
    javac_path=execute_command(cmd, need_out=True)
    if not javac_path:
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
    
    sybase_temp_path=plugins_temp_path+"sybase.sh"
    if not replace_string_in_file(sybase_temp_path,'HOST=\"\"', f'HOST=\"{args.hostname}\"'):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
        
    if not replace_string_in_file(sybase_temp_path,'PORT=\"\"', f'PORT=\"{args.port}\"'):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 

    if not replace_string_in_file(sybase_temp_path,'USERNAME=\"\"', f'USERNAME=\"{args.username}\"'):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 

    if not replace_string_in_file(sybase_temp_path,'PASSWORD=\"\"', f'PASSWORD=\"{args.passsword}\"'):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
    #JAVA_HOME="/usr/bin"

    if not replace_string_in_file(sybase_temp_path,'JAVA_HOME=\"/usr/bin\"', f'JAVA_HOME=\"{java_path}\"'):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 


    # Setting Executable Permissions for the Plugin
    print("    Creating executable plugin file")
    cmd=f"chmod 744 {plugins_temp_path}/{plugin_name}/{plugin_name}.sh"
    if not execute_command(cmd):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
    print("    Created executable plugin file")
    print("")



    # Validating the plugin output
    print("    Validating the plugin output")
    cmd=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.sh"

    result=execute_command(cmd, need_out=True)
    if not plugin_validator(result):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return
    print("    Plugin output validated sucessfully")
    print("")


    # Moving the plugin files into the Agent Directory
    print("    Moving the plugin into the Site24x7 Agent directory")
    if not move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
        print("")
        print("------------------------------ Plugin Automation Failed ------------------------------")
        return 
    print("    Moved the plugin into the Site24x7 Agent directory")
    print()

    print("------------------------------ Sucessfully Completed Plugin Automation ------------------------------")


if __name__ == "__main__":
    plugin_name="sybase"
    plugin_url="https://raw.githubusercontent.com/site24x7/plugins/suraj/"

    #user configs
    username = "new_username"
    password = "new_password"
    hostname = "localhost"
    port = "port"


    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--username', help='username for sybase',default=username)
    parser.add_argument('--password', help='password for sybase',default=password)
    parser.add_argument('--hostname', help='hostname for sybase',default=hostname)
    parser.add_argument('--port', help='port for sybase',default=port)

    args=parser.parse_args()

    initiate(plugin_name, plugin_url, args)