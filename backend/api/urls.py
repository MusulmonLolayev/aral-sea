from django.urls import path, re_path

from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)

from .views import *

urlpatterns = [

    # Path to obtain a new access and refresh token
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Submit your refresh token to this path to obtain a new access token
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # /countries
    path('countries', CountryListView.as_view()),

    # /regions_by_country/countryId
    path('regions_by_country/<countryId>', RegionListView.as_view()),

    # /districts_by_region/regionId
    path('districts_by_region/<regionId>', DistrictListView.as_view()),

    path('district_request', district_request),
    path('get_user_district', get_user_district),

    path('farm_request/<id>', FarmListView.as_view()),
    path('district_farms/<district_id>', farm_request),
    path('farm_request1', farm_request1),

    path('well_request/<int:id>', well_request),
    path('well_request', well_request),

    path('muster_pumping_request/<well_id>', MusterPumpingListView.as_view()),
    path('muster_pumping_request', muster_pumping_request),


    path('user_permissions/<app_name>/<model_name>', user_permissions),

    path('get_user_information', get_user_information),

    path('user_gourps', user_groups),

    path('user_role', user_role),

    path('get_technicians', get_technicians),

    path('attach_well_to_technician', attach_well_to_technician),

    path('staffs/<int:id>', staff_request),

    path('positions', position_request),
    
    path('users', user_request),

    path('groups', group_request),

    path('ugv_request', ugv_request),
    path('ugv_request/<int:well_id>', ugv_request),

    path('mgv_request', mgv_request),
    path('mgv_request/<int:well_id>', mgv_request),


    path('ugv_weighter', ugv_from_weighter),

    re_path('^muster_soil_request/pagination/$', MustorSoilView.as_view()),
    path('muster_soil_request/<int:id>', muster_soil_request),
    path('muster_soil_request', muster_soil_request),

    path('farms_by_user_district', farms_by_user_district),

    path('salt_degree_request', salt_degree_request),

    path('soil_deep_request/<int:mustersoilid>', soil_deep_request),
    
    path('soil_deep_request', soil_deep_request),

    path('soil_type_request', soil_type_request),

    path('crop_type_request', crop_type_request),

    path('well_by_farm/<int:farm_id>', well_by_farm),

    path('analysis_soil_request', analysis_soil_request),
    path('analysis_soil_request/<int:mustersoilid>', analysis_soil_request),
    path('report-6a/<int:district>/<str:date>', report_6a),
    path('report-soil-analysis/<int:district>/<str:date>', report_soil_analysis),

    re_path('^json_query/$', json_query),

    path('get_wells_by_ids', get_wells),
    path('get_farms_by_ids', get_farms),

    path('yield_request/<int:id>', yield_request),
    path('yield_request', yield_request),

    path('water_request/<int:id>', water_request),
    path('water_request', water_request),

    path('water_norm_request/<int:id>', water_norm_request),
    path('water_norm_request', water_norm_request),

    path('well_tool_data/<str:imei>', well_tool_data)
]

urlpatterns = format_suffix_patterns(urlpatterns)
