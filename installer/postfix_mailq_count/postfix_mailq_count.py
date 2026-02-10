

import subprocess
import json

HEARTBEAT = "true"

PLUGIN_VERSION = "1"

def get_data():
	data = {}
	data["plugin_version"]=PLUGIN_VERSION
	data['heartbeat_required']=HEARTBEAT
	try:
		cmd = 'mailq | grep -c "^[A-F0-9]"'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		(output, err) = p.communicate()
		p_status = p.wait()
		error=err.decode('utf-8')
		
		if p_status not in [0, 1]:
			raise Exception("Command failed with exit code {}: {}".format(p_status,error))
		
		data['Total Messages in Queue'] = int(output)
		
		cmd = 'mailq | grep "^[A-F0-9]" | awk \'{sum+=$2} END {print sum}\''
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		(output, err) = p.communicate()
		p_status = p.wait()
		if p_status == 0 and output.strip():
			total_bytes = int(output.strip())
			data['Total Message Size'] = round(total_bytes / 1024, 2)
		else:
			data['Total Message Size'] = 0.0
		
		qshape_metrics={"deferred":"Messages in Deferred Queue","active":"Messages in Active Queue","hold":"Messages in Hold Queue","incoming":"Messages in Incoming Queue","bounce":"Messages in Bounce Queue","corrupt":"Messages in Corrupt Queue","maildrop":"Messages in Maildrop Queue"}
		
		for i in qshape_metrics:
			cmd='qshape '+i+' | head'
			p=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE)
			(output,err)=p.communicate()
			p_status=p.wait()
			error=err.decode('utf-8')
			if p_status != 0:
				data[qshape_metrics[i]] = 0
				continue
			
			if not error:
				output_original=output.strip().decode("utf-8")
				output=output_original.split()
				if 'TOTAL' in output:
					index = output.index('TOTAL') + 1
					data[qshape_metrics[i]] = int(output[index])
				else:
					data["status"]=0
					data["msg"]="qshape command output does not contain TOTAL"+output_original
			else:
				data["status"]=0
				data["msg"]=error
		
		cmd = 'postconf -h queue_directory'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		(output, err) = p.communicate()
		p_status = p.wait()
		if p_status == 0:
			queue_dir = output.strip().decode('utf-8')
			cmd = 'du -sb ' + queue_dir + ' | awk \'{print $1}\''
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
			(output, err) = p.communicate()
			p_status = p.wait()
			if p_status == 0:
				bytes_size = int(output.strip())
				data['Total Queue Size'] = round(bytes_size / (1024 * 1024), 2)
			else:
				data['Total Queue Size'] = 0.0
		else:
			data['Total Queue Size'] = 0.0
		
		cmd = 'ps aux | grep postfix | grep -v grep | grep -v "python.*postfix_mailq" | awk \'{cpu+=$3; mem+=$4} END {print cpu, mem}\''
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		(output, err) = p.communicate()
		p_status = p.wait()
		if p_status == 0 and output.strip():
			usage = output.strip().decode('utf-8').split()
			if len(usage) == 2:
				data['Postfix CPU Usage'] = float(usage[0])
				data['Postfix Memory Usage'] = float(usage[1])
			else:
				data['Postfix CPU Usage'] = 0.0
				data['Postfix Memory Usage'] = 0.0
		else:
			data['Postfix CPU Usage'] = 0.0
			data['Postfix Memory Usage'] = 0.0
		
		cmd = 'ps aux | grep -E \'/postfix/|^postfix\' | grep -v grep | wc -l'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		(output, err) = p.communicate()
		p_status = p.wait()
		if p_status == 0:
			data['Postfix Process Count'] = int(output.strip())
		else:
			data['Postfix Process Count'] = 0
		
		if data['Total Messages in Queue'] > 0:
			data['Average Message Size in Queue'] = round(data['Total Message Size'] / data['Total Messages in Queue'], 2)
		else:
			data['Average Message Size in Queue'] = 0.0
			
	except Exception as e:
		data["status"]=0
		if output:
			data["msg"]=str(e)+output.decode("utf-8")
		else:
			data["msg"]=str(e)
	
	data["units"] = {
		"Total Queue Size": "MB",
		"Total Message Size": "KB",
		"Average Message Size in Queue": "KB",
		"Postfix CPU Usage": "%",
		"Postfix Memory Usage": "%"
	}
	return data
    
def run(param=None):
    return get_data()
    
if __name__ == '__main__':
	data=get_data()
	print(json.dumps(data, indent=2, sort_keys=False))
