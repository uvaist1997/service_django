# Generated by Django 3.1.5 on 2021-02-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_saleaccountledger_pricecategoryid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salereturnmaster',
            name='TaxType',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
