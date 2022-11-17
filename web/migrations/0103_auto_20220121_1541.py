# Generated by Django 3.1.5 on 2022-01-21 10:11

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0102_payment_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='salemaster',
            name='BillMargin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='salemaster',
            name='NonTaxableAmount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='salemaster',
            name='TaxableAmount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='salemaster',
            name='Treatment',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='salereturnmaster',
            name='BillMargin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='salereturnmaster',
            name='NonTaxableAmount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='salereturnmaster',
            name='TaxableAmount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='salereturnmaster',
            name='Treatment',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
