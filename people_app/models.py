from django.db import models

# Create your models here.


class Person (models.Model):
    '''
    Description:This is going to represent a person.\n
    '''
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    mass =  models.IntegerField()
    hair_color = models.CharField(max_length=100)
    skin_color =  models.CharField(max_length=100)
    eye_color = models.CharField(max_length=100)
    birth_year = models.CharField(max_length=100)
    # birth_year = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=100)
    homeworld = models.TextField(blank=True, null=True)
    films = models.TextField(blank=True, null=True)
    species = models.TextField(blank=True, null=True)
    vehicles = models.TextField(blank=True, null=True)
    starships = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=100)
    created    = models.CharField(max_length=100)
    edited    =  models.CharField(max_length=100)
    # created    = models.DateTimeField(auto_now_add=True)
    # edited    = models.DateTimeField(auto_now=True)


    

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
        
