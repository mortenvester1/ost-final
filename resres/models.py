from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Resource(models.Model):
    owner = models.ForeignKey(Users)
    name = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    availStart = models.DateTimeField('availablity begin')
    availEnd = models.DateTimeField('availablity end')

class Reservation(models.Model):
    user = models.ForeignKey(Users)
    resource = models.ForeignKey(Resource)
    startTime = models.DateTimeField('reservation begin')
    endTime = models.DateTimeField('reservation end')
