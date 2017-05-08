from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Users, Resource, Reservation
from .forms import SignUpForm
#from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def users(request):
    # To delete users from django
    #temp = User.objects.all()
    #temp.delete()


    users = Users.objects.all()
    return render(request, 'users.html', { "users" : users })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            #user = authenticate(username = username, password = raw_password)
            
            # Check if user exists in database
            # if yes, 
            num_email = Users.objects.filter(name = username).count()
            num_username = Users.objects.filter(email = email).count()
            num_results = num_email + num_username
            if num_results == 0:
                user = Users(name = username, password = raw_password, email = email)
                user.save()
                return redirect('/')

            return render(request, 'signup.html', {'form' : form, 'exist' : True})
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form' : form})


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

