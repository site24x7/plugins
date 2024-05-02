import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.json.JSONArray;
import org.json.JSONObject;

public class sybaseDB {
	public static void main(String[] args) {
		JSONObject data = new JSONObject();
    	JSONArray memArray = new JSONArray();
    	JSONArray userStatitistics = new JSONArray();
    	JSONArray cacheStats = new JSONArray();
    	JSONObject tabs = new JSONObject();
    	List<String> databse_list=new ArrayList<>();
    	
    	 try {
    		 Class.forName("com.sybase.jdbc4.jdbc.SybDriver");
    		 String PLUGIN_VERSION = args[0];
                 String HEARTBEAT_REQUIRED = args[1];
	         data.put("plugin_version",PLUGIN_VERSION);
                data.put("heartbeat_required", HEARTBEAT_REQUIRED);
		 String hostname = args[2];
		 String port = args[3];
		 String username = args[4];
		 String password = args[5];
		 
//		 String hostname = "localhost";
//		 String port = "5000";
//		 String username = "sa";
//		 String password = "Sathvika@123";
		 
		 
		 	 long startTime = System.currentTimeMillis();
    		 
	         String url = "jdbc:sybase:Tds:"+hostname+":"+port+"/master?charset=utf8";
	         Connection connection = DriverManager.getConnection(url, username, password);
	         long endTime = System.currentTimeMillis();
	         long timeElapsed = endTime - startTime;

	         data.put("connection_time_ns", timeElapsed);
	         Map<String, String> summary_metric = new HashMap<>();
	         summary_metric.put("sp_configure 'number of remote connections'","max_remote_connections");
	         summary_metric.put("sp_configure 'number of user connections'","max_user_connections");
	         summary_metric.put("sp_configure 'total logical memory'","free_memory");
	         
	         summary_metric.put("sp_configure 'number of locks'","max_locks");
	         
	         
	         Statement statement = connection.createStatement();

	         summary_metric(data,statement,summary_metric);
	         summary_procedure_cache(data,statement);
	         summary_data_cache(data,statement);
	         transaction(data,statement);
	         backup_database_detail(data,statement,databse_list);
	         database_detail(data,statement,databse_list);
	         
	         JSONArray tabList1 = new JSONArray();
	         tabList1.put("transaction_details");
	         tabList1.put("backup_database_details");
	         tabList1.put("database_details");
	         JSONObject  tabDetail1= new JSONObject();
	         tabDetail1.put("order", 2);
	         tabDetail1.put("tablist", tabList1);
	         
	         JSONArray tabList2 = new JSONArray();
	         tabList2.put("procedure_cache_usage");
	         tabList2.put("data_cache_usage");
	         JSONObject  tabDetail2= new JSONObject();
	         tabDetail2.put("order", 1);
	         tabDetail2.put("tablist", tabList2);
	         
	         tabs.put("Cache Details",tabDetail2 );
	         tabs.put("Database Details",tabDetail1 );
	         data.put("tabs", tabs);
	         System.out.println(data);
    		 
    	 }catch(Exception e) {
	    		data.put("msg",e);
	     }
	}
	private static ResultSet executeQuery(Statement statement,String query,JSONObject data) {
    	try {
    		ResultSet resultSet = statement.executeQuery(query);
    		return resultSet;
    	}catch(Exception e) {
    		data.put("msg",e);
    	}
		return null;
    }
	
