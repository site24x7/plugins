#!/usr/bin/python3
import json



metrics=[

# Queue Manager Metrics
"Connection Count",
"Status"


# Queue Metrics
"Queue Name",
"Current Queue Depth",
"Handles Open : Input Count",
"Handles Open : Output Count",
"Last Msg get Date",
"Last Msg get Time",
"Last Msg put Date",
"Last Msg put Time",
"Oldest Msg Age",
"No. of Uncommitted Msgs",
"High Queue Depth",
"Msg Dequeue Count",
"Msg Enqueue Count"



# Channel Metrics
"Channel Name",
"Channel Connection Name",
"Channel Status",
"No. of MQI calls",
"Bytes Sent",
"Bytes Received",
"Buffers Sent",
"Buffers Received",
"Channel Substate"
"Channel Start Date",
"Channel Start Time"


]

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={'Channel_Metrics.Bytes Sent':'Bytes','Channel_Metrics.Bytes Received':'Bytes'}


class IbmMq:

        def __init__(self,args):
                self.maindata={}
                self.queue_manager=args.queue_manager_name
                self.channel=args.channel_name
                self.queue_name=args.queue_name
                self.host=args.host
                self.port=args.port
                self.logsenabled=args.logs_enabled
                self.logtypename=args.log_type_name
                self.logfilepath=args.log_file_path



                self.maindata['plugin_version'] = PLUGIN_VERSION
                self.maindata['heartbeat_required']=HEARTBEAT
                self.maindata['units']=METRICS_UNITS



                if args.username == "None":
                        self.username=None
                else:
                        self.username=args.username
                if args.password == "None":
                        self.password=None
                else:
                        self.username=args.username
              


                self.conn_info='%s(%s)' % (self.host, self.port)
                self.main()




        def main(self):
                try:
                        global pymqi
                        import pymqi
                        self.mqConnector()


                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        

        def metricCollector(self):

        
                self.queueCollector()
                self.channelCollector()
                self.QMgrCollector()

                applog={}
                if(self.logsenabled in ['True', 'true', '1']):
                        applog["logs_enabled"]=True
                        applog["log_type_name"]=self.logtypename
                        applog["log_file_path"]=self.logfilepath
                else:
                        applog["logs_enabled"]=False
                self.maindata['applog'] = applog



                return self.maindata



                


        def mqConnector(self):

                try:
                        self.qmgr = pymqi.connect(self.queue_manager, self.channel, self.conn_info,self.username,self.password)
                        self.pcf = pymqi.PCFExecute(self.qmgr)
                        self.metricCollector()
                        
                except Exception as e:
                        
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)



        def QMgrCollector(self):
                try:

                        Queue_manager_status=["","STARTING","RUNNING","QUIESCING","STANDBY"]
                        attr={
                                pymqi.CMQCFC.MQIACF_Q_MGR_STATUS_ATTRS:[
                                        pymqi.CMQCFC.MQIACF_CHINIT_STATUS,
                                        pymqi.CMQCFC.MQIACF_CMD_SERVER_STATUS,
                                        pymqi.CMQCFC.MQIACF_CONNECTION_COUNT,
                                        pymqi.CMQCFC.MQIACF_Q_MGR_STATUS
                                        

                                ]
                        }
                        qmgr_responses=self.pcf.CMQCFC.MQCMD_INQUIRE_Q_MGR_STATUS(attr)

                        for response in qmgr_responses:
                                Qmgr_name=response[pymqi.CMQC.MQCA_Q_MGR_NAME]

                                if Qmgr_name.decode('utf-8').strip() == self.queue_manager:
                                        self.maindata["QManager_metrics.Connection Count"]=response[pymqi.CMQCFC.MQIACF_CONNECTION_COUNT]
                                        self.maindata["QManager_metrics.Status"]=Queue_manager_status[response[pymqi.CMQCFC.MQIACF_Q_MGR_STATUS]]



                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)                        

        def queueCollector(self):

                try:


                        
                        attr1= {

                                pymqi.CMQC.MQCA_Q_NAME :'*',
                        }
                        queue_responses1 = self.pcf.MQCMD_INQUIRE_Q(attr1)

                        attr2 = {

                        pymqi.CMQC.MQCA_Q_NAME :'*',
                        pymqi.CMQC.MQIA_Q_TYPE :pymqi.CMQC.MQQT_LOCAL,
                        pymqi.CMQCFC.MQIACF_STATUS_TYPE:pymqi.CMQCFC.MQIACF_Q_STATUS,
                        pymqi.CMQCFC.MQIACF_Q_STATUS_ATTRS:
                                [
                                 pymqi.CMQCFC.MQCACF_LAST_GET_DATE,
                                 pymqi.CMQCFC.MQCACF_LAST_GET_TIME,
                                 pymqi.CMQCFC.MQCACF_LAST_PUT_DATE,
                                 pymqi.CMQCFC.MQCACF_LAST_PUT_TIME,
                                 pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE,
                                 pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS ]
                        }
                        queue_responses2 = self.pcf.MQCMD_INQUIRE_Q_STATUS(attr2)

                        queue_responses3=self.pcf.MQCMD_RESET_Q_STATS(attr1)



                        for response in queue_responses1:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()==self.queue_name:

                                        self.maindata["Queue_Metrics.Queue Name"]= queue_name.decode("utf-8").strip()
                                        self.maindata["Queue_Metrics.Current Queue Depth"]=response[pymqi.CMQC.MQIA_CURRENT_Q_DEPTH]
                                        self.maindata["Queue_Metrics.Max Queue Depth"]=response[pymqi.CMQC.MQIA_MAX_Q_DEPTH]
                                        self.maindata["Queue_Metrics.Handles Open(Input Count)"]=response[pymqi.CMQC.MQIA_OPEN_INPUT_COUNT]
                                        self.maindata["Queue_Metrics.Handles Open(Output Count)"]=response[pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT]
                                        break

                        for response in queue_responses2:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()==self.queue_name:
                        
                                        self.maindata["Queue_Metrics.Last Msg get Date"]=response[pymqi.CMQCFC.MQCACF_LAST_GET_DATE].decode("utf-8")
                                        self.maindata["Queue_Metrics.Last Msg get Time"]=response[pymqi.CMQCFC.MQCACF_LAST_GET_TIME].decode("utf-8")
                                        self.maindata["Queue_Metrics.Last Msg put Date"]=response[pymqi.CMQCFC.MQCACF_LAST_PUT_DATE].decode("utf-8")
                                        self.maindata["Queue_Metrics.Last Msg put Time"]=response[pymqi.CMQCFC.MQCACF_LAST_PUT_TIME].decode("utf-8")
                                        self.maindata["Queue_Metrics.Oldest Msg Age"]=response[pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE]
                                        self.maindata["Queue_Metrics.No. of Uncommitted Msgs"]=response[pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS]
                                        break
 
                        for response in queue_responses3:
                                queue_name = response[pymqi.CMQC.MQCA_Q_NAME]

                                if queue_name.decode("utf-8").strip()==self.queue_name:    
                                        self.maindata["Queue_Metrics.High Queue Depth"]=response[pymqi.CMQC.MQIA_HIGH_Q_DEPTH]
                                        self.maindata["Queue_Metrics.Msg Dequeue Count"]=response[pymqi.CMQC.MQIA_MSG_DEQ_COUNT]
                                        self.maindata["Queue_Metrics.Msg Enqueue Count"]=response[pymqi.CMQC.MQIA_MSG_ENQ_COUNT]

                                        
                      




                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        return self.maindata
        



        def channelCollector(self):

                try:

                        channel_statuses=["Channel Inactive",
                                        "Channel Binding", 
                                        "Channel Starting", 
                                        "Channel Running", 
                                        "Channel Stopping", 
                                        "Channel Retrying", 
                                        "Channel Stopped", 
                                        "Channel Requesting", 
                                        "Channel Paused", 
                                        "Channel Disconnected", 
                                        "Channel Initializing", 
                                        "Channel Switching"]


                        channel_substate={
                                0:"Undefined State",
                                100:"End of batch processing",
                                200:"Network send",
                                300:"Network receive",
                                400:"Serialized on queue manager access",
                                500:"Resynching with partner",
                                600:"Heartbeating with partner",
                                700:"Running security exit",
                                800:"Running receive exit",
                                900:"Running send exit",
                                1000:"Running message exit",
                                1100:"Running retry exit",
                                1200:"Running channel auto-definition exit",
                                1250:"Network connect",
                                1300:"SSL Handshaking",
                                1400:"Name server request",
                                1500:"Performing MQPUT",
                                1600:"Performing MQGET",
                                1700:"Executing IBM MQ API call",
                                1800:"Compressing or decompressing data"
                                }
                        




                        attr={
                                pymqi.CMQCFC.MQCACH_CHANNEL_NAME:"*",
                                pymqi.CMQCFC.MQIACH_CHANNEL_INSTANCE_ATTRS : 
                                                        [ 
                                                        pymqi.CMQCFC.MQCACH_CHANNEL_NAME, 
                                                        pymqi.CMQCFC.MQCACH_CONNECTION_NAME, 
                                                        pymqi.CMQCFC.MQIACH_CHANNEL_STATUS, 
                                                        pymqi.CMQCFC.MQIACH_MSGS,
                                                        pymqi.CMQCFC.MQIACH_BYTES_SENT,
                                                        pymqi.CMQCFC.MQIACH_BYTES_RECEIVED,
                                                        pymqi.CMQCFC.MQIACH_BUFFERS_SENT,
                                                        pymqi.CMQCFC.MQIACH_BUFFERS_RECEIVED,
                                                        pymqi.CMQCFC.MQIACH_INDOUBT_STATUS,
                                                        pymqi.CMQCFC.MQIACH_CHANNEL_SUBSTATE,
                                                        pymqi.CMQCFC.MQCACH_CHANNEL_START_DATE,
                                                        pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME
                                                        ]}
                        

                        channel_responses=self.pcf.MQCMD_INQUIRE_CHANNEL_STATUS(attr)

                        for channel_response in channel_responses:
                                channel_name=channel_response[pymqi.CMQCFC.MQCACH_CHANNEL_NAME]
                                if channel_name.decode('utf-8').strip()==self.channel:
                                        self.maindata["Channel_Metrics.Channel Name"]=channel_name.decode('utf-8').strip()
                                        self.maindata["Channel_Metrics.Channel Connection Name"]=channel_response[pymqi.CMQCFC.MQCACH_CONNECTION_NAME].decode('utf-8').strip()
                                        self.maindata["Channel_Metrics.Channel Status"]=channel_statuses[channel_response[pymqi.CMQCFC.MQIACH_CHANNEL_STATUS]]
                                        self.maindata["Channel_Metrics.No. of MQI calls"]=channel_response[pymqi.CMQCFC.MQIACH_MSGS]
                                        self.maindata["Channel_Metrics.Bytes Sent"]=channel_response[pymqi.CMQCFC.MQIACH_BYTES_SENT]
                                        self.maindata["Channel_Metrics.Bytes Received"]=channel_response[pymqi.CMQCFC.MQIACH_BYTES_RECEIVED]
                                        self.maindata["Channel_Metrics.Buffers Sent"]=channel_response[pymqi.CMQCFC.MQIACH_BUFFERS_SENT]
                                        self.maindata["Channel_Metrics.Buffers Received"]=channel_response[pymqi.CMQCFC.MQIACH_BUFFERS_RECEIVED]

                                        substate_data=channel_response[pymqi.CMQCFC.MQIACH_CHANNEL_SUBSTATE]
                                        self.maindata["Channel_Metrics.Channel Substate"]=channel_substate.get(substate_data)
                                        self.maindata["Channel_Metrics.Channel Start Date"]=channel_response[pymqi.CMQCFC.MQCACH_CHANNEL_START_DATE].decode('utf-8')
                                        self.maindata["Channel_Metrics.Channel Start Time"]=channel_response[pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME].decode('utf-8')
                                        break
                except Exception as e:
                        self.maindata['status']=0
                        self.maindata['msg']=str(e)
                        return self.maindata
                
        

if __name__=="__main__":

        queue_manager_name = None
        channel_name = None
        queue_name=None
        host = None
        port = None
        username="None"
        password="None"

        import argparse
        parser=argparse.ArgumentParser()
        parser.add_argument('--queue_manager_name',help="Enter queue manager name",default=queue_manager_name)
        parser.add_argument('--channel_name',help="Enter channel name",default=channel_name)
        parser.add_argument('--queue_name',help="Enter queue name",default=queue_name)
        parser.add_argument('--host',help="Enter host name",default=host)
        parser.add_argument('--port',help="Enter port number",default=port)
        parser.add_argument('--username',help="Enter username",default=username)
        parser.add_argument('--password',help="Enter password",default=password)
        parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
        parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
        parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)

        args=parser.parse_args()


        ibm_obj=IbmMq(args)
        ibm_mq_metric_data=ibm_obj.metricCollector()
        print(json.dumps(ibm_mq_metric_data,indent=True))

