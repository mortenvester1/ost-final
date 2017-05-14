from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core import mail, serializers
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

import re
from .models import Resource, Reservation
from .forms import SignUpForm, ResourceForm, ReservationForm
from datetime import date, time, timedelta, datetime

def index(request):
    #logout(request)
    #if not request.user.is_authenticated():
    #    return redirect('/')
    
    try:
        user = request.user
        #print(user.email)
        resources = Resource.objects.all().order_by('-lastreservation')
        userResources = Resource.objects.filter(owner = user).order_by('name')
        reservations = Reservation.objects.filter(owner = user).order_by('date','start')
        out = { 'user' : user, \
                'resources' : resources, \
                'userResources' : userResources, \
                'userReservations' : reservations}
        
        return render(request, 'userpage.html', out)
    except:
        return render(request, 'index.html')

def emailreservationconfirmation(reservation, email, restype = 'new'):
    if restype == 'new':
        message = 'You have made the following Reservation\n\n'
        subject = 'Your ARRS Reservation: Booking'
    else:
        message = 'You have cancelled the following Reservation\n\n'
        subject = 'Your ARRS Reservation: Cancellation'
    message += 'Resource:' + str(reservation.resource.name) + "\n\n"
    message += 'date: ' + str(reservation.date) + "\n\n"
    message += 'start: ' + str(reservation.start) + '\n\n'
    message += 'end: ' + str(reservation.end) + '\n\n'
    message += 'duration: ' + str(reservation.duration) + '\n\n'
    
    print(email)
    connection = mail.get_connection()
    connection.open()        
    mail.send_mail(subject = subject, \
              message = message, \
              from_email = 'app68100833@heroku.com', \
              recipient_list = [str(email)], \
              fail_silently=False, connection=connection,)
    connection.close()
    return 

def search(request, q = ''):
    out = {}
    q = request.GET['q']
    if q == "":
        return render(request, 'search.html', out)
    else:
        qlist = q.split(' ')
        tags = Resource.objects.filter(tags__icontains=qlist[0])
        resources = Resource.objects.filter(name__icontains=qlist[0])
        if len(qlist) > 1:
            for query in qlist[1:]:
                tags = tags | Resource.objects.filter(tags__icontains=query)
                resources = resources | Resource.objects.filter(name__icontains=query)
        
        out['query'] = q
        out['tags'] = tags
        out['resources'] = resources
        return render(request, 'search.html', out)

    return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            exist = User.objects.filter(email = email)
            if len(exist) > 0:
                form.add_error(None, 'Email is already being used')
                return render(request, 'signup.html', {'form' : form})

            user = User.objects.create_user(username = username, password = raw_password, email = email)
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)            

            resources = Resource.objects.all()
            out = { 'user' : user, \
                    'resources' : resources}

            return render(request, 'userpage.html', out)
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
                resources = Resource.objects.all().order_by('-lastreservation')
                userResources = Resource.objects.filter(owner = user).order_by('name')
                reservations = Reservation.objects.filter(owner = user).order_by('date','start')

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
    #deletereservation()
    if not request.user.is_authenticated():
        return redirect('/')

    logout(request)
    return render(request, 'index.html')

def userpage(request):
    deletereservation()
    if not request.user.is_authenticated():
        return redirect('/')
    user = request.user
    resources = Resource.objects.all().order_by('-lastreservation')
    userResources = Resource.objects.filter(owner = user).order_by('name')
    reservations = Reservation.objects.filter(owner = user).order_by('date','start')
    
    # how to order resources
    # By time of last reservation
    out = {'user' : user, \
           'resources' : resources, \
           'userResources' : userResources, \
           'userReservations' : reservations}

    return render(request, 'userpage.html', out)

