from django.shortcuts import render


from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status


from .serializers import (
    VehicleCreateSerializer
)




class VehicleCreateAPIView(APIView):
    """
    Description:create a single car in a show room \n
    Type of request:POST\n
    Accepts headers: \n{
    Authorization: "Token " + authenticationToken
    }\n
    Request data type:JSON\n
    POST request body: \n{
        "name":"secondsecondssecondsecondecond",
        "store":"4",
        "description":"The description here."
    }\n
    Response success status:HTTP_201_created \n
    Response data type:JSON\n
    Sample Success:\n
            {
            "name": "secondsecondssecondsecondecond",
            "store": 17,
            "description":"The description here."
            }\n
    Response failure:\n{
        error: Sorry you must own a Shop to perform this.\tHTTP_401_UNAUTHORIZED\n
        error:Sorry only the owner of the store has this permission.\tHTTP_401_UNAUTHORIZED\n
    }
    """
    permission_classes = (IsAuthenticated,)
    def post(self,request,format=None):
        car_make =  request.data['car_make']
        registration_number =  request.data['registration_number']
        year_of_manufacturing =  request.data['year_of_manufacturing']
        car_color =  request.data['car_color']
        car_type =  request.data['car_type']
        is_available =  request.data['is_available']

        current_user = request.user.id

        data = {
            "creator":current_user,
            "car_make":car_make,
            "registration_number":registration_number,
            "year_of_manufacturing":year_of_manufacturing,
            "car_color":car_color,
            "car_type":car_type,
            "is_available":is_available
        }

        car_create_serializer = VehicleCreateSerializer(data=data)
        if car_create_serializer.is_valid():
            new_car = car_create_serializer.save()

            return Response(car_create_serializer.data,status=status.HTTP_201_CREATED)

        return Response(car_create_serializer.errors,status=status.HTTP_400_BAD_REQUEST)