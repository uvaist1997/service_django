# Generated by Django 3.1.5 on 2021-04-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0051_auto_20210414_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='saledetails',
            name='OrderStatus',
            field=models.BooleanField(default=False),
        ),
    ]
