import GPUtil
import json

PLUGIN_VERSION = "1"
HEARTBEAT_REQUIRED = "true"

result_json = {}
metric_units = {}

def metric_collector():
    try:
        gpus = GPUtil.getGPUs()
        i = 1
        for gpu in gpus: 
            result_json[gpu.name +"_" +  str(i) + "_memory_utilzation"] = round((gpu.memoryUtil)*100, 2)
            result_json[gpu.name + "_" +  str(i) + "_used_memory"] = gpu.memoryUsed
            result_json[gpu.name + "_" +  str(i) + "_temperature"] = gpu.temperature

            metric_units[gpu.name + "_" +  str(i) + "_memory_utilzation"] = "%"
            metric_units[gpu.name + "_" +  str(i) + "_used_memory"] = "MB"
            metric_units[gpu.name + "_" +  str(i) + "_temperature"] = "Celsius"
            i+= 1

        result_json["plugin_version"] = PLUGIN_VERSION
        result_json["units"]=metric_units

    except Exception as e:
        result_json["msg"]=str(e)
        result_json["status"]=0

    result_json["heartbeat_required"] = HEARTBEAT_REQUIRED
    

if __name__ == '__main__':
    metric_collector()
    print(json.dumps(result_json, indent=4, sort_keys=True))
