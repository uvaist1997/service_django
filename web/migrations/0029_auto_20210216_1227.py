# Generated by Django 3.1.5 on 2021-02-16 12:27

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0028_auto_20210216_1028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='CashOrBankId',
            new_name='CashAccountId',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='Amount',
            new_name='TotalAmount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='Balance',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='CardNetwork',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='Discount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='DueDate',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='LedgerId',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='Narration',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='NetAmount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='PaymentGateway',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='PaymentStatus',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='RefferenceNo',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='VoucherType',
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TransactionId', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('notes', models.CharField(blank=True, max_length=128, null=True)),
                ('PaymentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.payment')),
            ],
            options={
                'verbose_name': 'web_payment_detail',
                'verbose_name_plural': 'web_payment_details',
                'db_table': 'web_payment_details',
            },
        ),
    ]