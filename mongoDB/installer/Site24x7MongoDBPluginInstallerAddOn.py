#! /usr/bin/python3
import os
import subprocess
import json
import warnings
import urllib.parse
import urllib.request
import shutil

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
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False

def delete_folder(folder_name):
    try:
        shutil.rmtree(folder_name)
        return True
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False

def move_folder(source, destination):
    try:
        os.rename(source, destination)
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False
    return True

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
            print(f"    The plugin  \"{plugin_name}\" is already present in the agent directory.")
            move_option=input(f"    Do you want to reinstall the \"{plugin_name}\" plugin? \n    Select \"y\" to reinstall. Select \"n\" to add another Oracle instance for monitoring in the same plugin configuration file. (y/n)")
            if move_option=="n":
                multi_option=input(f"    Do you want to proceed with adding another MongoDB instance for monitoring in the same plugin configuration file? (y/n)")
                if multi_option=="y":
                    if not multi_config(plugins_temp_path+plugin_name+"/"+plugin_name+".cfg",plugin_dir+plugin_name+".cfg"):
                        return False
                else:
                    print("    Plugin not configured")
                    return False

            else:
                if not delete_folder(plugin_dir):
                    return False
                if not move_folder(plugins_temp_path+plugin_name, plugin_dir): 
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


def grant_previlege(args, db):
    try:
        roles = ["clusterMonitor"]  # Adjust roles as needed
        db.command("grantRolesToUser", args["username"], roles=roles)        
        return True
    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False


def create_user(args, db):
    try:
        roles = [
            {
                "role": "clusterMonitor",
                "db": "admin" 
            }
        ]
        db.command("createUser", args["username"], pwd=args["password"], roles=roles)
        return True

    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False

def check_user(db, args):     
    mongo_users = db.system.users.find()
    for mongo_user in mongo_users:
        if mongo_user['user']==args["username"]:
            return True
    return False

def mongod_server(args):
        
        try:
            if(args["admin_username"]!="None" and args["admin_password"]!="None" and args["authdb"]!="None"):
                mongod_server = "{0}:{1}@{2}:{3}/{4}".format(args["admin_username"],urllib.parse.quote(args["admin_password"]), args["host"], args["port"], args["authdb"])
            elif(args["admin_username"]!="None" and args["admin_password"]!="None"):
                mongod_server = "{0}:{1}@{2}:{3}".format(args["admin_username"], args["admin_password"], args["host"], args["port"])
            elif(args.authdb!="None"):
                mongod_server = "{0}:{1}/{2}".format(args["host"], args["port"], args["authdb"])
            else:
                mongod_server = "{0}:{1}".format(args["host"], args["port"])
            return mongod_server
        
        except Exception as e:
            print(colors.RED +"    "+str(e)+colors.RESET)
            return False


def mongo_connect(args):
    try:
        plugin_script_path=os.path.dirname(os.path.realpath(__file__))
        try:
            import pymongo
            pymongo_installed=True

        except ImportError:
            pymongo_installed=False

        if not pymongo_installed:
            import zipimport
            importer=zipimport.zipimporter(f"{plugin_script_path}/pymongo.pyz")
            bson=importer.load_module("bson")
            pymongo=importer.load_module("pymongo")


        mongod_server_string=mongod_server(args)
        mongo_uri = 'mongodb://' + mongod_server_string
        if args["tls"]:
            connection = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=10000,tls=args["tls"],tlscertificatekeyfile=args["tlscertificatekeyfile"],tlscertificatekeyfilepassword=args["tlscertificatekeyfilepassword"],tlsallowinvalidcertificates=args["tlsallowinvalidcertificates"])
        else:
            connection = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
        connection.list_database_names()
        return connection

    except Exception as e:
        print(colors.RED +"    "+str(e)+colors.RESET)
        return False

