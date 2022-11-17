# Generated by Django 3.1.5 on 2022-02-18 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0107_vansettings_creditlimit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('Date',), 'verbose_name': 'web_payment', 'verbose_name_plural': 'web_payments'},
        ),
        migrations.AlterModelOptions(
            name='reciept',
            options={'ordering': ('Date',), 'verbose_name': 'web_reciept', 'verbose_name_plural': 'web_reciepts'},
        ),
        migrations.AlterModelOptions(
            name='salemaster',
            options={'ordering': ('Date',), 'verbose_name': 'sales_master', 'verbose_name_plural': 'sales_masters'},
        ),
        migrations.AlterModelOptions(
            name='saleorder',
            options={'ordering': ('Date',), 'verbose_name': 'sales_order', 'verbose_name_plural': 'sales_orders'},
        ),
        migrations.AlterModelOptions(
            name='salereturnmaster',
            options={'ordering': ('Date',), 'verbose_name': 'sales_return_master', 'verbose_name_plural': 'sales_return_masters'},
        ),
    ]