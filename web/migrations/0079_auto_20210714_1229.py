# Generated by Django 3.1.5 on 2021-07-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0078_vansettings_cashbalance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billwise',
            name='Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]