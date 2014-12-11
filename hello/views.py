#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
import pymongo
import time

con=pymongo.Connection('127.0.0.1',27017)
db=con.cimc #find database

def index(req):
	return render_to_response('index.html',{})
@csrf_exempt
def user_review(req):
	collection=db.cimc_user #find table 
	message_table=db.cimc_message
	if req.is_ajax():
		username=req.POST['username']
		password=req.POST['password']
		email=req.POST['email']
		status=2
		recordtype=int(float(req.POST['recordtype']))
		recordname=req.POST['recordname']
		recordcode=req.POST['recordcode']
		recordtelphone=int(float(req.POST['recordtelphone']))
		recordcompany=req.POST['recordcompany']
		recordaddress=req.POST['recordaddress']
		regtime=int(time.time())
		userid='userid'
		for i in collection.find().sort([("userid",-1)]):
			userid=i['userid']+1
			break
		collection.insert({'username':username,'password':password,'email':email,'regtime':regtime,'status':2,'recordname':recordname,'recordcode':recordcode,'recordtelphone':recordtelphone,'recordcompany':recordcompany,'recordaddress':recordaddress,'userid':userid,'recordtype':recordtype})
	if req.method=='POST':
		pass_con=req.POST.get('content','')
		notpass_con=req.POST.get('content2','')	
		recover_con=req.POST.get('content3','')	
		#collection.update({'userid':1},{'$set':{'status':str(content)}})
		if pass_con != '':
			value=pass_con.split(',')
			for item in value:
				message={'from':'admin','to':int(float(item)),'type':1,'time':int(time.time()),'status':2,'result':1}
				message_table.update({'from':'admin','to':int(float(item)),'type':1,'status':2},message,upsert=True,multi=False)
