
import configparser
import os

def setenv(args):

    sysusername=args['sysusername']
    syspassword=args['syspassword']
    username=args['username']
    sid=args['sid']
    hostname=args['hostname']
    port=args['port']

    try:
        import cx_Oracle
    except Exception as e:
        print(str(e))

    try:
        try:
            conn = cx_Oracle.connect(sysusername,syspassword,hostname+':'+str(port)+'/'+sid)
            c = conn.cursor()
        except Exception as e:
            print(str(e))
            return
        
        query1=f"grant select_catalog_role to {username}"
        query2=f"grant create session to {username}"

        c.execute(query1)
        c.execute(query2)
        print(f"Permission Granted to User : {username}")

   
    except Exception as e:
        print(str(e))


def getdata():
    config = configparser.ConfigParser()
    file_name=os.getcwd().split('/')[-1]+".cfg"
    config.read(file_name)
    sections = config.sections()

    sysusername=input("Enter sysdba username : ")
    syspassword=input('Enter sysdba password : ')



    for section in sections:
        hostname=config[section]['hostname']
        sid=config[section]['sid']
        username=config[section]['username']
        port=config[section]['port']

        args={
            "hostname":hostname,
            "sid":sid,
            "username":username,
            "port":port,
            "sysusername":sysusername,
            "syspassword":syspassword

        }
        setenv(args)




if __name__ =="__main__":
    getdata()


