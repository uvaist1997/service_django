# Generated by Django 3.1.5 on 2021-02-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0025_remove_recieptdetail_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='reciept',
            name='CashAccountID',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
