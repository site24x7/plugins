#!usr/bin/python

import subprocess
import argparse
import json

heartbeat="true"
data={}
units={}
def rem(l):
	l=l.split(' ')
	try:
		while True:
			l.remove('')
	except ValueError:
			pass
	return l

def finder(l):
	size=[]
	c=0
	c1=0
	for i in l:
		try:
			c1+=1
			if ('g' or 'm'  in i) and c1==4:
				size.append(i)
			val=float(i)
			size.append(val)
			c+=1
			if c>=3:
				break
		except:
			pass
	return size
def metricCollector(vg,disk):

  try:
	output=subprocess.check_output("lvs "+vg,shell=True) 
	lvm=str(output.decode()).split('\n')
	lvm.pop(0)
	lvm.remove('')
	disk=disk.split(',')

	for i in lvm:

		info=rem(i)
		if info[0] in disk:
			space=finder(info)
			if 'm' in space[0]:
				space[0]=float(space[0].split('m')[0])/1024
			else:
				space[0]=float(space[0].split('g')[0])
			data_used=(space[1]/100)*space[0]
			meta_used=(space[2]/100)*space[0]
			data[info[0]+' Total Space']=space[0]
			data[info[0]+' Data Used in %']=space[1]
			data[info[0]+' Meta Used in %']=space[2]
			data[info[0]+' Data Used']=round(data_used,2)
			data[info[0]+' Meta Used']=round(meta_used,2)
			units[info[0]+' Data Used']='GB'
			units[info[0]+' Meta Used']='GB'
			units[info[0]+' Total Space']='GB'
			units[info[0]+' Data Used in %']='%'
			units[info[0]+' Meta Used in %']='%'
 	

  except Exception as e:
	data['status']=0
	data['msg']=e


if __name__== "__main__":

	parser=argparse.ArgumentParser()
	parser.add_argument('--vg',help="Volume Group",nargs='?')
	parser.add_argument('--lvm',help="Name of the LVM you want to monitor",nargs='?')
	parser.add_argument('--plugin_version',help="Plugin Version",nargs='?',default='1')
	args=parser.parse_args()
	metricCollector(args.vg,args.lvm)
	data['units']=units
	data['plugin_version']=args.plugin_version
	data['heartbeat_required']=heartbeat
	print(json.dumps(data,indent=4,sort_keys=True))
