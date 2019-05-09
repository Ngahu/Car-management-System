from django.shortcuts import render

from datetime import date
import datetime

from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status


from .serializers import (
    VehicleCreateSerializer,
    VehicleDetailSerializer,
    VehiclesListSerializer,
    VehicleUpdateSerializer
)


from rest_framework.generics import RetrieveUpdateAPIView


from .models import Vehicle



class RootAPIView(APIView):
    """
    returns a list of all the urls for this app
    """
    # permission_classes = (IsAuthenticated)
    def get(self,request,format=None):
        return Response({
            "create-car":reverse("show_room:create_car", request=request, format=format),
            "available-blue-cars":reverse("show_room:available_blue_cars", request=request, format=format),
            "all-available-unavailable":reverse("show_room:both_available_unavailable", request=request, format=format),
            "only-available":reverse("show_room:available_cars", request=request, format=format),
            

            

        })
    




class VehicleCreateAPIView(APIView):
    """
    Description:create a single car in a show room \n
    Type of request:POST\n
    Accepts headers: \n{
    Authorization: "Token " + authenticationToken
    }\n
    Request data type:JSON\n
    POST request body: \n{
	"car_make":"Toyota",
	"registration_number":"KAE 777G",
	"year_of_manufacturing":"2019-01-01",
	"car_color":"red",
	"car_type":"hatchback",
	"is_available":"True"
    }\n
    Response success status:HTTP_201_created \n
    Response data type:JSON\n
    Sample Success:\n
            {
            "creator": 1,
            "car_make": "Nissan maxima",
            "registration_number": "KAE 777G",
            "year_of_manufacturing": "2019-01-01",
            "is_available": true,
            "car_type": "saloon",
            "car_color": "red"
            }\n
    Response failure:\n{
        error: Sorry yourchoice is not a valid choice.\tHTTP_401_UNAUTHORIZED\n
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







class VehicleDetailAPIView(APIView):
    """
    Description:detail
    """
    permission_classes = (IsAuthenticated,)
    def get(self,request,id,format=None):
        current_user = request.user

        #get the car
        try:
            the_car = Vehicle.objects.get(id=id)

            serializer_class = VehicleDetailSerializer(the_car)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        
        except(Vehicle.DoesNotExist,OverflowError) as err:
            error = {
                "error":"Sorry,Car do not exist."
            }
            return Response(error,status=status.HTTP_404_NOT_FOUND)





class ListAvailableBlueCarsAPIView(APIView):
    '''
    list all available blue cars.\n
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        current_user = request.user


        try:
            cars_list = Vehicle.objects.available().filter(car_color='blue')
        
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        available_blue_cars_serializer = VehiclesListSerializer(
            cars_list,
            many=True,
            context={'request': request}
        )
        return Response(available_blue_cars_serializer.data,status=status.HTTP_200_OK)






class VehicleUpdateAPIView(RetrieveUpdateAPIView):
    """
    Description:Update a single car.\n
    Type of request:POST\n
    Accepts headers: \n{
    Authorization: "Token " + authenticationToken
    }\n
    Request data type:JSON\n
    POST request body: \n{
    "is_available": true,
    "car_color": "blue"
    }\n
    Response success status:HTTP_201_created \n
    Response data type:JSON\n
    Sample Success:\n
            
        {
            "is_available": true,
            "car_color": "red"
        }\n
    Response failure:\n{
        error: Sorry your color choice is not a valid choice.\tHTTP_401_UNAUTHORIZED\n
    }
    
    """
    queryset = Vehicle.objects.exclude(is_deleted=True)

    serializer_class = VehicleUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]










class ListAllAPIView(APIView):
    '''
    Description:List out a list of all the cars both available and unavailable \n
    Type of request:GET\n
    Accepts headers: \n{
    Authorization: "Token " + authenticationToken
    }\n
    Request data type:JSON\n
    Sample Response:\n 
    [
    {
        "url": "http://127.0.0.1:8000/showroom/car/16/",
        "car_make": "Suzuki Escudo",
        "is_available": true,
        "car_type": "hatchback",
        "car_color": "blue"
    }
    ]

    Response sucess status: \n HTTP_200_OK\n
    Response failure:\n{
        error: Sorry you must login to view this.\tHTTP_401_UNAUTHORIZED\n
    }
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        current_user = request.user


        try:
            all_cars_list = Vehicle.objects.exclude(is_deleted=True)
        
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        available_blue_cars_serializer = VehiclesListSerializer(
            all_cars_list,
            many=True,
            context={'request': request}
        )
        return Response(available_blue_cars_serializer.data,status=status.HTTP_200_OK)






class DeleteAllUnavailableVehicles(APIView):
    """
    Description:Delete all unavailable vehicles \n
    Type of request:GET\n
    Accepts headers: \n{
    Authorization: "Token " + authenticationToken
    }\n
    Request data type:JSON\n
    Sample Response:\n 
    {
    "success": "All unavailable cars have been deleted."
    }

    Response sucess status: \n HTTP_200_OK\n
    Response failure:\n{
        error: Sorry you must login to view this.\tHTTP_401_UNAUTHORIZED\n
    } 
    """ 
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):

        unavailable_cars = None
        
        #get all unavailable cars
        try:
            unavailable_cars = Vehicle.objects.unavailable()
        
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

        if unavailable_cars:
            print("unavailable_cars",unavailable_cars)
            for car in unavailable_cars:
                car.is_deleted = True
                car.deleted_at = datetime.datetime.now()
                car.save()

                success_response = {
                    "success":"All unavailable cars have been deleted."
                }
                return Response(success_response,status=status.HTTP_200_OK)
        
        error_message = {
            "error":"Sorry there are no unavailable cars"
        }
        return Response(error_message,status=status.HTTP_400_BAD_REQUEST)












class ListAllAvailableAPIView(APIView):
    '''
    Description:List out a list of all the cars  available  \n
    Type of request:GET\n
    Accepts headers: \n{
    Authorization: "Token " + authenticationToken
    }\n
    Request data type:JSON\n
    Sample Response:\n 
    [
    {
        "url": "http://127.0.0.1:8000/showroom/car/16/",
        "car_make": "Suzuki Escudo",
        "is_available": true,
        "car_type": "hatchback",
        "car_color": "blue"
    }
    ]

    Response sucess status: \n HTTP_200_OK\n
    Response failure:\n{
        error: Sorry you must login to view this.\tHTTP_401_UNAUTHORIZED\n
    }
    '''
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        current_user = request.user


        try:
            all_cars_list = Vehicle.objects.available().exclude(is_deleted=True)
        
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        available_blue_cars_serializer = VehiclesListSerializer(
            all_cars_list,
            many=True,
            context={'request': request}
        )
        return Response(available_blue_cars_serializer.data,status=status.HTTP_200_OK)
