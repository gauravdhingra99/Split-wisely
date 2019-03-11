from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.core import serializers
from django.http import JsonResponse


# PAYERS=list()
# OWERS=list()
# PAIDEE=list()
from rest_framework import generics,mixins
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from Expense.models import *
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
			


def ExpenseListAPIView(request):

	if request.method == 'GET':
		des=request.GET.get('description')	
		if des==None:
			qs=Expense.objects.filter(user=request.user)
			summ=Expense.objects.aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses": qs.values('category__name','description','amount','owe','date'),"sum":total})
		else:
			qs=Expense.objects.filter(user=request.user,description=des)
			summ=Expense.objects.filter(user=request.user).aggregate(Sum('amount'))
			total=list(summ.values())[0]			
			return render(request,'Expense/Expense_Page.html',{"expenses": qs.values('category__name','description','owe','amount','date'),"sum":total})



def ExpenseAddAPIView(request):
	if request.method == 'POST':
		#print(request.POST)
		category=request.POST.get('category','')
		date=request.POST.get('date','')
		description=request.POST.get('description','')
		amount=request.POST.get('amount','')
		groupname=[]
		if category and date and description and amount:
			cat,cr=Category.objects.get_or_create(name=category)
			if cr:
				cat.save()
			obj=Expense.objects.create(user=request.user,category=cat,date=date,description=description,amount=amount,owe=0.0)
			obj.save()
			qs=Expense.objects.filter(user=request.user)
			summ=Expense.objects.filter(user=request.user).aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses":qs.values('category__name','description','amount','owe','date'),"sum":total})
		else:
			return render(request,'Expense/Add_expense.html',{"message":"category ,description,amount,date required"})

	return render(request,'Expense/Add_expense.html')


def ExpenseDelView(request):
	if request.method == 'GET':
		print(request.method)
		des=request.GET.get('delt')	
		if des!=None:
			qs=Expense.objects.filter(user=request.user,description=des)
			if qs:
				qs.delete()
				queryset=Expense.objects.filter(user=request.user)
				print(qs)
				return render(request,'Expense/Expense_Page2.html',{"message":"Deleted","expenses": queryset.values('category__name','description','owe','amount','date')})
			else:
				queryset=Expense.objects.filter(user=request.user)
				return render(request,'Expense/Expense_Page2.html',{"message":"This expenses doesnt exists","expenses": queryset.values('category__name','description','owe','amount','date')})

		else:
			queryset=Expense.objects.filter(user=request.user)
			return render(request,'Expense/Expense_Page2.html',{"message":"Del Field cannot be empty on this url","expenses": queryset.values('category__name','description','owe','amount','date')})


def AllGroups(request):
	if request.method == 'GET':
		user=request.user
		grp=user.groups.all()
	return render(request,'Expense/Group_expense_Page.html',{"groupname": grp.values()})




def GroupExpenseView(request,id):

	if request.method == 'GET':
		UN=[]
		groupname=[]
		usernames=[]
		Musernames=[]
		grp=Group.objects.filter(id=id)		
		for i in grp:

			Allusers=User.objects.filter(groups__name=i)
			for ussers in Allusers:
				usernames.append(ussers)
				Musernames.append(ussers)
			usernames.append('Multiple-Users')
			print(usernames)
			Ausers=User.objects.all()
			for uss in Ausers:
				UN.append(uss)
#			print(UN)

			groups=GroupExpense.objects.filter(group=i)
			for j in groups:
				groupname.append(j.group)
				groupname.append(j.description)
				groupname.append(j.date)	
				groupname.append(j.amount)			
				groupname.append(j.paidby)
				if j.split==True:
					groupname.append("Equally")
				else:
					groupname.append("UnEqually")

			pdl="Add Group Expense-Balances Will Update"

		# print(groupname)
		return render(request,'Expense/Group_expense_Page2.html',{"groupname": groupname ,"id":id ,"username":usernames,'ALLUSERS':UN,'Musernames':Musernames,"disclamer":pdl})


def Add_Group(request):
	# print("asdadjadsaldj")
	if request.method == 'POST':
		# print(request.POST)
		Gname=request.POST.get('groupname')
		if Gname:
			Grop,created=Group.objects.get_or_create(name=Gname)
			if created:
				Grop.save()
			my_group = Group.objects.get(name=Grop.name) 
			my_group.user_set.add(request.user)
			user=request.user
			Groups=user.groups.all()
			return render(request,'Expense/Group_expense_Page.html',{"groupname":Groups.values()})
		else:
			return render(request,'Expense/Add_Group.html',{"message":"Group name required"})

	return render(request,'Expense/Add_Group.html')




