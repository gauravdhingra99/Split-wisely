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
			return render(request,'Expense/Expense_Page.html',{"expenses": qs.values(),"sum":total})
		else:
			qs=Expense.objects.filter(user=request.user,description=des)
			summ=Expense.objects.filter(user=request.user,description=des).aggregate(Sum('amount'))
			total=list(summ.values())[0]			
			return render(request,'Expense/Expense_Page.html',{"expenses": qs.values(),"sum":total})


def ExpenseAddAPIView(request):


	if request.method == 'POST':
		#print(request.POST)
		category=request.POST.get('category','')
		date=request.POST.get('date','')
		description=request.POST.get('description','')
		amount=request.POST.get('amount','')

		if category and date and description and amount:
			cat,created=Category.objects.get_or_create(name__iexact=category)
			if created:
				cat.save()
			obj,created=Expense.objects.get_or_create(user=request.user,category=cat,date=date,description=description,amount=amount)
			if created:
				obj.save()
			qs=Expense.objects.all()
			summ=Expense.objects.aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses":qs.values(),"sum":total})
		else:
			return render(request,'Expense/Add_expense.html',{"message":"category ,description,amount,date required"})

	return render(request,'Expense/Add_expense.html')











def AllGroups(request):
	if request.method == 'GET':
		grp=Group.objects.filter(user=request.user)
	return render(request,'Expense/Group_expense_Page.html',{"groupname": grp.values()})




def GroupExpenseView(request,id):

	if request.method == 'GET':
		groupname=[]
		groupnae=[]
		grp=Group.objects.filter(id=id)		
		print(grp.values())
		for i in grp:
			# print(i)
			Allusers=User.objects.filter(groups__name=i)
			groups=GroupExpense.objects.filter(group=i)
			# print(groups)
			for j in groups:
				groupname.append(j.group)
				groupname.append(j.description)
				groupname.append(j.date)	
				groupname.append(j.amount)			
				groupname.append(j.paidby)
				groupname.append(j.split)

		# print(groupname)
		return render(request,'Expense/Group_expense_Page2.html',{"groupname": groupname})


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



	





def GroupExpenseAddAPIView(request):

	if request.method == 'POST':

		description=request.POST.get('description','')
		date=request.POST.get('date','')
		amount=request.POST.get('amount','')
		paidby=request.POST.get('paidby','')
		split=request.POST.get('split','')
		G_id=request.query_params.get('id')		
		print(G_id)
		if description and date and amount and paidby and split:
			obj,created=GroupExpense.objects.get_or_create(group=,paidby=paidby,date=date,description=description,amount=amount,split=split)
			if created:
				obj.save()
			qs=Expense.objects.all()
			summ=Expense.objects.aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses":qs.values(),"sum":total})
		else:
			return render(request,'Expense/Add_Group_expense.html',{"message":"category ,description,amount,date required"})

	return render(request,'Expense/Add_Group_expense.html')









# def CreateGroupExpense(request):
# 	if request.method == 'POST':


# def deleteview(request):
# 	delt=request.GET.get('delt')
# 	print(delt)
# 	if delt!=None:
# 		tbd=Expense.objects.filter(description=delt)
# 		if tbd is not None:
# 			tbd.delete()
# 			data=Expense.objects.all()
# 			return render(request,'Expense/Expense_Page.html',{"expenses": data.values()})
# 		else:
# 			return render(request,{"message":"This Discription in not available"})



def ExpenseAddAPIView(request):


	if request.method == 'POST':
		#print(request.POST)
		category=request.POST.get('category','')
		date=request.POST.get('date','')
		description=request.POST.get('description','')
		amount=request.POST.get('amount','')

		if category and date and description and amount:
			cat,created=Category.objects.get_or_create(name__iexact=category)
			if created:
				cat.save()
			obj,created=Expense.objects.get_or_create(user=request.user,category=cat,date=date,description=description,amount=amount)
			if created:
				obj.save()
			qs=Expense.objects.all()
			summ=Expense.objects.aggregate(Sum('amount'))
			total=list(summ.values())[0]
			return render(request,'Expense/Expense_Page.html',{"expenses":qs.values(),"sum":total})
		else:
			return render(request,'Expense/Add_expense.html',{"message":"category ,description,amount,date required"})

	return render(request,'Expense/Add_expense.html')





# class ExpenseListAPIView(APIView):

# 	renderer_classes = [TemplateHTMLRenderer]
# 	template_name = 'Expense/index.html'	

# 	def get(self,request):
# 		print(request.GET)
# 		des=request.query_params.get('description')
# 		if des==None:
# 			qs=Expense.objects.filter(user=request.user)
# 			# print(qs)
# 			return Response({'expenses': qs.values()})
# 		else:
# 			qs=Expense.objects.filter(user=request.user,description=des)
# 			# print(qs)
# 			return Response({'expenses': qs.values()})


# class ExpenseAddAPIView(APIView):
	
	# renderer_classes = [TemplateHTMLRenderer]
	# template_name = 'Expense/Expense_Page.html'	



	# def post(self,request):
	# 	# print(request.data)
	# 	category=request.data.get('category','')
	# 	date=request.data.get('date','')
	# 	description=request.data.get('description','')
	# 	amount=request.data.get('amount','')
	# 	# print(category)
	# 	# print(type(category))
		

	# 	if category and date and description and amount:
	# 		cat,created=Category.objects.get_or_create(name=category)
	# 		if created:
	# 			# print(cat)
	# 			cat.save()
	# 		# print(request.user)
	# 		qs,namea=Expense.objects.get_or_create(user=request.user,category=cat,date=date,description=description,amount=amount)
	# 		if namea:
	# 			qs.save()
	# 		return Response({"data":qs.values()},status=200)
	# 	else:
	# 		return Response({"category ,description,amount,date required "},status=400)



	# def delete(self,request):
	# 	print("sdadadasd"+request.data)
	# 	description=request.data.get("description")
	# 	print("des"+description)
	# 	if description:
	# 		des=Expense.objects.filter(description=description)
	# 		if des is not None:
	# 			des.delete()
	# 			data=Expense.objects.all()
	# 			return Response({"data":data},status=200)
	# 		else:
	# 			return Response({"This Discription in not available"},status=400)
	# 	else:
	# 		return Response({"This Discription is REquired to delete"},status=400)	



	