	private static void summary_metric(JSONObject data,Statement statement,Map<String, String> summary_metric) {
		try {
			int metricNeedSize = summary_metric.size();
			String free_memory = "";
			String used_memory="";
			
			for (String query : summary_metric.keySet()) {
			    ResultSet resultSet =executeQuery(statement,query,data);
	            ResultSetMetaData metaData = resultSet.getMetaData();
	            int columnCount = metaData.getColumnCount();
	            String dataValue="";
	            if(resultSet.next()) {
	            	for (int i = 1; i <= columnCount; i++) {
	            		if( query.equals("sp_configure 'total logical memory'")) {
	            			if(metaData.getColumnName(i).equals("Memory Used") ) {
		            		dataValue = (String)resultSet.getObject(i);
		            		dataValue = dataValue.replaceAll("\\s{2,}", " ");
		            		data.put("used_memory", dataValue);
		            		used_memory=dataValue.trim();
	            		}
	            	}
	            		if(metaData.getColumnName(i).equals("Run Value") ) {
	            			dataValue = (String)resultSet.getObject(i);
	            			dataValue = dataValue.replaceAll("\\s{2,}", " ");
	            			data.put(summary_metric.get(query), dataValue);
	            			if(query.equals("sp_configure 'total logical memory'")) {
	            				free_memory=dataValue.trim();
	            				int total_mem=Integer.parseInt(free_memory)+Integer.parseInt(used_memory);
	            				data.put("total_memory", total_mem);
	            				
	            				double result = (double) Integer.parseInt(used_memory) / total_mem;
	            				DecimalFormat df = new DecimalFormat("#.##");
	            		        String roundedResult = df.format(result);
	            		        data.put("used_memory_percentage",Double.parseDouble(roundedResult.trim())*100);
	            			}
	            		}
	            		
	            	}
	            }
			
	        
	      }
			ResultSet resultSet =executeQuery(statement,"SELECT COUNT(*) as row_count FROM syslogins",data);
            ResultSetMetaData metaData = resultSet.getMetaData();
            if(resultSet.next()) {
            	data.put("active_user_connections",resultSet.getObject("row_count"));
            }else {
            	data.put("active_user_connections",0);
            }
            
            resultSet =executeQuery(statement,"SELECT COUNT(*) as row_count FROM syslocks",data);
            metaData = resultSet.getMetaData();
            if(resultSet.next()) {
            	data.put("active_locks",resultSet.getObject("row_count"));
            }else {
            	data.put("active_locks",0);
            }
            
            resultSet =executeQuery(statement,"SELECT COUNT(*) as row_count FROM syslogins",data);
            metaData = resultSet.getMetaData();
            if(resultSet.next()) {
            	data.put("number_of_login_accounts",resultSet.getObject("row_count"));
            }else {
            	data.put("number_of_login_accounts",0);
            }
            
            resultSet =executeQuery(statement,"SELECT COUNT(*) as row_count FROM sysremotelogins",data);
            metaData = resultSet.getMetaData();
            if(resultSet.next()) {
            	data.put("number_of_remote_login",resultSet.getObject("row_count"));
            }else {
            	data.put("number_of_remote_login",0);
            }
	             
	         
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}
	
	private static void summary_procedure_cache(JSONObject data,Statement statement) {
		try {
			JSONArray procedure_cache_arr = new JSONArray();
			Map<String, String> procedure_cache = new HashMap<>();
			procedure_cache.put("Num_active","procedure_cache_used");
			procedure_cache.put("Pct_act","procedure_cache_used_percentage");
			procedure_cache.put("Max_Used","max_procedure_cache");
			procedure_cache.put("Reuse_cnt","procedure_cache_reused");
			
			ResultSet resultSet =executeQuery(statement,"sp_monitorconfig 'procedure cache'",data);
            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();
            String metric="";
            String dataValue="";
            if(resultSet.next()) {
           	 for (int i = 1; i <= columnCount; i++) { 
           		if(procedure_cache.containsKey(metaData.getColumnName(i)) ) {
           			JSONObject procedure_cache_obj = new JSONObject();
           			procedure_cache_obj.put("value",resultSet.getObject(i));
           			procedure_cache_obj.put("name",procedure_cache.get(metaData.getColumnName(i)));
           			procedure_cache_arr.put(procedure_cache_obj);
	            }
	          
           	 } 	
           	
           	data.put("procedure_cache_usage",procedure_cache_arr);
            }
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}
	
	private static void summary_data_cache(JSONObject data,Statement statement) {
		try {
			JSONArray data_cache_arr = new JSONArray();
			Map<String, String> data_cache = new HashMap<>();
			data_cache.put("PhysicalReads","physical_reads");
			data_cache.put("LogicalReads","logical_reads");
			data_cache.put("PhysicalWrites","physical_writes");
			data_cache.put("CacheSize","cache_size");
			
			ResultSet resultSet =executeQuery(statement,"select * from monDataCache",data);
            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();
            String metric="";
            String dataValue="";
            if(resultSet.next()) {
           	 for (int i = 1; i <= columnCount; i++) { 
           		if(data_cache.containsKey(metaData.getColumnName(i)) ) {
           			JSONObject data_cache_obj = new JSONObject();
           			data_cache_obj.put("cache_value",resultSet.getObject(i));
           			data_cache_obj.put("name",data_cache.get(metaData.getColumnName(i)));
           			data_cache_arr.put(data_cache_obj);
	            }
	          
           	 } 	
           	
           	data.put("data_cache_usage",data_cache_arr);
            }
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}
	
	private static void transaction(JSONObject data,Statement statement) {
		try {
			JSONArray transaction_arr = new JSONArray();
			Map<String, String> transaction = new HashMap<>();
			transaction.put("coordinator","Coordinator");
			transaction.put("starttime","Starttime");
			transaction.put("state","State");
			transaction.put("connection","Connection");
			transaction.put("failover","Failover");
			
			ResultSet resultSet =executeQuery(statement,"sp_transactions",data);
            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();	
            	
           	 for (int i = 1; i <= columnCount; i++) { 
           		if(transaction.containsKey(metaData.getColumnName(i)) ) {
           			
           			JSONObject transaction_obj = new JSONObject();
           			if(resultSet.next()) {
           				transaction_obj.put("transaction_value",resultSet.getObject(i));
           			}
           			else {
           				transaction_obj.put("transaction_value",0);
           			}
           			transaction_obj.put("name",transaction.get(metaData.getColumnName(i)));
           			transaction_arr.put(transaction_obj);
	            }
           	 } 	
           	data.put("transaction_details",transaction_arr);
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}
	
	private static void backup_database_detail(JSONObject data,Statement statement,List<String> databse_list) {
		try {
			JSONArray bkp_db_arr = new JSONArray();
			Map<String, String> backup_database = new HashMap<>();
			backup_database.put("DBName","name");
			backup_database.put("BackupInProgress","backup_status");
			backup_database.put("SuspendedProcesses","suspended_processes");
			backup_database.put("TransactionLogFull","transaction_log_full");
			
			ResultSet resultSet =executeQuery(statement,"select DBName,BackupInProgress,SuspendedProcesses,TransactionLogFull from monOpenDatabases",data);
            ResultSetMetaData metaData = resultSet.getMetaData();
            int columnCount = metaData.getColumnCount();	
            while(resultSet.next()) {
            	JSONObject bkp_db_obj = new JSONObject();
            	for(int i=1;i<=columnCount;++i) {
            		bkp_db_obj.put(backup_database.get(metaData.getColumnName(i)),resultSet.getObject(i));
            		if(metaData.getColumnName(i).equals("DBName")) {
            			databse_list.add((String) resultSet.getObject(i));
            		}
                }   
            	bkp_db_arr.put(bkp_db_obj);
            }
            data.put("backup_database_details",bkp_db_arr);
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}
	
	private static void database_detail(JSONObject data,Statement statement,List<String> databse_list) {
		try {
			JSONArray db_arr = new JSONArray();
			for(int i=0;i<databse_list.size();++i) {
				JSONObject db_obj = new JSONObject();
				String query="select loginfo('"+databse_list.get(i)+"', 'oldest_active_transaction_pct') as log_used, loginfo('"+databse_list.get(i)+"', 'can_free_using_dump_tran') as log_size_available, loginfo('"+databse_list.get(i)+"', 'stp_span_pct') as log_used_percentage";
				ResultSet resultSet =executeQuery(statement,query,data);
	            ResultSetMetaData metaData = resultSet.getMetaData();
	            int columnCount = metaData.getColumnCount();
	            db_obj.put("name",databse_list.get(i));
	            while(resultSet.next()) {
	            	for(int j=1;j<=columnCount;++j) {
	            		db_obj.put(metaData.getColumnName(j),resultSet.getObject(j));
	            	}
	            }
	            db_arr.put(db_obj);
			}
			database_space_details(statement,db_arr,data);
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}
	
	private static void database_space_details(Statement statement,JSONArray db_arr,JSONObject data) {
		try {
			JSONArray db_arr1 = new JSONArray();
			String query="select db_name(d.dbid) as db_name, ceiling(sum(case when u.segmap != 4 then u.size/1048576.*@@maxpagesize end )) as total_size,ceiling(sum(case when u.segmap != 4 then size - curunreservedpgs(u.dbid, u.lstart, u.unreservedpgs) end)/1048576.*@@maxpagesize) as used_size,ceiling(100 * (1 - 1.0 * sum(case when u.segmap != 4 then curunreservedpgs(u.dbid, u.lstart, u.unreservedpgs) end) / sum(case when u.segmap != 4 then u.size end))) as used_size_percentage from master..sysdatabases d, master..sysusages u where u.dbid = d.dbid  and d.status not in (256,4096) group by d.dbid order by db_name(d.dbid)";
			ResultSet resultSet =executeQuery(statement,query,data);
			ResultSetMetaData metaData = resultSet.getMetaData();
	        int count = metaData.getColumnCount();
	        while(resultSet.next()) {
	        	String dbName = resultSet.getString(1);
	        	for(int l=0;l<db_arr.length();++l) {
	        		JSONObject obj=db_arr.getJSONObject(l);
	        		if(obj.get("name").equals(dbName)) {
	        			for(int i = 2; i <= count; i++) {
	                		String col=metaData.getColumnName(i);
	        	        	String val = resultSet.getString(i);
	        	        	obj.put(col, Integer.parseInt(val));
	                	}
	        			db_arr1.put(obj);
	        			break;
	        		}
	        	}
	        }
			data.put("database_details",db_arr1);
		}catch(Exception e) {
    		data.put("msg",e);
    	}
	}

}

