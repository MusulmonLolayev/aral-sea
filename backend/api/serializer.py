from rest_framework import serializers

from main.models import *

from django.contrib.auth.models import User, Group, Permission

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
    #region = RegionSerializer()
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

class StaffSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Staff
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('codename', )

class UgvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ugv
        fields = '__all__'

class MgvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mgv
        fields = '__all__'

class MusterSoilSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusterSoil
        fields = '__all__'


class SaltDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaltDegree
        fields = '__all__'

class SoilDeepSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilDeep
        fields = '__all__'

class SoilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilType
        fields = '__all__'

class CropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropType
        fields = '__all__'

class AnalysisSoilSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisSoil
        fields = '__all__'
