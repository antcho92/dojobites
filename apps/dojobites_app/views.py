from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from ..login_register.models import User
from .models import *
from django.db.models import Count
from datetime import datetime, timedelta

def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    datetime.now()
    user = User.objects.get(id=request.session['user_id'])
    d = datetime.now() - timedelta(hours=8) #Greenwich is currently 8 hours ahead of USA West Coast Time
    upcoming = Choice.objects.filter(users=user).exclude(date__lte=d)

    for i in range(len(upcoming)):
        print upcoming[i].date


    context = {
        "restaurants" : Restaurant.objects.all(),
        "comments": Comment.objects.all(),
        "user" : User.objects.get(id=request.session['user_id']),
        "upcoming": upcoming
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
    choice.users.add(user)
    return HttpResponse('You made a choice!')


def unjoin(request, restaurant_id):
    return redirect(reverse('bites:index'))

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
    restaurants = Restaurant.objects.all()
    return render(request, 'dojobites_app/new.html')

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
    context = {
        'restaurant': restaurant,
        #need to add query lookup for users but first need to add join functionality
    }
    return render(request, 'dojobites_app/details.html', context)

def show_choice(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    if request.method == 'POST':
        date = request.POST['date']
        choices = Choice.objects.filter(date=date).annotate(num_users=Count('users')).order_by('-num_users')
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'choices': choices
        }
    return render(request, 'dojobites_app/choices.html', context)

def show_rest(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    if request.method == 'POST':
        choice = Choice.objects.get(id=request.POST['choice'])
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user' : user,
            'choice' : choice
        }
    return render(request, 'dojobites_app/restaurant.html', context)

def calendar(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'dojobites_app/calendar.html', context)

def profile(request):
    u = User.objects.get(id=request.session['user_id'])
    context = {
        'u' : u,
        'choices': u.choices.all(),
    }
    return render(request, 'dojobites_app/profile.html', context)