def input_validate(msg, default=None, custom_msg=None):

    input_check=False
    while not input_check:
        if custom_msg:
                    option = input(f"{custom_msg}")
        else:
                    option = input(f"\n    Enter the {msg} of the MongoDB instance : ")
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
    print(colors.BLUE +"""    Hostname/IP Address, port, database, authentication database of the mongoDB instance is required to get metrics. These details will be configured in the plugin configuration file.
          """+ colors.RESET)
    

    parameter="hostname"
    host=input_validate(parameter, default="localhost")
    if not host:
        print()
        print(colors.RED + "------------------------------ Error occured. Hostname is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return

    parameter="port"
    port=input_validate(parameter, default="27017")
    if not port:
        print()
        print(colors.RED + "------------------------------ Error occured. Port is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return


    parameter="database"
    dbname=input_validate(parameter, default="admin")
    if not port:
        print()
        print(colors.RED + "------------------------------ Error occured. Database is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return

    parameter="authentication database"
    authdb=input_validate(parameter, default="admin")
    if not port:
        print()
        print(colors.RED + "------------------------------ Error occured. AuthDB is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return

    print(colors.BLUE +"""    A new monitoring user with \"clusterMonitor\" privileges is required to monitor MongoDB.\n    Provide the admin username and password of the MongoDB to proceed with creating a monitoring user.\n    Note: The admin username and password you provide will not be stored in any of the Site24x7 databases."""+ colors.RESET)

    admin_username=input_validate("admin username")
    if not admin_username:
        print()
        print(colors.RED + "------------------------------ Error occured. Admin username is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return

    admin_password=input_validate("admin password")
    if not admin_password:
        print()
        print(colors.RED + "------------------------------ Error occured. Admin password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        return

    print()
    custom_msgs="    Do you have TLS enabled in the MongoDB instance? (y/n) :"
    tls=input_validate("TLS Option", default="False", custom_msg=custom_msgs)
    if not tls:
        print(colors.RED + "------------------------------ Error occured. TLS preference is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
        exit()
    if tls.lower()=="y":
        tls=True

        tlscertificatekeyfile=input_validate("TLS certificate key file location")
        if not tlscertificatekeyfile:
          print(colors.RED + "------------------------------ Error occured. TLS certificate key location is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
          return
        args["tlscertificatekeyfile"]=tlscertificatekeyfile

        tlscertificatekeyfilepassword=input_validate("TLS certificate key file password")
        if not tlscertificatekeyfilepassword:
          print(colors.RED + "------------------------------ Error occured. TLS certificate key file password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
          return
        args["tlscertificatekeyfilepassword"]=tlscertificatekeyfilepassword

        custom_msgs="    Do you want to allow invalid certificates in the MongoDB instance? (y/n) :"
        tlsallowinvalidcertificates=input_validate("TLS allow invalid certificates", default="\'n\'", custom_msg=custom_msgs)
        if not tlsallowinvalidcertificates:
          print(colors.RED + "------------------------------ Error occured. TLS invalid certificates preference is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
          return         
        if tlsallowinvalidcertificates.lower()=="y":
            tlsallowinvalidcertificates=True
        else:
            tlsallowinvalidcertificates=False
    
        args['tlsallowinvalidcertificates']=tlsallowinvalidcertificates
    else:
        tls=False
        tlscertificatekeyfile=None
        tlscertificatekeyfilepassword=None
        tlsallowinvalidcertificates=None


    args={"host":host,"port":port,"dbname":dbname,"authdb":authdb,"admin_username":admin_username,"admin_password":admin_password, "tls":tls, "tlscertificatekeyfile":tlscertificatekeyfile, "tlscertificatekeyfilepassword":tlscertificatekeyfilepassword, "tlsallowinvalidcertificates":tlsallowinvalidcertificates}


    
    connection=mongo_connect(args)
    if not connection:
        print("    Connection not estabilished to the MongoDB instance. Check the previous inputs.")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------"+ colors.RESET)
        return

    print("    Connection estabilished to the MongoDB instance.")

    print()
    print(colors.BLUE + """    A user with default username "site24x7" will be created with \"clusterMonitor\" privileges.\n    Note: The created user credentials you provide will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases.
          """+ colors.RESET)

    print("    Select \"y\" to proceed with default username \"site24x7\". Select \"n\" to create a new username. ")
    user_option=input("    Do you want to proceed with default username \"site24x7\"? (y/n)")    
    if user_option=="Y" or user_option =="y":
        username="site24x7"
    elif user_option=="N" or user_option=="n":
        username=input("    Enter the username to be created with \"clusterMonitor\" privileges: ")
        if not username:
                username=input("    Enter the username to be created with \"clusterMonitor\" privileges: ")
                if not username:
                    print(colors.RED + "------------------------------ Error occured. A monitoring user is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
                    return
    else:
        return

    args['username']=username

    try:
        db=connection[dbname]
    except Exception as e:
        print(str(e))
        print(colors.RED + "------------------------------ Error occured. Process exited.  ------------------------------" + colors.RESET)
        return 

    if check_user(db, args):
        print(f"    The user {username} already exists in the MongoDB instance.")
        password=input_validate(msg=None,custom_msg=f"    Enter the existing password for the user {username}: ")
        if not password:
            print(colors.RED + "------------------------------ Error occured. The monitoring user password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
            return

        if not grant_previlege(args, db):
             return False
        args["password"]=password
    else:
        password=input_validate(msg=None,custom_msg=f"    Enter a new password for the user {username} : ")
        if not password:
            print(colors.RED + "------------------------------ Error occured. A monitoring user password is required to install the plugin. Process exited.  ------------------------------" + colors.RESET)
            return      
        args['password']=password
        if not create_user(args,db):
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
    print("    Downloading the MongoDB plugin files from Site24x7's GitHub repository.")

    if not down_move(plugin_name, plugin_url, plugins_temp_path):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 
    print(colors.GREEN +"    Downloaded the MongoDB plugin files successfully."+ colors.RESET)
    print()

    pyz_url="https://github.com/site24x7/plugins/raw/suraj/mongoDB/pymongo.pyz"
    if not download_file(url=pyz_url, path=plugins_temp_path+"mongoDB/"):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return 


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

    arguments=f"""--username={args["username"]} --password={args["password"]} --host={args["host"]} --port={args["port"]} --dbname={args["dbname"]} --authdb={args["authdb"]}"""
    cmd=f"{plugins_temp_path}/{plugin_name}/{plugin_name}.py"+ " "+arguments
    result=execute_command(cmd, need_out=True)
    if not plugin_validator(result):
        print("")
        print(colors.RED + "------------------------------ Error occured. Process exited. ------------------------------" + colors.RESET)
        return
    print("")

    print("    Adding the plugin configurations in the mongoDB.cfg file.")
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
    plugin_name="mongoDB"
    plugin_url="https://raw.githubusercontent.com/site24x7/plugins/suraj/mongoDB"
    initiate(plugin_name, plugin_url)
