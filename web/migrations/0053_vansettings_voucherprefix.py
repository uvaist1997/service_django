# Generated by Django 3.1.5 on 2021-04-23 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0052_saledetails_orderstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='vansettings',
            name='VoucherPrefix',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
