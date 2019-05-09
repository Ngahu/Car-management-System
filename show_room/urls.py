
from django.conf.urls import url

from .views import (
    VehicleCreateAPIView,
    VehicleDetailAPIView,
    ListAvailableBlueCarsAPIView
)



urlpatterns = [
    url('create-car/$', VehicleCreateAPIView.as_view(), name='create_car'),
    url('available-blue-cars/$', ListAvailableBlueCarsAPIView.as_view(), name='available_blue_cars'),
    url(r'^car/(?P<id>[0-9]+)/$', VehicleDetailAPIView.as_view(), name='car_detail'),
   
]






