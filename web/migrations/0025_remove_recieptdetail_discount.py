# Generated by Django 3.1.5 on 2021-02-13 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_auto_20210213_0514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recieptdetail',
            name='Discount',
        ),
    ]