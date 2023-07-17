#!/usr/bin/python3
import requests
import datetime
import json

PLUGIN_VERSION = 1
HEARTBEAT = True
METRIC_UNITS = { "Committed Virtual Memory Size": "GB",
 "Total Swap Space Size": "GB",
 "Free Swap Space Size": "GB",
 "Process Cpu Time": "s",
 "Total Physical Memory Size": "GB",
 "Process Cpu Load": "%",
 "System Cpu Load": "%",
 "Free Physical MemorySize": "GB",
 "Number Of Cores": "cores",
 "Heap Memory Usage": "GB",
 "None Heap Memory Usage": "GB",
 "Heap Memory Max":"GB",
 "JVM Up Time": "ms",
 "Thread Count": "threads",
 "Days Till Licence Expiry" : "days",
 "No of Respositories" : "repositories"
}



class JFrogArtifactory:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.info={}
        self.storageinfo={}
        self.package={}
        self.users=0
        self.groups=0
        self.api_key = args.api_key
        self.artifactory_url = args.artifactory_url

    def get_artifactory_info(self):
    
        try:
            url = f"{self.artifactory_url}/api/system/ping"          
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                info = response.json()
                self.maindata['status'] = 1
                self.maindata['msg'] = 'Artifactory is accessible'
                
            else:
                self.maindata['status'] = 0
                self.maindata['msg'] = 'Failed to retrieve Artifactory information'
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            #print(e)
            
    def bytes_to_gb(self,bytes):
    
        gb = bytes / (1024 ** 3)  # Divide by 1024^3 to convert bytes to GB
        gb = round(gb, 2) 
        return gb
        
        
    def get_users_info(self):
    
        try:
           users_url = f"{self.artifactory_url}/api/security/users"
           headers = {"Authorization": f"Bearer {self.api_key}"}
           response = requests.get(users_url, headers=headers)
           groups_url = f"{self.artifactory_url}/api/security/groups"
           response1 = requests.get(groups_url, headers=headers)
           license_url = f"{self.artifactory_url}/api/system/licenses" 
           response2 = requests.get(license_url, headers=headers) 
           if response.status_code == 200:
                self.maindata['Security Users']= len(response.json())
                self.maindata['Security Groups']= len(response1.json())
                self.maindata.update(response2.json())
                expiry_date = datetime.datetime.strptime(self.maindata["validThrough"], "%b %d, %Y")
                current_date = datetime.datetime.now()
                self.maindata['Days Till Licence Expiry']=(expiry_date - current_date).days
                
              
           else:
                self.maindata['status'] = 0
                self.maindata['msg'] = 'Failed to retrieve Artifactory information'
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            #print(e)
            
            
    def get_artifactory_metrics(self):
    
        try:
            url = f"{self.artifactory_url}/api/system/info"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                self.info.update(response.json())
                self.maindata['Committed Virtual Memory Size']=self.bytes_to_gb(self.info['committedVirtualMemorySize'])
                self.maindata['Total Swap Space Size']=self.bytes_to_gb(self.info['totalSwapSpaceSize'])
                self.maindata['Free Swap Space Size']=self.bytes_to_gb(self.info['freeSwapSpaceSize'])
                self.maindata['Process Cpu Time']=self.info['processCpuTime']
                self.maindata['Total Physical Memory Size']=self.bytes_to_gb(self.info['totalPhysicalMemorySize'])
                self.maindata['Open File Descriptor Count']=self.info['openFileDescriptorCount']
                self.maindata['Max File Descriptor Count']=self.info['maxFileDescriptorCount']
                self.maindata['Process Cpu Load']=self.info['processCpuLoad']
                self.maindata['System Cpu Load']=self.info['systemCpuLoad']
                self.maindata['Free Physical MemorySize']=self.bytes_to_gb(self.info['freePhysicalMemorySize'])
                self.maindata['Number Of Cores']=self.info['numberOfCores']
                self.maindata['Heap Memory Usage']=self.bytes_to_gb(self.info['heapMemoryUsage'])
                self.maindata['None Heap Memory Usage']=self.bytes_to_gb(self.info['noneHeapMemoryUsage'])
                self.maindata['Heap Memory Max']=self.bytes_to_gb(self.info['heapMemoryMax'])
                self.maindata['JVM Up Time']=self.info['jvmUpTime']
                self.maindata['Thread Count']=self.info['threadCount']
                
            else:
            
                self.maindata['status'] = 0
                self.maindata['msg'] = 'Failed to retrieve repository stats'

        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            
    def get_repository_stats(self):
    
        try:
        
            url = f"{self.artifactory_url}/api/storageinfo"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.storageinfo.update(response.json())
                repositories = self.storageinfo['repositoriesSummaryList'] 
                self.maindata['No of Respositories']=len(repositories)
                space=self.storageinfo["fileStoreSummary"]["totalSpace"].split(' ')
                self.maindata['Total Space']= space[0]
                METRIC_UNITS['Total Space']=space[1]
                space=self.storageinfo["fileStoreSummary"]["freeSpace"].split(' ')
                self.maindata['Free Space']= space[0]
                METRIC_UNITS['Free Space']=space[1]
                METRIC_UNITS['Free Space in %']='%'
                self.maindata['Free Space in %']= space[2].replace('%)','').replace('(','')
                space=self.storageinfo["fileStoreSummary"]["usedSpace"].split(' ')
                self.maindata['Used Space']= space[0]
                METRIC_UNITS['Used Space']=space[1]
                METRIC_UNITS['Used Space in %']='%'
                self.maindata['Used Space in %']= space[2].replace('%)','').replace('(','')
                space=self.storageinfo["binariesSummary"]["binariesSize"].split(' ')
                self.maindata['Binaries Size']= space[0]
                METRIC_UNITS['Binaries Size']=space[1]
                space=self.storageinfo["binariesSummary"]["artifactsSize"].split(' ')
                self.maindata['Artifacts Size']= space[0]
                METRIC_UNITS['Artifacts Size']=space[1]
                space=self.storageinfo["binariesSummary"]["optimization"].split('%')
                self.maindata['Optimization']= space[0]
                METRIC_UNITS['Optimization']='%'
                self.maindata['Binaries Count']= self.storageinfo["binariesSummary"]["binariesCount"]
                repo_stats = {}
                
                for repo in repositories:  
                   if repo['repoType'].capitalize()+' Repository Count' not in self.package:
                       self.package[(repo['repoType'].capitalize()+' Repository Count')]=1
                   else:
                        self.package[(repo['repoType'].capitalize()+' Repository Count')]+=1
                        
        except Exception as e:
        
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            #print(e)           

    def collect_metrics(self):

        self.get_artifactory_info()
        self.get_artifactory_metrics()
        self.get_repository_stats()
        self.get_users_info()
        self.maindata.update(self.package)
        self.maindata['units']= METRIC_UNITS
        
        if self.maindata['status'] == 0:
           if len(self.info) > 0 and self.maindata['msg'] == "Expecting value: line 1 column 1 (char 0)" :
              self.maindata['status'] = 1
              self.maindata['msg'] = 'Artifactory is accessible'
             
        return self.maindata
            
            
            
            
if __name__ == "__main__":

    api_key = "None"
    artifactory_url = "http://127.0.1.1:8082/artifactory"

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', help='JFrog Artifactory API Key', default=api_key)
    parser.add_argument('--artifactory_url', help='JFrog Artifactory URL', default=artifactory_url)
    args = parser.parse_args()

    obj = JFrogArtifactory(args)
    result = obj.collect_metrics()
    print(json.dumps(result, indent=True))
    