def Add_user_view(request,id):
	#print("thihssssssss"+request.method)
	if request.method=='POST':
		usernames=[]
		groupname=[]
		Musernames=[]

		UN=[]
		Uname=request.POST.get('addUser')
		Fname=User.objects.get(username=Uname)
		if Fname and Uname:
			my_group = Group.objects.get(id=id)
			my_group.user_set.add(Fname)
			grp=Group.objects.filter(id=id)		
			for i in grp:
				Allusers=User.objects.filter(groups__name=i)
				for ussers in Allusers:
					usernames.append(ussers)
					Musernames.append(ussers)


				usernames.append('Multiple-Users')

				Ausers=User.objects.all()
				for uss in Ausers:
					UN.append(uss)

				groups=GroupExpense.objects.filter(group=i)
				for j in groups:
					groupname.append(j.group)
					groupname.append(j.description)
					groupname.append(j.date)	
					groupname.append(j.amount)			
					groupname.append(j.paidby)
					if j.split==True:
						groupname.append("Equally")
					else:
						groupname.append("UnEqually")


			return render(request,'Expense/Group_expense_Page2.html',{"message":"User is Added",'username':usernames,'ALLUSERS':UN,"id":id,"groupname":groupname,"Musernames":Musernames})
		else:
			return render(request,'Expense/Add_Group.html',{"message":"Users field cannot be empty",'username':usernames,'ALLUSERS':UN,"id":id,"groupname":groupname,"Musernames":Musernames})

	return render(request,'Expense/Group_expense_Page2.html')





	#my_group = Group.objects.get(name='DJ') 
	#my_group.user_set.add(User.objects.get(id=2))



