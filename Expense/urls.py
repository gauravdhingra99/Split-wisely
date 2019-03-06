from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'Expense'

urlpatterns = [
	path('TotalExpenes/',ExpenseListAPIView ,name="expenses"),
	path('addexpense/',ExpenseAddAPIView,name='addexpense'),
	# path('TotalExpenes/',deleteview ,name="expenses"),
	]

