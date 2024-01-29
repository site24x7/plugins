#!/usr/bin/python3

import warnings
import os
warnings.filterwarnings("ignore", module="oracledb")
import oracledb


def setenv(args):

    sysusername = args.sysusername
    syspassword = args.syspassword
    username = args.username
    password = args.password
    sid = args.sid
    hostname = args.hostname
    port = args.port
    tls = args.tls.lower()
    wallet_location = args.wallet_location

    try:
        oracledb.init_oracle_client()
    except Exception as e:
        print(str(e))

    try:
        try:
            if tls=="true":
                    dsn=f"""(DESCRIPTION=
                            (ADDRESS=(PROTOCOL=tcps)(HOST={hostname})(PORT={port}))
                            (CONNECT_DATA=(SERVICE_NAME={sid}))
                            (SECURITY=(MY_WALLET_DIRECTORY={wallet_location}))
                            )"""
            else:
                dsn=f"{hostname}:{port}/{sid}"
            conn = oracledb.connect(user=sysusername, password=syspassword, dsn=dsn)
            c = conn.cursor()

        except Exception as e:
            print(str(e))
            return

        alter_session="""alter session set "_ORACLE_SCRIPT"=true"""
        create_query = f"CREATE USER {username} identified by {password}"
        query1 = f"GRANT SELECT_CATALOG_ROLE TO {username}"
        query2 = f"GRANT CREATE SESSION TO {username}"

        c.execute(alter_session)
        c.execute(create_query)
        print(f"Created New User {username}")

        conn.close()

        try:
            conn = oracledb.connect(user=sysusername, password=syspassword, dsn=dsn)
            c = conn.cursor()
        except Exception as e:
            print(str(e))
            return

        c.execute(query1)
        c.execute(query2)
        print(f"Permission Granted to User: {username}")
        conn.close()

    except Exception as e:
        print(str(e))


if __name__ == "__main__":

    sysusername = "sys_user"
    syspassword = "sys_password"
    username = "new_username"
    password = "new_password"
    sid = "ORCLCDB"
    hostname = "localhost"
    port = 2484
    tls="true"
    wallet_location = "/opt/oracle/product/19c/dbhome_1/wallet"
    oracle_home="/opt/oracle/product/19c/dbhome_1/"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--sysusername', help='hostname for oracle',default=sysusername)
    parser.add_argument('--syspassword', help='hostname for oracle',default=syspassword)
    parser.add_argument('--username', help='username for oracle',default=username)
    parser.add_argument('--password', help='password for oracle',default=password)
    parser.add_argument('--sid', help='sid for oracle',default=sid)
    parser.add_argument('--hostname', help='hostname for oracle',default=hostname)
    parser.add_argument('--port', help='port number for oracle',default=port)
    parser.add_argument('--tls', help='tls support for oracle',default=tls)
    parser.add_argument('--wallet_location', help='oracle wallet location',default=wallet_location)
    parser.add_argument('--oracle_home', help='oracle wallet location',default=oracle_home)

    args=parser.parse_args()
    os.environ['ORACLE_HOME']=args.oracle_home

    setenv(args)
