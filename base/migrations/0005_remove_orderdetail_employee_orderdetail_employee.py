# Generated by Django 4.0.4 on 2022-04-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_employee_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='employee',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='employee',
            field=models.ManyToManyField(to='base.employee'),
        ),
    ]
