//$Id$

import java.util.Map;

import javax.management.MBeanServerConnection;
import javax.management.ObjectName;
import javax.management.openmbean.CompositeData;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

/***
 * 
 * This Plugin executes the MulePlugin JAVA class to get the mule server details to monitor
 * @author anita
 *
 */
public class MulePlugin
{
	private final static char DELIMITER = '|';
	
	private final static char KEY_VALUE_SEPARATOR = ':';
	
	public static void main(String[] args)
	{
		/** Mule server Configurations **/
		String remoteHost = "localhost";
		int remotePort = 9999;
		
		/* Credentials to connect to the remote JMX port */
		Map<String, Object> jmxCredentials = null; 
		//jmxCredentials = new HashMap<String, Object>();
		//jmxCredentials.put("jmx.remote.credentials", new String[]{"user","pswd"});
		
		/*
		 * This variable will hold the required output data
		 * The values are formatted based on the description mentioned in below link
		 * 
		 * https://www.site24x7.com/help/admin/adding-a-monitor/plugins/custom-plugins.html#Shell
		 */
		StringBuilder data = new StringBuilder();
		
		try {
			JMXServiceURL jmxURL = new JMXServiceURL("service:jmx:rmi:///jndi/rmi://" + remoteHost + ":" + remotePort +"/jmxrmi");
			
			JMXConnector jmxConnector = JMXConnectorFactory.newJMXConnector(jmxURL, jmxCredentials);
			jmxConnector.connect();
			
			MBeanServerConnection mbean = jmxConnector.getMBeanServerConnection();
			
			/*
			 * Heap Memory Usage
			 */
			Object memoryMbean = mbean.getAttribute(new ObjectName("java.lang:type=Memory"), "HeapMemoryUsage");
			CompositeData cd = (CompositeData) memoryMbean;
			
			data.append("memory_usage");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(((Long)cd.get("used"))/(1024*1024));
			
			/*
			 * Fetching application level metrics of 'default' application 
			 */
			ObjectName application_totals = new ObjectName("Mule.default:type=Application,name=\"application totals\"");
			
			data.append(DELIMITER);
			
			data.append("min_processing_time");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "MinProcessingTime"));
			
			data.append(DELIMITER);
			
			data.append("max_processing_time");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "MaxProcessingTime"));
			
			data.append(DELIMITER);
			
			data.append("avg_processing_time");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "AverageProcessingTime"));
			
			data.append(DELIMITER);
			
			data.append("processed_events");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "ProcessedEvents"));
			
			data.append(DELIMITER);
			
			data.append("sync_events_received");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "SyncEventsReceived"));
			
			data.append(DELIMITER);
			
			data.append("async_events_received");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "AsyncEventsReceived"));
			
			data.append(DELIMITER);
			
			data.append("execution_errors");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "ExecutionErrors"));
			
			data.append(DELIMITER);
			
			data.append("fatal_errors");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(application_totals, "FatalErrors"));
			
			System.out.println(data.toString());
		}
		catch (Exception e)
		{
			//do Nothing
		}
	}
}
