from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'Expense'

urlpatterns = [
	path('TotalExpenes/',ExpenseListAPIView ,name="expenses"),
	path('addexpense/',ExpenseAddAPIView,name='addexpense'),
	path('GroupExpenses/',AllGroups,name='groups'),
	path('AddGroup/',Add_Group,name='Add_groups'),
	re_path(r'^GroupExpenses/(?P<id>[0-9]+)$',GroupExpenseView,name='group_expenses'),
	path('addGroupexpense/',GroupExpenseAddAPIView ,name="addgroupexpenses"),
	]


