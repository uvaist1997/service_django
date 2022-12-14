# Generated by Django 3.1.5 on 2021-03-03 07:54

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0040_reciept_advance_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('auto_id', models.PositiveIntegerField(db_index=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('WarehouseTo_id', models.BigIntegerField()),
                ('WarehouseFrom_id', models.BigIntegerField()),
                ('Date', models.DateTimeField()),
                ('Notes', models.CharField(max_length=128)),
                ('Total_qty', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('Total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('CompanyProductId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.companyproduct')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_stockorder_objects', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updater_stockorder_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'stock_order',
                'db_table': 'web_stock_order',
            },
        ),
        migrations.AddField(
            model_name='vansettings',
            name='Show_Cost_In_Stock_Order',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vansettings',
            name='StockOrderWarehouseFromId',
            field=models.BigIntegerField(default='0'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='StockOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductId', models.BigIntegerField()),
                ('PricelistId', models.BigIntegerField()),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('StockOrderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.stockorder')),
            ],
            options={
                'verbose_name': 'web_stock_order_detail',
                'verbose_name_plural': 'web_stock_order_details',
                'db_table': 'web_stock_order_details',
            },
        ),
    ]
