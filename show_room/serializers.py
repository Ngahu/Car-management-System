from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Vehicle

from car_management_app.core.choices import (
    CAR_TYPES_CHOICES,
    COLOR_CHOICES
)


class VehicleCreateSerializer(serializers.ModelSerializer):
    '''
    Description:This is the serializer to be used to create a new car in the database.\n
    '''
    car_color = serializers.ChoiceField(choices=COLOR_CHOICES)
    car_type = serializers.ChoiceField(choices=CAR_TYPES_CHOICES)
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
            









class ShopStoreAddSupplierSerializer(serializers.ModelSerializer):
    """
    Description:Add a supplier to a shop.\n
    """
    class Meta:
        model = ShopStore
        fields = (
            'suppliers',
        )
        def create(self,validated_data):
            added_supplier = ShopStore(
                suppliers = validated_data['suppliers']
            )
            added_supplier.save()

            return added_supplier