from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from ..login_register.models import User
from .models import *
from django.db.models import Count
import requests
from datetime import datetime, timedelta

def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    user = User.objects.get(id=request.session['user_id'])
    date = datetime.now().strftime('%Y-%m-%d')
    # d = datetime.now() - timedelta(hours=8) #Greenwich is currently 8 hours ahead of USA West Coast Time
    # upcoming = Choice.objects.filter(users=user).exclude(date__lte=d)
    # for i in range(len(upcoming)):
    #     print upcoming[i].date
    context = {
        "restaurants" : Restaurant.objects.order_by('-rating'),
        "comments" : Comment.objects.all(),
        "user" : User.objects.get(id=request.session['user_id']),
        'date': date
    }
    return render(request, 'dojobites_app/index.html', context)

def join(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        validation = Choice.objects.addChoice(request.POST, user)
        if validation[0]:
            messages.success(request, validation[1])
        else:
            for error in validation[1]:
                messages.error(request, error)
    return redirect(reverse('bites:calendar'))

def join_choice(request, choice_id):
    user = User.objects.get(id=request.session['user_id'])
    choice = Choice.objects.get(id=choice_id)
    if user in choice.users.all():
        return HttpResponse('You have already made your choice today!')
    choice.users.add(user)
    return HttpResponse('You made a choice!')

def random(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        validation = Choice.objects.addRandChoice(request.POST, user)
        if validation[0]:
            messages.success(request, validation[1])
        else:
            for error in validation[1]:
                messages.error(request, error)
    return redirect(reverse('bites:calendar'))

def unjoin_choice(request, choice_id):
    user = User.objects.get(id=request.session['user_id'])
    choice = Choice.objects.get(id=choice_id)
    choice.users.remove(user)
    if not len(choice.users.all()):
        choice.delete()
    return HttpResponse('You cancelled!')

def comment(request):
    if request.method=='POST':
        validation = Comment.objects.validate_comment(request.POST, request.session['user_id'])
        if validation[0]:
            messages.success(request, validation[1])
        else:
            messages.error(request, validation[1])
    return redirect(reverse('bites:index'))

def new(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'dojobites_app/new.html', {'user' : user})

def create(request):
    if request.method == "POST":
        result = Restaurant.objects.validate_restaurant(request.POST)
        if result[0]:
            messages.success(request, result[1])
            return redirect(reverse('bites:index'))
        for error in result[1]:
            messages.error(request, error)
    return redirect(reverse('bites:new'))

def details(request, restaurant_id):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    restaurant = Restaurant.objects.get(id=restaurant_id)
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'restaurant': restaurant,
        'user' : user
    }
    return render(request, 'dojobites_app/details.html', context)

def show_choice(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    if request.method == 'POST':
        date = request.POST['date']
        choices = Choice.objects.filter(date=date).annotate(num_users=Count('users')).order_by('-num_users','-restaurant__rating')
        user = User.objects.get(id=request.session['user_id'])
        valid = False if Choice.objects.filter(date=date, users=user).exists() else True
        context = {
            'user': user,
            'choices': choices,
            'valid' : valid
        }
    return render(request, 'dojobites_app/choices.html', context)

def show_rest(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    if request.method == 'POST':
        date = request.POST['date']
        choice = Choice.objects.get(id=request.POST['choice'])
        user = User.objects.get(id=request.session['user_id'])
        valid = False if Choice.objects.filter(date=date, users=user).exists() else True
        context = {
            'user' : user,
            'choice' : choice,
            'valid' : valid
        }
    return render(request, 'dojobites_app/restaurant.html', context)

def direction(request, restaurant_id):
    r = Restaurant.objects.get(id=restaurant_id)
    payload = {
                'origin' : '10777 Main St Bellevue WA',
                'destination' : r.location,
                'mode' : 'walking',
                'key' : 'AIzaSyAhMCk1vqD_DKO1L3UH_Z_gJnK5-MUz6Yo'
            }
    url = "https://maps.googleapis.com/maps/api/directions/json"
    res = requests.get(url, payload).json()
    if res['status'] == 'OK':
        context = {
            'result' : {
                'from' : res['routes'][0]['legs'][0]['start_address'],
                'to' : res['routes'][0]['legs'][0]['end_address'],
                'distance' : res['routes'][0]['legs'][0]['distance']['text'],
                'time' : res['routes'][0]['legs'][0]['duration']['text'],
                'steps' : res['routes'][0]['legs'][0]['steps']
            },
            'restaurant' : r.name
        }
    else:
        context = {
            'result' : {'error' : "Directions from {} to {} are not available...".format('CodingDojo', r.name)}
        }
    return render(request, 'dojobites_app/directions.html', context)

def calendar(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    restaurants = Restaurant.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'restaurants': restaurants,
        'user' : user
    }
    return render(request, 'dojobites_app/calendar.html', context)

def profile(request):
    u = User.objects.get(id=request.session['user_id'])
    context = {
        'u' : u,
        'choices': u.choices.order_by('date'),
    }
    return render(request, 'dojobites_app/profile.html', context)
