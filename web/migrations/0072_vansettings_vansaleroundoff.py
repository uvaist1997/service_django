# Generated by Django 3.1.5 on 2021-06-23 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0071_saleorderdetails_stockordermasterid'),
    ]

    operations = [
        migrations.AddField(
            model_name='vansettings',
            name='VanSaleRoundoff',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
