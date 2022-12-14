# Generated by Django 3.1.5 on 2022-02-03 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0105_remove_salemaster_billmargin'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleaccountledger',
            name='AdditionalNo',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='Address1',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='BuildingNumber',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='City',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='Country',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='District',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='State',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='StreetName',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
