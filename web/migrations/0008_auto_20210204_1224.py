# Generated by Django 3.1.5 on 2021-02-04 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_saleprice_isdefault'),
    ]

    operations = [
        migrations.AddField(
            model_name='saledetails',
            name='MasterId',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salemaster',
            name='MasterId',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
    ]
