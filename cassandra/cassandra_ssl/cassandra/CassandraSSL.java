import javax.management.MBeanServerConnection;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import javax.management.ObjectName;
import javax.management.openmbean.CompositeData;
import javax.management.ObjectInstance;
import javax.management.MBeanAttributeInfo;
import javax.management.MBeanInfo;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.Arrays;
import javax.rmi.ssl.*;
import java.util.Set;
import org.json.simple.JSONObject; 

@SuppressWarnings({"deprecation", "unchecked"})
public class CassandraSSL {
    public static void main(String[] args) {
        try {
        
            JSONObject jsonObj = new JSONObject(); 
            
            if(args.length < 8)
            {
            	jsonObj.put("status",0);
            	jsonObj.put("msg","parameters are missing");
                System.out.println(jsonObj.toString());
            }            
            
            String hostname = args[0];
            String port = args[1];
            
            String jmxuser = args[2];
            String jmxpassword = args[3];
            
            String keyStore = args[4];
            String keyStorePassword = args[5];
            String trustStore = args[6];
            String trustStorePassword = args[7];
            
            
            
            Map<String, Object> env = new HashMap<>();
            String[] credentials = new String[] {jmxuser, jmxpassword};
            
            System.setProperty("javax.net.ssl.keyStore", keyStore);
            System.setProperty("javax.net.ssl.keyStorePassword", keyStorePassword);
            System.setProperty("javax.net.ssl.trustStore", trustStore);
            System.setProperty("javax.net.ssl.trustStorePassword", trustStorePassword);
            
            
            String jmxUrl = "service:jmx:rmi:///jndi/rmi://"+hostname+":"+port+"/jmxrmi";
            //String jmxUrl = "service:jmx:rmi:///jndi/rmi://localhost:7199/jmxrmi";
            HashMap<String,ArrayList> metrics = new HashMap<String,ArrayList>();
            
            metrics.put("Total Latency (Read)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=TotalLatency","Count")));
            metrics.put("Total Latency (Write)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=TotalLatency","Count")));
            metrics.put("Cross Node Latency",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Messaging,name=CrossNodeLatency","Count")));
            metrics.put("Total Hints",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Storage,name=TotalHints","Count")));
            metrics.put("Throughtput (Writes)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency","Count")));
            
            metrics.put("Throughtput (Read)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency","Count")));
            metrics.put("Key cache hit rate",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Cache,scope=KeyCache,name=Hits","Count")));
            metrics.put("Load",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Storage,name=Load","Count")));
            metrics.put("Completed compaction tasks",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Compaction,name=CompletedTasks","")));
            metrics.put("Pending campaction tasks",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Compaction,name=PendingTasks","")));
            metrics.put("ParNew garbage collections (count)",new ArrayList<>(Arrays.asList("java.lang:type=GarbageCollector,name=ParNew","CollectionCount")));
            metrics.put("ParNew garbage collections (time)",new ArrayList<>(Arrays.asList("java.lang:type=GarbageCollector,name=ParNew","CollectionTime")));
            metrics.put("CMS garbage collections (count)",new ArrayList<>(Arrays.asList("java.lang:type=GarbageCollector,name=ConcurrentMarkSweep","CollectionCount")));
            metrics.put("CMS garbage collections (time)",new ArrayList<>(Arrays.asList("java.lang:type=GarbageCollector,name=ConcurrentMarkSweep","CollectionTime")));
            metrics.put("Exceptions",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Storage,name=Exceptions","")));
            metrics.put("Timeout exceptions (write)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Timeouts","Count")));
            metrics.put("Timeout exception (read)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Timeouts","Count")));
            metrics.put("Unavailable exceptions (write)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Unavailables","Count")));
            metrics.put("Unavailable exceptions (read)",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Unavailables","Count")));
            metrics.put("Pending tasks",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Compaction,name=PendingTasks","")));
            metrics.put("Dropped Mutations",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Table,name=DroppedMutations","")));
            metrics.put("Pending Flushes",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=Table,name=PendingFlushes","")));
            metrics.put("Blocked On Allocation",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=MemtablePool,name=BlockedOnAllocation","Count")));
            metrics.put("Currently Blocked Tasks",new ArrayList<>(Arrays.asList("org.apache.cassandra.metrics:type=ThreadPools,path=internal,scope=MemtableFlushWriter,name=CurrentlyBlockedTasks","")));
	    
	    jsonObj.put("plugin_version",1);
	    jsonObj.put("heartbeat_required","true");
	    

            // Set JMX environment properties
            //Map<String, Object> env = new HashMap<>();
            //String[] credentials = new String[] {"site24x7", "plugin123"};
            env.put(JMXConnector.CREDENTIALS, credentials);
	    env.put("com.sun.jndi.rmi.factory.socket", new SslRMIClientSocketFactory());

            // SSL properties
            /*System.setProperty("javax.net.ssl.keyStore", "/home/murali/cassandra/cassandra4.0.13/conf/NewCerts/cassandra4.keystore.jks");
            System.setProperty("javax.net.ssl.keyStorePassword", "cassandra");
            System.setProperty("javax.net.ssl.trustStore", "/home/murali/cassandra/cassandra4.0.13/conf/NewCerts/cassandra4.truststore.jks");
            System.setProperty("javax.net.ssl.trustStorePassword", "cassandra");*/

            // Connect to the JMX server
            JMXServiceURL serviceURL = new JMXServiceURL(jmxUrl);
            JMXConnector jmxConnector = JMXConnectorFactory.connect(serviceURL, env);
            MBeanServerConnection mbeanServerConnection = jmxConnector.getMBeanServerConnection();
            
            collectMetrics(mbeanServerConnection,metrics,jsonObj);
            System.out.println(jsonObj.toString());
            
            // Close the connection
            jmxConnector.close();
        } catch (Exception e) {
                JSONObject jsonObj = new JSONObject(); 
                jsonObj.put("status",0);
            	jsonObj.put("msg",e);
                System.out.println(jsonObj.toString());
        }
    }
    
    
    private static void collectMetrics(MBeanServerConnection mbeanServerConnection, HashMap<String,ArrayList> metrics, JSONObject jsonObj) throws Exception {
        
        for(Map.Entry<String,ArrayList> metric : metrics.entrySet())
        {
        	String metricDisplayName = metric.getKey();

		ArrayList attributeList = (ArrayList) metric.getValue();
		        	
        	String mBean = (String) attributeList.get(0);
        	String attributeName = (String) attributeList.get(1);
        	ObjectName mbeanName = new ObjectName(mBean);
        	if(!attributeName.equals(""))
        	{
        		 attributeName =(String) attributeList.get(1);
        	}
        	else{
        		MBeanInfo mbeanInfo = mbeanServerConnection.getMBeanInfo(mbeanName);
        		attributeName = mbeanInfo.getAttributes()[0].getName();
        	}
        	
        	
        	Object attributeValue = mbeanServerConnection.getAttribute(mbeanName, attributeName);
        	jsonObj.put(metricDisplayName,attributeValue);
        	
        	//System.out.println(metricDisplayName + " = " + attributeValue);
        }

        
    }

    private static void listTotalLatencyAttributes(MBeanServerConnection mbeanServerConnection) throws Exception {
        // Define the specific MBean for Total Latency
        ObjectName mbeanName = new ObjectName("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=TotalLatency");

        // Get MBeanInfo for the specified MBean
        MBeanInfo mbeanInfo = mbeanServerConnection.getMBeanInfo(mbeanName);

        // List all attributes
        MBeanAttributeInfo[] attributeInfos = mbeanInfo.getAttributes();
        System.out.println("Attribute:555 " + mbeanInfo.getAttributes()[0].getName());
        
        for (MBeanAttributeInfo attributeInfo : attributeInfos) {
            System.out.println("Attribute: " + attributeInfo.getName() + ", Type: " + attributeInfo.getType() + ", Description: " + attributeInfo.getDescription());
        }
    }
    private static void printClientRequestReadMetrics(MBeanServerConnection mbeanServerConnection) throws Exception {
        // Define the specific MBean for ClientRequest Read metrics
        ObjectName mbeanName = new ObjectName("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=*");

        // Get all attributes for this MBean
        Set<ObjectName> mbeanNames = mbeanServerConnection.queryNames(mbeanName, null);

        for (ObjectName objectName : mbeanNames) {
            for (String attributeName : mbeanServerConnection.getAttributes(objectName, null).asList().stream().map(a -> a.getName()).toArray(String[]::new)) {
                Object attributeValue = mbeanServerConnection.getAttribute(objectName, attributeName);

                if (attributeValue instanceof CompositeData) {
                    CompositeData compositeData = (CompositeData) attributeValue;
                    for (String key : compositeData.getCompositeType().keySet()) {
                        System.out.println(objectName + " - " + attributeName + "." + key + " = " + compositeData.get(key));
                    }
                } else {
                    System.out.println(objectName + " - " + attributeName + " = " + attributeValue);
                }
            }
        }
    }
}
