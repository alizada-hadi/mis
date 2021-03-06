# Generated by Django 4.0.4 on 2022-05-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_exhibition_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='product.jpg', upload_to='product/images'),
        ),
    ]
