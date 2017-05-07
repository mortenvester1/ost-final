from django.db import models
from django.utils import timezone

class Users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique = True)

class Resource(models.Model):
    owner = models.ForeignKey(Users)
    name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    availStart = models.DateTimeField(timezone.now())
    availEnd = models.DateTimeField(timezone.now())

class Reservation(models.Model):
    user = models.ForeignKey(Users)
    resource = models.ForeignKey(Resource)
    startTime = models.DateTimeField(timezone.now())
    endTime = models.DateTimeField(timezone.now())
