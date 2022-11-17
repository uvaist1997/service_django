# Generated by Django 3.1.5 on 2021-07-05 09:52

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0076_saleproductprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleproduct',
            name='minimumSalesPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
