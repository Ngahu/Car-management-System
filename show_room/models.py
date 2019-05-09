from django.db import models

from django.utils.translation import gettext_lazy as _

from car_management_app.core.choices import (
    COLOR_CHOICES,
    CAR_TYPES_CHOICES
)

from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = settings.AUTH_USER_MODEL





@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)





class VehicleManger(models.Manager):
    def available(self):
        return self.get_queryset().filter(is_available=True).exclude(is_deleted=True)
    
    def unavailable(self):
        return self.get_queryset().filter(is_available=False).exclude(is_deleted=True)
 

    






class Vehicle (models.Model):
    '''
    Description:This is going to represent a car.\n
    A car has several attributes:
            Carmake
            Color 
            registration Number
            YearOfManufuctring
            type of car
            Availability
            date created
            date updated
    '''
    creator = models.ForeignKey(User)
    car_make =  models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20)
    year_of_manufacturing = models.DateField(_("Year Of Manufacturing"))
    car_color = models.CharField(max_length=100,choices=COLOR_CHOICES,default='blue')
    car_type = models.CharField(max_length=100,choices=CAR_TYPES_CHOICES)
    is_available    = models.BooleanField(default=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    #soft delete 
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)


    objects = VehicleManger()



    

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        ordering = ['-date_created']

    def __str__(self):
        return self.car_make

    def get_absolute_url(self):
        pass
