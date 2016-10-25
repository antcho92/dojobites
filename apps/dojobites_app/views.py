from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from ..login_reg_app.models import User
from .models import *


def index(request):
    if 'user_id' not in request.session:
        return redirect(reverse('users:index'))
    context = {
        "dates" : Date.objects.all(),
        "restaurants" : Restaurant.objects.all(),
        # "comments": Comment.objects.all(),
    }
    return render(request, 'dojobites_app/index.html', context)

def join(request, restaurant_id):

    return redirect(reverse('bites:index'))

def unjoin(request, restaurant_id):
    return redirect(reverse('bites:index'))

def comment(request):
    if request.method=='POST':
        Comment.objects.validate_comment(request.POST, request.session['user_id'])
    return redirect(reverse('bites:index'))

def new(request):
    restaurants = Restaurant.objects.all()
    print "*"*70
    print "Restaurants:", restaurants.values()
    print "*"*70
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
