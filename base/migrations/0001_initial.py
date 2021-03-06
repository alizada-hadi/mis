# Generated by Django 4.0.4 on 2022-04-19 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=100)),
                ('social_number', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeSalaryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_per_month', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='?????????? ???????????? ??????')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.customer')),
            ],
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salary_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employeesalarytype')),
            ],
        ),
        migrations.CreateModel(
            name='Recieve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('amount_letter', models.CharField(max_length=200)),
                ('recived_at', models.DateField()),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='????')),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='????')),
                ('depth', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='??????')),
                ('direction', models.CharField(blank=True, choices=[('????????', '????????'), ('????', '????')], default='????????', max_length=30, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='?????????? / ??????????')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='???????? ???? ????????')),
                ('price_unit', models.CharField(choices=[('????????????', '????????????'), ('????????', '????????'), ('??????????', '??????????'), ('??????????', '??????????')], max_length=20)),
                ('alternative', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='??????????')),
                ('remain_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='?????????? ???????? ??????????')),
                ('type', models.CharField(max_length=200, verbose_name='?????????? ??????')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.category')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employee')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.order')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='emp_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employeetype'),
        ),
    ]
