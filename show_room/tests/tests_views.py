from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.


from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse

# automated
# new / blank db

from show_room.models import Vehicle

User = get_user_model()


class VehicleAPITestCase():
    def setUp(self):
        user_obj = User(username='joe', email='joe@test.com')
        user_obj.set_password("somerandopassword")
        user_obj.save()
        car = Vehicle.objects.create(
            creator = user_obj,
            car_make = "Audi",
            registration_number = "KCA 567T",
            year_of_manufacturing = "2019",
            car_color = "red",
            car_type = "saloon",
            is_available = "True"

        )
    

    def test_single_user(Self):
        user_count  = User.objects.count()
        self.assertEqual(user_count, 1)
    

    def test_single_car(self):
        car_count = Vehicle.objects.exclude(is_deleted = True).count()
        self.assertEqual(car_count, 1)

    
    def test_get_list(self):
        # test the get list
        data = {}
        url = api_reverse("show_room:both_available_unavailable")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_get_car(self):
        # test the get list
        the_car = Vehicle.objects.first()
        data = {}
        url = the_car.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        