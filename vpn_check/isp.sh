#!/bin/bash
export ip="`curl -s ipecho.net/plain ; echo`" && export isp="`nslookup $ip | grep -w name | cut -d '=' -f2`" && echo $isp
