from django.db import models
# from accounts.models import User
from django.contrib.auth import get_user_model
User=get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):

        return (self.name)


class Expense(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=300)
    amount = models.FloatField()


    def __str__(self):
        return self.description
