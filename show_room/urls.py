
from django.conf.urls import url

from .views import (
    VehicleCreateAPIView
)



urlpatterns = [
    url('create-car/$', VehicleCreateAPIView.as_view(), name='create_car'),
   
]






