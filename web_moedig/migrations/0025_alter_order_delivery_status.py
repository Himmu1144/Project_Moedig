# Generated by Django 4.1 on 2022-08-27 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0024_alter_order_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('1', 'Order placed'), ('2', 'Order Printed'), ('3', 'Order Shipped'), ('4', 'Order Picked')], default='1', max_length=1000),
        ),
    ]
