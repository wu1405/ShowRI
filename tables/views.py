#!/usr/bin/env python
from django.shortcuts import render,render_to_response
from tables.models import Reserved_tmp,Reserved_final
from awsinfo.aws_server.models import Info
#Info is our asset tables. All instance details include
from boto.ec2.connection import EC2Connection
from boto.ec2 import get_region
import os,sys
import logging
import boto.ec2
from django.db.models import Count, Min, Sum, Avg

logging.basicConfig(level=logging.INFO,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %Y-%m-%d %H:%M:%S',
	filename='info.log',
	filemode='w')


def GetRI(request,accounts):

	Reserved_tmp.objects.all().delete()
	count_num = 0

	for account in accounts.split('-'):
		logging.info("the current account is %s" % account)

		areas=('ap-southeast-1','sa-east-1','eu-west-1')

		QuerysetList = []
		for area in areas:
			awskey = os.environ.get('%s_readkey' % account)
			awssecret = os.environ.get('%s_readsecret' % account)
			myRegion = get_region(area)
			conn = EC2Connection(aws_access_key_id=awskey,aws_secret_access_key=awssecret,region=myRegion)
	
			result=conn.get_all_reserved_instances()
			#QuerysetList = []
			for i in result:
				if i.state == 'active':
					QuerysetList.append(Reserved_tmp(region=i.availability_zone,type=i.instance_type,count=i.instance_count,duration=i.duration,end=i.end,account=account))
					count_num += 1
		Reserved_tmp.objects.bulk_create(QuerysetList)
	rs = "%s results insert into Reserved_tmp succeed" % count_num
	logging.info(rs)


	# ALL the type  Merge
	TypeList = []
	for i in Reserved_tmp.objects.values('type').annotate().order_by():
		TypeList.append(i['type'])
	for i in Info.objects.values('type').annotate().order_by():
		TypeList.append(i['type'])
	TypeList = list(set(TypeList))
	logging.info("All type is %s" % TypeList)

	# All the region
	RegionList = []
	for i in Reserved_tmp.objects.values('region').annotate().order_by():
		RegionList.append(i['region'])
	logging.info("All type is %s" % RegionList)

	# insert into the table "Reserved_final"
	Reserved_final.objects.all().delete()
	result=[]
	count_num2 = 0	

	for account in accounts.split('-'):
		logging.info("the current account is %s" % account)
		for i in RegionList:
			for j in TypeList:
				ri_num_tmp=lambda x,y: Reserved_tmp.objects.filter(region=x,type=y,account=account).extra(select={'total':'sum(count)'}).values()[0]['total'] if Reserved_tmp.objects.filter(region=x,type=y,account=account).extra(select={'total':'sum(count)'}).values()[0]['total'] else 0
				used_num_tmp=Info.objects.filter(region=i,type=j,status='running',account=account).count()	
				result.append(Reserved_final(region=i,\
											type=j,\
											used_num=used_num_tmp,\
											ri_num=ri_num_tmp(i,j),\
											delta=int(ri_num_tmp(i,j)-used_num_tmp),\
											account = account))
	
				count_num2 += 1
	Reserved_final.objects.bulk_create(result)
	rs2 = "%s results insert into Reserved_final succeed" % count_num2
	logging.info(rs2)

	
	return render_to_response('insert_ri.html',{'rs':rs,'rs2':rs2})



def ShowTable(request):
	results=[]
	for i in Reserved_final.objects.all():
		results.append({'region':i.region,'type':i.type,'used_num':i.used_num,'ri_num':i.ri_num,'delta':i.delta,'account':i.account})

	return render_to_response('show_table.html',{'results':results})
