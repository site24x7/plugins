

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import javax.management.MBeanAttributeInfo;
import javax.management.MBeanInfo;
import javax.management.MBeanServerConnection;
import javax.management.ObjectInstance;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

public class JVMMonitoring {

	private static final String JMX_URL = "service:jmx:rmi:///jndi/rmi://[%s]:%d/jmxrmi";
	private JMXConnector jmxConnector = null;
	private MBeanServerConnection mBeanServerConnection = null;
	
	private static String pluginVersion = "1";
	private static String heartbeat = "false";
	private String host = "127.0.0.1";
	private int port = 7199;

	Map<String, Object> metrics = new LinkedHashMap<String, Object>();
	HashMap<String,String> keymap = new HashMap<>();

	ArrayList<MBeanAttributeInfo> list = new ArrayList<MBeanAttributeInfo>();

	public static void main(String[] args) {
		JVMMonitoring monitor = new JVMMonitoring();
		try {
			
			if(args.length ==0 || args.length == 2){
				if(args.length == 2){
					monitor.host = args[0];
					monitor.port = Integer.parseInt(args[1]);
				}
				
				monitor.connect();
				int i = 0;
				
				int limit = 25;
				int len = monitor.metrics.size();
				for (String key : monitor.metrics.keySet()) {
					if (i < (limit-1) || i<(len-2)) {
						System.out.print(key + ":" + monitor.metrics.get(key) + "|");
					} else {
						break;
					}
					
					i++;
				}
				System.out.print("plugin_version:"+pluginVersion+"|heartbeat_required:"+heartbeat);

			}
						
		} catch (Exception e) {
			System.out.println("status:0|msg:" + e.getMessage());
		}
	}

	public void connect() throws Exception {
		FileInputStream in = null;
		BufferedReader reader = null;
		
		
		try {
			JMXServiceURL jmxurl = new JMXServiceURL(String.format(JMX_URL, host, port));
			Map<String, Object> env = new HashMap<String, Object>();
			jmxConnector = JMXConnectorFactory.connect(jmxurl, env);
			mBeanServerConnection = jmxConnector.getMBeanServerConnection();
			
			keymap.put("ProcessCpuLoad", "CPU Usage");
			keymap.put("TotalLoadedClassCount", "Classes Loaded");
			keymap.put("UnloadedClassCount", "Classes Unloaded");
			keymap.put("FreePhysicalMemorySize", "Runtime Free Memory");//MB
			keymap.put("TotalPhysicalMemorySize", "Runtime Total Memory");//MB
			keymap.put("TotalCompilationTime", "Compilation Time");//ms
			
			keymap.put("DaemonThreadCount", "Daemon threads");
			keymap.put("ThreadCount", "Live threads");
			keymap.put("PeakThreadCount", "Peak threads");
			keymap.put("TotalStartedThreadCount", "Total Started Threads");//Sleeping threads
			keymap.put("CurrentThreadUserTime", "User Time");//ms
			keymap.put("CurrentThreadCpuTime", "CPU Time");//ms
			
			keymap.put("CollectionCount", "Collections Count");
			keymap.put("CollectionTime", "Time Spent");//ms
			
			
			HashMap<String, Properties> map = new HashMap<>();
						
			
			Properties osprop = new Properties();
			osprop.put("metrics", new String[]{"ProcessCpuLoad","FreePhysicalMemorySize","TotalPhysicalMemorySize"});
			map.put("java.lang:type=OperatingSystem", osprop);
			
			Properties threadprop = new Properties();
			threadprop.put("metrics",  new String[]{"DaemonThreadCount","ThreadCount","PeakThreadCount","TotalStartedThreadCount","CurrentThreadUserTime","CurrentThreadCpuTime"});
			map.put("java.lang:type=Threading",threadprop);
			
			Properties gcprop = new Properties();
			gcprop.put("metrics" ,new String[]{"CollectionCount","CollectionTime"});
			gcprop.put("name", new String[]{"Copy","MarkSweepCompact","ParNew","ConcurrentMarkSweep","PSScavenge","PSMarkSweep"});
			map.put("java.lang:type=GarbageCollector", gcprop);
		
			Properties compprop = new Properties();
			compprop.put("metrics" ,new String[]{"TotalCompilationTime"});
			map.put("java.lang:type=Compilation", compprop);
		
			Properties loadingprop = new Properties();
			loadingprop.put("metrics" ,new String[]{"TotalLoadedClassCount","UnloadedClassCount"});
			map.put("java.lang:type=ClassLoading", loadingprop);
			
			Properties runtimeprop = new Properties();
			runtimeprop.put("metrics" ,new String[]{"Uptime","VmName"});
			map.put("java.lang:type=Runtime", runtimeprop);
		
			for (String mBeanName : map.keySet()) {
				try {
					
					Properties props = map.get(mBeanName);
					
					if(props.containsKey("name")){
						String[] names = (String[])props.get("name");
						
						for(String name: names){
							getData(mBeanName.trim()+",name="+name.trim(),  Arrays.asList((String[])props.get("metrics")));
						}
					}else{
						getData(mBeanName,  Arrays.asList((String[])props.get("metrics")));
					}
					
					
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			
		} catch (Exception e) {
		
			//e.printStackTrace();
			System.out.println("status:0|errmsg:Cannot connect to " + host + " using port :" + port);
		} finally {
			if (in != null)
				in.close();

			if (reader != null)
				reader.close();

			if (jmxConnector != null)
				jmxConnector.close();
		}
		
	}

	public void getData(String mBeanName, List<String> list) throws Exception{

		NumberFormat formatter = new DecimalFormat("#0.00");
		ObjectName oname = new ObjectName(mBeanName);
		Set<ObjectInstance> instances = mBeanServerConnection.queryMBeans(oname, null);
		Iterator<ObjectInstance> iterator = instances.iterator();

		while (iterator.hasNext()) {
			ObjectInstance instance = iterator.next();
			
			try {
				MBeanInfo info = mBeanServerConnection.getMBeanInfo(instance.getObjectName());
				MBeanAttributeInfo[] attributes = info.getAttributes();
				
				for (MBeanAttributeInfo attribute : attributes) {
						try{
							
							Object obj = mBeanServerConnection.getAttribute(oname,attribute.getName());
							String key = attribute.getName();
							
							Hashtable<String, String> keyPropList = oname.getKeyPropertyList();
							if(list.contains(key)){
								String namekey = keymap.containsKey(key) ? ((keyPropList.size()>1) ? keyPropList.get("name") +" " + keymap.get(key) : keymap.get(key)) : key;
									
								if (obj instanceof Long || obj instanceof Double || obj instanceof Integer ) {
									metrics.put(namekey, formatter.format(obj));
								} else if (obj instanceof String) {
									metrics.put(namekey, (String) obj);
								} else if (obj instanceof Boolean){
									metrics.put(namekey, obj);
								}
								
							}
							
						}catch(Exception e){
							e.printStackTrace();
						}
							
				}
			} catch (NullPointerException e) {
				e.printStackTrace();
			}
		}
	
	}
}
