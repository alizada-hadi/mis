# Generated by Django 4.0.4 on 2022-05-07 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_remove_orderdetail_options_remove_orderdetail_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
