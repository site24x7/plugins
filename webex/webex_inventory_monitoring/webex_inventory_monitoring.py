#!/usr/bin/python

import json
import argparse
import urllib2
import urllib
import datetime
import time
import logging
import os
import sys

PLUGIN_VERSION = 1  ###Mandatory -If any changes in the plugin metrics, increment the version number.
HEARTBEAT = "true"  ###Mandatory -Set this to true to receive alerts when there is no data from the plugin within the poll interval
#METRIC_UNITS = {"CPU": "%", "Memory": "%"}  ###OPTIONAL - The unit defined here will be displayed in the Dashboard.

ACCESS_TOKEN = ""  ## WILL BE POPULATED FROM CONFIGS
REFRESH_TOKEN = ""  ## WILL BE POPULATED FROM CONFIGS
CLIENT_ID = ""  ## WILL BE POPULATED FROM CONFIGS
CLIENT_SECRET = ""  ## WILL BE POPULATED FROM CONFIGS
useCustomFields = False ## WILL BE POPULATED FROM CONFIGS
ORGIDS = [] ## WILL BE POPULATED FROM CONFIGS
TEAMS = [] ## WILL BE POPULATED FROM CONFIGS
LOGGING = True

class Plugin():
    ##########################  USER INPUT PARAMS   #################################################################################

    #######  MANDATORY PARAMS ######
    isTokenValid = True
    PAGING = "200"
    cntrlr = False
    flag = True
    ORGID = []
    TEAM = []
    ACC_TKN=""
    ROOMID = []
    HEADER=""
    newTokenGenerated = False
    plugin_perf="" #To store the performance related metrics of the plugin

    #################   API'S USED  ################################

    MYDETAILS_API="https://webexapis.com/v1/people"   #TEST API USED TO TEST ACCESS TOKEN VALIDITY
    GEN_ACCESS_TOKEN_API="https://api.ciscospark.com/v1/access_token"
    ORG_LIST_API="https://webexapis.com/v1/organizations"
    TEAM_LIST_API="https://webexapis.com/v1/teams"

    HYBRID_CLUSTER_API="https://webexapis.com/v1/hybrid/clusters"
    DEVICES_API="https://webexapis.com/v1/devices?orgId="
    HYBRID_CONNECTORS_API="https://webexapis.com/v1/hybrid/connectors?orgId="
    PEOPLE_LIST_API= "https://webexapis.com/v1/people?orgId="
    MEMBERSHIP_LIST_API="https://webexapis.com/v1/team/memberships?teamId="
    PLACES_LIST_API="https://webexapis.com/v1/places?orgId="
    ROLES_LIST_API="https://webexapis.com/v1/roles"
    ROOM_LIST_API="https://webexapis.com/v1/rooms?max="
    ROOM_MESSAGES_LIST_API="https://webexapis.com/v1/messages?roomId="
    EVENTS_LIST_API="https://webexapis.com/v1/events?max="

    ##########################  USER INPUT PARAMS ENDS HERE  #########################################################################

    def devicesCount(self):
        try:
            count = 0
            apiHit=0;
            start = time.time()
            for orgid in self.ORGID:
                check = True
                link = self.DEVICES_API + orgid
                while (check):
                    apiHit = apiHit + 1
                    contents_devices = self.getReq(link)
                    contents_devices_json = json.loads(contents_devices.read())
                    count = count + len(contents_devices_json['items'])
                    if ("Link" in contents_devices.info()):
                        linkTemp = contents_devices.info().get('Link')
                        start = linkTemp.find("<") + 1
                        end = linkTemp.find(">")
                        link = linkTemp[start:end]
                    else:
                        check = False
            self.data['Admin - Devices Count'] = count
        except Exception as e:
            self.data["msg"] += "Devices List Fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Devices-Cnt,"+str(apiHit)+","+str(time.time()-start)+"\n"



    def peopleInOrgCount(self):
        try:
            count = 0
            apiHit = 0;
            start = time.time()
            for orgid in self.ORGID:
                check = True
                link = self.PEOPLE_LIST_API + orgid
                while (check):
                    apiHit = apiHit + 1
                    contents_people = self.getReq(link)
                    contents_people_json = json.loads(contents_people.read())
                    count = count + len(contents_people_json['items'])
                    if ("Link" in contents_people.info()):
                        linkTemp = contents_people.info().get('Link')
                        start = linkTemp.find("<") + 1
                        end = linkTemp.find(">")
                        link = linkTemp[start:end]
                    else:
                        check = False
            self.data['People Count'] = count
        except Exception as e:
            self.data["msg"] += "List People fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "List-People,"+str(apiHit)+","+str(time.time()-start)+ "\n"

    def hybridClusterCount(self):
        apiHit = 0;
        start = time.time()
        try:
            link = self.HYBRID_CLUSTER_API
            contents_hybrid_clusters = self.getReq(link).read()
            apiHit=apiHit+1
            if len(contents_hybrid_clusters) == 2 or bool(
                    contents_hybrid_clusters and contents_hybrid_clusters.strip()):
                self.data["Hybrid - Clusters Count"] = 0
            else:
                contents_hybrid_clusters_json = json.loads(contents_hybrid_clusters)
                self.data["Hybrid - Clusters Count"] = len(contents_hybrid_clusters_json['items'])
        except Exception as e:
            self.data["msg"] += "List Hybrid Cluster fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Hybrid-Cluster," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def hybridConnectorsCount(self):
        apiHit = 0;
        start = time.time()
        try:
            count = 0
            for id in self.ORGID:
                count = 0
                link = self.HYBRID_CONNECTORS_API + id
                contents_hybrid_connectors = self.getReq(link).read()
                apiHit=apiHit+1
                if len(contents_hybrid_connectors) == 2 or bool(
                        contents_hybrid_connectors and contents_hybrid_connectors.strip()):
                    count = count + 0
                else:
                    contents_hybrid_connectors_json = json.loads(contents_hybrid_connectors)
                    count = count + len(contents_hybrid_connectors_json['items'])
            self.data['Hybrid - Connectors Count'] = count
        except Exception as e:
            self.data["msg"] += "Hybrid Connectors fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Hybrid-Connector," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def roomMembershipOrgCount(self):
        apiHit = 0;
        start = time.time()
        try:
            count = 0
            for team in self.TEAM:
                link = self.MEMBERSHIP_LIST_API + team
                contents_memberships = self.getReq(link).read()
                apiHit=apiHit+1
                contents_memberships_json = json.loads(contents_memberships)
                count = count + len(contents_memberships_json['items'])
            self.data['Room - Memberships Count'] = count

        except Exception as e:
            self.data["msg"] += "Room Membership fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Room-Memberships," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def placesCount(self):
        apiHit = 0;
        start = time.time()
        try:
            count = 0
            for id in self.ORGID:
                link = self.PLACES_LIST_API + id
                contents_memberships = self.getReq(link).read()
                apiHit=apiHit+1
                contents_memberships_json = json.loads(contents_memberships)
                count = count + len(contents_memberships_json['items'])
            self.data['Places Count'] = count
        except Exception as e:
            self.data["msg"] += "Places List fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Places Count," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def rolesCount(self):
        apiHit = 0;
        start = time.time()
        try:
            link = self.ROLES_LIST_API
            contents_roles = self.getReq(link).read()
            apiHit=apiHit+1
            contents_roles_json = json.loads(contents_roles)
            self.data['Admin - Roles Count'] = len(contents_roles_json['items'])

        except Exception as e:
            self.data["msg"] += "Roles List fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Roles Count," + str(apiHit) + "," + str((time.time() - start)) + "\n"


    def messagesCountExchangedInRooms(self):
        try:
            apiHit = 0;
            start = time.time()
            count = 0
            for room in self.ROOMID:
                check = True
                link = self.ROOM_MESSAGES_LIST_API + room + "&max=" + self.PAGING
                while (check):
                    contents_messages = self.getReq(link)
                    contents_messages_json = json.loads(contents_messages.read())
                    apiHit=apiHit+1
                    count = count + len(contents_messages_json['items'])
                    if ("Link" in contents_messages.info()):
                        linkTemp = contents_messages.info().get('Link')
                        start = linkTemp.find("<") + 1
                        end = linkTemp.find(">")
                        link = linkTemp[start:end]
                    else:
                        check = False

            self.data['Total Messages Exchanged'] = count

        except Exception as e:
            self.data["msg"] += "Messages from each room fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Msg count in rooms," + str(apiHit) + "," + str(time.time() - start) + "\n"


    def roomsCount(self):
        try:
            apiHit = 0;
            start = time.time()
            count = 0
            check = True
            link = self.ROOM_LIST_API + self.PAGING
            while (check):
                contents_rooms = self.getReq(link)
                contents_rooms_json = json.loads(contents_rooms.read())
                apiHit=apiHit+1
                count = count + len(contents_rooms_json['items'])
                for i in range(len(contents_rooms_json['items'])):
                    self.ROOMID += [str(contents_rooms_json['items'][i].get('id'))]
                if ("Link" in contents_rooms.info()):
                    linkTemp = contents_rooms.info().get('Link')
                    start = linkTemp.find("<") + 1
                    end = linkTemp.find(">")
                    link = linkTemp[start:end]
                else:
                    check = False

            self.data['Admin - Rooms Count'] = count
        except Exception as e:
            self.data["msg"] += "Rooms List fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Rooms Count," + str(apiHit) + "," + str(time.time()-start) + "\n"

    def eventsCount(self):
        try:
            apiHit = 0;
            start = time.time()
            check = True
            link = self.EVENTS_LIST_API + self.PAGING
            mesCreated = mesUpdated = mesDeleted = memCreated = memUpdated = memDeleted = 0
            while (check):
                contents_messages = self.getReq(link)
                contents_messages_json = json.loads(contents_messages.read())
                apiHit=apiHit+1
                for i in range(len(contents_messages_json['items'])):
                    temp = contents_messages_json['items'][i]
                    if (temp.get('resource') == "messages" and temp.get('type') == "created"):
                        mesCreated = mesCreated + 1
                    elif (temp.get('resource') == "messages" and temp.get('type') == "updated"):
                        mesUpdated = mesUpdated + 1
                    elif (temp.get('resource') == "messages" and temp.get('type') == "deleted"):
                        mesDeleted = mesDeleted + 1
                    elif (temp.get('resource') == "memberships" and temp.get('type') == "created"):
                        memCreated = memCreated + 1
                    elif (temp.get('resource') == "memberships" and temp.get('type') == "updated"):
                        memUpdated = memUpdated + 1
                    elif (temp.get('resource') == "memberships" and temp.get('type') == "deleted"):
                        memDeleted = memDeleted + 1

                if ("Link" in contents_messages.info()):
                    linkTemp = contents_messages.info().get('Link')
                    start = linkTemp.find("<") + 1
                    end = linkTemp.find(">")
                    link = linkTemp[start:end]
                else:
                    check = False
            self.data['Messages Created'] = mesCreated
            self.data['Messages Updated'] = mesUpdated
            self.data['Messages Deleted'] = mesDeleted
            self.data['Memberships Created'] = memCreated
            self.data['Memberships Updated'] = memUpdated
            self.data['Memberships Deleted'] = memDeleted
        except Exception as e:
            self.data["msg"] += "Events fetch Exception "
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Rooms Count," + str(apiHit) + "," + str(time.time() - start) + "\n"


    def fetchMetricStat(self):
        self.devicesCount()
        self.peopleInOrgCount()
        self.hybridClusterCount()
        self.hybridConnectorsCount()
        self.roomMembershipOrgCount()
        self.placesCount()
        self.rolesCount()
        self.roomsCount()
        self.messagesCountExchangedInRooms()
        self.eventsCount()

    def getOrgCount(self):
            self.plugin_perf += "\n"
            apiHit = 0;
            start = time.time()
            link = self.ORG_LIST_API
            contents_org_membership = self.getReq(link).read()
            apiHit = apiHit + 1
            contents_org_membership_json = json.loads(contents_org_membership)
            self.data['Admin - Org Count'] = len(contents_org_membership_json)
            self.ORGID = [contents_org_membership_json['items'][0]['id']]
            self.plugin_perf += "Org Count," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def getTeamsCount(self):
        count = 0
        apiHit = 0;
        start = time.time()
        link = self.TEAM_LIST_API
        contents_teams = self.getReq(link).read()
        apiHit=apiHit+1
        contents_teams_json = json.loads(contents_teams)
        teams=[]
        for i in range(len(contents_teams_json)):
            self.TEAM += [str(contents_teams_json["items"][i]["id"])]
            count = count + 1
        self.data['Admin - Teams Count'] = count
        self.plugin_perf += "Teams Count," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def getReq(self, link):
        return urllib2.urlopen(urllib2.Request(
                link,
                headers=self.HEADER
            ))


    def getData(self):  ### The getData method contains Sample data. User can enhance the code to fetch Original data
        if(self.flag==False):
            self.data['status'] = 0  # If api check failed priliminary tests mark the monitor as down
            return self.data
        try:  ##set the data object based on the requirement
            if useCustomFields == True:
                self.data['Admin - Org Count'] = len(ORGIDS)
                self.data['Admin - Teams Count'] = len(TEAMS)
                self.ORGID = ORGIDS
                self.TEAM = TEAMS
            else:
                self.getOrgCount()
                self.getTeamsCount()

            # Fetch All metrics for this plugin
            self.fetchMetricStat()

            if self.data["msg"]=="":
                self.data["msg"]="AVAILABLE"
        except Exception as e:
            self.data['status'] = 0  ###OPTIONAL-In case of any errors,Set 'status'=0 to mark the plugin as down.
            self.data["msg"] = str(e)  ###OPTIONAL- Set the custom message to be displayed in the "Errors" field of Log Report
        return self.data


    def generateAccessToken(self):
        url = self.GEN_ACCESS_TOKEN_API
        data = urllib.urlencode(
            {'grant_type': 'refresh_token', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
             'refresh_token': REFRESH_TOKEN})
        req = urllib2.Request(url, data)
        contents_json = json.loads(urllib2.urlopen(req).read())
        self.ACC_TKN = contents_json["access_token"]
        with open('Resouce_Inventory_Metrics', 'r') as fin:
            data = fin.read().splitlines(True)

        with open('Resouce_Inventory_Metrics', 'w') as fout:
            fout.writelines("[CONFIGURATIONS]\nACCESS_TOKEN=\"" + self.ACC_TKN + "\"\n")
            fout.writelines(data[2:])
        self.data["msg"] += "New Access Token Generated "
        self.newTokenGenerated = True


    def checkTokenValidity(self): # To check the validity of Access Token
        self.HEADER = {"Authorization": 'Bearer ' + self.ACC_TKN}
        link=self.MYDETAILS_API
        try:
            res = self.getReq(link).read()
            # PROCESS HERE
        except urllib2.HTTPError as e:
            if str(e.code)=="401" and str(e.reason=="Unauthorized"):
                self.data["msg"] += "Token Unauthorized or expired "
                ################ GENERATING NEW ACCESS TOKEN ###########################
                try:
                    self.generateAccessToken()
                except Exception as e:
                     self.data["msg"] += str(e)
                     self.data["msg"] += "Problem Generating Access Token "
                     self.flag = False

                ###################################################################
            else:
                self.data["msg"] += e.read()
                self.flag=False

    def __init__(self):
        self.data = {}
        self.data["plugin_version"] = PLUGIN_VERSION
        self.data["heartbeat_required"] = HEARTBEAT
        self.data["msg"]=""
        self.ACC_TKN = ACCESS_TOKEN
        self.HEADER = {"Authorization": 'Bearer ' + self.ACC_TKN}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--access_token', help='Access Token')
    parser.add_argument('--client_id', help='Client Id')
    parser.add_argument('--client_secret', help='Client Secret')
    parser.add_argument('--refresh_token', help='Refresh Token')
    parser.add_argument('--use_custom_fields', help='Use Custom Fields')
    parser.add_argument('--orgids', help='Organisations Ids')
    parser.add_argument('--teams', help='Teams Ids')
    parser.add_argument('--logging', help='Is Logging required')

    args = parser.parse_args()

    if args.access_token:
        useCustomFields = args.use_custom_fields
        ACCESS_TOKEN = args.access_token
        CLIENT_ID = args.client_id
        CLIENT_SECRET = args.client_secret
        REFRESH_TOKEN = args.refresh_token
        LOGGING = args.logging
        if args.use_custom_fields:
            ORGIDS = args.orgids.split(",")
            TEAMS = args.teams.split(",")

        plugin = Plugin()
        plugin.checkTokenValidity()
        if plugin.newTokenGenerated:
            plugin.checkTokenValidity()
        data = plugin.getData()
        print(json.dumps(data, indent=4, sort_keys=True))  ###Print the output in JSON format
        if LOGGING == True:
            path = sys.path[0] + "/plugin_perf.log"
            if os.path.exists(path) and (os.path.getsize(path)) > 10 * 1024:
                os.remove(path)
            logging.basicConfig(filename='plugin_perf.log', filemode='a', format='%(asctime)s - %(message)s',
                                level=logging.INFO)
            logging.info(plugin.plugin_perf)
    else:
        result = {}
        result['plugin_version'] = PLUGIN_VERSION
        result['heartbeat_required'] = HEARTBEAT
        result['status'] = 0
        result['msg'] = 'No args passed'
        print(json.dumps(result, indent=4, sort_keys=True))




