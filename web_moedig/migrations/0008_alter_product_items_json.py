# Generated by Django 4.1 on 2022-08-19 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0007_product_items_json_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='items_json',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
