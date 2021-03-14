from django.urls import path

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

    path('farm_request/<id>', FarmListView.as_view()),
    path('well_request/<id>', WellListView.as_view()),
    path('well_request', well_request),

    path('muster_pumping_request/<well_id>', MusterPumpingListView.as_view()),
    path('muster_pumping_request', muster_pumping_request),


    path('user_permissions/<app_name>/<model_name>', user_permissions),

    path('user_gourps', user_groups),

    path('user_role', user_role),

]

urlpatterns = format_suffix_patterns(urlpatterns)