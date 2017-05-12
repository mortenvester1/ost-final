from datetime import date, time, timedelta
from django.utils import timezone
from django import forms
from django.db import models
from django.contrib.auth.models import User


#class Users(models.Model):
#    name = models.CharField(max_length=100, unique = True)
#    password = models.CharField(max_length=100)
#    email = models.CharField(max_length=100, unique = True)

class Resource(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100, default="")
    start = models.TimeField(default=time(00, 00))
    end = models.TimeField(default=time(00, 00))
    url = models.CharField(max_length=100, default="")
    lastreservation = models.DateTimeField(default=timezone.now)

class Reservation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    #date = models.BigIntegerField(default=0)
    start = models.TimeField(default=time(00, 00))
    duration = models.CharField(max_length=5, default='00:00')
    end = models.TimeField(default=time(00, 00))
    timestamp = models.DateTimeField(default=timezone.now)
