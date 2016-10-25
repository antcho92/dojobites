from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..login_reg_app.models import User
from .models import *


def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    context = {
        "restaurants" : Restaurant.objects.all(),
        "comments": Comment.objects.all(),
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
def calendar(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'dojobites_app/calendar.html', context)
