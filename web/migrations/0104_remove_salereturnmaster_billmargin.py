# Generated by Django 3.1.5 on 2022-01-21 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0103_auto_20220121_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salereturnmaster',
            name='BillMargin',
        ),
    ]
