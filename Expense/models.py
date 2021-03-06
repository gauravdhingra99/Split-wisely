from django.db import models
# from accounts.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User=get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):

        return str(self.pk)


class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=300)
    amount = models.FloatField()
    owe=models.FloatField(default=0.0)

    def __str__(self):
        return self.description

# user = models.ForeignKey(User,on_delete=models.CASCADE)
class GroupExpense(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=300)
    amount = models.FloatField()
    paidby=models.CharField(User,null=False,max_length=300)
    split=models.BooleanField(default=False)

    def __str__(self):
        return (self.description)



'''
GroupExpense.group.user_set.all()[1].expense_set.all()
''' 
