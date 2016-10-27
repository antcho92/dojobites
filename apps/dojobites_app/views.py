from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from ..login_reg_app.models import User
from .models import *
from django.db.models import Count
from datetime import datetime

def index(request):
    # print "*"*70
    # print "Restaurants:", Restaurant.objects.values('id', 'name')
    # print "Choice:", Choice.objects.values('id', 'users', 'restaurant', 'date')
    # print "*"*70
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    context = {
        "restaurants" : Restaurant.objects.all(),
        "comments": Comment.objects.all(),
        "user" : User.objects.get(id=request.session['user_id'])
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

def join_ajax(request, date, restaurant_id):
    user = User.objects.get(id=request.session['user_id'])
    r = Restaurant.objects.get(id=restaurant_id)
    choice = Choice.objects.get(date=date, restaurant=r)
    choice.users.add(user)
    return HttpResponse('Joined successfully!')


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
    restaurant = Restaurant.objects.get(id=restaurant_id)
    context = {
        'restaurant': restaurant,
        #need to add query lookup for users but first need to add join functionality
    }
    return render(request, 'dojobites_app/details.html', context)

def show_choice(request):
    if request.method == 'POST':
        date = request.POST['date']
        choices = Choice.objects.filter(date=date)
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'choices': choices
        }
    return render(request, 'dojobites_app/choices.html', context)

def show_rest(request):
    if request.method == 'POST':
        c = Choice.objects.get(id=request.POST['choice'])
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user' : user,
        }
    return render(request, 'dojobites_app/restaurant.html', context)

def calendar(request):
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
