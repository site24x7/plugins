import java.io.BufferedReader;
import java.io.FileInputStream;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
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

//$Id$

public class JVMMemoryMonitoring {

	private static final String JMX_URL = "service:jmx:rmi:///jndi/rmi://[%s]:%d/jmxrmi";
	private JMXConnector jmxConnector = null;
	private MBeanServerConnection mBeanServerConnection = null;

	private static String host = "127.0.0.1";
	private static int port = 7199;

	Map<String, Object> metrics = new LinkedHashMap<String, Object>();
	HashMap<String, String> keymap = new HashMap<>();

	ArrayList<MBeanAttributeInfo> list = new ArrayList<MBeanAttributeInfo>();

	public static void main(String[] args) {
		JVMMemoryMonitoring monitor = new JVMMemoryMonitoring();
		try {

			if (args.length == 0 || args.length == 2) {
				if (args.length == 2) {
					host = args[0];
					port = Integer.parseInt(args[1]);
				}

				monitor.connect();
				int i = 0;

				int limit = 25;
				int len = monitor.metrics.size();
				for (String key : monitor.metrics.keySet()) {
					if (i < (limit - 1) || i < (len - 2)) {
						System.out.print(key + ":" + monitor.metrics.get(key));
					} else {
						System.exit(1);
					}
					if (!(i == (limit - 1) || (i == len - 1))) {
						System.out.print("|");
					}

					i++;
				}

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

			keymap.put("committed", "Committed");
			keymap.put("max", "Max");
			keymap.put("used", "Used");
			
			keymap.put("HeapMemoryUsage", "Heap");
			keymap.put("NonHeapMemoryUsage", "Non Heap");
			

			HashMap<String, Properties> map = new HashMap<>();

			
			Properties memprop = new Properties(); memprop.put("subtype", new String[]{"HeapMemoryUsage", "NonHeapMemoryUsage"});
			memprop.put("metrics" ,new String[]{"committed","max","used"});
			map.put("java.lang:type=Memory", memprop);
			

			Properties memmgrprop = new Properties();
			memmgrprop.put("subtype", new String[] { "Usage" });
			memmgrprop.put("metrics", new String[] { "committed", "max", "used" });
			map.put("java.lang:type=MemoryPool,name=*", memmgrprop);

			for (String mBeanName : map.keySet()) {
				getData(mBeanName.trim(), map.get(mBeanName));
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

	public void getData(String mBeanName, Properties prop) throws Exception {

		NumberFormat formatter = new DecimalFormat("#0.00");

		ObjectName oname = new ObjectName(mBeanName);
		Set<ObjectInstance> instances = mBeanServerConnection.queryMBeans(oname, null);
		Iterator<ObjectInstance> iterator = instances.iterator();

		List<String> list = Arrays.asList((String[]) prop.get("subtype"));
		String[] keys = (String[]) prop.get("metrics");

		while (iterator.hasNext()) {
			ObjectInstance instance = iterator.next();
			String newmbean = mBeanName.replace("*", "");
			String name = (instance.getObjectName()).toString().replace(newmbean, "");
			
			try {
				MBeanInfo info = mBeanServerConnection.getMBeanInfo(instance.getObjectName());
				MBeanAttributeInfo[] attributes = info.getAttributes();

				for (MBeanAttributeInfo attribute : attributes) {
					try {
						if (list.contains(attribute.getName())) {
							Object obj = mBeanServerConnection.getAttribute(instance.getObjectName(), attribute.getName());
							CompositeData cd = (CompositeData) obj;
							for (String key : keys) {
								String namekey = keymap.containsKey(key) ? ( name.isEmpty()?  (keymap.containsKey(attribute.getName())? keymap.get(attribute.getName()):attribute.getName()) : name) + " " + keymap.get(key) : key;
								if (cd.get(key) instanceof Long || cd.get(key) instanceof Double || cd.get(key) instanceof Integer) {
									metrics.put(namekey, formatter.format(cd.get(key)));
								} else if (cd.get(key) instanceof String) {
									metrics.put(namekey, (String) cd.get(key));
								} else if (cd.get(key) instanceof Boolean) {
									metrics.put(namekey, cd.get(key));
								}
							}

						}

					} catch (NullPointerException e) {
						//e.printStackTrace();
					}

				}

			} catch (NullPointerException e) {
				//e.printStackTrace();
			}

		}
	}

}
