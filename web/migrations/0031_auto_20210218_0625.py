# Generated by Django 3.1.5 on 2021-02-18 06:25

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0030_paymentdetail_ledgerid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vansettings',
            name='CreditLimit',
        ),
        migrations.AddField(
            model_name='saleaccountledger',
            name='Credit_Limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]