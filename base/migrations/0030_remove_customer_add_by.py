# Generated by Django 4.0.4 on 2022-05-07 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_employeeattendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='add_by',
        ),
    ]
