import java.util.Map;

import javax.management.MBeanServerConnection;
import javax.management.ObjectName;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

/**
 * 
 * @author magesh rajan
 *
 */
public class EhcachePlugin 
{
	private final static char DELIMITER = '|';

	private final static char KEY_VALUE_SEPARATOR = ':';

	public static void main(String[] args)
	{
		String remoteHost = "localhost";
		
		int remotePort = 9999;

		String cacheManagerName = "plus";
		
		String cacheName = "cache1";
		/*
		 *  Credentials to connect to the remote JMX port
		 */
		Map<String, Object> jmxCredentials = null; 
		/*jmxCredentials = new HashMap<String, Object>();
		jmxCredentials.put("jmx.remote.credentials", new String[]{"user","pwd"});*/

		/*
		 * This variable will hold the required output data
		 * The values are formatted based on the description mentioned in below link
		 * 
		 * https://www.site24x7.com/help/admin/adding-a-monitor/plugins/custom-plugins.html#Shell
		 */
		StringBuilder data = new StringBuilder();

		try 
		{
			JMXServiceURL jmxURL = new JMXServiceURL("service:jmx:rmi:///jndi/rmi://" + remoteHost + ":" + remotePort +"/jmxrmi");

			JMXConnector jmxConnector = JMXConnectorFactory.newJMXConnector(jmxURL, jmxCredentials);
			jmxConnector.connect();

			MBeanServerConnection mbean = jmxConnector.getMBeanServerConnection();


			/*
			 * Fetching statistics of the give cache manager
			 */
			ObjectName cache_statistics = new ObjectName("net.sf.ehcache:type=CacheStatistics,CacheManager="+cacheManagerName+",name="+cacheName);

			data.append(DELIMITER);

			data.append("object_count");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(cache_statistics, "ObjectCount"));

			data.append(DELIMITER);

			data.append("cache_hits");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(cache_statistics, "CacheHits"));

			data.append(DELIMITER);

			data.append("cache_hits_percentage");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(cache_statistics, "CacheHitPercentage"));

			data.append(DELIMITER);

			data.append("cache_misses");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(cache_statistics, "CacheMisses"));

			data.append(DELIMITER);

			data.append("cache_misses_percentage");
			data.append(KEY_VALUE_SEPARATOR);
			data.append(mbean.getAttribute(cache_statistics, "CacheMissPercentage"));

			System.out.println(data.toString());
		}
		catch (Exception e)
		{
			//do Nothing
		}
	}
}
