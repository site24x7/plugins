#!/bin/bash

##### Site24x7 Configuration Constants #####
PLUGIN_VERSION=1
HEARTBEAT_REQUIRED=true

##### Plugin Initialization #####

DATA='{}'

DATA=$( echo $DATA | jq '. + {"plugin_version": "'$PLUGIN_VERSION'"}') 
DATA=$( echo $DATA | jq '. + {"heartbeat_required": "'$HEARTBEAT_REQUIRED'"}') 

##### Plugin Code #####


##### ss -s | grep UDP is not working with the bash due to some library issue. So, parsing the whole output
##### Actual Output :
# Total: 1848 (kernel 2585)
# TCP:   71 (estab 31, closed 8, orphaned 2, synrecv 0, timewait 7/0), ports 0
# 
# Transport Total     IP        IPv6
# *	  2585      -         -        
# RAW	  1         0         1        
# UDP	  21        18        3        
# TCP	  63        53        10       
# INET	  85        71        14       
# FRAG	  0         0         0      

CMD='ss -s'
declare OUTPUT=$($CMD)

SAVEIFS=$IFS   		# Save current IFS, as changing this will affect the system settings.
IFS=$'\n'      		# Change IFS to new line. Will be changed back to SAVEIFS
OUTPUT=($OUTPUT) 	# Convert the String to String[] with newline as the split



## Iterate each line and check if it starts with UDP/TCP. 
## Assumptions : 
## 	For udp, Only a single line of UDP is available
##	For TCP, ignore the line TCP:
for (( i=0; i<${#OUTPUT[@]}; i++ ))
do
	## If it matches, split the line with space to get the metrics
    if [[ ${OUTPUT[$i]} = UDP* ]]
	then
		LINE="${OUTPUT[$i]}"
		IFS=$' '     # Change IFS to new line
		VALS=($LINE) # split to array $OUTPUT
		IFS=$SAVEIFS   # Restore IFS
		
		### Transport 	Total     IP        IPv6
		### UDP	  		21        18        3        
		DATA=$( echo $DATA | jq '. + {"udp_total": 	'${VALS[1]}'}') 
		DATA=$( echo $DATA | jq '. + {"udp_ip": 	'${VALS[2]}'}') 
		DATA=$( echo $DATA | jq '. + {"udp_ipv6": 	'${VALS[3]}'}') 
	fi

	if [[ ${OUTPUT[$i]} = TCP* && ${OUTPUT[$i]} != TCP:* ]]
	then
		LINE="${OUTPUT[$i]}"
		IFS=$' '     # Change IFS to new line
		VALS=($LINE) # split to array $OUTPUT
		IFS=$SAVEIFS   # Restore IFS
		
		### Transport 	Total     IP        IPv6
		### TCP	  		21        18        3        
		DATA=$( echo $DATA | jq '. + {"tcp_total": 	'${VALS[1]}'}') 
		DATA=$( echo $DATA | jq '. + {"tcp_ip": 	'${VALS[2]}'}') 
		DATA=$( echo $DATA | jq '. + {"tcp_ipv6": 	'${VALS[3]}'}') 
	fi
done

IFS=$SAVEIFS   		# Restore IFS

### Print the data
echo $DATA  | jq '.' 
