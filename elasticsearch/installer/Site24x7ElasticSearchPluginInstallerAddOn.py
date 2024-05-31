#! /usr/bin/python3
import os
import subprocess
import json
import warnings
import urllib.parse
import urllib.request
import shutil
import configparser



warnings.filterwarnings("ignore")
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m' 



def multi_config(read_file, write_file):
    try:
        with open(read_file, "r") as f:
            config_details=f.read()
            with open(write_file, "a") as f:
                f.write("\n")
                f.write("\n")

                f.write(config_details)
        return True
    except Exception as e:
        print("    "+str(e))
        return False



def delete_folder(folder_name):
    try:
        shutil.rmtree(folder_name)
        return True
    except Exception as e:
        print("    "+str(e))
        return False



def move_folder(source, destination):
    try:
        os.rename(source, destination)
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True



def remove_section_from_config(config_file, section_name):
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.has_section(section_name):
        config.remove_section(section_name)
        with open(config_file, 'w') as configfile:
            config.write(configfile)



def check_parse(plugin_name, plugin_dir, plugin_temp_path):

    file_path=plugin_dir+plugin_name+".cfg"
    temp_file_path=plugin_temp_path+plugin_name+"/"+plugin_name+".cfg"
    config = configparser.ConfigParser()
    config.read(file_path)
    sections = config.sections()

    config_temp = configparser.ConfigParser()
    config_temp.read(temp_file_path)
    section_name = config_temp.sections()[0]
    if section_name in sections:
        remove_section_from_config(file_path, section_name)



def move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
    try:
        if not check_directory(agent_plugin_path):
            print(f"    {agent_plugin_path} Agent Plugins Directory not Present")
            return False
        plugin_dir=agent_plugin_path+plugin_name+"/"
        if not check_directory(plugin_dir):

            if not move_folder(plugins_temp_path+plugin_name, plugin_dir): 
                return False
        else:
            check_parse(plugin_name, plugin_dir, plugins_temp_path)

            if not multi_config(plugins_temp_path+plugin_name+"/"+plugin_name+".cfg",plugin_dir+plugin_name+".cfg"):
                 return False

    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True



def plugin_config_setter(plugin_name, plugins_temp_path, arguments, display_name):
    try:
        full_path=plugins_temp_path+plugin_name+"/"
        config_file_path=full_path+plugin_name+".cfg"

        arguments='\n'.join(arguments.replace("--","").split())
        with open(config_file_path, "w") as f:
            f.write(f"[{display_name}]\n"+arguments)

    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True



def plugin_validator(output):
    try:
        result=json.loads(output.decode())
        if "status" in result:
            if result['status']==0:
                print("    Plugin execution encountered a error")
                if "msg" in result:
                    print(result['msg'])
            return False
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True






def download_file(url, path):
    filename=url.split("/")[-1]
    full_path=path+filename
    urllib.request.urlretrieve(url, full_path)
    response=urllib.request.urlopen(url)
    if response.getcode() == 200 :
        print(colors.GREEN +f"      {filename} Downloaded"+ colors.RESET)
    else:
        print(colors.RED +f"      {filename} Download Failed with response code {str(response.status_code)}"+ colors.RESET)
        return False
    return True



def down_move(plugin_name, plugin_url, plugins_temp_path):
    temp_plugin_path=os.path.join(plugins_temp_path,plugin_name+"/")
    if not check_directory(temp_plugin_path):
        if not make_directory(temp_plugin_path):return False

    py_file_url=plugin_url+"/"+plugin_name+".py"
    cfg_file_url=plugin_url+"/"+plugin_name+".cfg"
    if not download_file(py_file_url, temp_plugin_path):return False
    if not download_file(cfg_file_url, temp_plugin_path):return False
    return True



def execute_command(cmd, need_out=False):
    try:
        if not isinstance(cmd, list):
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
        print(colors.RED +"    "+str(e)+colors.RESET)
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



def input_validate(msg, default=None, custom_msg=None):

    input_check=False
    while not input_check:
        if custom_msg:
                    option = input(f"{custom_msg}")
        else:
                    option = input(f"\n    Enter the {msg} of the Elasticsearch instance : ")
        if not option :
            print(f"    No {msg} entered.")
            if default:
                continue_option=input(f"    Do you want to use the default value \"{default}\"? (y/n):")
                if continue_option =="Y" or continue_option=="y":
                    option=default
                    input_check=True
                    return option
                
            continue_option=input(f"    A {msg} is required to get metrics. Do you want to enter a {msg} (y/n) : ")

            if continue_option=="Y" or continue_option=="y":
                input_check=False
            else:
                input_check=True
                return False
        else:
            input_check=True
        
    return option



