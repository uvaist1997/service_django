# Generated by Django 3.1.5 on 2021-09-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0092_salemaster_check_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salemaster',
            name='check_date',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]