from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Expense)
admin.site.register(GroupExpense)
admin.site.register(Category)

