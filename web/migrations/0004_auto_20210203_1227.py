# Generated by Django 3.1.5 on 2021-02-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_taxcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vansettings',
            old_name='GSTSalesType',
            new_name='BankAccountID',
        ),
        migrations.AddField(
            model_name='vansettings',
            name='CashAccountID',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vansettings',
            name='UserID',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vansettings',
            name='sales_account',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vansettings',
            name='sales_return_account',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
    ]
