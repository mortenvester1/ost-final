from django.http import HttpResponse
from django.shortcuts import render
from .models import Users, Resource, Reservation

def index(request):
    return render(request, 'index.html')

def users(request):
    users = Users.objects.all()
    return render(request, 'users.html', { "users" : users })

def createUser(request):
    user = Users(name = 'user1', \
                 password = 'passw1', \
                 email = 'email1')
    user.save()
    return HttpResponse('Not Done yet')

def login(request):
    return HttpResponse('Not Done yet')

def getUser(request):
    return HttpResponse('Not Done yet')

def getResource(request):
    return HttpResponse('Not Done yet')

def createResource(request):
    resource = Resource(owner = 'owner1', \
                        name = 'resource1', \
                        url = 'url1', \
                        tags = 'tags1', \
                        availStart = 'Start1', \
                        availEnd = 'End1')
    Resource.save()
    return HttpResponse('Not Done yet')    

def deleteReservation(request):
    return HttpResponse('Not Done yet')    

def getReservation(request):
    return HttpResponse('Not Done yet')

def createReservation(request):
    Reservation = Reservation(user = 'user1', \
                              Resource = 'resource1', \
                              startTime = 'startTime', \
                              endTime = 'endTime')
    Reservation.save()
    return HttpResponse('Not Done yet')    

def deleteReservation(request):
    return HttpResponse('Not Done yet')    

