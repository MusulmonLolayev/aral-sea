from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone


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


class Position(models.Model):
    title = models.CharField(max_length=50)
    group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Staff(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)

    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    districts = models.ManyToManyField(District)

    def __str__(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)


class Farm(models.Model):
    name = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name# + " ({})".format(self.district)


class Well(models.Model):
    number = models.CharField(max_length=30)
    imei = models.CharField(max_length=15, default='')

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


class MusterPumping(models.Model):
    starting_pumping = models.TimeField(default=timezone.now)
    finishing_pumping = models.TimeField(default=timezone.now)
    count_gall = models.IntegerField(default=0)
    size_gall = models.FloatField(default=0)
    ugv_before_pumping = models.FloatField(default=0)
    ugv_after_pumping = models.FloatField(default=0)
    bottom = models.FloatField(default=0)
    speed_water = models.FloatField(default=0)
    elevated = models.FloatField(default=0)
    reduced = models.FloatField(default=0)
    water_salinity = models.FloatField(default=0)
    date = models.DateField(default=datetime.date.today)

    well = models.ForeignKey(Well, on_delete = models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return "Number {}: depth={}".format(self.well.number, self.depth)


class Ugv(models.Model):
    well = models.ForeignKey(Well, on_delete = models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete = models.SET_NULL, null = True)
    degree = models.FloatField(default=0)
    date = models.DateTimeField(default=datetime.datetime.now())


class Mgv(models.Model):
    well = models.ForeignKey(Well, on_delete = models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete = models.SET_NULL, null = True)
    degree = models.FloatField(default=0)
    date = models.DateField(default=datetime.date.today)


class SaltDegree(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CropType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class MusterSoil(models.Model):
    well = models.ForeignKey(Well, on_delete = models.CASCADE, null = True)
    contour_no = models.CharField(max_length=40)
    pit_no = models.IntegerField(default=0)
    area_size = models.FloatField(default=0)
    salt_degree = models.ForeignKey(SaltDegree, on_delete = models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    crop_type = models.ForeignKey(CropType, on_delete = models.CASCADE)

    location_x = models.FloatField(default=0)
    location_y = models.FloatField(default=0)

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)


class SoilType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class SoilDeep(models.Model):
    from_deep = models.FloatField(default=0)
    to_deep = models.FloatField(default=0)
    soil_type = models.ForeignKey(SoilType, on_delete = models.CASCADE)
    muster_soil = models.ForeignKey(MusterSoil, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.from_deep}-{self.to_deep} sm"


class AnalysisSoil(models.Model):
    muster_soil = models.OneToOneField(MusterSoil, on_delete=models.SET_NULL, null=True)
    electric_wire  = models.FloatField(default=0)
    hco3 = models.FloatField(default=0)
    cl = models.FloatField(default=0)
    so4 = models.FloatField(default=0)
    ca = models.FloatField(default=0)
    mg = models.FloatField(default=0)

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)


class YieldSize(models.Model):
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    cropt_type = models.ForeignKey(CropType, on_delete=models.SET_NULL, null=True)
    salt_degree = models.ForeignKey(SaltDegree, on_delete=models.SET_NULL, null=True)
    size = models.FloatField(default=0)
    year = models.DateField(default=datetime.date.today)


class WaterSize(models.Model):
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    size = models.FloatField(default=0)
    cropt_type = models.ForeignKey(CropType, on_delete=models.SET_NULL, null=True)
    year = models.DateField(default=datetime.date.today)


class WaterNorm(models.Model):
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    size = models.FloatField(default=0)
    year = models.DateField(default=datetime.date.today)


class WellToolData(models.Model):
    imei = models.CharField(max_length=15, default='')
    date_time = models.DateTimeField(default=timezone.now())
    degree = models.FloatField(default=0)
    salinity = models.FloatField(default=0)
    temperature = models.FloatField(default=0)



class ReportFakeModel(models.Model):

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('can_report', 'Reporting rights'),
        )
