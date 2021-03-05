from django.shortcuts import render

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions

from main.models import *

from .serializer import *


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
        regionId = self.kwargs['regionId']
        return District.objects.filter(region_id=regionId)

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

        return Farm.objects.all()
        

class WellListView(ListAPIView):
    serializer_class = WellSerializer
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        id = int(self.kwargs['id'])
        if id != 0:
            return Well.objects.filter(pk = id, user = self.request.user)
        return Well.objects.filter(user = self.request.user)

class MusterPumpingListView(ListAPIView):
    serializer_class = MusterPumping
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        well_id = int(self.kwargs['well_id'])
        if well_id != 0:
            return MusterPumping.objects.filter(well=well_id)
        return MusterPumping.objects.filter()


class MusterPumpingListCreateAPIView(ListCreateAPIView):
    permission_classes=[DjangoModelPermissions]
    serializer_class = MusterPumpingSerializer

    def get_queryset(self):
        return MusterPumping.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        request.data['instance']['user']=request.user.id 
        serializer = MusterPumping(data=request.data.get('instance'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data.get('id'), status=201)
        else:
            return Response(serializer.errors, status=406)

@api_view(['POST', 'DELETE', 'PUT'])
@permission_classes([DjangoModelPermissions])
def well_request(request):
    return Response("ssss", status=500)
    try:
        ins_name = 'instance'
        # Create object
        if request.method == 'POST':
            request.data[ins_name]['user']=request.user.id 
            serializer = MusterPumping(data=request.data.get(ins_name))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data.get('id'), status=201)
            else:
                return Response(serializer.errors, status=406)
        
        # find suitable instance
        try:
            instance = MusterPumping.objects.get(id=request.data.get(ins_name).get('id'))
        except:
            return Response(status=404)
        
        # Update object
        if request.method == 'PUT':
            request.data[ins_name]['user']=request.user.id 
            serializer = MusterPumping(instance, data=request.data.get(ins_name))
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:
                return Response(serializer.errors, status=406)
        else:
            instance.delete()
            return Response('Deleted', status=200)
    except:
        Response(status=500)