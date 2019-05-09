
from django.conf.urls import url

from .views import (
    VehicleCreateAPIView,
    VehicleDetailAPIView,
    ListAvailableBlueCarsAPIView,
    VehicleUpdateAPIView,
    ListAllAPIView,
    DeleteAllUnavailableVehicles,
    ListAllAvailableAPIView,
    RootAPIView,
    UserLoginAPIView,
    UserRegisterAPIView
)



urlpatterns = [
    #Auth 
    url('login/$', UserLoginAPIView.as_view(), name='user_login'),
    url('register/$', UserRegisterAPIView.as_view(), name='user_register'),


    url('api/v1/$', RootAPIView.as_view(), name='root_api_view'),
    url('create-car/$', VehicleCreateAPIView.as_view(), name='create_car'),

    url('delete-unavailable-cars/$', DeleteAllUnavailableVehicles.as_view(), name='delete_unavailable_cars'),
    


    url('available-blue-cars/$', ListAvailableBlueCarsAPIView.as_view(), name='available_blue_cars'),

    url('all-available-unavailable/$', ListAllAPIView.as_view(), name='both_available_unavailable'),
    
    url('only-available/$', ListAllAvailableAPIView.as_view(), name='available_cars'),

    url(r'^car/(?P<id>[0-9]+)/$', VehicleDetailAPIView.as_view(), name='car_detail'),

    url(r'^car/(?P<id>[0-9]+)/edit/$', VehicleUpdateAPIView.as_view(), name='update_car'),

   
]






