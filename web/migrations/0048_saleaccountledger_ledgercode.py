# Generated by Django 3.1.5 on 2021-04-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0047_vansettings_pricecategoryid'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleaccountledger',
            name='LedgerCode',
            field=models.CharField(default='-', max_length=128),
            preserve_default=False,
        ),
    ]
