
import json
import subprocess

PLUGIN_VERSION = "1"
HEARTBEAT = "true"
error_msg = ""

def convert_elapsed_time(elapsed_str):
    global error_msg
    try:
        if not elapsed_str or elapsed_str == "-":
            return "-"
        
        if "-" in elapsed_str:
            parts = elapsed_str.split("-")
            days = int(parts[0])
            time_part = parts[1]
        else:
            days = 0
            time_part = elapsed_str
        
        time_components = time_part.split(":")
        
        if len(time_components) == 3: 
            hours, minutes, seconds = map(int, time_components)
        elif len(time_components) == 2: 
            hours = 0
            minutes, seconds = map(int, time_components)
        else:
            return "-"
        
        result_parts = []
        if days > 0:
            result_parts.append("{} day{}".format(days, "s" if days != 1 else ""))
        if hours > 0:
            result_parts.append("{} hr{}".format(hours, "s" if hours != 1 else ""))
        if minutes > 0:
            result_parts.append("{} min".format(minutes))
        if seconds > 0:
            result_parts.append("{} sec".format(seconds))
        
        if not result_parts:
            return "0 sec"
        
        return ", ".join(result_parts)
        
    except Exception as e:
        if error_msg:
            error_msg += "; "
        error_msg += "Error converting elapsed time '{}': {}".format(elapsed_str, str(e))
        return "-"

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
                "Elapsed": convert_elapsed_time(etime) if etime else "-",
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
            
            longest_elapsed = "-"
            try:
                ps_output = run_command("ps -eo pid,etime | grep -E '^\\s*({})\\s+' | head -1".format('|'.join([z['PID'] for z in zombies if str(z['PID']).isdigit()])))
                if ps_output:
                    original_elapsed = ps_output.split()[1] if len(ps_output.split()) > 1 else "-"
                    longest_elapsed = convert_elapsed_time(original_elapsed)
                else:
                    longest_elapsed = zombies[0]['Elapsed']
            except:
                longest_elapsed = zombies[0]['Elapsed'] if zombies else "-"
            
            data['Longest Running Zombie (Elapsed)'] = longest_elapsed
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
