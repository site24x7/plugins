#!/usr/bin/python

import json
import argparse
import urllib2
import urllib
import datetime
import logging
import time
import sys
import os

PLUGIN_VERSION = 1  ### Mandatory -If any changes in the plugin metrics, increment the version number.
HEARTBEAT = "true"  ### Mandatory -Set this to true to receive alerts when there is no data from the plugin within the poll interval

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
    msg = ""
    flag = True
    ORGID = []
    TEAM = []
    ACC_TKN = ""
    ROOMID = []
    HEADER=""
    newTokenGenerated = False
    plugin_perf="" #To store the performance related metrics of the plugin

    #################   API'S USED  ################################

    MYDETAILS_API = "https://webexapis.com/v1/people"  # TEST API USED TO TEST ACCESS TOKEN VALIDITY
    GEN_ACCESS_TOKEN_API = "https://api.ciscospark.com/v1/access_token"
    ORG_LIST_API = "https://webexapis.com/v1/organizations"
    TEAMS_LIST_API = "https://webexapis.com/v1/hybrid/clusters"

    AUDIT_EVENT_API = "https://webexapis.com/v1/adminAudit/events?orgId="
    LISENCES_API = "https://webexapis.com/v1/licenses"
    RESOURCE_GRP_MEMBERSHISP_API="https://webexapis.com/v1/resourceGroup/memberships"

    ##########################  USER INPUT PARAMS ENDS HERE  #########################################################################

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

    def generateAccessToken(self):
        url = self.GEN_ACCESS_TOKEN_API
        data = urllib.urlencode(
            {'grant_type': 'refresh_token', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
             'refresh_token': REFRESH_TOKEN})
        req = urllib2.Request(url, data)
        contents_json = json.loads(urllib2.urlopen(req).read())
        self.ACC_TKN = contents_json["access_token"]
        with open('Admin_License_Metrics.cfg', 'r') as fin:
            data = fin.read().splitlines(True)

        with open('Admin_License_Metrics.cfg', 'w') as fout:
            fout.writelines("[CONFIGURATIONS]\nACCESS_TOKEN=\"" + self.ACC_TKN + "\"\n")
            fout.writelines(data[2:])
        self.data["msg"] += "New Access Token Generated "
        self.newTokenGenerated = True

    def getReq(self, link):
        return urllib2.urlopen(urllib2.Request(
                link,
                headers=self.HEADER
            ))

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
        link = self.TEAMS_LIST_API
        contents_teams = self.getReq(link).read()
        apiHit=apiHit+1
        contents_teams_json = json.loads(contents_teams)
        teams=[]
        for i in range(len(contents_teams_json)):
            self.TEAM += [str(contents_teams_json["items"][i]["id"])]
            count = count + 1
        self.data['Admin - Teams Count'] = count
        self.plugin_perf += "Teams Count," + str(apiHit) + "," + str((time.time() - start)) + "\n"

    def fetchMetricStat(self):
        self.getAuditEventsCount()
        self.licenseListCount()
        self.resourceGrpMembershipCount()

    def getAuditEventsCount(self):
        ### Only Audit event data last one day will be
        try:
            apiHit = 0;
            start = time.time()
            count = 0
            dateE = str(datetime.datetime.today().isoformat("T"))
            dateE = dateE[0:len(dateE) - 3] + "Z"
            dateS = str((datetime.datetime.today() - datetime.timedelta(days=15)).isoformat("T"))
            dateS = dateS[0:len(dateS) - 3] + "Z"
            for id in self.ORGID:
                link = self.AUDIT_EVENT_API + id + "&from=" + dateS + "&to=" + dateE + "&max=" + self.PAGING
                check = True
                while (check):
                    contents_audit = self.getReq(link)
                    contents_audit_json = json.loads(contents_audit.read())
                    apiHit=apiHit+1
                    count = count + len(contents_audit_json['items'])
                    if ("Link" in contents_audit.info()):
                        linkTemp = contents_audit.info().get('Link')
                        start = linkTemp.find("<") + 1
                        end = linkTemp.find(">")
                        link = linkTemp[start:end]
                    else:
                        check = False
            self.data["Admin Audit Events"] = count
        except Exception as e:
            self.msg = "Admin Audit Events Fetch Exception"
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "Admin Audit Event Count,"+str(apiHit)+","+str(time.time()-start)+"\n"

    def licenseListCount(self):
        try:
            apiHit = 0;
            start = time.time()
            link=self.LISENCES_API
            contents_licenses = self.getReq(link).read()
            apiHit=apiHit+1
            contents_licenses_json = json.loads(contents_licenses)
            for i in range(0, len(contents_licenses_json['items'])):
                self.data[contents_licenses_json['items'][i]['name'] + " Total Units"] = \
                    contents_licenses_json['items'][i]['totalUnits']
                self.data[contents_licenses_json['items'][i]['name'] + " Consumed Units"] = \
                    contents_licenses_json['items'][i]['consumedUnits']

        except Exception as e:
            self.msg = "License list fetch Exception"
            self.plugin_perf += link+" "+str(e)+"\n"

        finally:
            self.plugin_perf += "License List Count,"+str(apiHit)+","+str(time.time()-start)+"\n"

    def resourceGrpMembershipCount(self):
        try:
            link = self.RESOURCE_GRP_MEMBERSHISP_API
            apiHit = 0;
            start = time.time()
            contents_org_membership = self.getReq(link).read()
            apiHit=apiHit+1
            contents_org_membership_json = json.loads(contents_org_membership)
            countPending = 0
            countActivated = 0
            countError = 0
            for i in range(len(contents_org_membership_json['items'])):
                status = contents_org_membership_json['items'][i].get("status")
                if (status == "activated"):
                    countActivated = countActivated + 1
                if (status == "pending"):
                    countPending = countPending + 1
                if (status == "error"):
                    countError = countError + 1

            self.data['Resource Group Membership Active'] = countActivated
            self.data['Resource Group Membership Pending'] = countActivated
            self.data['Resource Group Membership Error'] = countError
        except Exception as e:
            self.msg = "Resource Group Membership fetch Exception"
            self.plugin_perf += link+" "+str(e)+"\n"
        finally:
            self.plugin_perf += "License List Count,"+str(apiHit)+","+str(time.time()-start)+"\n"

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

            self.data["msg"] = str(
                 e)  ###OPTIONAL- Set the custom message to be displayed in the "Errors" field of Log Report
        return self.data

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


