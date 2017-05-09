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
    tags = models.CharField(max_length=100, default="")
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    url = models.CharField(max_length=100, default="")

class Reservation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    date = models.BigIntegerField(default=0)
