# Generated by Django 4.1 on 2022-08-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0018_rename_order_product_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
