# Generated by Django 3.1.5 on 2021-09-21 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_einvoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='einvoice',
            name='VoucherType',
            field=models.CharField(default='w', max_length=128),
            preserve_default=False,
        ),
    ]
