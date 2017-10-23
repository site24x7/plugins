#!/bin/bash
export PLUGIN_VERSION="1"
export HEARTBEAT="true"
export METRICS_UNITS="{php_cpu - % , php_mem - % , mysql_cpu - % , mysql_mem - %}"

#Change this value to "ENABLED" only if you have configured apache stats as mentioned in the help doc
APACHE_STATS="DISABLED"
#Change the Apache stats URL accordingly. Retain the "?auto" suffix.
APACHE_STATUS_URL="http://localhost:80/status?auto"

APACHE_VERSION="NONE"
PHP_VERSION="NONE"
MYSQL_VERSION="NONE"


findApacheVersion()
{
if [ -f /usr/sbin/apache2 ]; then
        APACHE_VERSION_COMMAND="apache2 -v"
elif [ -f /usr/sbin/httpd ]; then
        APACHE_VERSION_COMMAND="httpd -v"
fi

$APACHE_VERSION_COMMAND 2>/dev/null | awk 'BEGIN{
FS="version:";
ORS="|";
}
{
if(NR == 1)
if($2) 
        print "apache_version:"$2
else
        print "apache_version:-1"
}'

/bin/ps -eo pid,fname | grep -v grep | grep -E '(apache|httpd)' | wc -l | awk 'BEGIN{
ORS="|";
}
{
if(NR==1)
        if ($0 > 0)
                print "apache_status:1"
else
                print "apache_status:0"
}'

}

findMySQLVersion()
{

MYSQL_VERSION_COMMAND="mysqld --version"
$MYSQL_VERSION_COMMAND 2>/dev/null | awk 'BEGIN{
FS=" ";       
ORS="|";
}
{ if(NR==1)
        if($3)
                print "mysql_version:"$3
        else
                print "mysql_version:0"
}'

/bin/ps -eo fname,%cpu,%mem | grep -v grep | grep -E -i '(mysql)' | awk 'BEGIN {
	cpu=0;
	mem=0;
	ORS="|";
}
{
	#print $3,$4,NR
	cpu = cpu + $2
	mem = mem + $3
	#print cpu,mem
}
END {
	if(NR > 0)
		print "mysql_cpu:"cpu/NR"|mysql_mem:"mem/NR"|mysql_status:1"
	else
		print "mysql_status:0"
}'


}

findPHPVersion()
{

PHP_VERSION_COMMAND="php -v"
$PHP_VERSION_COMMAND 2>/dev/null | awk 'BEGIN{
FS=" ";
ORS="|";
}
{ if(NR==1)
        if($2)
                print "php_version:"$2
        else
                print "php_version:-1"
}'

/bin/ps -eo fname,%cpu,%mem | grep -v grep | grep -E -i '(php)' | awk 'BEGIN {
	cpu=0;
	mem=0;
	ORS="|";
}
{
	#print $3,$4,NR
	cpu = cpu + $2
	mem = mem + $3
	#print cpu,mem
}
END {
	if(NR > 0)
		print "php_cpu:"cpu/NR"|php_mem:"mem/NR"|php_status:1"
	else
		print "php_status:0"
}'
}

getApacheStats()
{	
	
        curl -sS $APACHE_STATUS_URL 2>/dev/null | awk 'BEGIN{ 
        FS=":";
        RS="\n";
        ORS="|";
        }
        {
		if($1)       
			if(NR < 10) 
                        	print "apache",$1":"$2
        }
        END{ print "plugin_version:'"$PLUGIN_VERSION"'|heartbeat_required:'"$HEARTBEAT"'|units:'"$METRICS_UNITS"'"}'
}

main()
{
        findApacheVersion
        findPHPVersion
        findMySQLVersion
	if [ "$APACHE_STATS" = "ENABLED" ]; then
        	getApacheStats | rev | cut -c 2- | rev
	else
		echo "plugin_version:"$PLUGIN_VERSION"|heartbeat_required:"$HEARTBEAT"|units:"$METRICS_UNITS
	fi
}

main
