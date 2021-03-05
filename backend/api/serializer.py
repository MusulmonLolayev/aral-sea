from rest_framework import serializers

from main.models import *

from django.contrib.auth.models import User

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Region
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = District
        fields = '__all__'

class FarmSerializer(serializers.ModelSerializer):
    #district = DistrictSerializer()
    class Meta:
        model = Farm
        fields = '__all__'

class WellSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Well
        fields = '__all__'

    farm_name = serializers.SerializerMethodField()
    def get_farm_name(self, obj):
        return obj.farm.name

class MusterPumpingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MusterPumping
        fields = '__all__'