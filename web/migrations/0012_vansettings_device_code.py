# Generated by Django 3.1.5 on 2021-02-05 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20210205_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='vansettings',
            name='Device_Code',
            field=models.CharField(default='1', max_length=128),
            preserve_default=False,
        ),
    ]
