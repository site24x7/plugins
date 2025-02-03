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
import javax.management.openmbean.CompositeData;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

public class JVMMonitoring {

	private static final String JMX_URL = "service:jmx:rmi:///jndi/rmi://%s:%d/jmxrmi";
	private JMXConnector jmxConnector = null;
	private MBeanServerConnection mBeanServerConnection = null;
	
	private static String pluginVersion = "1";
	private static String heartbeat = "true";
	private static String host = "127.0.0.1";
	private static int port = 7199;

	Map<String, Object> metrics = new LinkedHashMap<String, Object>();
	HashMap<String,String> keymap = new HashMap<>();

	ArrayList<MBeanAttributeInfo> list = new ArrayList<MBeanAttributeInfo>();

	public static void main(String[] args) {
		JVMMonitoring monitor = new JVMMonitoring();
		try {
			
			if (args.length == 4) {
                host = args[0];
                port = Integer.parseInt(args[1]);
                pluginVersion = args[2];
                heartbeat = args[3]; 

            } else {
                System.out.println("Usage: JVMMonitoring <host> <port> <plugin_version> <heartbeat_required>");
                return;
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
				System.out.print("plugin_version:"+pluginVersion+"|heartbeat_required:"+heartbeat+"|");
				Map<String, String> unitsMap = new HashMap<>();
				unitsMap.put("Classes Unloaded", "class");
				unitsMap.put("Classes Loaded", "class");
				unitsMap.put("Uptime", "ms");
				unitsMap.put("Runtime Free Memory", "bytes");
				unitsMap.put("Runtime Total Memory", "bytes");
				unitsMap.put("CPU Usage", "%");
				unitsMap.put("CPU Time", "ns");
				unitsMap.put("User Time", "ns");
				unitsMap.put("Compilation Time", "ms");
				unitsMap.put("Heap Committed", "bytes");
				unitsMap.put("Heap Max", "bytes");
				unitsMap.put("Heap Used", "bytes");
				unitsMap.put("Non Heap Committed", "bytes");
				unitsMap.put("Non Heap Max", "bytes");
				unitsMap.put("Non Heap Used", "bytes");
				unitsMap.put("Compressed Class Space,type=MemoryPool Committed", "bytes");
				unitsMap.put("Compressed Class Space,type=MemoryPool Max", "bytes");
				unitsMap.put("Compressed Class Space,type=MemoryPool Used", "bytes");
				unitsMap.put("Metaspace,type=MemoryPool Committed", "bytes");
				unitsMap.put("Metaspace,type=MemoryPool Max", "bytes");
				unitsMap.put("Metaspace,type=MemoryPool Used", "bytes");
				unitsMap.put("CodeHeap 'non-nmethods',type=MemoryPool Committed", "bytes");
				unitsMap.put("CodeHeap 'non-nmethods',type=MemoryPool Max", "bytes");
				unitsMap.put("CodeHeap 'non-nmethods',type=MemoryPool Used", "bytes");
				unitsMap.put("CodeHeap 'profiled nmethods',type=MemoryPool Committed", "bytes");
				unitsMap.put("CodeHeap 'profiled nmethods',type=MemoryPool Max", "bytes");
				unitsMap.put("CodeHeap 'profiled nmethods',type=MemoryPool Used", "bytes");
				unitsMap.put("G1 Eden Space,type=MemoryPool Committed", "bytes");
				unitsMap.put("G1 Eden Space,type=MemoryPool Max", "bytes");
				unitsMap.put("G1 Eden Space,type=MemoryPool Used", "bytes");
				unitsMap.put("G1 Old Gen,type=MemoryPool Committed", "bytes");
				unitsMap.put("G1 Old Gen,type=MemoryPool Max", "bytes");
				unitsMap.put("G1 Old Gen,type=MemoryPool Used", "bytes");
				unitsMap.put("G1 Survivor Space,type=MemoryPool Committed", "bytes");
				unitsMap.put("G1 Survivor Space,type=MemoryPool Max", "bytes");
				unitsMap.put("G1 Survivor Space,type=MemoryPool Used", "bytes");
		
				StringBuilder unitsOutput = new StringBuilder("units:{");
				boolean first = true;
				for (Map.Entry<String, String> entry : unitsMap.entrySet()) {
					if (!first) {
						unitsOutput.append(",");
					}
					unitsOutput.append(entry.getKey()).append("-").append(entry.getValue());
					first = false;
				}
				unitsOutput.append("}");
		
				System.out.print(unitsOutput.toString());
		
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
			keymap.put("FreePhysicalMemorySize", "Runtime Free Memory");
			keymap.put("TotalPhysicalMemorySize", "Runtime Total Memory");
			keymap.put("TotalCompilationTime", "Compilation Time");
			
			keymap.put("DaemonThreadCount", "Daemon threads");
			keymap.put("ThreadCount", "Live threads");
			keymap.put("PeakThreadCount", "Peak threads");
			keymap.put("TotalStartedThreadCount", "Total Started Threads");
			keymap.put("CurrentThreadUserTime", "User Time");
			keymap.put("CurrentThreadCpuTime", "CPU Time");
			
			keymap.put("CollectionCount", "Collections Count");
			keymap.put("CollectionTime", "Time Spent");
			
			
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
			runtimeprop.put("metrics", new String[]{"Uptime", "VmName"});
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

            keymap.put("committed", "Committed");
			keymap.put("max", "Max");
			keymap.put("used", "Used");
			
			keymap.put("HeapMemoryUsage", "Heap");
			keymap.put("NonHeapMemoryUsage", "Non Heap");
			
			Properties memprop = new Properties(); memprop.put("subtype", new String[]{"HeapMemoryUsage", "NonHeapMemoryUsage"});
			memprop.put("metrics" ,new String[]{"committed","max","used"});
			map.put("java.lang:type=Memory", memprop);
			

			Properties memmgrprop = new Properties();
			memmgrprop.put("subtype", new String[] { "Usage" });
			memmgrprop.put("metrics", new String[] { "committed", "max", "used" });
			map.put("java.lang:type=MemoryPool,name=*", memmgrprop);

			for (String mBeanName : map.keySet()) {
                if (mBeanName.contains("Memory")) { 
                    getMemoryData(mBeanName.trim(), map.get(mBeanName));
                } else {
                    getData(mBeanName.trim(), Arrays.asList((String[]) map.get(mBeanName).get("metrics")));
                }
            }
			
		} catch (Exception e) {
		
			// e.printStackTrace();
			System.out.println("status:0|errmsg:Cannot connect to " + host + " using port :" + port+"|");
		} finally {
			if (in != null)
				in.close();

			if (reader != null)
				reader.close();

			if (jmxConnector != null)
				jmxConnector.close();
		}
		
	}
    public void getMemoryData(String mBeanName, Properties prop) throws Exception {
        NumberFormat formatter = new DecimalFormat("#0.00");
    
        ObjectName oname = new ObjectName(mBeanName);
        Set<ObjectInstance> instances = mBeanServerConnection.queryMBeans(oname, null);
        Iterator<ObjectInstance> iterator = instances.iterator();
    
        Object subtypeObj = prop.get("subtype");
        if (subtypeObj == null || !(subtypeObj instanceof String[])) {
            System.out.println("Warning: 'subtype' not found for " + mBeanName);
            return; 
        }
        List<String> list = Arrays.asList((String[]) subtypeObj);
    
        Object metricsObj = prop.get("metrics");
        if (metricsObj == null || !(metricsObj instanceof String[])) {
            System.out.println("Warning: 'metrics' not found for " + mBeanName);
            return;
        }
        String[] keys = (String[]) metricsObj;
    
        while (iterator.hasNext()) {
            ObjectInstance instance = iterator.next();
            String newmbean = mBeanName.replace("*", "");
            String name = instance.getObjectName().toString().replace(newmbean, "");
    
            try {
                MBeanInfo info = mBeanServerConnection.getMBeanInfo(instance.getObjectName());
                MBeanAttributeInfo[] attributes = info.getAttributes();
    
                for (MBeanAttributeInfo attribute : attributes) {
                    try {
                        if (list.contains(attribute.getName())) {
                            Object obj = mBeanServerConnection.getAttribute(instance.getObjectName(), attribute.getName());
                            CompositeData cd = (CompositeData) obj;
                            for (String key : keys) {
                                String namekey = keymap.containsKey(key)
                                    ? (name.isEmpty() ? (keymap.containsKey(attribute.getName()) ? keymap.get(attribute.getName()) : attribute.getName()) : name.replace("java.lang:name=", ""))
                                    + " " + keymap.get(key)
                                    : key;
    
                                if (cd.get(key) instanceof Number) {
                                    metrics.put(namekey, formatter.format(cd.get(key)));
                                } else if (cd.get(key) instanceof String) {
                                    metrics.put(namekey, (String) cd.get(key));
                                } else if (cd.get(key) instanceof Boolean) {
                                    metrics.put(namekey, cd.get(key));
                                }
                            }
                        }
                    } catch (NullPointerException e) {
                        System.out.println("Warning: Missing attribute: " + attribute.getName());
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    
	public void getData(String mBeanName, List<String> list) throws Exception {
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
					try {
						if (attribute.getName().equals("BootClassPath")) {
							continue;
						}
	
						Object obj = mBeanServerConnection.getAttribute(oname, attribute.getName());
						String key = attribute.getName();
	
						Hashtable<String, String> keyPropList = oname.getKeyPropertyList();
						if (list.contains(key)) {
							String namekey = keymap.containsKey(key)
								? ((keyPropList.size() > 1) ? keyPropList.get("name") + " " + keymap.get(key) : keymap.get(key))
								: key;
	
							if (obj instanceof Number) {
								metrics.put(namekey, formatter.format(obj));
							} else if (obj instanceof String) {
								metrics.put(namekey, (String) obj);
							} else if (obj instanceof Boolean) {
								metrics.put(namekey, obj);
							}
						}
					} catch (UnsupportedOperationException e) {
						System.out.println("Skipping unsupported attribute: " + attribute.getName());
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			} catch (NullPointerException e) {
				e.printStackTrace();
			}
		}
	}
	
}
