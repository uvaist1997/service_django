# Generated by Django 3.1.5 on 2021-08-20 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_softwareversion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CompanyId', models.CharField(max_length=50)),
                ('log_type', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=512)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'verbose_name': 'activity_log',
                'verbose_name_plural': 'activity_log',
                'db_table': 'activity_log',
            },
        ),
    ]
