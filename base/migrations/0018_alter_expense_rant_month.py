# Generated by Django 4.0.4 on 2022-04-22 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_expense_alternative_alter_expense_rant_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='rant_month',
            field=models.DateField(blank=True, null=True),
        ),
    ]
