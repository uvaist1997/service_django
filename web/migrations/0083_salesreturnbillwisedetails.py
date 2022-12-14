# Generated by Django 3.1.5 on 2021-08-13 05:36

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0082_auto_20210728_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReturnBillWiseDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('VoucherNumber', models.CharField(max_length=128)),
                ('VoucherType', models.CharField(max_length=128)),
                ('Due_Date', models.DateField(blank=True, null=True)),
                ('Date', models.DateField(blank=True, null=True)),
                ('DueAmount', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('Invoice_Amount', models.DecimalField(decimal_places=2, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('SaleReturnMasterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_return_master1', to='web.salereturnmaster', verbose_name='sale_return_master1')),
            ],
            options={
                'verbose_name': 'return_billwise_detail',
                'verbose_name_plural': 'return_billwise_details',
                'db_table': 'return_billwise_details',
            },
        ),
    ]
