# Generated by Django 4.1 on 2022-08-27 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0021_alter_order_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(default='Your Order Has Been PLaced', max_length=1000),
        ),
    ]