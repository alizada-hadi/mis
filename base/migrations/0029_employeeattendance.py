# Generated by Django 4.0.4 on 2022-05-05 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_category_description_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('حاضر', 'حاضر'), ('غایب', 'غایب'), ('تاخیر بیش از یک ساعت', 'تاخیر بیش از یک ساعت')], default='حاضر', max_length=20)),
                ('penalty_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.employee')),
            ],
        ),
    ]
