# Generated by Django 3.1.5 on 2021-02-22 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0037_saleaccountledger_billwiseapplicable'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastsalesprice',
            name='Van_ID',
            field=models.BigIntegerField(default='0'),
            preserve_default=False,
        ),
    ]
