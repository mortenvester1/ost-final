from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Resource, Reservation
from .forms import SignUpForm, ResourceForm, ReservationForm

def index(request):
    #logout(request)
    return render(request, 'index.html')

def DEVprint(request):
    if not request.user.is_authenticated():
        return redirect('/')
    
    users = User.objects.all()
    resources = Resource.objects.all()
    reservations = Reservation.objects.all()
    #users.delete()
    resources.delete()
    reservations.delete()
    out = { "users" : users ,\
            "resources" : resources, \
            "reservations" : reservations}

    return render(request, 'DEVprint.html', out)

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

            resources = Resource.objects.all()
            out = { 'user' : user, \
                    'resources' : resources}

            print('here2')
            return render(request, 'userpage.html', out)                 
    else:
        form = SignUpForm()
    print('here')
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
                resources = Resource.objects.all()
                userResources = Resource.objects.filter(owner = user)
                reservations = Reservation.objects.filter(owner = user)

                out = { 'user' : user, \
                        'resources' : resources, \
                        'userResources' : userResources, \
                        'userReservations' : reservations}

                return render(request, 'userpage.html', out)                 

            return render(request, 'userlogin.html', {'form' : form})
    else:
        form = AuthenticationForm()
    return render(request, 'userlogin.html', {'form' : form})

def userlogout(request):
    if not request.user.is_authenticated():
        return redirect('/')

    logout(request)
    return render(request, 'index.html')

def userpage(request):
    if not request.user.is_authenticated():
        return redirect('/')
    user = request.user
    resources = Resource.objects.all()
    userResources = Resource.objects.filter(owner = user)
    reservations = Reservation.objects.filter(owner = user)

    out = {'user' : user, \
           'resources' : resources, \
           'userResources' : userResources, \
           'userReservations' : reservations}

    return render(request, 'userpage.html', out)

def createresource(request):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            owner = request.user
            name = form.cleaned_data.get('name')
            tags = form.cleaned_data.get('tags')
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')

            #Check if exists, then fail
            count = Resource.objects.filter(owner = owner, name = name).count()
            if count > 0:
                form = ResourceForm()
                return render(request, 'createresource.html', {'form' : form})                
            
            resource = Resource(owner = owner,\
                                name = name, \
                                tags = tags, \
                                start = start,\
                                end = end)
            
            resource.save()
            resource.url = "rid" + str(resource.id)
            resource.save()

            return redirect('userpage.html')                 

        return render(request, 'createresource.html', {'form' : form})

    else:
        form = ResourceForm()
    
    return render(request, 'createresource.html', {'form' : form})

def viewresource(request, rid = 0):    
    if not request.user.is_authenticated():
        return redirect('/')
    
    out = {}
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        rid = request.GET['rid']
        resource = Resource.objects.filter(url = "rid"+rid)[0]
        out['resource'] = resource
        
        if request.user == resource.owner:
            modifyForm = ResourceForm(request.POST)
            #out['modify'] = modifyForm

            if modifyForm.is_valid():
                resource.name = modifyForm.cleaned_data.get('name')
                resource.tags = modifyForm.cleaned_data.get('tags')
                resource.start = modifyForm.cleaned_data.get('start')
                resource.end = modifyForm.cleaned_data.get('end')
                resource.save()
                return redirect('userpage.html')

        if form.is_valid():
            uName = request.user
            rName = resource
            date = form.cleaned_data.get('date')
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')
            reservation = Reservation(owner = uName,\
                                      resource = rName,\
                                      date = date,\
                                      start = start,\
                                      end = end)
            reservation.save()
            return redirect('userpage.html')
        
        else:
            out['user'] = request.user
            out['form'] = form
            return render(request, 'viewresource.html', out)
    else:
        rid = request.GET['rid']
        resource = Resource.objects.filter(url = "rid"+rid)
        if len(resource) > 0:
            out['resource'] = resource[0]
            tags = resource[0].tags.split(' ')
            out['tags'] = tags
        else:
            out = {}
            print('here4')
            return render(request, 'viewresource.html', out)

    
        form = ReservationForm()
        out['form'] = form
        if request.user == resource[0].owner:
            modifyForm = ResourceForm({'name' : resource[0].name, \
                                       'tags' : resource[0].tags,\
                                       'start' : resource[0].start,\
                                       'end' : resource[0].end})
            out['modify'] = modifyForm
        return render(request, 'viewresource.html', out)


def viewtags(request, tag = ""):
    if not request.user.is_authenticated():
        return redirect('/')
    tag = request.GET['tag']

    res = []
    resources = Resource.objects.all()
    for resource in resources:
        if tag in resource.tags.split(' '):
            res.append(resource)
    
    out = {}
    if tag != "":
        out['tags'] = res
    
    out['tag'] = tag

    return render(request, 'viewtags.html', out)

def cancelreservation(request, rid = 0):
    if not request.user.is_authenticated():
        return redirect('/')

    rid = request.GET['rid']
    reservation = Reservation.objects.filter(id = rid)[0]
    
    user = request.user
    if user == reservation.owner:
        reservation.delete()
        resources = Resource.objects.all()
        userResources = Resource.objects.filter(owner = user)
        reservations = Reservation.objects.filter(owner = user)

        out = {'user' : user, \
           'resources' : resources, \
           'userResources' : userResources, \
           'userReservations' : reservations}

        return render(request, 'userpage.html', out)
    else:
        return redirect('/')
