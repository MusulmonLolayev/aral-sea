# Generated by Django 3.1.4 on 2022-01-30 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20211127_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mustersoil',
            name='contour_no',
            field=models.CharField(max_length=40),
        ),
    ]
