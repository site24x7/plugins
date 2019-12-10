

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.net.URL;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.management.MBeanAttributeInfo;
import javax.management.MBeanInfo;
import javax.management.MBeanServerConnection;
import javax.management.ObjectInstance;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

public class JMXMonitoring {

	private static final String JMX_URL = "service:jmx:rmi:///jndi/rmi://[%s]:%d/jmxrmi";
	private JMXConnector jmxConnector = null;
	private MBeanServerConnection mBeanServerConnection = null;

	private String host = "127.0.0.1";
	private int port = 7199;

	Map<String, Object> metrics = new LinkedHashMap<String, Object>();
	String filePath = "metrics.txt";

	ArrayList<MBeanAttributeInfo> list = new ArrayList<MBeanAttributeInfo>();

	public static void main(String[] args) {
		JMXMonitoring monitor = new JMXMonitoring();
		try {
			
			if(args.length ==0 || args.length == 3){
				
				if(args.length == 3){
					monitor.host = args[0];
					monitor.port = Integer.parseInt(args[1]);
					monitor.filePath = args[2];
				}
				
				monitor.connect();
				int i = 0;
				
				int limit = 25;
				int len = monitor.metrics.size();
				for (String key : monitor.metrics.keySet()) {
					if (i < (limit-1) || i<(len-2)) {
						System.out.print(key + ":" + monitor.metrics.get(key) );
					} else {
						System.exit(1);
					}
					if(!(i == (limit-1) || (i == len-1))){
						System.out.print("|");
					}
					
					i++;
				}

			}else{
				System.out.println("status:0|msg:Invalid input args");
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
			
			
			Object path = this.getClass().getResource(filePath);
			
			if(path == null){
				throw new FileNotFoundException(filePath);
			}
			
			String filepath = ((URL)path).getFile();
			in = new FileInputStream(filepath);

			reader = new BufferedReader(new InputStreamReader(in));
			ArrayList<String> list = new ArrayList<String>();

			String ipline;
			while ((ipline = reader.readLine()) != null) {
				if (!ipline.startsWith("#") && !ipline.isEmpty()) {
					list.add(ipline);
				}
			}

			NumberFormat formatter = new DecimalFormat("#0.0000");
			for (String line : list) {
				try {
					String[] splitline = line.split(" ");

					int len = splitline.length;
					String mBeanName = splitline[0];
					String attributetype = len == 2 ? null : splitline[1];
					String label = len == 2 ? splitline[1] : splitline[2];

					ObjectName oname = new ObjectName(mBeanName);
					// System.out.println(oname);
					Set<ObjectInstance> instances = mBeanServerConnection.queryMBeans(oname, null);
					Iterator<ObjectInstance> iterator = instances.iterator();

					while (iterator.hasNext()) {
						ObjectInstance instance = iterator.next();
						try {
							String oname1Str = instance.getObjectName().toString();
							ObjectName oname1 = new ObjectName(oname1Str);
							MBeanInfo info = mBeanServerConnection.getMBeanInfo(oname1);
							MBeanAttributeInfo[] attributes = info.getAttributes();
							for (MBeanAttributeInfo attribute : attributes) {
								if (attributetype == null || attribute.getName().matches(attributetype)) {
									Object obj = mBeanServerConnection.getAttribute(oname1,attribute.getName());

									String key = replaceTokens(oname1Str, label);
									if (obj instanceof Long) {
										metrics.put(key, formatter.format(obj));
									} else if (obj instanceof Double) {
										metrics.put(key, formatter.format(obj));
									} else if (obj instanceof String) {
										metrics.put(key, (String) obj);
									} else {
										metrics.put(key, obj);
									}
								}
							}
						} catch (NullPointerException e) {
							//e.printStackTrace();
						}
					}
				} catch (Exception e) {
					//e.printStackTrace();
				}
			}
		} catch (FileNotFoundException fe) {
			System.out.println("status:0|errmsg:Unable to file metric file " + filePath);
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

	private String replaceTokens(String mBeanName, String text) {

		HashMap<String, String> replacements = new HashMap<String, String>();
		int firstColon = mBeanName.indexOf(':');
		String[] props = mBeanName.substring(firstColon + 1).split(
				"(?!\\B\"[^\"]*),(?![^\"]*\"\\B)");
		for (int i = 0; i < props.length; i++) {
			String[] parts = props[i].split("=");
			replacements.put(parts[0], parts[1]);
		}

		Pattern pattern = Pattern.compile("\\<(.+?)\\>");
		Matcher matcher = pattern.matcher(text);
		StringBuilder builder = new StringBuilder();
		int i = 0;
		while (matcher.find()) {
			String replacement = replacements.get(matcher.group(1));
			builder.append(text.substring(i, matcher.start()));
			if (replacement == null)
				builder.append(matcher.group(0));
			else
				builder.append(replacement);
			i = matcher.end();
		}
		builder.append(text.substring(i, text.length()));
		return builder.toString().replaceAll("\"", "").replaceAll(" ", "-");
	}
}
