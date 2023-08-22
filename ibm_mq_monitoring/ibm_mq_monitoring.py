#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


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
        



    def main(self):
           
           pcf=self.mqConnector()
           if not pcf:
                  return self.maindata
           
           return self.metriccollector(pcf)


    def mqConnector(self):

            try:    
                    try: 
                        import pymqi
                        #For Q_Manager
                        self.attr={
                                    pymqi.CMQCFC.MQIACF_Q_MGR_STATUS_ATTRS:[
                                    pymqi.CMQCFC.MQIACF_CHINIT_STATUS,
                                    pymqi.CMQCFC.MQIACF_CMD_SERVER_STATUS,
                                    pymqi.CMQCFC.MQIACF_CONNECTION_COUNT,
                                    pymqi.CMQCFC.MQIACF_Q_MGR_STATUS
                                    ]
                                    }
                        self.Qmgr_name_query=pymqi.CMQC.MQCA_Q_MGR_NAME
                        self.Connection_Count_query=pymqi.CMQCFC.MQIACF_CONNECTION_COUNT
                        self.Status_query=pymqi.CMQCFC.MQIACF_Q_MGR_STATUS

                        # For Q_collector
                        self.q_name_query=pymqi.CMQC.MQCA_Q_NAME
                        self.attr1= {

                                pymqi.CMQC.MQCA_Q_NAME :'*',
                        }
                        
                        self.attr2 = {

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


                        self.Current_Queue_Depth_query=pymqi.CMQC.MQIA_CURRENT_Q_DEPTH
                        self.Max_Queue_Depth_query=pymqi.CMQC.MQIA_MAX_Q_DEPTH
                        self.Handles_Open_Input_Count_query=pymqi.CMQC.MQIA_OPEN_INPUT_COUNT
                        self.Handles_Open_Output_Count_query=pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT
                        self.Last_Msg_get_Date_query=pymqi.CMQCFC.MQCACF_LAST_GET_DATE
                        self.Last_Msg_get_Time_query=pymqi.CMQCFC.MQCACF_LAST_GET_TIME
                        self.Last_Msg_put_Date_query=pymqi.CMQCFC.MQCACF_LAST_PUT_DATE
                        self.Last_Msg_put_Time_query=pymqi.CMQCFC.MQCACF_LAST_PUT_TIME
                        self.Oldest_Msg_Age_query=pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE
                        self.No_of_Uncommitted_Msgs_query=pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS
                        self.High_Queue_Depth_query=pymqi.CMQC.MQIA_HIGH_Q_DEPTH
                        self.Msg_Dequeue_Count_query=pymqi.CMQC.MQIA_MSG_DEQ_COUNT
                        self.Msg_Enqueue_Count_query=pymqi.CMQC.MQIA_MSG_ENQ_COUNT

                        #For Channel Collector
                        self.attr3={
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
                        self.channel_name_query=pymqi.CMQCFC.MQCACH_CHANNEL_NAME
                        self.Channel_Connection_Name=pymqi.CMQCFC.MQCACH_CONNECTION_NAME
                        self.Channel_Status=pymqi.CMQCFC.MQIACH_CHANNEL_STATUS
                        self.No_of_MQI_calls=pymqi.CMQCFC.MQIACH_MSGS
                        self.Bytes_Sent=pymqi.CMQCFC.MQIACH_BYTES_SENT
                        self.Bytes_Received=pymqi.CMQCFC.MQIACH_BYTES_RECEIVED
                        self.Buffers_Sent=pymqi.CMQCFC.MQIACH_BUFFERS_SENT
                        self.Buffers_Received=pymqi.CMQCFC.MQIACH_BUFFERS_RECEIVED                              
                        self.substate_data=pymqi.CMQCFC.MQIACH_CHANNEL_SUBSTATE
                        self.Channel_Start_Date=pymqi.CMQCFC.MQCACH_CHANNEL_START_DATE
                        self.Channel_Start_Time=pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME


                    except Exception as e:
                            self.maindata['status']=0
                            self.maindata['msg']=str(e)
                            return 
                    try:
                        qmgr = pymqi.connect(self.queue_manager, self.channel, self.conn_info,self.username,self.password)
                        pcf = pymqi.PCFExecute(qmgr)
                        return pcf
                    
                    except Exception as e:
                            self.maindata['status']=0
                            self.maindata['msg']=str(e)
                            return 
                           
            except Exception as e:
                    
                    self.maindata['status']=0
                    self.maindata['msg']=str(e)
                    return


    def metriccollector(self, pcf):
        
        QMgrdata=self.QMgrCollector(pcf)
        if not QMgrdata:
               return self.maindata
        else:
               self.maindata.update(QMgrdata)


        QCollectdata=self.queueCollector(pcf)
        if not QCollectdata:
               return self.maindata
        else:
               self.maindata.update(QCollectdata)
        

        Channeldata=self.channelCollector(pcf)
        if not Channeldata:
               return self.maindata
        else:
               self.maindata.update(Channeldata)
        
        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["logs_enabled"]=False
        self.maindata['applog'] = applog

        return self.maindata
           


    def QMgrCollector(self, pcf):
            try:
                    maindata={}

                    Queue_manager_status=["","STARTING","RUNNING","QUIESCING","STANDBY"]

                    qmgr_responses=pcf.CMQCFC.MQCMD_INQUIRE_Q_MGR_STATUS(self.attr)

                    for response in qmgr_responses:
                            Qmgr_name=response[self.Qmgr_name_query]

                            if Qmgr_name.decode('utf-8').strip() == self.queue_manager:
                                    maindata["QManager_metrics.Connection Count"]=response[self.Connection_Count_query]
                                    maindata["QManager_metrics.Status"]=Queue_manager_status[response[self.Status_query]]
                    return maindata

            except Exception as e:
                    self.maindata['status']=0
                    self.maindata['msg']=str(e)     
                    return

    def queueCollector(self, pcf):

            try:
                    maindata={}

                    queue_responses1 = pcf.MQCMD_INQUIRE_Q(self.attr1)
                    queue_responses2 = pcf.MQCMD_INQUIRE_Q_STATUS(self.attr2)
                    queue_responses3=pcf.MQCMD_RESET_Q_STATS(self.attr1)


                    for response in queue_responses1:
                            queue_name = response[self.q_name_query]

                            if queue_name.decode("utf-8").strip()==self.queue_name:

                                    maindata["Queue_Metrics.Queue Name"]= queue_name.decode("utf-8").strip()
                                    maindata["Queue_Metrics.Current Queue Depth"]=response[self.Current_Queue_Depth_query]
                                    maindata["Queue_Metrics.Max Queue Depth"]=response[self.Max_Queue_Depth_query]
                                    maindata["Queue_Metrics.Handles Open(Input Count)"]=response[self.Handles_Open_Input_Count_query]
                                    maindata["Queue_Metrics.Handles Open(Output Count)"]=response[self.Handles_Open_Output_Count_query]
                                    break

                    for response in queue_responses2:
                            queue_name = response[self.q_name_query]

                            if queue_name.decode("utf-8").strip()==self.queue_name:
                    
                                    maindata["Queue_Metrics.Last Msg get Date"]=response[self.Last_Msg_get_Date_query].decode("utf-8")
                                    maindata["Queue_Metrics.Last Msg get Time"]=response[self.Last_Msg_get_Time_query].decode("utf-8")
                                    maindata["Queue_Metrics.Last Msg put Date"]=response[self.Last_Msg_put_Date_query].decode("utf-8")
                                    maindata["Queue_Metrics.Last Msg put Time"]=response[self.Last_Msg_put_Time_query].decode("utf-8")
                                    maindata["Queue_Metrics.Oldest Msg Age"]=response[self.Oldest_Msg_Age_query]
                                    maindata["Queue_Metrics.No. of Uncommitted Msgs"]=response[self.No_of_Uncommitted_Msgs_query]
                                    break

                    for response in queue_responses3:
                            queue_name = response[self.q_name_query]

                            if queue_name.decode("utf-8").strip()==self.queue_name:    
                                    maindata["Queue_Metrics.High Queue Depth"]=response[self.High_Queue_Depth_query]
                                    maindata["Queue_Metrics.Msg Dequeue Count"]=response[self.Msg_Dequeue_Count_query]
                                    maindata["Queue_Metrics.Msg Enqueue Count"]=response[self.Msg_Enqueue_Count_query]
                    return maindata

            except Exception as e:
                    self.maindata['status']=0
                    self.maindata['msg']=str(e)
                    return 



    def channelCollector(self, pcf):

            try:
                    maindata={}

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
                    
                    

                    channel_responses=pcf.MQCMD_INQUIRE_CHANNEL_STATUS(self.attr3)

                    for channel_response in channel_responses:
                            channel_name=channel_response[self.channel_name_query]
                            if channel_name.decode('utf-8').strip()==self.channel:
                                    maindata["Channel_Metrics.Channel Name"]=channel_name.decode('utf-8').strip()
                                    maindata["Channel_Metrics.Channel Connection Name"]=channel_response[self.Channel_Connection_Name].decode('utf-8').strip()
                                    maindata["Channel_Metrics.Channel Status"]=channel_statuses[channel_response[self.Channel_Status]]
                                    maindata["Channel_Metrics.No. of MQI calls"]=channel_response[self.No_of_MQI_calls]
                                    maindata["Channel_Metrics.Bytes Sent"]=channel_response[self.Bytes_Sent]
                                    maindata["Channel_Metrics.Bytes Received"]=channel_response[self.Bytes_Received]
                                    maindata["Channel_Metrics.Buffers Sent"]=channel_response[self.Buffers_Sent]
                                    maindata["Channel_Metrics.Buffers Received"]=channel_response[self.Buffers_Received]

                                    substate_data=channel_response[self.substate_data]
                                    maindata["Channel_Metrics.Channel Substate"]=channel_substate.get(substate_data)
                                    maindata["Channel_Metrics.Channel Start Date"]=channel_response[self.Channel_Start_Date].decode('utf-8')
                                    maindata["Channel_Metrics.Channel Start Time"]=channel_response[self.Channel_Start_Time].decode('utf-8')
                                    break
                    return maindata
            except Exception as e:
                    self.maindata['status']=0
                    self.maindata['msg']=str(e)
                    return 








if __name__=="__main__":
    
    queue_manager_name = None
    channel_name = None
    queue_name= None
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
    ibm_mq_metric_data=ibm_obj.main()
    print(json.dumps(ibm_mq_metric_data,indent=True))
