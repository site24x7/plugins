import os
import requests
import subprocess
import json
import warnings
import re
import zipfile
import shutil
import pymysql

warnings.filterwarnings("ignore")

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'  # Reset to default color

hostname=""
port=""
sys_username=""
sys_password=""
monitoring_username="site24x7"
monitoring_password="site24x7"

def establish_db_connection(hostname, sys_username, sys_password, port):
    try:
        connection = pymysql.connect(host=hostname,user=sys_username,passwd=sys_password,port=int(port))
        return connection
    except pymysql.Error as e:
        return False

def multi_config(read_file, write_file):
    try:
        with open(read_file, "r") as f:
            config_details=f.read()
            with open(write_file, "a") as f:
                f.write("\n")
                f.write(config_details)
        return True
    except Exception as e:
        print("    "+str(e))
        return False

def multi_config(read_file, write_file):
    try:
        with open(read_file, "r") as f:
            config_details=f.read()
            with open(write_file, "a") as f:
                f.write("\n")
                f.write(config_details)
        return True
    except Exception as e:
        print("    "+str(e))
        return False

def move_folder(source,destination):
    try:
        if os.path.exists(destination):
            print(colors.BLUE+"A MySQL plugin already exists in the agent directory."+colors.RESET)
            i=1
            while i<=3:
                cx_inp=input("Do you want to proceed with adding another MySQL instance for monitoring in the same plugin configuration file? (Y or N) ")
                if(cx_inp == "Y" or cx_inp=="y" or cx_inp.lower()=="yes"):
                    if not multi_config(source+"/mysql_monitoring.cfg",destination+"/mysql_monitoring.cfg"):
                        return False
                    else:
                        print(colors.GREEN+"Configuration of the new instance added successfully in the plugin. "+colors.RESET)
                        break
                elif(cx_inp == "N" or cx_inp=="n" or cx_inp.lower()=="no"):
                    shutil.rmtree(destination)
                    shutil.move(source, destination)
                    print(colors.GREEN+"Plugin installed successfully."+colors.RESET)
                    break
                else:
                    if i == 3:
                        print(colors.RED+"Process exited."+colors.RESET)
                        return False
                    print(colors.BLUE+"Valid input is required."+colors.RESET)
                i += 1
        else:
            shutil.move(source, destination)
            print(colors.GREEN+"Plugin installed successfully."+colors.RESET)

    except Exception as e:
        print(colors.RED + str(e) + colors.RESET)
        return False
    return True



def move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
    try:
        if not check_directory(agent_plugin_path):
            return False
        if not move_folder(plugins_temp_path+plugin_name, agent_plugin_path+plugin_name): 
            return False

    except Exception as e:
        print(colors.RED + str(e) + colors.RESET)
        return False
    return True


def plugin_config_setter(plugin_name, plugins_temp_path, arguments,hostname):
    try:
        full_path=plugins_temp_path+plugin_name+"/"
        config_file_path=full_path+plugin_name+".cfg"

        arguments='\n'.join(arguments.replace("--","").split())
        with open(config_file_path, "w") as f:
            f.write(f"\n[{hostname}]\n"+arguments)

    except Exception as e:
        print(colors.RED + str(e) + colors.RESET)
        return False
    return True


def plugin_validator(output):
    try:
        result=json.loads(output.decode())
        if "status" in result:
            if result['status']==0:
                print(colors.RED + "Plugin execution encountered a error" + colors.RESET)
                if "msg" in result:
                    print(colors.RED + result['msg'] + colors.RESET)
            return False

    except Exception as e:
        print(colors.RED + str(e) + colors.RESET)
        return False
    
    return True



def download_file(url, path):
    filename=url.split("/")[-1]
    response=requests.get(url, stream=True)
    if response.status_code == 200 :
        with open(os.path.join(path,filename), "wb") as f:
            f.write(response.content)
        print(colors.GREEN + filename+ " Downloaded" + colors.RESET)
    else:
        print(colors.RED + filename+ " Download Failed with response code"+ {str(response.status_code)}  + colors.RESET)
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
        cmd=cmd.split()
        result=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(colors.RED +cmd+" execution failed with return code "+ {result.returncode}+ colors.RESET)
            print(colors.RED + str(result.stderr) + colors.RESET)
            return False
        if need_out:
            return result.stdout
        return True
    except Exception as e:
       print(colors.RED + str(e) + colors.RESET)
       return False

