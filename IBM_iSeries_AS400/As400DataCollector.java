import com.ibm.as400.access.*;
import java.util.*;
import org.json.JSONObject;    

public class As400DataCollector {
	@SuppressWarnings({"deprecation"})
	
	public static void main(String args[])
	{
	        	JSONObject data = new JSONObject();
	        	String PLUGIN_VERSION = args[0];
            		String HEARTBEAT_REQUIRED = args[1];
	        	data.put("plugin_version",PLUGIN_VERSION);
            		data.put("heartbeat_required", HEARTBEAT_REQUIRED);
			String hostname = args[2];
			String username = args[3];
			String password = args[4];

			try
			{
				AS400 as400 = new AS400(hostname, username, password);
				as400.setGuiAvailable(false);
				as400.validateSignon();
				SystemStatus sysstat = new SystemStatus(as400);
				float  sppoll=0,uncpu=0,sppollz=0,uncpuz=0;
                               data.put("ASP Percentage",sysstat.getPercentSystemASPUsed());
                               data.put("ASP Total",String.valueOf(sysstat.getSystemASP())+"_MB");
                               data.put("CPU Percentage",sysstat.getPercentProcessingUnitUsed());
                               data.put("Permanent Address Percentage",sysstat.getPercentPermanentAddresses());
                               data.put("Temporary Address Percentage",sysstat.getPercentTemporaryAddresses());
                               data.put("Current Unprotected Used",sysstat.getCurrentUnprotectedStorageUsed());
                               data.put("Maximum Unprotected",sysstat.getMaximumUnprotectedStorageUsed());
                               data.put("Main Storage",sysstat.getMainStorageSize());
                               data.put("Number Of Processors",sysstat.getNumberOfProcessors());
                               data.put("Number of Pools",sysstat.getPoolsNumber());
                               data.put("Users SignedOn",sysstat.getUsersCurrentSignedOn());
                               data.put("Total Jobs",sysstat.getJobsInSystem());
                               data.put("No of Active Jobs",sysstat.getActiveJobsInSystem());
                               data.put("No of Batch Jobs",sysstat.getBatchJobsRunning());
                               data.put("Jobs Waiting for Message",sysstat.getBatchJobsWaitingForMessage());
                               data.put("Active Threads",sysstat.getActiveThreadsInSystem());
                               data.put("Batch Jobs Waiting to Print",sysstat.getBatchJobsEndedWithPrinterOutputWaitingToPrint());
                               data.put("Batchjobs Ending",sysstat.getBatchJobsEnding());
                               data.put("Batchjobs Held on Jobqueue",sysstat.getBatchJobsHeldOnJobQueue());
                               data.put("Batchjobs Held While Running",sysstat.getBatchJobsHeldWhileRunning());
                               data.put("Batchjobs on Held Jobqueue",sysstat.getBatchJobsOnAHeldJobQueue());
                               data.put("Batchjobs on Unassigned Jobqueue",sysstat.getBatchJobsOnUnassignedJobQueue());
                               data.put("Batchjobs Waitingto Run",sysstat.getBatchJobsWaitingToRunOrAlreadyScheduled());
                               data.put("No of Partitions",sysstat.getNumberOfPartitions());
                               data.put("Total Auxiliary Storage",sysstat.getTotalAuxiliaryStorage());
                               data.put("User Sessions Ended for Waiting to Print",sysstat.getUsersSignedOffWithPrinterOutputWaitingToPrint());
                               data.put("User Suspended by Groupjobs",sysstat.getUsersSuspendedByGroupJobs());
                               data.put("User Suspended by Systemrequest",sysstat.getUsersSuspendedBySystemRequest());
                               data.put("Users Temporarily Signedoff",sysstat.getUsersTemporarilySignedOff());
                               data.put("Current Processing Capacity",sysstat.getCurrentProcessingCapacity());
                               data.put("Current Interactive Performance Percentage",sysstat.getPercentCurrentInteractivePerformance());
                               data.put("Maximum Jobs",String.valueOf(sysstat.getMaximumJobsInSystem()));
                               sppoll=sysstat.getPercentSharedProcessorPoolUsed();
                               uncpu=sysstat.getPercentUncappedCPUCapacityUsed();
                               if(sppoll<0)
                               {
                                   data.put("Shared Processing Pooler",sppollz);
                               }
                               else
                               {
                                   data.put("Shared Processing Pooler",sppoll);
                               }
                               if(uncpu<0)
                               {
                                   data.put("Uncapped CPU Capacity Percentage",uncpuz);
                               }
                               else
                               {
                                   data.put("Uncapped CPU Capacity Percentage",uncpu);
                               }
                               
                               
                               SystemValue sv=null;
                               SystemValueList svl = new SystemValueList(as400);
                               Map<String,Object> p = new HashMap<String,Object>();
                               Vector v = svl.getGroup(SystemValueList.GROUP_ALL);
                               Enumeration list = v.elements();
                               while (list.hasMoreElements())
                               {
                                   sv=(SystemValue)list.nextElement();
                                   p.put(sv.getName(),sv.getValue());
                               }
                               data.put("System Name",p.get("SYSNAME"));
                               data.put("Model",p.get("QMODEL")+" "+p.get("QPRCFEAT"));
                               data.put("System Version","V"+as400.getVersion()+"R"+as400.getRelease()+"M"+as400.getModification());
                               data.put("Serial",p.get("QSRLNBR"));
                               data.put("Security Level",p.get("QSECURITY"));
                               data.put("Auto Device Configuration",String.valueOf(p.get("QAUTOCFG")));
                               data.put("System Console",p.get("QCONSOLE"));
                               data.put("Job Message Queue Initial Size",String.valueOf(p.get("QJOBMSGQSZ"))+"_kb");
                               data.put("Job Message Queue Maximum Size",String.valueOf(p.get("QJOBMSGQTL"))+"_kb");
                               data.put("Spooling Control Initial Size",String.valueOf(p.get("QJOBSPLA"))+"_bytes");
                              as400.disconnectAllServices();
                              JSONObject unit = new JSONObject();
                              unit.put("ASP Percentage","%");
                              unit.put("CPU Percentage","%");
                              unit.put("Permanent Address Percentage","%");
                              unit.put("Temporary Address Percentage","%");
                              unit.put("Current Unprotected Used","MB");
                              unit.put("Maximum Unprotected","MB");
                              unit.put("Main Storage","kb");
                              unit.put("Total Auxiliary Storage","MB");
                              unit.put("Current Interactive Performance Percentage","%");
                              unit.put("Shared Processing Pooler","%");
                              unit.put("Uncapped CPU Capacity Percentage","%");
                              data.put("units",unit);
                              System.out.println(data);
			}
			catch(Exception e)
			{
				//System.out.println("Error while connecting AS400");
				data.put("msg",e.toString());
				data.put("status",0);
				System.out.println(data);
			}
	}

}
