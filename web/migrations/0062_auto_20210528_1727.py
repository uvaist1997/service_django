# Generated by Django 3.1.5 on 2021-05-28 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0061_auto_20210528_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reciept',
            name='Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reciept',
            name='DueDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salereturnmaster',
            name='Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]