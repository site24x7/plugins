#!/usr/bin/python3
import os
import json
import traceback

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {
    "QManager Connection Count": "connections",
    "queues": {"oldest_msg_age": "s"},
    "channels": {"bytes_sent": "bytes", "bytes_received": "bytes"},
}
current_file_path = os.path.dirname(os.path.abspath(__file__))


class IbmMq:

    def __init__(self, args):
        self.maindata = {}
        self.queue_manager = args.queue_manager_name
        self.channel = args.channel_name
        # self.queue_name=args.queue_name
        self.host = args.host
        self.port = args.port
        self.logsenabled = args.logs_enabled
        self.logtypename = args.log_type_name
        self.logfilepath = args.log_file_path

        self.maindata["plugin_version"] = PLUGIN_VERSION
        self.maindata["heartbeat_required"] = HEARTBEAT
        self.maindata["units"] = METRICS_UNITS
        self.maindata.update(
            {
                "tabs": {
                    "Queues": {"order": "1", "tablist": ["queues"]},
                    "Channels": {"order": "2", "tablist": ["channels"]},
                    "Listeners": {"order": "3", "tablist": ["listeners"]},
                }
            }
        )

        if args.username == "None":
            self.username = None
        else:
            self.username = args.username
        if args.password == "None":
            self.password = None
        else:
            self.password = args.password

        self.conn_info = "%s(%s)" % (self.host, self.port)

    def channel_selector(self, channel_name, mqi_calls, mqi_value):
        if not channel_name in mqi_calls.keys():
            return True
        elif mqi_value > mqi_calls[channel_name]:
            return True
        else:
            return False

    def rem(self, mount_data):
        while "" in mount_data:
            mount_data.remove("")
        return mount_data

    def main(self):

        pcf = self.mqConnector()
        if not pcf:
            return self.maindata

        return self.metriccollector(pcf)
    
    def info_dir(self):
        
        info_dir=os.path.join(current_file_path,"info")
        
        if not os.path.isdir(info_dir):
            os.makedirs(info_dir)
        return

    def mqConnector(self):

        try:
            try:
                import pymqi

                # For Q_Manager
                self.attr = {
                    pymqi.CMQCFC.MQIACF_Q_MGR_STATUS_ATTRS: [
                        pymqi.CMQCFC.MQIACF_CHINIT_STATUS,
                        pymqi.CMQCFC.MQIACF_CMD_SERVER_STATUS,
                        pymqi.CMQCFC.MQIACF_CONNECTION_COUNT,
                        pymqi.CMQCFC.MQIACF_Q_MGR_STATUS,
                    ]
                }
                self.Qmgr_name_query = pymqi.CMQC.MQCA_Q_MGR_NAME
                self.Connection_Count_query = pymqi.CMQCFC.MQIACF_CONNECTION_COUNT
                self.Status_query = pymqi.CMQCFC.MQIACF_Q_MGR_STATUS

                # For Q_collector
                self.q_name_query = pymqi.CMQC.MQCA_Q_NAME
                self.attr1 = {
                    pymqi.CMQC.MQCA_Q_NAME: "*",
                }

                self.attr2 = {
                    pymqi.CMQC.MQCA_Q_NAME: "*",
                    pymqi.CMQC.MQIA_Q_TYPE: pymqi.CMQC.MQQT_LOCAL,
                    pymqi.CMQCFC.MQIACF_STATUS_TYPE: pymqi.CMQCFC.MQIACF_Q_STATUS,
                    pymqi.CMQCFC.MQIACF_Q_STATUS_ATTRS: [
                        pymqi.CMQCFC.MQCACF_LAST_GET_DATE,
                        pymqi.CMQCFC.MQCACF_LAST_GET_TIME,
                        pymqi.CMQCFC.MQCACF_LAST_PUT_DATE,
                        pymqi.CMQCFC.MQCACF_LAST_PUT_TIME,
                        pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE,
                        pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS,
                    ],
                }

                self.Current_Queue_Depth_query = pymqi.CMQC.MQIA_CURRENT_Q_DEPTH
                self.Max_Queue_Depth_query = pymqi.CMQC.MQIA_MAX_Q_DEPTH
                self.Handles_Open_Input_Count_query = pymqi.CMQC.MQIA_OPEN_INPUT_COUNT
                self.Handles_Open_Output_Count_query = pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT
                self.Last_Msg_get_Date_query = pymqi.CMQCFC.MQCACF_LAST_GET_DATE
                self.Last_Msg_get_Time_query = pymqi.CMQCFC.MQCACF_LAST_GET_TIME
                self.Last_Msg_put_Date_query = pymqi.CMQCFC.MQCACF_LAST_PUT_DATE
                self.Last_Msg_put_Time_query = pymqi.CMQCFC.MQCACF_LAST_PUT_TIME
                self.Oldest_Msg_Age_query = pymqi.CMQCFC.MQIACF_OLDEST_MSG_AGE
                self.No_of_Uncommitted_Msgs_query = pymqi.CMQCFC.MQIACF_UNCOMMITTED_MSGS
                self.High_Queue_Depth_query = pymqi.CMQC.MQIA_HIGH_Q_DEPTH
                self.Msg_Dequeue_Count_query = pymqi.CMQC.MQIA_MSG_DEQ_COUNT
                self.Msg_Enqueue_Count_query = pymqi.CMQC.MQIA_MSG_ENQ_COUNT

                # For Channel Collector
                self.attr3 = {
                    pymqi.CMQCFC.MQCACH_CHANNEL_NAME: "*",
                    pymqi.CMQCFC.MQIACH_CHANNEL_INSTANCE_ATTRS: [
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
                        pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME,
                        pymqi.CMQCFC.MQIACH_CHANNEL_INSTANCE_TYPE,
                    ],
                }
                self.channel_name_query = pymqi.CMQCFC.MQCACH_CHANNEL_NAME
                self.Channel_Connection_Name = pymqi.CMQCFC.MQCACH_CONNECTION_NAME
                self.Channel_Status = pymqi.CMQCFC.MQIACH_CHANNEL_STATUS
                self.No_of_MQI_calls = pymqi.CMQCFC.MQIACH_MSGS
                self.Bytes_Sent = pymqi.CMQCFC.MQIACH_BYTES_SENT
                self.Bytes_Received = pymqi.CMQCFC.MQIACH_BYTES_RECEIVED
                self.Buffers_Sent = pymqi.CMQCFC.MQIACH_BUFFERS_SENT
                self.Buffers_Received = pymqi.CMQCFC.MQIACH_BUFFERS_RECEIVED
                self.substate_data = pymqi.CMQCFC.MQIACH_CHANNEL_SUBSTATE
                self.Channel_Start_Date = pymqi.CMQCFC.MQCACH_CHANNEL_START_DATE
                self.Channel_Start_Time = pymqi.CMQCFC.MQCACH_CHANNEL_START_TIME

                self.attr4 = {pymqi.CMQCFC.MQCACH_LISTENER_NAME: "*"}
                self.listener_name = pymqi.CMQCFC.MQCACH_LISTENER_NAME
                self.listener_port = pymqi.CMQCFC.MQIACH_PORT
                self.listener_backlog = pymqi.CMQCFC.MQIACH_BACKLOG
                self.listener_status = pymqi.CMQCFC.MQIACH_LISTENER_STATUS

            except Exception as e:
                self.maindata["status"] = 0
                self.maindata["msg"] = str(e)

                return
            try:
                # print(self.__dict__)
                qmgr = pymqi.connect(
                    self.queue_manager,
                    self.channel,
                    self.conn_info,
                    self.username,
                    self.password,
                )

                pcf = pymqi.PCFExecute(qmgr)
                return pcf

            except Exception as e:
                self.maindata["status"] = 0
                self.maindata["msg"] = str(e)

                return

        except Exception as e:

            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

            return

    def metriccollector(self, pcf):

        QMgrdata = self.QMgrCollector(pcf)
        if not QMgrdata:
            return self.maindata
        else:
            self.maindata.update(QMgrdata)

        QCollectdata = self.queueCollector(pcf)
        if not QCollectdata:
            return self.maindata
        else:
            self.maindata.update(QCollectdata)

        Channeldata = self.channelCollector(pcf)
        if not Channeldata:
            return self.maindata
        else:
            self.maindata.update(Channeldata)

        Listenerdata = self.listenerCollector(pcf)
        if not Listenerdata:
            return self.maindata
        else:
            self.maindata.update(Listenerdata)

        applog = {}
        if self.logsenabled in ["True", "true", "1"]:
            applog["logs_enabled"] = True
            applog["log_type_name"] = self.logtypename
            applog["log_file_path"] = self.logfilepath
        else:
            applog["logs_enabled"] = False
        self.maindata["applog"] = applog

        return self.maindata

    def QMgrCollector(self, pcf):
        try:
            maindata = {}

            Queue_manager_status = ["", "STARTING", "RUNNING", "QUIESCING", "STANDBY"]

            qmgr_responses = pcf.CMQCFC.MQCMD_INQUIRE_Q_MGR_STATUS(self.attr)

            for response in qmgr_responses:
                Qmgr_name = response[self.Qmgr_name_query]

                if Qmgr_name.decode("utf-8").strip() == self.queue_manager:
                    maindata["QManager Connection Count"] = response[
                        self.Connection_Count_query
                    ]
                    maindata["QManager Status"] = Queue_manager_status[
                        response[self.Status_query]
                    ]
            return maindata

        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

            return

    def queueCollector(self, pcf):

        try:
            maindata = {}

            queue_responses1 = pcf.MQCMD_INQUIRE_Q(self.attr1)
            queue_responses2 = pcf.MQCMD_INQUIRE_Q_STATUS(self.attr2)
            queue_responses3 = pcf.MQCMD_RESET_Q_STATS(self.attr1)
            queues = []
            queues_dict = {}
            ignore_queues_starting_with = ["SYSTEM", "PYMQPCF", "AMQ"]

            for response in queue_responses1:

                queue_name = response[self.q_name_query].decode("utf-8").strip()
                queue_check = queue_name.split(".")

                if not queue_check[0] in ignore_queues_starting_with and response[20]==1:
                    # print(response)
                    queue = {}

                    queue["name"] = queue_name
                    queue["current_queue_depth"] = response[
                        self.Current_Queue_Depth_query
                    ]
                    queue["max_queue_depth"] = response[self.Max_Queue_Depth_query]
                    queue["handles_qpen_input_count"] = response[
                        self.Handles_Open_Input_Count_query
                    ]
                    queue["handles_open_output_count"] = response[
                        self.Handles_Open_Output_Count_query
                    ]
                    queues_dict[queue_name] = queue
                    # print(response[self.q_name_query])

            for response in queue_responses2:
                queue_name = response[self.q_name_query].decode("utf-8").strip()
                queue_check = queue_name.split(".")

                if not queue_check[0] in ignore_queues_starting_with:

                    queue = queues_dict[queue_name]
                    queue["oldest_msg_age"] = response[self.Oldest_Msg_Age_query]
                    queue["no_of_uncommitted_msgs"] = response[
                        self.No_of_Uncommitted_Msgs_query
                    ]
                    queues_dict[queue_name] = queue

            for response in queue_responses3:
                queue_name = response[self.q_name_query].decode("utf-8").strip()
                queue_check = queue_name.split(".")

                if not queue_check[0] in ignore_queues_starting_with:

                    queue = queues_dict[queue_name]
                    queue["high_queue_depth"] = response[self.High_Queue_Depth_query]
                    queue["msg_dequeue_count"] = response[self.Msg_Dequeue_Count_query]
                    queue["msg_enqueue_count"] = response[self.Msg_Enqueue_Count_query]
                    queues.append(queue)
            maindata["queues"] = queues
            # print(queues)
            return maindata

        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

            # print(queue)
            return

    def object_status(self, attribute_list, file, json_array, key):
        
        self.info_dir()

        attribute_status_file = os.path.join(current_file_path,"info", (file + "-"+self.queue_manager+".txt"))

        if os.path.isfile(attribute_status_file):
            try:
                f = open(attribute_status_file, "r")
                attribute_check = f.read().split("\n")
                if "" in attribute_check:
                    attribute_check = self.rem(attribute_check)
            except Exception as e:
                self.maindata["status"] = 0
                self.maindata["msg"] = str(e)

            set1 = set(attribute_check)
            set2 = set(attribute_list)

            all = set1.intersection(set2)
            inactive = list(set1 - set2)

            for i in inactive:
                json_array.append({"name": i, key: 0})

            if not (len(all) == len(set2)):
                all = set1.union(set2)
                try:
                    f = open(attribute_status_file, "a")
                    f.truncate(0)
                    f.write("\n".join(all))
                    f.close()
                except Exception as e:
                    self.maindata["status"] = 0
                    self.maindata["msg"] = str(e)

            return json_array

        else:
            try:
                f = open(attribute_status_file, "a")
                f.write("\n".join(attribute_list))
                f.close()
            except Exception as e:
                self.maindata["status"] = 0
                self.maindata["msg"] = str(e)

            return json_array

        return json_array

    def channelCollector(self, pcf):

        try:
            maindata = {}

            channel_statuses = [
                "Channel Inactive",
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
                "Channel Switching",
            ]

            channel_substate = {
                0: "Undefined State",
                100: "End of batch processing",
                200: "Network send",
                300: "Network receive",
                400: "Serialized on queue manager access",
                500: "Resynching with partner",
                600: "Heartbeating with partnQM_APPLEer",
                700: "Running security exit",
                800: "Running receive exit",
                900: "Running send exit",
                1000: "Running message exit",
                1100: "Running retry exit",
                1200: "Running channel auto-definition exit",
                1250: "Network connect",
                1300: "SSL Handshaking",
                1400: "Name server request",
                1500: "Performing MQPUT",
                1600: "Performing MQGET",
                1700: "Executing IBM MQ API call",
                1800: "Compressing or decompressing data",
            }

            import pymqi

            prefix = "*"
            args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: prefix}

            channel_responses = pcf.MQCMD_INQUIRE_CHANNEL_STATUS(args)  # self.attr3)
            channels = {}
            mqi_calls = {}
            channel_list = []

            for channel_response in channel_responses:
                # print(channel_response[self.Channel_Status])

                channel_name = channel_response[3501].decode("utf-8").strip()
                channels_dict = {}
                # print(channel_name)

                if self.channel_selector(
                    channel_name, mqi_calls, channel_response[self.No_of_MQI_calls]
                ):

                    channels_dict["name"] = channel_name
                    # maindata["Channel_Metrics.Channel Connection Name"]=channel_response[self.Channel_Connection_Name].decode('utf-8').strip()
                    channels_dict["channel_status"] = channel_response[
                        self.Channel_Status
                    ]
                    channels_dict["no_of_mqi_calls"] = channel_response[
                        self.No_of_MQI_calls
                    ]
                    channels_dict["bytes_sent"] = channel_response[self.Bytes_Sent]
                    channels_dict["bytes_received"] = channel_response[
                        self.Bytes_Received
                    ]
                    channels_dict["buffers_sent"] = channel_response[self.Buffers_Sent]
                    channels_dict["buffers_received"] = channel_response[
                        self.Buffers_Received
                    ]
                    substate_data = channel_response[self.substate_data]
                    channels_dict["sub_state"] = substate_data

                    channels[channel_name] = channels_dict

                    mqi_calls[channel_name] = channel_response[self.No_of_MQI_calls]
                    channel_list.append(channel_name)

            channels = self.object_status(
                channel_list, "channels", list(channels.values()), "channel_status"
            )

            maindata["channels"] = channels

            return maindata
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

            return

    def listenerCollector(self, pcf):
        try:
            maindata = {}
            listeners = []
            response = pcf.MQCMD_INQUIRE_LISTENER_STATUS(self.attr4)
            listener_list = []

            for listener_info in response:
                listener_name = listener_info[self.listener_name].decode()
                listener_dict = {
                    "name": listener_name,
                    "port": listener_info[self.listener_port],
                    "backlog": listener_info[self.listener_backlog],
                    "state": listener_info[self.listener_status],
                    "status": 1,
                }

                listeners.append(listener_dict)
                listener_list.append(listener_name)

            maindata["listeners"] = listeners
            listeners = self.object_status(
                listener_list, "listeners", listeners, "status"
            )

            return maindata
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

        return