def createresource(request):
    #deletereservation()
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

            if start > end:
                form.add_error(None, "Availability not valid")
                return render(request, 'createresource.html', {'form' : form})                


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
    deletereservation()    
    if not request.user.is_authenticated():
        return redirect('/')
    
    out = {}
    rid = request.GET['rid']
    resource = Resource.objects.filter(url = "rid"+rid)[0]
    reservations = Reservation.objects.filter(resource = resource).order_by('date','start')

    out['reservations'] = reservations
    if request.method == 'POST' and 'modify' in request.POST:
        rid = request.GET['rid']
        #resource = Resource.objects.filter(url = "rid"+rid)[0]
        tags = resource.tags.split(' ')
        out['user'] = request.user
        out['tags'] = tags
        out['resource'] = resource
        modForm = ResourceForm(request.POST)

        if modForm.is_valid():
            resource.name = modForm.cleaned_data.get('name')
            resource.tags = modForm.cleaned_data.get('tags')
            resource.start = modForm.cleaned_data.get('start')
            resource.end = modForm.cleaned_data.get('end')
            resource.save()
            return redirect('userpage.html')
        else:
            modForm = ResourceForm({'name' : resource.name, \
                                    'tags' : resource.tags,\
                                    'start' : resource.start,\
                                    'end' : resource.end})
            modForm.add_error(None, "Information not valid")
            resForm = ReservationForm()
            out['modify'] = modForm
            out['form'] = resForm
            return render(request, 'viewresource.html', out)

    elif request.method == 'POST' and 'reservation' in request.POST:
        rid = request.GET['rid']
        #resource = Resource.objects.filter(url = "rid"+rid)[0]
        tags = resource.tags.split(' ')
        out['user'] = request.user
        out['tags'] = tags
        out['resource'] = resource
        resForm = ReservationForm(request.POST)

        if resForm.is_valid():
            uname = request.user
            resou = resource
            datestamp = resForm.cleaned_data.get('date')
            start = resForm.cleaned_data.get('start')
            duration = resForm.cleaned_data.get('duration')
            timestamp = timezone.now()#datetime.time(datetime.now())
            try:
                temp = duration.split(':')
                hour = int( temp[0] ) + start.hour +\
                       ( start.minute +  int( temp[1] ) ) // 60
                minu = ( start.minute + int( temp[1] ) ) % 60
                end = time( hour = hour, minute = minu )
            except:
                if hour >= 24:
                    resForm.add_error(None, "Duration cannot span days")
                else:
                    resForm.add_error(None, "Duration not valid")
                out['form'] = resForm
                
                if request.user == resource.owner:
                    end = "%s:%s" % (resource.end.hour, resource.end.minute)
                    start = "%s:%s" % (resource.start.hour, resource.start.minute)
                    modForm = ResourceForm({'name' : resource.name, \
                                            'tags' : resource.tags,\
                                            'start' : start,\
                                            'end' : end})
                    out['modify'] = modForm                
                
                return render(request, 'viewresource.html', out)
            
            if datestamp < date.today():
                resForm.add_error(None, 'Date is in the past')
                if request.user == resource.owner:
                    end = "%s:%s" % (resource.end.hour, resource.end.minute)
                    start = "%s:%s" % (resource.start.hour, resource.start.minute)
                    modForm = ResourceForm({'name' : resource.name, \
                                            'tags' : resource.tags,\
                                            'start' : start,\
                                            'end' : end})
                    out['modify'] = modForm                
                out['form'] = resForm
                return render(request, 'viewresource.html', out)


            x = verifyreservationtime(resou, start, end, datestamp)
            if x > 0:
                if x == 1:
                    resForm.add_error(None, "Reservation time not valid.")
                elif x == 2:
                    resForm.add_error(None, "Resource not available.")
                elif x == 3:
                    resForm.add_error(None, "Duration must be at least one minute")

                if request.user == resource.owner:
                    end = "%s:%s" % (resource.end.hour, resource.end.minute)
                    start = "%s:%s" % (resource.start.hour, resource.start.minute)
                    modForm = ResourceForm({'name' : resource.name, \
                                            'tags' : resource.tags,\
                                            'start' : start,\
                                            'end' : end})
                    out['modify'] = modForm

                out['form'] = resForm
                return render(request, 'viewresource.html', out)

            else:
                reservation = Reservation(owner = uname,\
                                      resource = resou,\
                                      date = datestamp,\
                                      start = start,\
                                      duration = duration,\
                                      end = end,\
                                      timestamp = timestamp)
                reservation.save()
                resource.lastreservation = timestamp
                resource.currentcount += 1
                resource.reservationcount += 1
                resource.save()
                
                email = request.user.email
                #emailreservationconfirmation(reservation, email = 'o9hhu@vmani.com')
                emailreservationconfirmation(reservation, email)
                return redirect('userpage.html')

    else:
        rid = request.GET['rid']
        #resource = Resource.objects.filter(url = "rid"+rid)[0]
        tags = resource.tags.split(' ')

        resForm = ReservationForm()
        out['user'] = request.user
        out['tags'] = tags
        out['resource'] = resource
        out['form'] = resForm

        if request.user == resource.owner:
            end = "%s:%s" % (resource.end.hour, resource.end.minute)
            start = "%s:%s" % (resource.start.hour, resource.start.minute)
            modForm = ResourceForm({'name' : resource.name, \
                                    'tags' : resource.tags,\
                                    'start' : start,\
                                    'end' : end})
            out['modify'] = modForm
        return render(request, 'viewresource.html', out)


