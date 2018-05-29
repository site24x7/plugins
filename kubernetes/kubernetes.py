#!/usr/bin/python

'''
Created on 28-May-2018
@author: giri
'''
import six.moves.urllib.request as urllib
import traceback
import json
import sys

PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"


result_json = {}
result_json["plugin_version"] = PLUGIN_VERSION
result_json["heartbeat_required"] = HEARTBEAT
result_json["status"] = 1

KUBERNETES_HOST = "127.0.0.1" #KUBERNETES API SERVER HOST
KUBERNETES_PORT = "8001" #KUBERNETES API SERVER PORT

KUBERNETES_RBAC = 0

KUBERNETES_ROOT_URL = 'http://{}:{}/api'.format(KUBERNETES_HOST, KUBERNETES_PORT)

KUBERNETES_ROOL_URLS = 'http://{}:{}/apis'.format(KUBERNETES_HOST, KUBERNETES_PORT)

pods_url = lambda : KUBERNETES_ROOT_URL+"/v1/pods"
namespace_url = lambda : KUBERNETES_ROOT_URL+"/v1/namespaces"
deployment_url = lambda :  KUBERNETES_ROOL_URLS+"/apps/v1/deployments"


def default_result_handler():
	result_json = {}
	result_json["plugin_version"] = PLUGIN_VERSION
	result_json["heartbeat_required"] = HEARTBEAT
	return result_json

def log_helper(func):
	def wrapper(*args, **kwargs):
		try:
			return func(*args)
		except Exception as e:
			result_json = default_result_handler()
			result_json["msg"] = repr(e)
			result_json["status"] = 0
			print(json.dumps(result_json))
			sys.exit(1)
	return wrapper

@log_helper
def handle_api_call(func):
	req = urllib.Request(func())
	res = urllib.urlopen(req)
	result = json.loads(res.read().decode())
	res.close()
	return result

@log_helper
def collect_pods_metrics():
	result = handle_api_call(pods_url)
	result_json["total_pods"] = len(result.get("items", []))
	items = result.get("items", [])
	for each_item in items:
		namespace = each_item.get("metadata", {}).get("namespace", None)
		status = each_item.get("status", {}).get("phase", None)
		if namespace and status:
			cons_string = "{}_pods_{}".format(namespace, status)
			result_json[cons_string] = result_json[cons_string]+1 if cons_string in result_json else 1


@log_helper
def collect_deployments_metrics():
	result = handle_api_call(deployment_url)
	result_json["total_deployments"] = len(result.get("items", []))
	items = result.get("items", [])
	for each_item in items:
		namespace = each_item.get("metadata", {}).get("namespace", None)
		desired_replicas = each_item.get("status", {}).get("replicas", None)
		available_replicas = each_item.get("status", {}).get("availableReplicas", None)
		if namespace and desired_replicas:
			cons_string = "{}_replicas_{}".format("desired", namespace)
			result_json[cons_string] = result_json[cons_string]+int(desired_replicas) if cons_string in result_json else int(desired_replicas)
			if namespace and available_replicas:
				cons_string = "{}_replicas_{}".format("unavailable", namespace)
				result_json[cons_string] = result_json[cons_string]+int(desired_replicas)-int(available_replicas) if cons_string in result_json else \
												int(desired_replicas)-int(available_replicas)



@log_helper
def handle_kube_metrics_collection():
	collect_pods_metrics()
	collect_deployments_metrics()
	print(json.dumps(result_json))




handle_kube_metrics_collection()