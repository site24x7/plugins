
import json
import subprocess

PLUGIN_VERSION = "1"
HEARTBEAT = "true"
error_msg = ""

def run_command(cmd):
    global error_msg
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8', errors='replace').strip()
    except Exception as e:
        if error_msg:
            error_msg += "; "
        error_msg += "Command '{}' failed: {}".format(cmd, str(e))
        return ""

def get_zombie_details():
    global error_msg
    zombies = []
    try:
        ps_output = run_command("ps -eo pid,ppid,user,etime,stat,comm,cmd | awk '$5 ~ /Z/'")
        if not ps_output:
            return zombies

        for line in ps_output.splitlines():
            parts = line.split(None, 6)
            if len(parts) < 7:
                continue

            pid, ppid, user, etime, stat, comm, cmd = parts
            parent_cmd = run_command("ps -p {} -o comm=".format(ppid))

            zombies.append({
                "PID": pid or -1,
                "PPID": ppid or -1,
                "User": user or "-",
                "Elapsed": etime or "-",
                "State": stat or "-",
                "name": comm or "-",                
                "Zombie_Command": cmd or "-",       
                "Parent_Command": parent_cmd.strip() if parent_cmd else "Unknown"
            })
    except Exception as e:
        if error_msg:
            error_msg += "; "
        error_msg += "Error getting zombie details: {}".format(e)
    return zombies

def metricCollector():
    global error_msg
    error_msg = "" 
    
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT

    data['zombies'] = -1
    data['Unique Users with Zombies'] = -1
    data['Unique Parent Commands'] = -1
    data['Longest Running Zombie (Elapsed)'] = "-"

    data['zombie_process_details'] = [{
        "PID": -1,
        "PPID": -1,
        "User": "-",
        "Elapsed": "-",
        "State": "-",
        "name": "-",
        "Zombie_Command": "-",
        "Parent_Command": "-"
    }]

    try:
        zombies = get_zombie_details()
        zombie_count = len(zombies)
        data['zombies'] = zombie_count

        if zombie_count > 0:
            users = [z['User'] for z in zombies]
            parent_cmds = [z['Parent_Command'] for z in zombies]
            data['Unique Users with Zombies'] = len(set(users))
            data['Unique Parent Commands'] = len(set(parent_cmds))
            data['Longest Running Zombie (Elapsed)'] = max([z['Elapsed'] for z in zombies])
            data['zombie_process_details'] = zombies

    except Exception as e:
        if error_msg:
            error_msg += "; "
        error_msg += str(e)

    if error_msg:
        data['msg'] = error_msg

    return data

def run(param=None):
    return metricCollector()

if __name__ == '__main__':
    print(json.dumps(metricCollector(), indent=4))
