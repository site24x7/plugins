import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.HttpClientBuilder;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class MerakiDataCollector {

    private static final boolean IS_DEMO = false;

    private static JSONObject outputJson = new JSONObject();
    private static String networkId, apiKey, baseURL;
    private static String TRAFFIC_UNIT = "bytes";
    private static String POLL_INTERVAL = "5";
    private static String PLUGIN_VERSION = "1";
    private static String HEARTBEAT_REQUIRED = "true";
    private static StringBuilder errorMessage = new StringBuilder();
    public static void main(String args[]) {
        if(args.length == 6 || IS_DEMO) {
            String pollIntervalInMinutes = args[3];
            apiKey = IS_DEMO ? "": args[0];
            networkId = IS_DEMO ? "": args[1];
            baseURL = IS_DEMO ? "": args[2];
            POLL_INTERVAL = IS_DEMO ? "300": String.valueOf((Integer.parseInt(pollIntervalInMinutes) * 60));
            PLUGIN_VERSION = IS_DEMO ? "1": args[4];
            HEARTBEAT_REQUIRED = IS_DEMO ? "true": args[5];
            try {
                outputJson.put("plugin_version",PLUGIN_VERSION);
                outputJson.put("heartbeat_required", HEARTBEAT_REQUIRED);
                outputJson.put("status", "1");
                getNetworkLatencyStats();
                getNetworkConnectionStats();
                getNetworkFailedConnections();
                outputJson.put("PollingInterval", pollIntervalInMinutes);
                outputJson.put("units",getUnitsJson());
                outputJson.put("msg", errorMessage.toString());
                System.out.println(outputJson);
            } catch (Exception ex) {
            	
            }
        }
    }
    
    private static void getNetworkLatencyStats() {
    	JSONObject latencyResponse;
        BufferedReader rd = null;
        try {
        	if(!IS_DEMO) {
        		URIBuilder uriBuilder = new URIBuilder(baseURL +"/networks/"+networkId+"/latencyStats");
	            uriBuilder.addParameter("timespan",POLL_INTERVAL);
	            HttpClient client = HttpClientBuilder.create().build();
	            HttpGet request = new HttpGet(uriBuilder.build());
	            request.addHeader("X-Cisco-Meraki-API-Key", apiKey);
	            HttpResponse response = client.execute(request);
	            rd = new BufferedReader(
	                    new InputStreamReader(response.getEntity().getContent()));

	            StringBuffer result = new StringBuffer();
	            String line = "";
	            while ((line = rd.readLine()) != null) {
	                result.append(line);
	            }
	            latencyResponse = new JSONObject(result.toString());
        	} else {
        		String result = getNetworkLatencyStatsDemoValue();
        		latencyResponse = new JSONObject(result);
        	}
            outputJson.put("Average Background Traffic", IS_DEMO? String.valueOf(Math.round(Math.random() * 10000000)) : latencyResponse.getJSONObject("backgroundTraffic").get("avg").toString());
            outputJson.put("Average BestEffort Traffic", IS_DEMO? String.valueOf(Math.round(Math.random() * 10000000)) : latencyResponse.getJSONObject("bestEffortTraffic").get("avg").toString());
            outputJson.put("Average Video Traffic", IS_DEMO? String.valueOf(Math.round(Math.random() * 10000000)) : latencyResponse.getJSONObject("videoTraffic").get("avg").toString());
            outputJson.put("Average Voice Traffic",  IS_DEMO? String.valueOf(Math.round(Math.random() * 10000000)) : latencyResponse.getJSONObject("voiceTraffic").get("avg").toString());
            
        } catch (Exception ex) {
        	try {
				outputJson.put("status", "0");
				errorMessage.append("Unable to collect Network Latency stats : "+ex.getMessage()+"\n");
			} catch (JSONException e) {
				e.printStackTrace();
			}
        } finally {
            try{
                rd.close();
            } catch(Exception e) {
                
            }
        }
    }

    private static void getNetworkConnectionStats() {
    	JSONObject connectionStatsResponse;
        BufferedReader rd = null;
        try {
        	if(!IS_DEMO) {
        		URIBuilder uriBuilder = new URIBuilder(baseURL +"/networks/"+networkId+"/connectionStats");
	            uriBuilder.addParameter("timespan",POLL_INTERVAL);
	            HttpClient client = HttpClientBuilder.create().build();
	            HttpGet request = new HttpGet(uriBuilder.build());
	            request.addHeader("X-Cisco-Meraki-API-Key", apiKey);
	            HttpResponse response = client.execute(request);
	            rd = new BufferedReader(
	                    new InputStreamReader(response.getEntity().getContent()));

	            StringBuffer result = new StringBuffer();
	            String line = "";
	            while ((line = rd.readLine()) != null) {
	                result.append(line);
	            }
	            connectionStatsResponse = new JSONObject(result.toString());
        	} else {
        		String result = getNetworkConnectionStatsDemoValue();
        		connectionStatsResponse = new JSONObject(result);
        	}
            outputJson.put("Assoc", connectionStatsResponse.get("assoc").toString());
            outputJson.put("Auth", connectionStatsResponse.get("auth").toString());
            outputJson.put("DHCP", connectionStatsResponse.get("dhcp").toString());
            outputJson.put("DNS", connectionStatsResponse.get("dns").toString());
            outputJson.put("Successful Connections", connectionStatsResponse.get("success").toString());

        } catch (Exception ex) {
        	try {
				outputJson.put("status", "0");
				errorMessage.append("Unable to collect Network Connection stats : "+ex.getMessage()+"\n");
			} catch (JSONException e) {
				e.printStackTrace();
			}
        } finally {
            try{
                rd.close();
            } catch(Exception e) {
                
            }
        }
    }

    private static void getNetworkFailedConnections() {
    	JSONArray failedConnectionsArray;
        BufferedReader rd = null;
        try {
        	if(!IS_DEMO) {
        		URIBuilder uriBuilder = new URIBuilder(baseURL +"/networks/"+networkId+"/failedConnections");
	            uriBuilder.addParameter("timespan",POLL_INTERVAL);
	            HttpClient client = HttpClientBuilder.create().build();
	            HttpGet request = new HttpGet(uriBuilder.build());
	            request.addHeader("X-Cisco-Meraki-API-Key", apiKey);
	            HttpResponse response = client.execute(request);
	            rd = new BufferedReader(
	                    new InputStreamReader(response.getEntity().getContent()));

	            StringBuffer result = new StringBuffer();
	            String line = "";
	            while ((line = rd.readLine()) != null) {
	                result.append(line);
	            }
	            failedConnectionsArray = new JSONArray(result.toString());
        	} else {
        		String result = getNetworkFailedConnectionsDemoValue();
        		failedConnectionsArray = new JSONArray(result);
        	}            
            outputJson.put("Number of Failed Connections", String.valueOf(failedConnectionsArray.length()));
        } catch (Exception ex) {
        	try {
				outputJson.put("status", "0");
				errorMessage.append("Unable to collect Network Failed Connection stats : "+ex.getMessage()+"\n");
			} catch (JSONException e) {
				e.printStackTrace();
			}

        } finally {
            try{
                rd.close();
            } catch(Exception e) {

            }
        }
    }

    private static JSONObject getUnitsJson() {
	JSONObject json = new JSONObject();
    	try {
    		json.put("Average Background Traffic", TRAFFIC_UNIT);
    		json.put("Average BestEffort Traffic", TRAFFIC_UNIT);
    		json.put("Average Video Traffic", TRAFFIC_UNIT);
    		json.put("Average Voice Traffic", TRAFFIC_UNIT);
    	} catch(Exception ex) {

    	}
	return json;
    }

    private static String getNetworkLatencyStatsDemoValue() throws Exception{
    	String sampleResponse = "{\"backgroundTraffic\":{\"rawDistribution\":{\"0\":1234,\"1\":2345,\"2\":3456,\"4\":4567,\"8\":5678,\"16\":6789,\"32\":7890,\"64\":8901,\"128\":9012,\"256\":83,\"512\":1234,\"1024\":2345,\"2048\":9999},\"avg\":606.52},\"bestEffortTraffic\":{\"rawDistribution\":{\"0\":1234,\"1\":2345,\"2\":3456,\"4\":4567,\"8\":5678,\"16\":6789,\"32\":7890,\"64\":8901,\"128\":9012,\"256\":83,\"512\":1234,\"1024\":2345,\"2048\":9999},\"avg\":486.52},\"videoTraffic\":{\"rawDistribution\":{\"0\":1234,\"1\":2345,\"2\":3456,\"4\":4567,\"8\":5678,\"16\":6789,\"32\":7890,\"64\":8901,\"128\":9012,\"256\":83,\"512\":1234,\"1024\":2345,\"2048\":9999},\"avg\":936.52},\"voiceTraffic\":{\"rawDistribution\":{\"0\":1234,\"1\":2345,\"2\":3456,\"4\":4567,\"8\":5678,\"16\":6789,\"32\":7890,\"64\":8901,\"128\":9012,\"256\":83,\"512\":1234,\"1024\":2345,\"2048\":9999},\"avg\":106.52}}";
    	JSONObject json = new JSONObject(sampleResponse);
    	return json.toString();
    }

    private static String getNetworkConnectionStatsDemoValue() throws Exception {
    	String sampleResponse = "{\"assoc\":1,\"auth\":5,\"dhcp\":0,\"dns\":0,\"success\":51}";
    	JSONObject json = new JSONObject(sampleResponse);
    	return json.toString();
    }

    private static String getNetworkFailedConnectionsDemoValue() throws Exception {
    	String sampleResponse = "[{\"ssidNumber\":0,\"vlan\":-1,\"clientMac\":\"00:61:71:c8:51:27\",\"serial\":\"Q2JC-2MJM-FHRD\",\"failureStep\":\"auth\",\"type\":\"802.1X auth fail\",\"ts\":1532032592},{\"ssidNumber\":0,\"vlan\":-1,\"clientMac\":\"00:61:71:c8:51:27\",\"nodeId\":\"Q2FJ-3SHB-Y2K2\",\"failureStep\":\"auth\",\"type\":\"802.1X auth fail\",\"ts\":1532032593},{\"ssidNumber\":0,\"vlan\":-1,\"clientMac\":\"00:61:71:c8:51:27\",\"nodeId\":\"Q2FJ-3SHB-Y2K2\",\"failureStep\":\"auth\",\"type\":\"802.1X auth fail\",\"ts\":1532032594},{\"ssidNumber\":0,\"vlan\":-1,\"clientMac\":\"00:61:71:c8:51:27\",\"nodeId\":\"Q2FJ-3SHB-Y2K2\",\"failureStep\":\"auth\",\"type\":\"802.1X auth fail\",\"ts\":1532032595},{\"ssidNumber\":0,\"vlan\":-1,\"clientMac\":\"1c:4d:70:7f:5e:5e\",\"nodeId\":\"Q2FJ-3SHB-Y2K2\",\"failureStep\":\"assoc\",\"type\":\"802.1X auth fail\",\"ts\":1532032592},{\"ssidNumber\":0,\"vlan\":-1,\"clientMac\":\"1c:4d:70:81:8d:0a\",\"nodeId\":\"Q2FJ-3SHB-Y2K2\",\"failureStep\":\"auth\",\"type\":\"802.1X auth fail\",\"ts\":1532032595}]";
    	JSONArray jsonArray = new JSONArray(sampleResponse);
    	return jsonArray.toString();
    }
}

