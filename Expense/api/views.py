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




class ExpenseListAPIView(APIView):

	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'Expense/index.html'

	def get(self,request):
		if request.query_params.get('description')==None:
			return Response({'expenses': Expense.objects.filter(user=request.user).values()})
		else:
			return Response({'expenses': Expense.objects.filter(user=request.user,description=des).values()})


class ExpenseAddAPIView(APIView):
	
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'Expense/Expense_Page.html'	



	def post(self,request):
		category=request.data.get('category','')
		date=request.data.get('date','')
		description=request.data.get('description','')
		amount=request.data.get('amount','')
		

		if category and date and description and amount:
			cat,created=Category.objects.get_or_create(name=category)
			if created:
				cat.save()
			qs,namea=Expense.objects.get_or_create(user=request.user,category=cat,date=date,description=description,amount=amount)
			if namea:
				qs.save()
			return Response({"data":qs.values()},status=200)
		else:
			return Response({"category ,description,amount,date required "},status=400)



	def delete(self,request):
		if request.data.get("description"):
			des=Expense.objects.filter(description=request.data.get("description"))
			if des is not None:
				des.delete()
				return Response({"data":Expense.objects.all()},status=200)
			else:
				return Response({"This Discription in not available"},status=400)
		else:
			return Response({"This Discription is REquired to delete"},status=400)	
