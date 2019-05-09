from django.shortcuts import render

from datetime import date
import datetime
from django.db.models import Q
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

from rest_framework.authtoken.models import Token

from rest_framework.generics import RetrieveUpdateAPIView


from .models import Vehicle

from django.contrib.auth import get_user_model
User = get_user_model()


class RootAPIView(APIView):
    """
    returns a list of all the urls for this app
    """
    # permission_classes = (IsAuthenticated)
    def get(self,request,format=None):
        return Response({
            "login":reverse("show_room:user_login", request=request, format=format),

            
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
        if not  'car_make' and 'registration_number' and 'year_of_manufacturing' and 'car_color' and 'car_type'  and 'is_available' in request.data:
            all_fields_error = {
                "error":"Sorry,All fields are a compulsory"
            }
            return Response(all_fields_error.errors,status=status.HTTP_400_BAD_REQUEST)

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








class  UserLoginAPIView(APIView):
    """
    Description:Authenticate a  user\n
    Type of request:POST\n
    Request data type:JSON\n
    POST request body: \n
        {
            "username":"joe@hello.com",
            "password":"mysecretstrongpassword"
        }\n
    Response success status:HTTP_201_created \n
    Response data type:JSON\n
    Sample success Response: \n
                                {
                                    "user": 1,
                                    "username": "joe@hello.com",
                                    "key": "efdf1021940672734726abbe04e434199214c759"
                                }\n    
    Response failure: \n
    {
        "error": "The username or password you entered is incorrect. Please try again."
    }\n
    """
    def post(self,request,*args,**kwargs):
        username = request.data['username']
        password = request.data['password']


        if " " in username:
            error = {
                "error":"Sorry username should not have spaces"
            }
            return Response(error,status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(Q(username=username)).distinct()
        # print(user)

      
        if user.exists and user.count() ==1:
            user_object = user.first()
        else:
            error = {
                "error":"The username or password you entered is incorrect. Please try again"
            }
            return Response(error,status=status.HTTP_403_FORBIDDEN)


        if user_object:
            #check the user's password   
            if not user_object.check_password(password):
                error = {
                    "error":"The username or password you entered is incorrect. Please try again."
                }       
                return Response(error,status=status.HTTP_403_FORBIDDEN)
            
            try:
                token = Token.objects.get(user_id=user_object.id)

                success_login_response = {
                    "key":token.key,
                    "username":user_object.username,
                    "user":user_object.id
                }
                return Response(success_login_response,status=status.HTTP_200_OK)
            
            except Token.DoesNotExist:
                error = {
                    "error":"Sorry This  user is not active please contact us!"
                }
                return Response(error,status=status.HTTP_400_BAD_REQUEST)

