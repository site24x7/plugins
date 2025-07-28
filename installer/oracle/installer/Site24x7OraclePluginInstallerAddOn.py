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

def check_user(user, c):
    try:
        query=f"SELECT * FROM dba_users WHERE username = \'{user.upper()}\'"
        cursor=execute_query(query, c, result=True)
        rows=cursor.fetchall()
        return len(rows)==1
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False


def close_cursor(c):
    try:
        c.close()
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True

def connect_cursor(args):
    try:
        import oracledb
        conn = oracledb.connect(user=args["sysusername"], password=args["syspassword"], dsn=args["dsn"])
        c = conn.cursor()
        return c
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False

def execute_query(query, c, result=False):
    try:
        c.execute(query)
        if result:
            return c
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True

def setuser(args, c):
    try:


        #alter_session="""alter session set "_ORACLE_SCRIPT"=true"""
        create_query = f"CREATE USER {args['username']} identified by {args['password']}"
        query1 = f"GRANT SELECT_CATALOG_ROLE TO {args['username']}"
        query2 = f"GRANT CREATE SESSION TO {args['username']}"

        #if not execute_query(alter_session, c): return False

        if check_user(args["username"], c):
            print()
            print(f"    The {args['username']} already exists in the Oracle instance.")
            if not execute_query(query1, c): return False 
            if not execute_query(query2, c): return False 
            if not close_cursor(c): return False
            return True
        
        if not execute_query(create_query, c):return False

        if not close_cursor(c): return False
        
        c = connect_cursor(args)
        if not c:
            return False

        if not execute_query(query1, c): return False 
        if not execute_query(query2, c): return False 
        
        if not close_cursor(c): return False

        return True


    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False


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
                    option = input(f"\n    Enter the {msg} of the Oracle instance : ")
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
    print(colors.BLUE +"""    Hostname/IP Address, port, and SID of the Oracle instance is required to get metrics. These details will be configured in the plugin configuration file.
          """+ colors.RESET)
    hostname=input_validate("hostname", default="localhost")
    if not hostname:
        print()
        print(colors.RED + "------------------------------ Error occured. Hostname is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    port=input_validate("port", default="1521")
    if not port:
        print()
        print(colors.RED + "------------------------------ Error occured. Port is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    sid=input_validate("SID")
    if not sid:
        print()
        print(colors.RED + "------------------------------ Error occured. SID is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    oracle_home=input_validate("Oracle Home path")
    if not oracle_home:
        print()
        print(colors.RED + "------------------------------ Error occured. Oracle Home Path is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    os.environ['ORACLE_HOME']=oracle_home

    print()
    custom_msgs="    Do you have TLS enabled in the Oracle instance? (y/n) :"
    tls=input_validate("TLS Option", default="False", custom_msg=custom_msgs)
    if not tls:
        print(colors.RED + "------------------------------ Error occured. TLS preference is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    if tls.lower()=="y":
        tls="true"
        wallet_location=input_validate("Wallet location")
        if not wallet_location:
         print(colors.RED + "------------------------------ Error occured. Wallet location is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
         return
    else:
        tls="false"
        wallet_location=None

    
    print(colors.GREEN +"    Hostname, Port, SID, Oracle Home path, and TLS preference received."+ colors.RESET)
    print()

    print(colors.BLUE +"""    A new monitoring user with SELECT_CATALOG_ROLE and CREATE SESSION privileges is required to monitor Oracle.\n    Provide the admin username (DBA Role) and password of the Oracle to proceed with creating a monitoring user.\n    Note: The admin username and password you provide will not be stored in any of the Site24x7 databases."""+ colors.RESET)
    
    sysusername=input_validate("admin username (DBA Role)")
    if not sysusername:
        print()
        print(colors.RED + "------------------------------ Error occured. Admin username is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    syspassword=input_validate("admin password")
    if not syspassword:
        print()
        print(colors.RED + "------------------------------ Error occured. Admin password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return
    
    dsn=f"{hostname}:{port}/{sid}"
    if tls=="true":
        dsn=f"""(DESCRIPTION=
                (ADDRESS=(PROTOCOL=tcps)(HOST={hostname})(PORT={port}))
                (CONNECT_DATA=(SERVICE_NAME={sid}))
                (SECURITY=(MY_WALLET_DIRECTORY={wallet_location}))
                )"""  
    args={"hostname":hostname, "port":port, "sid": sid, "oracle_home":oracle_home, "tls":tls, "sysusername":sysusername, "syspassword":syspassword, "dsn":dsn, "wallet_location":wallet_location}
    
    c = connect_cursor(args)
    if not c:
        print("    Connection not estabilished to the Oracle instance. Check the previous inputs.")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------"+ colors.RESET)
        return
    print(colors.GREEN + "    Connection to the Oracle instance established successfully."+ colors.RESET)

    print()
    print(colors.BLUE +"""    A new monitoring user with SELECT_CATALOG_ROLE and CREATE SESSION privileges is required to monitor Oracle.\n    Provide the admin username (DBA Role) and password of the Oracle to proceed with creating a monitoring user.\n    Note: The admin username and password you provide will not be stored in any of the Site24x7 databases."""+ colors.RESET)

    print("")
    print("    Select \"y\" to proceed with default username \"site24x7\". Select \"n\" to create a new username. ")
    user_option=input("    Do you want to proceed with default username \"site24x7\"? (y/n)")    
    if user_option=="Y" or user_option =="y":
        username="site24x7"
    elif user_option=="N" or user_option=="n":
        username=input("    Enter the username to be created with \"SELECT_CATALOG_ROLE and CREATE SESSION\" privileges: ")
        if not username:
                username=input("    Enter the username to be created with \"SELECT_CATALOG_ROLE and CREATE SESSION\" privileges: ")
                if not username:
                    print(colors.RED + "------------------------------ Error occured. A monitoring user is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
                    return
    else:
        return

    args['username']=username

    if check_user(username,c):
        print(f"    The user {username} already exists in the Oracle instance.")
        password=input_validate(msg=None,custom_msg=f"    Enter the existing password for the user {username}: ")
        if not password:
            print(colors.RED + "------------------------------ Error occured. The monitoring user password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
            return
        args['password']=password

    else:
        password=input_validate(msg=None,custom_msg=f"    Enter a new password for the user {username} : ")
        print(password)
        if not password:
            print(colors.RED + "------------------------------ Error occured. A monitoring user password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
            return
        args['password']=password
        if not setuser(args,c):
            print(colors.RED + "------------------------------ Error occured. Process exited.  ------------------------------" + colors.RESET)
            return

    
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
    print("    Downloading the Oracle plugin files from Site24x7's GitHub repository.")

    if not down_move(plugin_name, plugin_url, plugins_temp_path):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 
    print(colors.GREEN +"    Downloaded the Oracle plugin files successfully."+ colors.RESET)
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


    arguments=f"""--username={args["username"]} --password={args["password"]} --hostname={args["hostname"]} --sid={args["sid"]} --port={args["port"]} --tls={args["tls"]} --wallet_location={args["wallet_location"]} --oracle_home={args["oracle_home"]}"""
    cmd=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.py"+ " "+arguments
    result=execute_command(cmd, need_out=True)
    if not plugin_validator(result):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return
    print("")

    print("    Adding the plugin configurations in the oracle.cfg file.")
    if not plugin_config_setter(plugin_name, plugins_temp_path, arguments, display_name=args["sid"]):
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
    plugin_name="oracle"
    plugin_url="https://raw.githubusercontent.com/site24x7/plugins/master/oracle"
    initiate(plugin_name, plugin_url)
