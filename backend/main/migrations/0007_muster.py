# Generated by Django 3.1.4 on 2021-02-21 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_well_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Muster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.FloatField(default=0)),
                ('degree_salt', models.FloatField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.well')),
            ],
        ),
    ]