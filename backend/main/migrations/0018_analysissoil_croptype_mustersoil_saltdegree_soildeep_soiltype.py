# Generated by Django 3.1.4 on 2021-11-21 12:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_mgv_ugv'),
    ]

    operations = [
        migrations.CreateModel(
            name='CropType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SaltDegree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SoilType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SoilDeep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_deep', models.FloatField(default=0)),
                ('to_deep', models.FloatField(default=0)),
                ('soiltype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.soiltype')),
            ],
        ),
        migrations.CreateModel(
            name='MusterSoil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contour_no', models.IntegerField(default=0)),
                ('pit_no', models.IntegerField(default=0)),
                ('area_size', models.FloatField(default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('location_x', models.FloatField(default=0)),
                ('location_y', models.FloatField(default=0)),
                ('croptype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.croptype')),
                ('salt_degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.saltdegree')),
                ('well', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.well')),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisSoil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electric_wire', models.FloatField(default=0)),
                ('hco3', models.FloatField(default=0)),
                ('cl', models.FloatField(default=0)),
                ('so4', models.FloatField(default=0)),
                ('ca', models.FloatField(default=0)),
                ('mg', models.FloatField(default=0)),
                ('mustersoil', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.mustersoil')),
            ],
        ),
    ]