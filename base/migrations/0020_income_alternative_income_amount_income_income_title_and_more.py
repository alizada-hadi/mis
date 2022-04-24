# Generated by Django 4.0.4 on 2022-04-24 16:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_expense_paid_amount_expense_remain_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='alternative',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='income',
            name='income_title',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='income',
            name='price_unit',
            field=models.CharField(choices=[('افغانی', 'افغانی'), ('دالر', 'دالر'), ('کلدار', 'کلدار'), ('تومان', 'تومان')], default='افغانی', max_length=20),
        ),
        migrations.AddField(
            model_name='income',
            name='recieved_at',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
