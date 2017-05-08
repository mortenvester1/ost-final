from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#class Users(models.Model):
#    name = models.CharField(max_length=100, unique = True)
#    password = models.CharField(max_length=100)
#    email = models.CharField(max_length=100, unique = True)

class Resource(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    availStart = models.DateTimeField(timezone.now())
    availEnd = models.DateTimeField(timezone.now())

class Reservation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    startTime = models.DateTimeField(timezone.now())
    endTime = models.DateTimeField(timezone.now())
