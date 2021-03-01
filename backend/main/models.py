from django.db import models
from django.contrib.auth.models import User
import datetime

class Country(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
        
class District(models.Model):
    name = models.CharField(max_length=30)
    region = models.ForeignKey(Region, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name

class Farm(models.Model):
    name = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name + " ({})".format(self.district)

class Well(models.Model):
    number = models.CharField(max_length=30)

    farm = models.ForeignKey(Farm, on_delete = models.CASCADE)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)

    built_year = models.IntegerField(default=0)
    depth = models.FloatField(default=0)
    diameter = models.FloatField(default=0)

    # if material is True, then the well was made from polythene and otherwise was made from metal
    material = models.BooleanField(default=True)

    area = models.FloatField(default=0)
    label = models.FloatField(default=0)

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)

    def __str__(self):
        return str(self.farm) + ", Number {}".format(self.number)

class Muster(models.Model):
    depth = models.FloatField(default=0)
    degree_salt = models.FloatField(default=0)

    well = models.ForeignKey(Well, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "Number {}: depth={}, degree of salt={}".format(self.well.number, self.depth, self.degree_salt)