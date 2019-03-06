from rest_framework import serializers

from .models import *


class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ('__all__')

