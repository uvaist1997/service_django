# Generated by Django 3.1.5 on 2021-02-17 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0029_auto_20210216_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentdetail',
            name='LedgerId',
            field=models.BigIntegerField(default='0'),
            preserve_default=False,
        ),
    ]