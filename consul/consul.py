#!/usr/bin/python3
import json
import requests

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class emqx:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.host=args.host
        self.port=args.port

    
    def metriccollector(self):
        


        # Construct the API request URL
        url = f"http://{self.host}:{self.port}/v1/agent/metrics"



        response = requests.get(url)
        raw_metric_data=response.json()
        gauge_metrics=[ "consul.autopilot.failure_tolerance",
                        "consul.autopilot.healthy",
                        "consul.raft.applied_index",
                        "consul.raft.commitNumLogs",
                        "consul.raft.last_index",
                        "consul.raft.leader.dispatchNumLogs",
                        "consul.runtime.alloc_bytes",
                        "consul.runtime.free_count",
                        "consul.runtime.heap_objects",
                        "consul.runtime.malloc_count",
                        "consul.runtime.num_goroutines"
                        "consul.runtime.sys_bytes",
                        "consul.runtime.total_gc_pause_ns",
                        "consul.runtime.total_gc_runs",
                        "consul.session_ttl.active" ]


        counter_metrics=[
                        "consul.client.rpc",
                        "consul.raft.apply",
                        "consul.raft.barrier",
                        "consul.rpc.query",
                        "consul.rpc.request"]
        
        sample_metrics=[

                        "consul.acl.ResolveToken",
                        "consul.http.GET.v1.agent.metrics",
                        "consul.leader.barrier",
                        "consul.leader.reconcile",
                        "consul.leader.reconcileMember",
                        "consul.memberlist.gossip",
                        "consul.raft.commitTime",
                        "consul.raft.fsm.enqueue",
                        "consul.raft.leader.dispatchLog"
        ]


        raw_gauge_metrics=raw_metric_data["Gauges"]
        for metric in raw_gauge_metrics:
            for metric_name in gauge_metrics:
                if metric_name == metric["Name"]:
                    metric_name=metric_name.replace("."," ").title()
                    self.maindata[metric_name]=metric["Value"]

        raw_counter_metrics=raw_metric_data["Counters"]
        for metric in raw_counter_metrics:
            for metric_name in counter_metrics:
                if metric_name == metric["Name"]:
                    metric_name=metric_name.replace("."," ").title()
                    self.maindata[metric_name]=metric["Count"]

        raw_sample_metrics=raw_metric_data["Samples"]
        for metric in raw_sample_metrics:
            for metric_name in sample_metrics:
                if metric_name == metric["Name"]:
                    metric_name=metric_name.replace("."," ").title()
                    self.maindata[metric_name]=metric["Count"]

        return self.maindata




if __name__=="__main__":
    
    host="localhost"
    port=8500


    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host', help='emqx host',default=host)
    parser.add_argument('--port', help='emqx port',default=port)


    args=parser.parse_args()

    obj=emqx(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))