def make_directory(path):
    
    if not check_directory(path):
        try:
            os.mkdir(path)
            print(colors.GREEN + path+ " directory created." + colors.RESET)
        
        except Exception as e:
            print(colors.RED + "Unable to create "+path +"Directory : " +str(e) + colors.RESET)
            return False
    return True


def check_directory(path):
    return os.path.isdir(path)

def initiate(plugin_name, plugin_url):

    agent_path="/opt/site24x7/monagent/" 
    agent_temp_path=agent_path+"temp/"
    agent_plugin_path=agent_path+"plugins/"

    # Creating the Agent Plugin Temporary Directory
    plugins_temp_path=os.path.join(agent_temp_path,"plugins/")
    if not check_directory(plugins_temp_path):
        if not make_directory(plugins_temp_path):
            print("")
            print(colors.RED+"------------------------------ Plugin Automation Failed ------------------------------"+colors.RESET)
            return 
    print("")

    # Downloading the files from GitHub
    print("Downloading the plugin files from Site24x7 GitHub repository.")
    if not down_move(plugin_name, plugin_url, plugins_temp_path):
       print("")
       print(colors.RED+"------------------------------ Download failed. Process exited.------------------------------"+colors.RESET)
       return 
    print(colors.GREEN+"Plugin files downloaded successfully."+colors.RESET)
    print("")

    # Setting Executable Permissions for the Plugin
    #print(colors.BLUE+" Creating an executable plugin file."+colors.RESET)
    cmd=f"chmod 744 {plugins_temp_path}/{plugin_name}/{plugin_name}.py"
    if not execute_command(cmd):
        print("")
        print(colors.RED+"------------------------------Plugin executable file could not be created. Exited plugin installation process. ------------------------------"+colors.RESET)
        return 
    #print(colors.GREEN+" Executable plugin file created successfully."+colors.RESET)
    #print("")

    #getting credentials form user
    print(colors.BLUE+"A user with SELECT and GRANT role is required to get MySQL metrics."+colors.RESET)
    print("")
    i=1
    while i<=3:
        cx_inp = input("Proceed to create a user in your MySQL instance? (Y or N)")
        if(cx_inp == "Y" or cx_inp=="y" or cx_inp.lower()=="yes"):
            print(colors.BLUE+"To create a user with reading privileges,  a hostname, port, admin username, and admin password is required. "+colors.RESET)
            print("")
            break
        elif(cx_inp == "N" or cx_inp=="n" or cx_inp.lower()=="no"):
            print("Without a monitoring user, MySQL cannot be monitored")
            print(colors.RED+"Process exited"+colors.RESET)
            return
        else:
            if i == 3:
                print(colors.RED+"Process exited."+colors.RESET)
                return
            print(colors.BLUE+"Valid input is required."+colors.RESET)
        i += 1

    i=1
    while i<=3:
        hostname=input("Enter the hostname or IP :")
        if hostname:
            break
        if i==3:
            print(colors.RED+"Without a hostname, MySQL can't be monitored"+colors.RESET)
            return
        i += 1

    i=1
    while i<=3:
        port=input("Enter the port :")
        if port:
            break
        if i==3:
            print(colors.RED+"Without a port, MySQL can't be monitored"+colors.RESET)
            return
        i += 1

    sys_username=input("Enter admin username : ")
    sys_password=input("Enter admin password : ")
    print("")
    print(colors.BLUE+"Checking the admin user connection"+colors.RESET)

    db=establish_db_connection(hostname,sys_username,sys_password,port)
    #import pymysql
    #db = pymysql.connect(host=hostname,user=sys_username,passwd=sys_password,port=int(port))
    if not db:
        print(colors.RED+"Error occurred. Check the details and rerun the installer."+colors.RESET)
        return 
    print("")
    print(colors.GREEN+"Admin user connected successfully"+colors.RESET)
    print("")
    print(colors.BLUE+"A user with SELECT and GRANT role will be created to get MySQL metrics."+colors.RESET)
    print(colors.BLUE+"It will be created with default username 'site24x7' and default password 'site24x7' "+colors.RESET)
    print(colors.BLUE+"Note that the username and the password will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases."+colors.RESET)
    print("")
    i=1
    while i<=3:
        new_up=input("Select  'Y' to input either new or existing username and password. Select 'N' to proceed with default username and password: ")
        if(new_up == "Y" or new_up=="y" or new_up.lower()=="yes"):
            monitoring_username=input("Enter the username :")
            if not monitoring_username:
                monitoring_username="site24x7"
            monitoring_password=input("Enter the user password :")
            if not monitoring_password:
                monitoring_password="site24x7"
            break

        elif(new_up == "N" or new_up=="n" or new_up.lower()=="no"):
            monitoring_username="site24x7"
            monitoring_password="site24x7"
            break
        else:
            if i == 3:
                print(colors.RED+"Process exited."+colors.RESET)
                return
            print(colors.BLUE+"Valid input is required."+colors.RESET)
        i += 1
       
    # Connecting with mysql and creating user
    try:
        cursor = db.cursor()
        cursor.execute("SELECT User FROM mysql.user WHERE User = '"+monitoring_username+"'")
        cmd=f"CREATE USER '{monitoring_username}'@'{hostname}' IDENTIFIED BY '{monitoring_password}'"
        if not cursor.fetchall():
            cursor.execute(cmd)
            print(colors.GREEN+"User created successfully."+colors.RESET)
        else:
            print(colors.BLUE+ monitoring_username + " User already exists."+colors.RESET)
        cmd=f"GRANT SELECT ON mysql.* TO '{monitoring_username}'@'{hostname}'"
        cursor.execute(cmd)
        cmd=f"GRANT SUPER ON *.* TO '{monitoring_username}'@'{hostname}'"
        cursor.execute(cmd)
        cmd=f"FLUSH PRIVILEGES"
        cursor.execute(cmd)
        cmd=f"use mysql"
        cursor.execute(cmd)
        cmd=f"UPDATE mysql.user SET Super_Priv='Y' WHERE user= '{monitoring_username}' AND host='{hostname}'"
        cursor.execute(cmd)
        cmd=f"FLUSH PRIVILEGES"
        cursor.execute(cmd)
        print(colors.GREEN+"User privileges granted successfully."+colors.RESET)
    except Exception as e:
        print(colors.RED+str(e)+colors.RESET)

    shutil.copyfile("pymysql.zip",plugins_temp_path+"mysql_monitoring/pymysql.zip")
    
    shutil.unpack_archive('pymysql.zip', plugins_temp_path+"mysql_monitoring/")

    # Remove the original pymysql.zip file
    os.remove(plugins_temp_path+"mysql_monitoring/pymysql.zip")
    print("")

    # Updating pyhton path
    print(colors.BLUE+"   Installation in progress."+colors.RESET)
    cmd="which python3"
    output=subprocess.check_output(cmd, shell=True, text=True)
    file_path=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.py"
    with open(file_path, 'r') as file:
        file_content = file.read()
    updated_content = file_content.replace("#!/usr/bin/python", "#!"+output)
    with open(file_path, 'w') as file:
        file.write(updated_content)

    #print(colors.GREEN+'The Python path is updated successfully.'+colors.RESET)

    # Validating the plugin output
    print(colors.BLUE+" Validating the plugin."+colors.RESET)
    cmd=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.py --username={monitoring_username} --password={monitoring_password} --host={hostname} --port={port}"

    result=execute_command(cmd, need_out=True)
    if not plugin_validator(result):
        print("")
        print(colors.RED+"Validation failed. Plugin not installed. Process exited."+colors.RESET)
        return
    print(colors.GREEN+"Plugin output validated successfully."+colors.RESET)
    print("")


    # Setting the plugin config file
    print(colors.BLUE+" Adding the configurations in the .cfg file."+colors.RESET)
    arguments=f"--username={monitoring_username} --password={monitoring_password} --host={hostname} --port={port}"
    if not plugin_config_setter(plugin_name, plugins_temp_path, arguments,hostname):
        print("")
        print(colors.RED+"Error occurred. Process exited."+colors.RESET)
        return 
    print(colors.GREEN+"Configurations added successfully."+colors.RESET)
    print()
    

    # Moving the plugin files into the Agent Directory
    print(colors.BLUE+" Installation in progress."+colors.RESET)
    if not move_plugin(plugin_name, plugins_temp_path, agent_plugin_path):
        print("")
        print(colors.RED+"Error occurred. Process exited."+colors.RESET)
        return 
    


if __name__ == "__main__":
    plugin_name="mysql_monitoring"
    plugin_url="https://raw.githubusercontent.com/site24x7/plugins/master/mysql_monitoring/"


    initiate(plugin_name, plugin_url)
