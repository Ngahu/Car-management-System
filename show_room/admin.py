from django.contrib import admin

# Register your models here.
from .models import Vehicle


class VehivleAdmin(admin.ModelAdmin):
    list_display = [
        'creator',
        'car_make',
        'registration_number',
        'is_available',
        'date_created'
    ]
    search_fields = [
        'creator',
        'car_make'
    ]



admin.site.register(Vehicle,VehivleAdmin)