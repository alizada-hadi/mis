# Generated by Django 4.0.4 on 2022-04-20 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_orderdetail_completion_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='employee',
        ),
    ]