def initiate(plugin_name, plugin_url):

    args={}
    agent_path="/opt/site24x7/monagent/"
    agent_temp_path=agent_path+"temp/"
    agent_plugin_path=agent_path+"plugins/"

    print()
    print(colors.GREEN +"------------------------   Installing the plugin ----------------------------"+ colors.RESET)
    print()
    print(colors.BLUE +"""    Hostname/IP Address, port of the Elasticsearch instance is required to get metrics. These details will be configured in the plugin configuration file.
          """+ colors.RESET)
          
    host=input_validate("hostname", default="localhost")
    if not host:
        print()
        print(colors.RED + "------------------------------ Error occured. Hostname is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    args["host"]=host


    port=input_validate("port", default="9200")
    if not port:
        print()
        print(colors.RED + "------------------------------ Error occured. Port is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    args["port"]=port


    print()
    custom_msgs="    Do you have SSL enabled in the instance? (y/n) :"
    ssl_option=input_validate("SSL Option", default="False", custom_msg=custom_msgs)
    if not ssl_option:
        print(colors.RED + "------------------------------ Error occured. SSL preference is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    if ssl_option.lower()=="y":
        ssl_option="YES"
    else:
        ssl_option="NO"

    args["ssl_option"]=ssl_option


    print()
    custom_msgs="    Do you have username/password enabled in the instance? (y/n) :"
    username_preference=input_validate("username/password", default="False", custom_msg=custom_msgs)
    if not username_preference:
        print(colors.RED + "------------------------------ Error occured. Username preference is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return



    if username_preference.lower()=="y":
        username_preference="true"
        username=input_validate("Elasticsearch username")
        if not username:
            print()
            print(colors.RED + "------------------------------ Error occured. Username is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
            return

        password=input_validate("Elasticsearch password")
        if not password:
            print()
            print(colors.RED + "------------------------------ Error occured. Password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
            return


    else:
        username_preference="false"
        username="None"
        password="None"

    args["username"]=username
    args["password"]=password

    print(    args["username"])
    print(colors.GREEN +"    Hostname, Port, Username, Password and SSL preference received."+ colors.RESET)
    print()


    if not check_directory(agent_temp_path):
            print("    Site24x7 Linux agent directory not found.")
            print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
            return

    plugins_temp_path=os.path.join(agent_temp_path,"plugins/")
    if not check_directory(plugins_temp_path):
        if not make_directory(plugins_temp_path):
            print("")
            print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
            return 
    print(colors.GREEN +"    Installation in progress."+ colors.RESET)
    print()
    print("    Downloading the Elasticsearch plugin files from Site24x7's GitHub repository.")


    if not down_move(plugin_name, plugin_url, plugins_temp_path):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 
    print(colors.GREEN +"    Downloaded the Elasticsearch plugin files successfully."+ colors.RESET)
    print()


    py_update_cmd = [ "sed", "-i", "1s|^.*|#! /usr/bin/python3|", f"{plugins_temp_path}{plugin_name}/{plugin_name}.py" ]
    if not execute_command(py_update_cmd):
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 


    cmd=f"chmod 744 {plugins_temp_path}/{plugin_name}/{plugin_name}.py"
    if not execute_command(cmd):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 
    print("")


    arguments=f"""--username={args["username"]} --password={args["password"]} --host={args["host"]} --port={args["port"]} --ssl_option={args["ssl_option"]}"""
    cmd=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.py"+ " "+arguments
    result=execute_command(cmd, need_out=True)
    if not plugin_validator(result):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return
    print("")


    print("    Adding the plugin configurations in the elasticsearch.cfg file.")
    if not plugin_config_setter(plugin_name, plugins_temp_path, arguments, display_name=args["host"]):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 
    print("    Plugin configurations added successfully.")
    print()


    print("    Updating the plugin in the Site24x7 Agent directory")
    if not move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 
    print("    Added the plugin in the Site24x7 Agent directory")
    print()

    print(colors.GREEN +"------------------------------  Plugin installed successfully ------------------------------"+ colors.RESET)



if __name__ == "__main__":
    plugin_name="elasticsearch"
    plugin_url="https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch"
    initiate(plugin_name, plugin_url)
