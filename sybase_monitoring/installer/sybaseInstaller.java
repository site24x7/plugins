import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class sybaseInstaller {
	public static void main(String[] args) {
		try {
			Class.forName("com.sybase.jdbc4.jdbc.SybDriver");
			 String hostname = args[0];
			 String port = args[1];
			 String username = args[2];
			 String password = args[3];
			 
			 String url = "jdbc:sybase:Tds:"+hostname+":"+port+"/master?charset=utf8";
	         Connection connection = DriverManager.getConnection(url, username, password);
	         Statement statement = connection.createStatement();
	         
	         List<String> cmd= new ArrayList<>();
	         cmd.add("sp_configure 'enable monitoring', 1");
	         cmd.add("sp_configure 'statement statistics active', 1");
	         cmd.add("EXEC sp_configure 'per object statistics active', 1");
	         cmd.add("EXEC sp_configure 'wait event timing', 1");
	         cmd.add("sp_configure 'statement statistics active', 1");
	         
	         for(int i=0;i<cmd.size();++i) {
	        	 ResultSet resultSet = statement.executeQuery(cmd.get(i));
	        	 ResultSetMetaData metaData = resultSet.getMetaData();
	         }
			 
		}catch(Exception e) {
    		System.out.println(e);
     }
	}

}