#				message_table.insert(message)
				collection.update({'userid':int(float(item))},{'$set':{'status':2}})
		elif notpass_con != '':
			value=notpass_con.split(',')
			for item in value:
				message={'from':'admin','to':int(float(item)),'type':1,'time':int(time.time()),'status':-1,'result':1}
				message_table.update({'from':'admin','to':int(float(item)),'type':1,'status':-1},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':-1}})
		elif recover_con != '':
			#collection.update({'userid':1},{'$set':{'status':str(recover_con)}})
			value=recover_con.split(',')
			for item in value:
#				message={'from':'admin','to':int(float(item)),'type':1,'time':int(time.time()),'status':1,'result':1}
				message_table.remove({'from':'admin','to':int(float(item)),'type':1})
				collection.update({'userid':int(float(item))},{'$set':{'status':1}})
	user=[]
	user_review=[]
	for i in collection.find().sort([("regtime",-1)]):
		if i['status']==0 or i['status']==1:
			item=[]
			item.append(i['recordname'])
			item.append(i['recordcompany'])
			item.append(i['recordtelphone'])
			item.append(i['recordcode'])
			item.append(i['recordaddress'])
			if int(i['recordtype'])==1:
				item.append('个人用户')
			else:
				item.append('厂商用户')
			item.append(i['userid'])
			user.append(item)
		else:
			item=[]
			item.append(i['recordname'])
			item.append(i['recordcompany'])
			item.append(i['recordtelphone'])
			item.append(i['recordcode'])
			regtime=float(i['regtime'])
			item.append(transfer_time(regtime))
			if int(i['recordtype'])==1:
				item.append('个人用户')
			else:
				item.append('厂商用户')
			item.append(i['userid'])
			if i['status']==2:
				item.append('审核通过')
			else:
				item.append('审核未通过')
			user_review.append(item)
	return render_to_response('user-review.html',{'user':user,'user_review':user_review},context_instance=RequestContext(req))

@csrf_exempt
def device_review(req):
	collection=db.cimc_device #find table 
	message_table=db.cimc_message
	if req.is_ajax():
		#collection.update({'userid':16},{'$set':{'status':8}})
		serial_str=req.POST['serialnumber']
		serial_userid=req.POST['userid']
		serial_list=serial_str.split('/')
		collection.update({'userid':int(float(serial_userid))},{'$set':{'serialnumber':serial_list}})
		#collection.update({'userid':19},{'$set':{'status':int(float(seroa_userid))}})
	if req.method=='POST':
		pass_company_con=req.POST.get('content','')
		notpass_company_con=req.POST.get('content2','')	
		pass_bind_con=req.POST.get('content3','')
		notpass_bind_con=req.POST.get('content4','')	
		recover_con=req.POST.get('content5','')	
		#collection.update({'userid':1},{'$set':{'status':str(content)}})
		#collection.update({'userid':1},{'$set':{'status':str(pass_bind_con)}})
		if pass_company_con != '':
			value=pass_company_con.split(',')
			for item in value:
				device_type=''
				for device_item in collection.find({'level':2,'userid':int(float(item))}):
					device_type=device_item['devicetype']
				message={'from':'admin','to':int(float(item)),'type':2,'time':int(time.time()),'status':2,'result':1,'devicetype':device_type}
				message_table.update({'from':'admin','to':int(float(item)),'type':2,'status':2},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':2}},multi=True)
		elif notpass_company_con != '':
			value=notpass_company_con.split(',')
			for item in value:
				device_type=''
				for device_item in collection.find({'level':2,'userid':int(float(item))}):
					device_type=device_item['devicetype']
				message={'from':'admin','to':int(float(item)),'type':2,'time':int(time.time()),'status':-1,'result':1,'devicetype':device_type}
				message_table.update({'from':'admin','to':int(float(item)),'type':2,'status':-1},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':-1}},multi=True)
		elif pass_bind_con != '':
			value=pass_bind_con.split(',')
			for item in value:
				device_number=''
				for number_item in collection.find({'level':3,'userid':int(float(item))}):
					device_number=number_item['devicenumber']
				message={'from':'admin','to':int(float(item)),'type':3,'time':int(time.time()),'status':2,'result':1,'devicenumber':device_number}
				message_table.update({'from':'admin','to':int(float(item)),'type':3,'status':2},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':2}})
		elif notpass_bind_con != '':
			value=notpass_bind_con.split(',')
			for item in value:
				device_number=''
				for number_item in collection.find({'level':3,'userid':int(float(item))}):
					device_number=number_item['devicenumber']
				message={'from':'admin','to':int(float(item)),'type':3,'time':int(time.time()),'status':-1,'result':1,'devicenumber':device_number}
				message_table.update({'from':'admin','to':int(float(item)),'type':3,'status':-1},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':-1}})
		elif recover_con != '':
			value=recover_con.split(',')
		        #collection.update({'userid':1},{'$set':{'state':str(value)}})
			for item in value:
				message_table.remove({'from':'admin','to':int(float(item))})
				collection.update({'userid':int(float(item))},{'$set':{'status':1}},multi=True)
	device=[]
	devicebind=[]
	device_review=[]
	for i in collection.find().sort([("recordtime",-1)]):
		if i['status']==0 or i['status']==1:
			if i['level']==3:
				item=[]
				item.append(i['devicecompany'])
				item.append(i['devicetype'])
				item.append(i['chaintype'])	
				serial_split=''			
				for j,serial_item in enumerate(i['serialnumber']):
					if j!=(len(i['serialnumber'])-1):
						serial_split=serial_split+serial_item+'/'
					else:
						serial_split=serial_split+serial_item
				item.append(serial_split)
				uploadtime=float(i['recordtime'])/1000
				item.append(transfer_time(uploadtime))
				item.append(i['userid'])
				devicebind.append(item)
			elif i['level']==2:
				item=[]
				item.append(i['devicecompany'])
				item.append(i['devicetype'])
				item.append(i['chaintype'])
				uploadtime=float(i['recordtime'])/1000
				item.append(transfer_time(uploadtime))
				item.append(i['userid'])
				device.append(item)
		elif i['level']!=1:
			item=[]
			if i['level']==3:
				item.append('个人用户')
			else:
				item.append('设备厂商')
			item.append(i['devicecompany'])
			item.append(i['devicetype'])
			item.append(i['chaintype'])
			if i['level']==3:
				item.append(i['serialnumber'])
			else:
				item.append('XXXXXXXXX')
			uploadtime=float(i['recordtime'])/1000
			item.append(transfer_time(uploadtime))
			item.append(i['userid'])
			if i['status']==2:
				item.append('审核通过')
			else:
				item.append('审核未通过')
			device_review.append(item)
	return render_to_response('device-review.html',{'device':device,'device_bind':devicebind,'device_review':device_review},context_instance=RequestContext(req))
def middleware_review(req):
	collection=db.cimc_midware #find table
	message_table=db.cimc_message
	message_table=db.cimc_message 
	if req.method=='POST':
		pass_con=req.POST.get('content','')
		notpass_con=req.POST.get('content2','')	
		recover_con=req.POST.get('content3','')	
		#collection.update({'userid':1},{'$set':{'status':str(content)}})
		if pass_con != '':
			value=pass_con.split(',')
			for item in value:
				midware_id=''
				for midware_item in collection.find({'userid':int(float(item))}):
					midware_id=midware_item['midwareid']
				message={'from':'admin','to':int(float(item)),'type':4,'time':int(time.time()),'status':1,'result':1,'midware_id':midware_id}
				message_table.update({'from':'admin','to':int(float(item)),'type':4,'status':1},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':1}})
		elif notpass_con != '':
			value=notpass_con.split(',')
			for item in value:
				midware_id=''
				for midware_item in collection.find({'userid':int(float(item))}):
					midware_id=midware_item['midwareid']
				message={'from':'admin','to':int(float(item)),'type':4,'time':int(time.time()),'status':-1,'result':1,'midware_id':midware_id}
				message_table.update({'from':'admin','to':int(float(item)),'type':4,'status':-1},message,upsert=True,multi=False)
				collection.update({'userid':int(float(item))},{'$set':{'status':-1}})
		elif recover_con != '':
			value=recover_con.split(',')
		        #collection.update({'userid':1},{'$set':{'state':str(value)}})
			for item in value:
				message_table.remove({'from':'admin','to':int(float(item)),'type':4})
				collection.update({'userid':int(float(item))},{'$set':{'status':0}})
	midware=[]
	midware_review=[]
	for i in collection.find().sort([("uploadtime",-1)]):
		if i['status']==0:
			item=[]
			item.append(i['devicecompany'])
			item.append(i['midwareversion'])
			item.append(i['devicetype'])
			uploadtime=float(i['uploadtime'])
			item.append(transfer_time(uploadtime))
			item.append(i['userid'])
			midware.append(item)
		else:
			item=[]
			item.append(i['devicecompany'])
			item.append(i['midwareversion'])
			item.append(i['uploadtime'])
			uploadtime=float(i['uploadtime'])
			item.append(transfer_time(uploadtime))
			item.append(i['userid'])
			if i['status']==1:
				item.append('审核通过')
			else:
				item.append('审核未通过')
			midware_review.append(item)
	return render_to_response('middleware-review.html',{'midware':midware,'midware_review':midware_review},context_instance=RequestContext(req))
	return render_to_response('middleware-review.html',{})
def kvm_manage(req):
	return render_to_response('kvm-manage.html',{})
def server_info(req):
	return render_to_response('server-info.html',{})

def transfer_time(timestamp):
	time_array=time.localtime(timestamp)
	result_time=time.strftime("%Y-%m-%d %H:%M:%S",time_array)
	return result_time
# Create your views here.