def viewtags(request, tag = ""):
    deletereservation()
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

def rss(request, rid = 0):
    deletereservation()

    if not request.user.is_authenticated():
        return redirect('/')

    rid = request.GET['rid']
    try:
        resource = Resource.objects.filter(id = int(rid))
        reservations = Reservation.objects.filter(resource = resource)
        data = serializers.serialize("xml", reservations)

    except:
        reservations = Reservation.objects.filter(id = 0)
        data = serializers.serialize("xml", reservations)
    
    out = {'data' : data}
    return render(request, 'rss.html', out)

def cancelreservation(request, rid = 0):
    #deletereservation()
    timenow = timezone.now()
    if not request.user.is_authenticated():
        return redirect('/')

    rid = request.GET['rid']
    reservation = Reservation.objects.filter(id = rid)[0]
    
    user = request.user
    if user == reservation.owner:
        resource = reservation.resource
        resource.currentcount -= 1
        resource.save()
        
        email = request.user.email
        #emailreservationconfirmation(reservation, email = 'o9hhu@vmani.com')
        emailreservationconfirmation(reservation, email, restype = 'cancel')
        reservation.delete()        

        resources = Resource.objects.all().order_by('-lastreservation')
        userResources = Resource.objects.filter(owner = user).order_by('name')
        reservations = Reservation.objects.filter(owner = user).order_by('date','start')

        out = {'user' : user, \
           'resources' : resources, \
           'userResources' : userResources, \
           'userReservations' : reservations}

        return render(request, 'userpage.html', out)
    else:
        return redirect('/')

def deleteresource(request, rid = 0):
    user = request.user
    if not request.user.is_authenticated():
        return redirect('/')
    else:
        rid = request.GET['rid']
        resource = Resource.objects.filter(id = int(rid))[0]
        if user != resource.owner:
            return redirect('/')

        reservations = Reservation.objects.filter(resource = resource)
        #len(reservations)
        reservations.delete()
        resource.delete()

        resources = Resource.objects.all()
        userResources = Resource.objects.filter(owner = user)
        reservations = Reservation.objects.filter(owner = user)
        
        resources = resources.order_by('-lastreservation')
        reservations = reservations.order_by('date','start')
        userResources = userResources.order_by('name')


        out = {'user' : user, \
               'resources' : resources, \
               'userResources' : userResources, \
               'userReservations' : reservations}

        return render(request, 'userpage.html', out)

def deletereservation():
    #print('I went here')
    datenow = date.today()
    timenow = datetime.now().time()
    deleteSet = Reservation.objects.filter(date__lte=datenow)
    deleteSet = deleteSet.filter(end__lt=timenow)

    resources = []
    for res in deleteSet:
        if res.resource not in resources:
            res.resource.currentcount -= 1
            res.resource.save()
            resources.append(res.resource)

    
    deleteSet.delete()
    return

def verifyreservationtime(resource, start, end, date):
    start = timedelta(hours = start.hour, \
                      minutes = start.minute)
    end = timedelta(hours = end.hour, \
                    minutes = end.minute)
    resourcestart = timedelta(hours = resource.start.hour, \
                              minutes = resource.start.minute)
    resourceend = timedelta(hours = resource.end.hour, \
                            minutes = resource.end.minute)
    # Duration is 0
    if start == end:
        return 3 
    elif end < start:
        return 1

    # Starts outside Limits
    if start < resourcestart:
        return 1
        # Ends outside Limits
    elif end > resourceend:
        return 1    

    reservations = Reservation.objects.filter(resource = resource, date = date)
    result = []
    for res in reservations:
        reservationstart = timedelta(hours = res.start.hour, \
                                     minutes = res.start.minute)
        reservationend = timedelta(hours = res.end.hour, \
                                   minutes = res.end.minute) 
        # No Other Reservation
        if ( start <= reservationstart ) and ( end <= reservationstart):
            result.append(0)
        elif ( start >= reservationend ) and ( end >= reservationend):
            result.append(0)
    
    if len(result) == len(reservations):
        return 0
    else:
        return 2
