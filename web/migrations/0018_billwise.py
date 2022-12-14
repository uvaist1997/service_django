# Generated by Django 3.1.5 on 2021-02-08 11:35

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0017_taxcategory_companyproductid'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillWise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('TransactionID', models.BigIntegerField()),
                ('VoucherType', models.CharField(max_length=128)),
                ('VoucherNo', models.BigIntegerField()),
                ('Date', models.DateTimeField()),
                ('Due_Date', models.DateTimeField()),
                ('Invoice_Amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('Due_Amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('CompanyProductId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.companyproduct')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_billwise_objects', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updater_billwise_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'bill_wise',
                'db_table': 'web_bill_wise',
            },
        ),
    ]
