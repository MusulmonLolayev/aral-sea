# Generated by Django 3.1.4 on 2022-02-21 10:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_reportfakemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ugv',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 15, 7, 21, 753215)),
        ),
    ]
