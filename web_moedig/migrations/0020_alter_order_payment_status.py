# Generated by Django 4.1 on 2022-08-24 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0019_order_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]