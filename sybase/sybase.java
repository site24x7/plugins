import com.sybase.jdbc4.jdbc.*;
import java.sql.*;
import java.sql.Connection;
import java.sql.Driver;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;

import org.json.JSONObject;

public class sybase {
	    public static void main(String[] args) {
	        try {
	            Class.forName("com.sybase.jdbc4.jdbc.SybDriver");
	            String url = "jdbc:sybase:Tds:localhost:5002/master?charset=utf8";
	            String username = "sa";
	            String password = "site24x7";
	            Connection connection = DriverManager.getConnection(url, username, password);
	            JSONObject data = new JSONObject();
	            
	            HashMap<String,String> summaryData = new HashMap<>();
//	            summaryData.put("", value);
	            
	            
	            List<String> metricNeed= new ArrayList<>();
	            metricNeed.add("max concurrently recovered db");
	            metricNeed.add("number of checkpoint tasks");
	            metricNeed.add("number of dump load retries");
	            metricNeed.add("recovery interval in minutes");
	            metricNeed.add("extended cache size");
	            metricNeed.add("number of index trips");
	            metricNeed.add("total data cache size");
	            metricNeed.add("maximum dump conditions");
	            metricNeed.add("memory dump compression level");
	            metricNeed.add("number of dump threads");
	            metricNeed.add("disk i/o structures");
	            metricNeed.add("number of devices");
	            metricNeed.add("number of disk tasks");
	            metricNeed.add("number of large i/o buffers");
	            metricNeed.add("page utilization percent");
	            metricNeed.add("solaris async i/o mode");
	            metricNeed.add("number of java sockets");
	            metricNeed.add("size of global fixed heap");
	            metricNeed.add("size of process object heap");
	            metricNeed.add("size of shared class heap");
	            metricNeed.add("deadlock retries");
	            metricNeed.add("lock hashtable size");
	            metricNeed.add("lock spinlock ratio");
	            metricNeed.add("lock table spinlock ratio");
	            metricNeed.add("lock wait period");
	            metricNeed.add("number of locks");
	            metricNeed.add("read committed with lock");
	            metricNeed.add("messaging memory");
	            metricNeed.add("number of alarms");
	            metricNeed.add("number of mailboxes");
	            metricNeed.add("number of messages");
	            metricNeed.add("number of open databases");
	            metricNeed.add("number of open indexes");
	            metricNeed.add("number of open objects");
	            metricNeed.add("number of open partitions");
	            metricNeed.add("number of remote connections");
	            metricNeed.add("number of remote logins");
	            metricNeed.add("number of remote sites");
	            metricNeed.add("number of user connections");
	            metricNeed.add("number of worker processes");
	            metricNeed.add("open index hash spinlock ratio");
	            metricNeed.add("open index spinlock ratio");
	            metricNeed.add("partition spinlock ratio");
	            metricNeed.add("procedure cache size");
	            metricNeed.add("process wait events");
	            metricNeed.add("remote server pre-read packets");
	            metricNeed.add("size of global fixed heap");
	            metricNeed.add("size of process object heap");
	            metricNeed.add("size of shared class heap");
	            metricNeed.add("stack size");
	            metricNeed.add("statement cache size");
	            metricNeed.add("statement pipe max messages");
	            metricNeed.add("threshold event max messages");
	            metricNeed.add("total data cache size");
	            metricNeed.add("total logical memory");
	            metricNeed.add("total physical memory");
	            metricNeed.add("user log cache size");
	            metricNeed.add("user log cache spinlock ratio");
	            metricNeed.add("workload manager cache size");
	            metricNeed.add("number of engines at startup");
	            metricNeed.add("number of network tasks");
	            metricNeed.add("default network packet size");
	            metricNeed.add("number of backup connections");
	            metricNeed.add("permission cache entries");
	            metricNeed.add("session tempdb log cache size");
	            metricNeed.add("stack guard size");
	            metricNeed.add("user log cache queue size");
//	            metricNeed.add("");
//	            metricNeed.add("");
//	            metricNeed.add("");
//	            metricNeed.add("");
//	            metricNeed.add("");
//	            metricNeed.add("");
//	            System.out.println(metricNeed);
	            
	            Statement statement = connection.createStatement();
	            for(int c=0; c<metricNeed.size();++c) {
	            	String query = "sp_configure"+" '"+metricNeed.get(c)+"'";
//	            	System.out.println(query);
	            	ResultSet resultSet = statement.executeQuery(query);
	            	ResultSetMetaData metaData = resultSet.getMetaData();
	            	
	            	int columnCount = metaData.getColumnCount();
	            	if(resultSet.next()) {
	            		String metric="";
		            	String dataValue="";
		            	for (int i = 1; i <= columnCount; i++) {
		            		if(metaData.getColumnName(i).equals("Parameter Name") ) {
		            			metric = (String)resultSet.getObject(i);
		            			metric = metric.replaceAll("\\s{2,}", " ");
		            		}
		            		else if(metaData.getColumnName(i).equals("Run Value") ) {
		            			dataValue = (String)resultSet.getObject(i);
		            			dataValue = dataValue.replaceAll("\\s{2,}", " ");
		            		}
		            	}
		            	data.put(metric, dataValue);
	            	}
	            	
	            	
	            }
//	            int columnCount = metaData.getColumnCount();
//	            while (resultSet.next()) {
//	            	String metric="";
//	            	String dataValue="";
//	            	for (int i = 1; i <= columnCount; i++) {
//	            		if(metaData.getColumnName(i).equals("Parameter Name") ) {
//	            			metric = (String)resultSet.getObject(i);
//	            			metric = metric.replaceAll("\\s{2,}", " ");
//	            		}
//	            		else if(metaData.getColumnName(i).equals("run_value") ) {
//	            			dataValue = (String)resultSet.getObject(i);
//	            			dataValue = dataValue.replaceAll("\\s{2,}", " ");
//	            		}
//	                    String columnName = metaData.getColumnName(i);
//	                    Object value = resultSet.getObject(i);
//	                    System.out.println(columnName+":"+value);
//	                }
//	            	System.out.println("--------------");
	            	
//	            }
	            
	            System.out.println(data);
	            connection.close();
	        } catch (ClassNotFoundException e) {
	            e.printStackTrace();
	        } catch (SQLException e) {
	            e.printStackTrace();
	        }
	    }
}

