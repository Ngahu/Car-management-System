from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Vehicle

from car_management_app.core.choices import (
    CAR_TYPES_CHOICES,
    COLOR_CHOICES
)



class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Description:The serializer to validate the user details during registration\n
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        )
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_admin', 'is_active',)

        def create(self,validated_data):
            user = User(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name = validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user



class VehicleCreateSerializer(serializers.ModelSerializer):
    '''
    Description:This is the serializer to be used to create a new car in the database.\n
    '''
    car_color = serializers.ChoiceField(choices=COLOR_CHOICES)
    car_type = serializers.ChoiceField(choices=CAR_TYPES_CHOICES)
    # creator = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    class Meta:
        model = Vehicle
        fields = (
            'creator',
            'car_make',
            'registration_number',
            'year_of_manufacturing',
            'is_available',
            'car_type',
            'car_color'
        )

        def create(self,validated_data):
            '''Create a new instance to the vehicle instance
            '''
            new_vehicle = Vehicle(
                creator = validated_data['creator'],
                car_make = validated_data['car_make'],
                registration_number = validated_data['registration_number'],
                year_of_manufacturing = validated_data['year_of_manufacturing'],
                is_available = validated_data['is_available'],
                car_type = validated_data['car_type'],
                car_color = validated_data['car_color']
            )
            new_vehicle.save()
            return new_vehicle






class ReadUserSerializer(serializers.ModelSerializer):
    """
    Description: Returns a read only user details
    """
    class Meta:
        model = User
        fields =(
            'id',
            'first_name',
            'last_name',
            'email'
        )







class VehicleDetailSerializer(serializers.ModelSerializer):
    """
    Returns the details of a single vehicle
    """
    creator = ReadUserSerializer()
    class Meta:
        model = Vehicle
        fields = (
            'creator',
            'car_make',
            'registration_number',
            'year_of_manufacturing',
            'is_available',
            'car_type',
            'car_color',
            'is_deleted',
            'deleted_at',
            'date_created',
            'date_updated',
            
        )






class VehiclesListSerializer(serializers.ModelSerializer):
    """
    Returns a list of all cars
    """
    url = serializers.HyperlinkedIdentityField(
        view_name = 'show_room:car_detail',
        lookup_field = 'id'
    ) 
    update_url = serializers.HyperlinkedIdentityField(
        view_name = 'show_room:update_car',
        lookup_field = 'id'
    )

    class Meta:
        model = Vehicle
        fields = (
            'url',
            'update_url',
            'car_make',
            'is_available',
            'car_type',
            'car_color',
            
        )









class VehicleUpdateSerializer(serializers.ModelSerializer):
    '''
    Description:This is the serializer to be used to update.\n
    '''
    car_color = serializers.ChoiceField(choices=COLOR_CHOICES)
    
    class Meta:
        model = Vehicle
        fields = (
            'is_available',
            'car_color'
        )

