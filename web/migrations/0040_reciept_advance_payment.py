# Generated by Django 3.1.5 on 2021-02-24 08:57

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0039_vansettings_show_last_sales_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='reciept',
            name='Advance_Payment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
