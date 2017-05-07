from django.http import HttpResponse
from django.shortcuts import render
from .models import Users, Resource, Reservation

def index(request):
    return render(request, 'index.html')
    #return HttpResponse("Hello, world.\n"+s)

def addUser(request):
    return HttpResponse('User Added')

def p1(request):
    return render(request, 'p1.html')