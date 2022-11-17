# Generated by Django 3.1.5 on 2022-02-07 12:15

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0106_auto_20220203_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='vansettings',
            name='CreditLimit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
