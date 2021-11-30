import re
from django.db.models import query
from django.shortcuts import render

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions

from django.contrib.auth.models import Permission

from main.models import *

from django.db import transaction

from .serializer import *

import traceback

def get_user_role(request):
    # roles by groups: texniklar=0, tuman_administratorlari = 1 for just now
    group = request.user.groups.all()
    role = 0
    if len(group) > 0:
        role_name = group[0].name

        if role_name == "tuman_administratorlari":
            role = 1
    
    return role

def get_user_permissions(user):
    permissions = []
    for group in Group.objects.filter(user=user):
        for per in group.permissions.all():
            permissions.append(per.codename)
    return permissions

class CountryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class RegionListView(ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        This view should return a list of all the regions
        for the currently country.
        """
        countryId = self.kwargs['countryId']
        return Region.objects.filter(country_id=countryId)

class DistrictListView(ListAPIView):
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        This view should return a list of all the districts
        for the currently region.
        """
        #regionId = self.kwargs['regionId']
        #reg_districts = District.objects.filter(region_id=regionId)
        #districts = []
        user_districts = self.request.user.staff.districts.all()
        """print(user_districts)
        for district in reg_districts:
            print(district in user_districts)
            if district in user_districts:
                districts.append(district)"""
        return user_districts

class FarmListView(ListAPIView):
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        This view should return a list of all the districts
        for the currently region.
        """
        
        id = int(self.kwargs['id'])
        if id != 0:
            return Farm.objects.filter(pk = id)
        districts = self.request.user.staff.districts.all()
        if len(districts) == 0:
            return Farm.objects.all()
        q = Farm.objects.filter(district=districts[0])
        for i in range(1, len(districts)):
            q += Farm.objects.filter(district=districts[i])
        return q
        
class WellListView(ListAPIView):
    serializer_class = WellSerializer
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        id = int(self.kwargs['id'])
        
        role = get_user_role(self.request)
        # Respond all well which are connected to texniklar
        if role == 0:
            return Well.objects.filter(user = self.request.user)
        elif role == 1:
            farms = Farm.objects.filter(district = self.request.user.staff.district)

            query = Well.objects.filter(farm = farms[0])
            for i in range(1, len(farms)):
                query = query.union(Well.objects.filter(farm = farms[i]))
            return query
    
        return Well.objects.all()[:10]

class MusterPumpingListView(ListAPIView):
    serializer_class = MusterPumpingSerializer
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        if "well_id" in self.kwargs:
            well_id = int(self.kwargs['well_id'])
            return MusterPumping.objects.filter(well=well_id)
        return MusterPumping.objects.filter()

@api_view(['POST', 'DELETE', 'PUT', 'GET'])
def well_request(request, id=0):
    try:
        if request.method == 'GET':
            if id != 0:
                well = Well.objects.get(pk = id)
                return Response(WellSerializer(well).data, status=200)
            
            # if the user is technician, then must send the well which were attached to the user
            if request.user.has_perm('main.add_musterpumping'):
                query = Well.objects.filter(user=request.user)
                return Response(WellSerializer(query, many=True).data, status=200)
            
            # if the user is the district controller, then must send the all well in the district
            if request.user.has_perm('main.add_well'):
                # the user is the district controller, then the user must have one district, so we get the first one
                farms = Farm.objects.filter(district = request.user.staff.districts.all()[0])
                query = Well.objects.filter(farm = farms[0])

                for i in range(1, len(farms)):
                    query = query.union(Well.objects.filter(farm = farms[i]))
                return Response(WellSerializer(query, many=True).data, status=200)
            return Response("Not have permission", status=403)
        # Create object
        if request.method == 'POST':
            request.data['user']=request.user.id 
            serializer = WellSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)
        
        # find suitable instance
        try:
            instance = Well.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            request.data['user']=request.user.id 
            serializer = WellSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(['POST', 'DELETE', 'PUT'])
def muster_pumping_request(request):
    try:
        if request.method == "POST":
            permission = request.user.has_perm('main.add_musterpumping')
            if permission == False:
                return Response("You do not have permission", status=403)
            
            serializer = MusterPumpingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)

        # find suitable instance
        try:
            instance = MusterPumping.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            permission = request.user.has_perm('main.change_musterpumping')
            if permission == False:
                return Response("You do not have permission", status=403)

            request.data['user']=request.user.id 
            serializer = MusterPumpingSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            permission = request.user.has_perm('main.delete_musterpumping')
            if permission == False:
                return Response("You do not have permission", status=403)
            instance.delete()
            return Response('Deleted', status=200)
    except:
        Response(status=500)

@api_view(["GET"])
def user_permissions(request, app_name, model_name):
    permissions = {
        'view': request.user.has_perm(app_name + '.view_' + model_name),
        'add': request.user.has_perm(app_name + '.add_' + model_name),
        'change': request.user.has_perm(app_name + '.change_' + model_name),
        'delete': request.user.has_perm(app_name + '.delete_' + model_name),
    }
    return Response(permissions, status=200)

@api_view(["GET"])
def user_groups(request):
    groups = []
    for item in request.user.groups.all():
        groups.append(item.name)
    return Response(groups, status=200)

@api_view(["GET"])
def user_role(request):
    role = get_user_role(request)
    return Response(role, status=200)

@api_view(["GET"])
def get_technicians(request):
    try:
        current_staff = Staff.objects.get(user=request.user)
        districts = current_staff.districts.all()
        if len(districts) > 0:
            technicians = Staff.objects.filter(districts=districts[0]).exclude(id=current_staff.id)
            for i in range(1, len(districts)):
                technicians += Staff.objects.filter(districts=districts[i])
            technicians = technicians.filter(position__priority__lt = current_staff.position.priority)
        return Response(StaffSerializer(technicians, many=True).data, status=200)
    except:
        traceback.print_exc()
        return Response("Not found", status=404)

@api_view(["PUT"])
def attach_well_to_technician(request):
    wells = request.data['wells']
    technician = request.data['technician']
    technician = Staff.objects.get(pk=technician)
    
    with transaction.atomic():
        for well_id in wells:
            well = Well.objects.get(pk=well_id)
            well.user = technician.user
            well.save()
    return Response(status=200)

@api_view(['GET', 'POST'])
def staff_request(request, id=0):
    if request.method == 'GET':
        if id == 0:
            user_districts = request.user.staff.districts.all()
            if len(user_districts) != 0:
                staffs = []
                for district in user_districts:
                    for item in Staff.objects.filter(districts=district):
                        if (not (item in staffs)) and item.position.priority == request.user.staff.position.priority - 1:
                            staffs.append(item)
                return Response(StaffSerializer(staffs, many=True).data, status=200)
            else:
                return Response(StaffSerializer(Staff.objects.all(), many=True).data, status=200)
        else:
            staff = Staff.objects.get(pk=id)
            user = staff.user
            response = {"staff": StaffSerializer(staff).data, "user": {'id': user.id, 'username': user.username}}
            return Response(response, status=200)

@api_view(['POST', 'PUT'])
@transaction.atomic
def user_request(request):
    if request.method == 'POST':
        user = UserSerializer(data=request.data.get('user'))
        staff = StaffSerializer(data=request.data.get('staff'))
        if user.is_valid() and staff.is_valid():
            # add to group by position
            position = Position.objects.get(pk=request.data.get('staff').get('position'))

            user_data = request.data.get('user')
            user_instance = User.objects.create_user(username=user_data.get('username'), password=user_data.get('password'))
            user_instance.groups.add(position.group.id)

            staff.save()
            staff.instance.user = user_instance
            staff.save()

            response = {"user": user_instance.id, "staff": staff.instance.id}
            return Response(response, status=200)
        else:
            return Response('Not acceptable', status=406)
    if request.method == 'PUT':
        
        user_instance = User.objects.get(pk=request.data.get('user').get('id'))
        staff_instance = Staff.objects.get(pk=request.data.get('staff').get('id'))

        user = UserSerializer(data=request.data.get('user'), instance=user_instance)
        staff = StaffSerializer(data=request.data.get('staff'), instance=staff_instance)

        if user.is_valid() and staff.is_valid():
            # add to group by position
            new_position = Position.objects.get(pk=request.data.get('staff').get('position'))

            user_instance.groups.clear()
            user_instance.groups.add(new_position.group.id)

            staff.save()

            return Response("Ok", status=200)
        else:
            return Response('Not acceptable', status=406)

@api_view(['GET'])
def position_request(reqeust):
    if reqeust.method == 'GET':
        return Response(PositionSerializer(Position.objects.filter(priority__lt = reqeust.user.staff.position.priority), many=True).data, status=200)

@api_view(['GET'])
def group_request(reqeust):
    if reqeust.method == 'GET':
        return Response(GroupSerializer(Group.objects.all(), many=True).data, status=200)

@api_view(['GET'])
def get_permission(request):    
    permissions = get_user_permissions(request.user)
    return Response(permissions, status=200)

@api_view(['POST', 'DELETE', 'PUT', 'GET'])
def ugv_request(request, well_id=0):
    try:
        if request.method == 'GET':
            if well_id != 0:
                well = Well.objects.get(pk = well_id)
                ugvs = Ugv.objects.filter(well=well)
                return Response(UgvSerializer(ugvs, many=True).data, status=200)
            
            # send all ugvs which the user has
            ugvs = Ugv.objects.filter(staff=request.user.staff)
            return Response(UgvSerializer(ugvs, many=True).data, status=200)
        # Create object
        if request.method == 'POST':
            request.data['staff']=request.user.staff.id
            serializer = UgvSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)
        
        # find suitable instance
        try:
            instance = Ugv.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            request.data['staff']=request.user.staff.id 
            serializer = UgvSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(['POST', 'DELETE', 'PUT', 'GET'])
def mgv_request(request, well_id=0):
    try:
        if request.method == 'GET':
            if well_id != 0:
                well = Well.objects.get(pk = well_id)
                mgvs = Mgv.objects.filter(well=well)
                return Response(MgvSerializer(mgvs, many=True).data, status=200)
            
            # send all ugvs which the user has
            mgvs = Mgv.objects.filter(staff=request.user.staff)
            return Response(UgvSerializer(mgvs, many=True).data, status=200)
        # Create object
        if request.method == 'POST':
            request.data['staff']=request.user.staff.id
            serializer = MgvSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)
        
        # find suitable instance
        try:
            instance = Mgv.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            request.data['staff']=request.user.staff.id 
            serializer = MgvSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        traceback.print_exc()
        Response(status=500)        

@api_view(['GET'])
def ugv_from_weighter(request):
    return Response("Ok", status=200)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def muster_soil_request(request, id=0):
    try:
        if request.method == 'GET':
            if id == 0:
                if request.user.has_perm('main.add_analysissoil'):
                    return Response(MusterSoilSerializer(MusterSoil.objects.all(), many=True).data, status=200)
                else:
                    return Response(MusterSoilSerializer(MusterSoil.objects.filter(user=request.user), many=True).data, status=200)
            else:
                try:
                    obj = MusterSoil.objects.get(pk=id)
                    return Response(MusterSoilSerializer(obj).data, status=200)
                except:
                    return Response("Not Found", status=404)                    
        # Create object
        if request.method == 'POST':
            request.data['user']=request.user.id
            serializer = MusterSoilSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                analysis_soil_analysis = AnalysisSoil()
                analysis_soil_analysis.muster_soil = serializer.instance
                analysis_soil_analysis.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)
        
        # find suitable instance
        try:
            instance = MusterSoil.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            request.data['user']=request.user.id 
            serializer = MusterSoilSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(['GET'])
def farms_by_user_district(request):
    try:
        query = []
        for district in request.user.staff.districts.all():
            for farm in Farm.objects.filter(district=district):
                query.append(farm)
        return Response(FarmSerializer(query, many=True).data, status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(['GET'])
def well_by_farm(request, farm_id):
    try:
        return Response(WellSerializer(Well.objects.filter(farm=farm_id), many=True).data, status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(["GET"])
def salt_degree_request(request):
    try:
        return Response(SaltDegreeSerializer(SaltDegree.objects.all(), many=True).data, status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(["GET", "POST", "PUT", "DELETE"])
def soil_deep_request(request, mustersoilid=0):
    try:
        if request.method == "GET":
            if mustersoilid != 0:
                return Response(SoilDeepSerializer(SoilDeep.objects.filter(muster_soil=mustersoilid), many=True).data, status=200)
            else:
                Response(status=400)
        
        # Create object
        if request.method == 'POST':
            serializer = SoilDeepSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)

        # find suitable instance
        try:
            instance = SoilDeep.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            serializer = SoilDeepSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(["GET"])
def soil_type_request(request):
    try:
        return Response(SoilTypeSerializer(SoilType.objects.all(), many=True).data, status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(["GET"])
def crop_type_request(request):
    try:
        return Response(CropTypeSerializer(CropType.objects.all(), many=True).data, status=200)
    except:
        traceback.print_exc()
        Response(status=500)

@api_view(["GET", "POST", "PUT", "DELETE"])
def analysis_soil_request(request, mustersoilid=0):
    try:
        if request.method == "GET":
            if mustersoilid != 0:
                return Response(AnalysisSoilSerializer(AnalysisSoil.objects.filter(muster_soil=mustersoilid), many=True).data, status=200)
            else:
                Response(status=400)
        
        # Create object
        if request.method == 'POST':
            serializer = AnalysisSoilSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)

        # find suitable instance
        try:
            instance = AnalysisSoil.objects.get(id=request.data.get('id'))
        except:
            return Response(status=404)
        
        
        # Update object
        if request.method == 'PUT':
            request.data['user']=request.user.id

            serializer = AnalysisSoilSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        traceback.print_exc()
        Response(status=500)