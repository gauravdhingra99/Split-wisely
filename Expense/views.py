from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum



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
			return render(request,'Expense/Expense_Page.html',{"expenses": qs.values('category__name','description','amount','date'),"sum":total})
		else:
			qs=Expense.objects.filter(user=request.user,description=des)
			summ=Expense.objects.filter(user=request.user,description=des).aggregate(Sum('amount'))
			total=list(summ.values())[0]			
			return render(request,'Expense/Expense_Page.html',{"expenses": qs.values('category__name','description','amount','date'),"sum":total})


def ExpenseAddAPIView(request):


	if request.method == 'POST':
		#print(request.POST)
		category=request.POST.get('category','')
		date=request.POST.get('date','')
		description=request.POST.get('description','')
		amount=request.POST.get('amount','')

		if category and date and description and amount:
			cat,cr=Category.objects.get_or_create(name=category)
			if cr:
				cat.save()
			obj,created=Expense.objects.get_or_create(user=request.user,category=cat,date=date,description=description,amount=amount)
			if created:
				obj.save()
			qs=Expense.objects.all()
			summ=Expense.objects.aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses":qs.values('category__name'),"sum":total})
		else:
			return render(request,'Expense/Add_expense.html',{"message":"category ,description,amount,date required"})

	return render(request,'Expense/Add_expense.html')





def AllGroups(request):
	if request.method == 'GET':
		grp=Group.objects.filter(user=request.user)
	return render(request,'Expense/Group_expense_Page.html',{"groupname": grp.values()})




def GroupExpenseView(request,id):

	if request.method == 'GET':
		UN=[]
		groupname=[]
		usernames=[]
		grp=Group.objects.filter(id=id)		
		for i in grp:

			Allusers=User.objects.filter(groups__name=i)
			for ussers in Allusers:
				usernames.append(ussers)
#			print(usernames)
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
				groupname.append(j.split)

		# print(groupname)
		return render(request,'Expense/Group_expense_Page2.html',{"groupname": groupname ,"id":id ,"username":usernames,'ALLUSERS':UN})


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
			Groups=Group.objects.all()
			return render(request,'Expense/Group_expense_Page.html',{"groupname":Groups.values()})
		else:
			return render(request,'Expense/Add_Group.html',{"message":"Group name required"})

	return render(request,'Expense/Add_Group.html')




def Add_user_view(request,id):
	#print("thihssssssss"+request.method)
	if request.method=='POST':
		usernames=[]
		groupname=[]
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
					groupname.append(j.split)


			return render(request,'Expense/Group_expense_Page2.html',{"message":"User is Added",'username':usernames,'ALLUSERS':UN,"id":id,"groupname":groupname})
		else:
			return render(request,'Expense/Add_Group.html',{"message":"Users field cannot be empty",'username':usernames,'ALLUSERS':UN,"id":id,"groupname":groupname})

	return render(request,'Expense/Group_expense_Page2.html',{'username':usernames})





	#my_group = Group.objects.get(name='DJ') 
	#my_group.user_set.add(User.objects.get(id=2))



def GroupExpenseAddAPIView(request,id):
	if request.method == 'POST':
		UN=[]
		groupname=[]
		usernames=[]	
		description=request.POST.get('description','')
		date=request.POST.get('date','')
		amount=request.POST.get('amount','')
		paidby=request.POST.get('paidby','')
		split=request.POST.get('split','')
		grp=Group.objects.filter(id=id)	
		userNam = User.objects.get(username=paidby)
		if description and date and amount and paidby and grp and split:
			obj=GroupExpense.objects.create(group=grp[0],paidby=userNam,date=date,description=description,amount=amount,split=split)
			obj.save()
			#print(obj)
			#qs=GroupExpense.objects.all()

			grp=Group.objects.filter(id=id)	   # All group of that id	
			for i in grp:
				Allusers=User.objects.filter(groups__name=i) # all Users in that group 
				Count=Allusers.count()
				for ussers in Allusers:
					# print(type(ussers))
					usernames.append(ussers)

				Divamount=int(amount)/Count   	#Equal divided amoun'''
				print(Divamount)

				for Users_in_Group in Allusers:
					cat,created=Category.objects.get_or_create(name='Group')
					if created:
						cat.save()
					obj,created=Expense.objects.get_or_create(user=Users_in_Group,category=cat,date=date,description=description,amount=Divamount)
					if created:
						obj.save()

				qs=Expense.objects.all()
				print(qs)		
				groups=GroupExpense.objects.filter(group=i) #Group Expense of that that Group 

				Ausers=User.objects.all() # All Existing USers
				for uss in Ausers:
					UN.append(uss)

				for j in groups:
					groupname.append(j.group)
					groupname.append(j.description)
					groupname.append(j.date)	
					groupname.append(j.amount)			
					groupname.append(j.paidby)
					groupname.append(j.split)


			# summ=GroupExpense.objects.aggregate(Sum('amount'))
			# total=list(summ.values())[0]
			return render(request,'Expense/Group_expense_Page2.html',{"groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id})
		else:
			return render(request,'Expense/Group_expense_Page2.html',{"message":"description,amount,date ,paid by ,split required","groupname":groupname,"username":usernames,'ALLUSERS':UN,"id":id})

	return render(request,'Expense/Group_expense_Page2.html')




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
			obj,created=Expense.objects.get_or_create(user=request.user,category=cat,date=date,description=description,amount=amount)
			if created:
				obj.save()
			qs=Expense.objects.filter(user=request.user)
			# user=request.user
			# grp=Group.objects.filter(id=user.id)
			# groups=GroupExpense.objects.filter(group=grp[0])
			# for j in groups:
			# 	groupname.append(j.group)
			# 	groupname.append(j.description)
			# 	groupname.append(j.date)	
			# 	groupname.append(j.amount)			
			# 	groupname.append(j.paidby)
			# 	groupname.append(j.split)


			summ=Expense.objects.aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses":qs.values('category__name','description','amount','date'),"sum":total})
		else:
			return render(request,'Expense/Add_expense.html',{"message":"category ,description,amount,date required"})

	return render(request,'Expense/Add_expense.html')













