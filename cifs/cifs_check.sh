#!/bin/bash
check(){
	#echo "check"
	#echo $1
        path=$1
	ipaddr=$(mount -l -t cifs | grep -w "$path" | awk -F'[(|,|=|)]' '{ for(i=1;i<=NF;i++) if ($i == "addr") print $(i+1) }')
	#echo $ipaddr
        if [ "$ipaddr" ]
        then
		echo "$ipaddr" |
                while read line
                do
                        #echo "$line:ss"
                        df -k ${MP} &>/dev/null &
                        DFPID=$!
                        #echo $DFPID
                        for (( i=1 ; i< 3 ; i++ )) ; do
                                if ps -p $DFPID > /dev/null ; then
					sleep 1
                                else
                                       break
                                fi
                        done
                        if ps -p $DFPID > /dev/null ; then
                                $(kill -s SIGTERM $DFPID &>/dev/null)
                                #echo 'stale error'
                                echo "-2"
                        else 
                                varr=$(findmnt | grep -w $path)
                                disk=$(df $path | grep -w $path)
                                disp="$varr@@@@@@$disk"
                                
                                if [ "$output" ]
                                then
                                        echo "$disp%%1"
                                else
                                        echo "$disp%%0"
                                fi
                        fi
                done
        else
                echo "-1"
        fi
}
main(){
	#echo "main"
        check $1
}
main $1
