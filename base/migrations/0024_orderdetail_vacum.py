# Generated by Django 4.0.4 on 2022-04-28 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_order_date_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='vacum',
            field=models.CharField(blank=True, choices=[('رنگ', 'رنگ'), ('واکیوم', 'واکیوم')], max_length=20, null=True),
        ),
    ]
