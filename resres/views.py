from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Resource, Reservation
from .forms import SignUpForm

def index(request):
    return render(request, 'index.html')

def users(request):
    # To delete users from django
    users = User.objects.all()
    #users.delete()

    #users = Users.objects.all()
    return render(request, 'users.html', { "users" : users })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username = username, password = raw_password, email = email)
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)            
            # Check if user exists in database
            #num_results = User.objects.filter(username = username).count()
            #if num_results > 0:
            #    return render(request, 'signup.html', {'form' : form, 'exist' : True})

            return render(request, 'index.html', {'user' : request.user})
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form' : form})

def userlogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if request.user.is_authenticated():
                return render(request, 'index.html', {'user' : request.user})                 

            return render(request, 'userlogin.html', {'form' : form})
    else:
        form = AuthenticationForm()

    return render(request, 'userlogin.html', {'form' : form})

def userlogout(request):
    logout(request)
    return redirect('/')

def getUser(request):
    return HttpResponse('Not Done yet')

def getResource(request):
    resources = Resource.objects.all()
    return render(request, 'resources.html', { "resource" : resources })

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
    reservations = Reservation.objects.all()
    return render(request, 'reservations.html', { "reservation" : reservations })

def createReservation(request):
    Reservation = Reservation(user = 'user1', \
                              Resource = 'resource1', \
                              startTime = 'startTime', \
                              endTime = 'endTime')
    Reservation.save()
    return HttpResponse('Not Done yet')    

def deleteReservation(request):
    return HttpResponse('Not Done yet')    

