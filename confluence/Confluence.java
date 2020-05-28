import javax.management.MBeanAttributeInfo;
import javax.management.MBeanInfo;
import javax.management.MBeanServerConnection;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

import java.util.Arrays;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

public class Confluence {
	public static String host, port, pluginVersion, heartbeatRequired;
	public static void main(String[] args) {
		try {
			if(args.length == 4){
				host = args[0];
				port = args[1];
				pluginVersion = args[2];
				heartbeatRequired = args[3];
			}
			MBeanServerConnection connection = getServerConnection();
			ObjectName query = new ObjectName("Confluence:*");
			Set<ObjectName> mbeans = connection.queryNames(query, null);
			printJmxAttributes(mbeans, connection);
		}
		catch(Exception e){
		}
	}

	private static MBeanServerConnection getServerConnection() {
		MBeanServerConnection connection = null;
		try{
			JMXServiceURL jmxurl = new JMXServiceURL("service:jmx:rmi:///jndi/rmi://"+host+":"+port+"/jmxrmi");
			Map<String, String[]> env = new HashMap<String, String[]>();
			if((System.getenv("RMI_UNAME") != null && System.getenv("RMI_PASSWORD") != null) && (System.getenv("RMI_UNAME").length() > 0 && System.getenv("RMI_PASSWORD").length() > 0)){
				String[] credentials = {System.getenv("RMI_UNAME"), System.getenv("RMI_PASSWORD")};
				env.put(JMXConnector.CREDENTIALS, credentials);
			}
			JMXConnector jmxConnector = JMXConnectorFactory.connect(jmxurl, env);
			connection = jmxConnector.getMBeanServerConnection();
		}
		catch(Exception e){
			String errorMessage = "{" +
				String.format("\n\t\"plugin_version\" : \"%s\",", pluginVersion) +
				String.format("\n\t\"heartbeat_required\" : \"%s\"", heartbeatRequired) +
				"\n\t\"status\" : 0" +
				"\n\t\"msg\" : \"" + e.toString().trim().replace("\n", "") +"\"" +
				"\n}";
			System.out.println(errorMessage);
			System.exit(0);
		}
		return connection;
	}

	private static void printJmxAttributes(Set<ObjectName> mbeans, MBeanServerConnection connection){
		System.out.print("{");
		System.out.print(String.format("\n\t\"plugin_version\" : \"%s\",\n", pluginVersion));
		System.out.print(String.format("\t\"heartbeat_required\" : \"%s\"", heartbeatRequired));
		String value = "";
		boolean isValue;
		List<String> ignoreMetrics = new ArrayList<String>();
		ignoreMetrics.add("CacheStatistics");
		ignoreMetrics.add("SchedulingStatistics");
		ignoreMetrics.add("SystemInformation");
		String units = "\t\"units\": {" +
			"\n\t\t\"IndexingStatistics.LastElapsedMilliseconds\" : \"ms\"," +
			"\n\t\t\"RequestMetrics.AverageExecutionTimeForLastTenSeconds\" : \"ms\"" +
			"\n\t}";
		try
		{
			for (ObjectName mbean : mbeans) {
				isValue = false;
				if(!isStringInArrayList(ignoreMetrics, mbean.toString())){
					ObjectName oname = new ObjectName(mbean.toString());
					MBeanInfo info = connection.getMBeanInfo(oname);
					Set<MBeanAttributeInfo> attributes = new HashSet<MBeanAttributeInfo>(Arrays.asList(info.getAttributes()));
					for (MBeanAttributeInfo attribute : attributes) {
						Object obj;
						if(attribute.getName().equals("Value")){
							isValue = true;
							obj = connection.getAttribute(oname,attribute.getName());
							value = obj.toString();
							continue;
						}
						System.out.print(",");
						if(isValue){
							isValue = false;
							obj = connection.getAttribute(oname,attribute.getName());
							System.out.print("\n\t\"" + obj + "\" : \"" + value + "\"");
						}
						else{
							obj = connection.getAttribute(oname,attribute.getName());
							System.out.print("\n\t\"" + mbean.toString().substring("Confluence:name=".length()) + "." + attribute.getName() + "\" : \"" + obj + "\"");
						}
					}
				}
			}
			System.out.print(",\n");
			System.out.print(units);
			System.out.print("\n}\n");
		}
		catch(Exception e){}
	}
	private static boolean isStringInArrayList(List<String> ignoreMetrics, String metricName){
		for(String toIgnore : ignoreMetrics){
			if(metricName.contains(toIgnore)){
				return true;
			}
		}
		return false;
	}
}