if __name__ == "__main__":

    queue_manager_name = "QM1"
    channel_name = "DEV.APP.SVRCONN"
    host = "localhost"
    port = "1414"
    username = "app"
    password = "plugin"

    import argparse, platform

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queue_manager_name",
        help="Enter queue manager name",
        default=queue_manager_name,
    )
    parser.add_argument(
        "--channel_name", help="Enter channel name", default=channel_name
    )
    parser.add_argument("--host", help="Enter host name", default=host)
    parser.add_argument("--port", help="Enter port number", default=port)
    parser.add_argument("--username", help="Enter username", default=username)
    parser.add_argument("--password", help="Enter password", default=password)
    parser.add_argument(
        "--logs_enabled",
        help="enable log collection for this plugin application",
        default="False",
    )
    parser.add_argument(
        "--log_type_name", help="Display name of the log type", nargs="?", default=None
    )
    parser.add_argument(
        "--log_file_path",
        help="list of comma separated log file paths",
        nargs="?",
        default=None,
    )

    args = parser.parse_args()

    ibm_obj = IbmMq(args)
    ibm_mq_metric_data = ibm_obj.main()

    if (platform.system() == "Windows"):
        print(json.dumps(ibm_mq_metric_data))
    else:
        print(json.dumps(ibm_mq_metric_data, indent=True))
