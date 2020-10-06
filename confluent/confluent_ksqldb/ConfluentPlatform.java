import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
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

public class ConfluentPlatform {
 
 public static String pluginVersion="1";
 private String host="127.0.0.1";
 private String port="9990";
 private String filePath="metrics.txt";
 private static JMXConnector jmxConnector = null;
 private static MBeanServerConnection connection = null;
 public static void main(String[] args) {
	 	try {
	 		
			ConfluentPlatform cp = new ConfluentPlatform();		
			if(args.length == 2){
				cp.host = args[0];
				cp.port = args[1];
			}

			cp.getConnection(cp.host, cp.port);
			Map<String,Object> metrics = cp.getMetrics();
			printMetrics(metrics);

	 	}
	 	catch(Exception e) {
	 		System.out.print("plugin_version:"+pluginVersion+"|heartbeat:true|status:0|msg:Error Occurred");
	 	}finally {
	 		try {
				jmxConnector.close();
			} catch (Exception e) {
				// TODO Auto-generated catch block
				// e.printStackTrace();
			}
	 	}


}
 private void getConnection(String host,String port) throws Exception{
		String JMX_URL = "service:jmx:rmi:///jndi/rmi://"+host+":"+port+"/jmxrmi";
		JMXServiceURL jmxurl = new JMXServiceURL(String.format(JMX_URL, host, port));
		Map<String, Object> env = new HashMap<String, Object>();
		jmxConnector = JMXConnectorFactory.connect(jmxurl, env);
		connection = jmxConnector.getMBeanServerConnection();
 }
 
 private ArrayList<String> getRequiredMBeansList(String filePath) throws Exception{
	 	
	 	Object path = this.getClass().getResource(filePath);
		if(path == null){
			throw new FileNotFoundException(filePath);
		}	
		String filepath = ((URL)path).getFile();
		FileInputStream in = new FileInputStream(filepath);
		BufferedReader reader = new BufferedReader(new InputStreamReader(in));
		ArrayList<String> list = new ArrayList<String>();

		String line;
		while ((line = reader.readLine()) != null) {
			if (!line.startsWith("#") && !line.isEmpty()) {
				list.add(line);
			}
		}
		
		in.close();
		reader.close();
		
		return list;
 }
 
 private Map<String,Object> getMetrics() throws Exception {
		
	 	ArrayList<String> requiredMbeans = getRequiredMBeansList(filePath);
		NumberFormat formatter = new DecimalFormat("#0.0000");
		Map<String, Object> metrics = new LinkedHashMap<String, Object>();

		for(String mbean:requiredMbeans ) {
			String[] splitline = mbean.split(" ");
			int len = splitline.length;
			String mBeanName = splitline[0];
			String attributetype = len == 2 ? null : splitline[1];
			String label = len == 2 ? splitline[1] : splitline[2];
			ObjectName query = new ObjectName(mBeanName);
			Set<ObjectInstance> mbeans = connection.queryMBeans(query, null);
			Iterator<ObjectInstance> iterator = mbeans.iterator();
			while (iterator.hasNext()) {
				ObjectInstance instance = iterator.next();
				try {
					String oname1Str = instance.getObjectName().toString();
					ObjectName oname1 = new ObjectName(oname1Str);
					MBeanInfo info = connection.getMBeanInfo(oname1);
					MBeanAttributeInfo[] attributes = info.getAttributes();
					for (MBeanAttributeInfo attribute : attributes) {
						if (attributetype == null || attribute.getName().matches(attributetype)) {
							Object obj = connection.getAttribute(oname1,attribute.getName());
	
							String key = replaceTokens(oname1Str, label);
							if(attributetype ==null) {
								key = key + ":" +attribute.getName();
							}
							if (obj instanceof Long) {
								metrics.put(key, formatter.format(obj));
							} else if (obj instanceof Double) {
								Double d = Double.valueOf(obj.toString());
								if(!d.isNaN()) {
									metrics.put(key, formatter.format(obj));
								}
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


		}
		
		return metrics;
		
 }
 
 private static void printMetrics(Map<String,Object> metrics) {
		int i = 0;
		
		int limit = 25;
		int len = metrics.size();
		for (String key : metrics.keySet()) {

			if (i < (limit-1) || i<(len-2)) {
				System.out.print(key + ":" + metrics.get(key) );
			} else {
				System.out.print("plugin_version:"+pluginVersion+"|heartbeat:true|status:0|msg:No metrics Available");

				System.exit(1);
			}
			if(!(i == (limit-1) || (i == len-1))){
				System.out.print("|");
			}
			
			i++;
		}
				System.out.print("|plugin_version:"+pluginVersion+"|heartbeat:true");
 }
 
	private static String replaceTokens(String mBeanName, String text) {

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
