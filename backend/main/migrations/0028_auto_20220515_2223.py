# Generated by Django 3.1.4 on 2022-05-15 17:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20220405_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='WellToolData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.CharField(default='', max_length=15)),
                ('date_time', models.DateTimeField(default=datetime.datetime(2022, 5, 15, 17, 23, 43, 20510, tzinfo=utc))),
                ('degree', models.FloatField(default=0)),
                ('salinity', models.FloatField(default=0)),
                ('temperature', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='well',
            name='imei',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='ugv',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 15, 22, 23, 43, 20510)),
        ),
    ]
