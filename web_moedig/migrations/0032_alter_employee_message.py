# Generated by Django 4.1 on 2022-09-02 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_moedig', '0031_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='message',
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
    ]
