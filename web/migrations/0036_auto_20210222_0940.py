# Generated by Django 3.1.5 on 2021-02-22 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0035_auto_20210219_1041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vansettings',
            old_name='AllowSalesLessThanMinimumSalesPrice',
            new_name='Allow_Sales_Below_Min_Sales_Price',
        ),
        migrations.RenameField(
            model_name='vansettings',
            old_name='AllowSalesLessThanPrice',
            new_name='Allow_Sales_Below_Purchase_Price',
        ),
    ]
