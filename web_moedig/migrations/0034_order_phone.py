# Generated by Django 4.1 on 2022-09-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0033_profile_is_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=13),
            preserve_default=False,
        ),
    ]