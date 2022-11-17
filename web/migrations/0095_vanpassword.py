# Generated by Django 3.1.5 on 2021-11-11 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0094_auto_20211111_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='VanPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('is_expired', models.BooleanField(default=False)),
                ('vansettings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.vansettings')),
            ],
            options={
                'verbose_name': 'van_settigns_password',
                'verbose_name_plural': 'van_settigns_passwords',
                'db_table': 'van_settigns_passwords',
            },
        ),
    ]
