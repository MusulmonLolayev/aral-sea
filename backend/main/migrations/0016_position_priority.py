# Generated by Django 3.1.4 on 2021-06-17 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_staff_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='priority',
            field=models.IntegerField(default=1),
        ),
    ]
