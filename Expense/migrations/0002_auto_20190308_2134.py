# Generated by Django 2.1.7 on 2019-03-08 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='owe',
            field=models.FloatField(default=0.0),
        ),
    ]
