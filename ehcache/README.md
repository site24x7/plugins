
Plugin for Ehcache Monitoring
=============================

Ehcache is an open source, standards-based cache that boosts performance, offloads your database, and simplifies scalability.It's the most widely-used Java-based cache because it's robust, proven, full-featured, and integrates with other popular libraries and frameworks.

Using this plugin you can monitor the performance metrics of your Ehcache.

PreRequisites
==============

Please specify the correct path in "JAVA_HOME" variable in the "ehcache.sh"

Please specify proper value in the below variable in "EhcachePlugin.java"

remoteHost : Name of the host where the ehcache is running
remotePort : JMX port of ehcache
cacheManagerName : Name of the cache manager
cacheName  : Name of the cache

Please uncomment the jmxCredetials and update user and pswd if needed

	jmxCredentials = new HashMap<String, Object>();
	jmxCredentials.put("jmx.remote.credentials", new String[]{"user","pwd"});
	
	
For monitoring Ehcache your application must register CacheStatistics in the JDK platform MBeanServer. Below is the sample code for how to register MBeanServer.

CacheManager manager = new CacheManager();
MBeanServer mBeanServer = ManagementFactory.getPlatformMBeanServer();
ManagementService.registerMBeans(manager, mBeanServer, false, false, false, true);

JMX creates a standard way of instrumenting classes and making them available to a monitoring infrastructure. So you must pass the below jvm arguments in your application to enable JMX

-Dcom.sun.management.jmxremote 
-Dcom.sun.management.jmxremote.port=9999 
-Dcom.sun.management.jmxremote.ssl=false 
-Dcom.sun.management.jmxremote.authenticate=false

Ehcache Plugin Attributes:
==========================

Some of the collected Ehcache attributes are as follows:

`ObjectCount` : Total number of elements stored in the cache <br />
`CacheHits`:	Total number of times a requested item was found in the cache
`CacheMisses` : Total number of times a requested element was not found in the cache.
`CacheHitPercentage`  : Percentage of successful hits.
`CacheMissPercentage` :	Percentage of accesses that failed to find anything.
