# Generated by Django 3.1.5 on 2021-02-08 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_billwise'),
    ]

    operations = [
        migrations.AddField(
            model_name='billwise',
            name='CustomerID',
            field=models.BigIntegerField(default='1'),
            preserve_default=False,
        ),
    ]