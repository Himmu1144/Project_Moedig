# Generated by Django 4.1 on 2022-08-18 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0006_alter_product_uploaded_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='items_json',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