def GroupExpenseAddAPIView(request,id):
	UN=[]
	groupname=[]
	usernames=[]	
	Musernames=[]
	onlyusername=[]	
	if request.method == 'POST':
		grp=Group.objects.filter(id=id)	
		for i in grp:
			Allusers=User.objects.filter(groups__name=i) # all Users in that group 
			Count=Allusers.count()
			for ussers in Allusers:
				usernames.append(ussers)
				Musernames.append(ussers)
				onlyusername.append(ussers.username)

			usernames.append('Multiple-Users')

		Ausers=User.objects.all() # All Existing USers
		for uss in Ausers:
			UN.append(uss)

		Gpn=Group.objects.filter(id=id)[0].name					


		pdlist=[]
		userNam=[]
		userName=[]
		description=request.POST.get('description','')
		date=request.POST.get('date','')
		amount=request.POST.get('amount','')
		paidby=request.POST.get('paidby','')
		#print(Musernames)
		# print("paidby"+str(paidby))
		if paidby== 'Multiple-Users':
			cnt=0
			while(cnt<Count):
				y=request.POST.get(str(Musernames[cnt]),'0')
				pdlist.append(int(y))
				userNam.append(User.objects.get(username=Musernames[cnt]))
				userName.append(Musernames[cnt])
				cnt=cnt+1
			if sum(pdlist)!= int(amount):
				return render(request,'Expense/Group_expense_Page2.html',{"message":"amount and Distribution of money is not Same Please Add Again","groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id,"Musernames":Musernames})


		else:
			userNam.append(User.objects.get(username=paidby))
			# print(userNam)

		split=request.POST.get('split','')
#		print(pdlist)
	


		# def get_users(request):
		# 	data = serializers.serialize('json', userNam)
		# 	print(data)
		# 	return JsonResponse(data, safe=False)


		
		print("--------------------------------------------")
		print(onlyusername)
		if description and date and amount and paidby!='Multiple-Users' and grp and split:
			print('here')
			obj=GroupExpense.objects.create(group=grp[0],paidby=paidby,date=date,description=description,amount=amount,split=split)
			obj.save()
			if len(Allusers)>1:
				Divamount=int(amount)/Count
				Famount=int(amount)-Divamount
			else:
				Famount=int(amount)

			Dicts={userNam[0]:Famount}
			#print(Dicts)
			Dict1={userNam[0]:Famount}
			global Dict2
			Dict2={'':''}
			ul=0
			pdlist.append(amount)
			for Users_in_Group in Allusers:
				if Users_in_Group !=userNam[0]:
					pdlist.append(0)
					Dicts.update({Users_in_Group:"-"+str(Divamount)})
					Dict2.update({Users_in_Group:(Divamount)})
				else:
					continue
			del Dict2['']
			# for i in PAYERS:
			# 	for j,k in i.items():
			# 		for l in OWERS:
			# 			for m,n in l.items():
			# 				if j==m:
			# 					k=k-n
			# 					dict.update({j:k})
			 	

			
			

			pdl={userNam[0]:amount}
			
			for U_in_Group,FO in Dicts.items():
				cat,created=Category.objects.get_or_create(name='Group - ' + str(Gpn))
				if created:
					cat.save()
				if float(FO)<=0.0:
					obj,created=Expense.objects.get_or_create(user=U_in_Group,category=cat,date=date,description=description,amount=0,owe=float(FO))
					if created:
						obj.save()
				else:
					obj,created=Expense.objects.get_or_create(user=U_in_Group,category=cat,date=date,description=description,amount=amount,owe=float(FO))
					if created:
						obj.save()


			groups=GroupExpense.objects.filter(group=grp[0]) #Group Expense of that that Group 

			for j in groups:
				groupname.append(j.group)
				groupname.append(j.description)
				groupname.append(j.date)	
				groupname.append(j.amount)			
				groupname.append(j.paidby)
				if j.split==True:
					groupname.append("Equally")
				else:
					groupname.append("UnEqually")

				#print(groupname)

			
	


			return render(request,'Expense/Group_expense_Page2.html',{"groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id,"Musernames":Musernames,"Dicts":Dicts,"Dict1":Dict1,"Dict2":Dict2,"NM":userNam[0],"PAID":pdl,"description":description})

		elif description and date and amount and paidby=='Multiple-Users' and grp and split:
			print("thid id usersnmrs")
			print(userName)
			obj=GroupExpense.objects.create(group=grp[0],paidby=onlyusername,date=date,description=description,amount=amount,split=split)
			obj.save()
			c=0
			sm=sum(pdlist)
			Divamount=int(sm)/Count
			print("this is sum"+str(sm))
			finlst=[]
			while(c<len(pdlist)):
				finlst.append(pdlist[c]-Divamount)
				c=c+1
			Dict1={"":""}
			Dict2={"":""}
			c=0
			while(c<len(finlst)):
				if(finlst[c]>0):
					Dict1.update({userNam[c]:finlst[c]})
				else:
					Dict2.update({userNam[c]:abs(float(finlst[c]))})
				c=c+1
			del Dict2['']
			del Dict1['']
			print(Dict1)
			print(Dict2)
			print(userNam)
			print(pdlist)
			print(Divamount)
			print(finlst)

			ul=0		
			for Users_in_Group in Allusers:
				cat,created=Category.objects.get_or_create(name='Group - ' + str(Gpn))
				if created:
					cat.save()
				obj=Expense.objects.create(user=Users_in_Group,category=cat,date=date,description=description,amount=pdlist[ul],owe=float(finlst[ul]))
				obj.save()
				ul=ul+1

			groups=GroupExpense.objects.filter(group=grp[0]) #Group Expense of that that Group 

			for j in groups:
				groupname.append(j.group)
				groupname.append(j.description)
				groupname.append(j.date)	
				groupname.append(j.amount)			
				groupname.append(j.paidby)
				if j.split==True:
					groupname.append("Equally")
				else:
					groupname.append("UnEqually")

			print(groupname)

			pdl={"":""}
			i=0
			while(i<len(pdlist)):
				pdl.update({userNam[i]:pdlist[i]})
				i=i+1

			del pdl['']

				

			return render(request,'Expense/Group_expense_Page2.html',{"groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id,"Musernames":Musernames,"Dict1":Dict1,"Dict2":Dict2,"PAID":pdl,"description":description})
		

		else:
			return render(request,'Expense/Group_expense_Page2.html',{"message":"description,amount,date ,paid by ,split required","groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id,"Musernames":Musernames})

	return render(request,'Expense/Group_expense_Page2.html',{"groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id,"Musernames":Musernames})

















